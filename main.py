from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
import asyncio
import re
import json
from datetime import datetime
import boto3 
from validation import validate_input_data

urls = [
'https://finance.yahoo.com/quote/%5EDJI?p=%5EDJI',
'https://finance.yahoo.com/quote/%5ERUT?p=%5ERUT',
'https://finance.yahoo.com/quote/CL%3DF?p=CL%3DF',
'https://finance.yahoo.com/quote/GC%3DF?p=GC%3DF',
'https://finance.yahoo.com/quote/BTC-USD?p=BTC-USD',
'https://finance.yahoo.com/quote/ETH-USD?p=ETH-USD',
'https://finance.yahoo.com/quote/USDT-USD?p=USDT-USD',
'https://finance.yahoo.com/quote/BNB-USD?p=BNB-USD']

# client = boto3.client('kinesis')
def write_stream(data):
    with boto3.client('kinesis') as client:
        response = client.put_records(Records=data, StreamName='stock-stream')
        print(response)
        
async def main(urls):
    session = AsyncHTMLSession()
    tasks = (extract_soup_fields(session,url) for url in urls)
    return await asyncio.gather(*tasks)

async def extract_soup_fields(session,url):
    page = await session.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table_dict = dict()
    record_dict = dict()
    record_dict = extract_general_info(soup,record_dict)
    record_dict = set_stock_schema(soup,record_dict)
    table_dict = extract_table_fields(soup,table_dict)
    table_dict = clean_table_fields(table_dict)
    record_dict = upsert_table_fields(table_dict,record_dict)
    payload = generate_payload(record_dict,"stock_name")
    payload = validate_input_data(payload)
    return payload

def extract_general_info(soup,record_dict):
    name = soup.h1.text
    results = soup.find('div', {'class': 'D(ib) Mend(20px)'})
    regularMarketPrice = results.find('fin-streamer', {'data-field': 'regularMarketPrice'}).get("value")
    regularMarketChange = results.find('fin-streamer', {'data-field': 'regularMarketChange'}).get("value")
    regularMarketChangePercent = results.find('fin-streamer', {'data-field': 'regularMarketChangePercent'}).get("value")
    date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    record_dict['stock_name'] = name
    record_dict['timestamp'] = date
    record_dict['regular_market_price'] = regularMarketPrice
    record_dict['regular_market_change'] = regularMarketChange
    record_dict['regular_market_change_percent'] = regularMarketChangePercent
    return record_dict

def set_stock_schema(soup,record_dict):
    quoteSummary = soup.find('div', {'id': 'quote-summary'}).find_all('tr')
    if len(quoteSummary) == 6:
        record_dict['type'] = 0
    elif len(quoteSummary) == 8:
        record_dict['type'] = 1
    else:
        record_dict['type'] = 2
    return record_dict

def extract_table_fields(soup,table_dict):
    quoteSummary = soup.find('div', {'id': 'quote-summary'}).find_all('tr')
    for tr in quoteSummary:
        td = tr.find_all('td')
        table_dict[td[0].text] = td[1].text
    return table_dict

def clean_table_fields(table_dict):
    transformed_dict = dict()
    for key,value in table_dict.items():
        key = re.sub('[^A-Za-z0-9]+', '', key)
        value = re.sub('[^A-Za-z0-9.-]+', '', value)
        if '-' in value:
            transformed_dict[key+'Upper'] = value.split('-')[1]
            transformed_dict[key+'Lower'] = value.split('-')[0]
            continue
        transformed_dict[key] = value
    table_dict = transformed_dict
    return table_dict

def upsert_table_fields(table_dict,record_dict):
    record_dict.update(table_dict)
    return record_dict

def generate_payload(record:dict,partition_key):
    payload = dict()
    payload["Data"] = json.dumps(record)
    payload["PartitionKey"] = record[partition_key]
    return payload

if __name__ == '__main__':
    with boto3.client('kinesis') as client:
        debounce = 0
        while True and debounce < 5:
            try :
                records = asyncio.run(main(urls))
            except Exception as e:
                debounce += 1
                print(e)
                continue
            debounce = 0
            response = client.put_records(Records=records, StreamName='stock-stream')
            print(response)

