from cerberus import Validator

schema = {
    'stock_name': {'type': 'string', 'required': True},
    'timestamp': {'type': 'string', 'required': True},
    'regular_market_price': {'type': 'string', 'required': True},
    'regular_market_change': {'type': 'string', 'required': True},
    'regular_market_change_percent': {'type': 'string', 'required': True},
    'type': {'type': 'integer', 'required': True},
    'PreviousClose': {'type': 'string', 'required': False},
    'Open': {'type': 'string', 'required': False},
    'DaysRangeUpper': {'type': 'string', 'required': False},
    'DaysRangeLower': {'type': 'string', 'required': False},
    '52WeekRangeUppe': {'type': 'string', 'required': False},
    '52WeekRangeLower': {'type': 'string', 'required': False},
    'Algorithm': {'type': 'string', 'required': False},
    'MarketCap': {'type': 'string', 'required': False},
    'CirculatingSupply': {'type': 'string', 'required': False},
    'MaxSupply': {'type': 'string', 'required': False},
    'Volume': {'type': 'string', 'required': False},
    'Volume24hr': {'type': 'string', 'required': False},
    'AvgVolume': {'type': 'string', 'required': False},
    'Volume24hrAllCurrencies': {'type': 'string', 'required': False},
    'PreSettlement': {'type': 'string', 'required': False},
    'Bid': {'type': 'string', 'required': False},
    'Ask': {'type': 'string', 'required': False},
    'LastPrice': {'type': 'string', 'required': False},
}

    
def validate_input_data(data,schema = schema):
    v = Validator(schema, purge_unknown=True)
    if v.validate(data):
        return v.document
    else:
        print(v.document)
        raise ValueError(v.errors)

