from cerberus import Validator
from cerberus import cerberus_error_handler

schema = {
    'stock_name': {'type': 'string', 'required': True},
    'timestamp': {'type': 'string', 'required': True},
    'regular_market_price': {'type': 'float', 'required': True},
    'regular_market_change': {'type': 'float', 'required': True},
    'regular_market_change_percent': {'type': 'float', 'required': True},
    'type': {'type': 'integer', 'required': True},
    'PreviousClose': {'type': 'float', 'required': False},
    'Open': {'type': 'float', 'required': False},
    'DaysRangeUpper': {'type': 'float', 'required': False},
    'DaysRangeLower': {'type': 'float', 'required': False},
    '52WeekRangeUppe': {'type': 'float', 'required': False},
    '52WeekRangeLower': {'type': 'float', 'required': False},
    'Algorithm': {'type': 'string', 'required': False},
    'MarketCap': {'type': 'string', 'required': False},
    'CirculatingSupply': {'type': 'string', 'required': False},
    'MaxSupply': {'type': 'string', 'required': False},
    'Volume': {'type': 'integer', 'required': False},
    'Volume24hr': {'type': 'string', 'required': False},
    'AvgVolume': {'type': 'integer', 'required': False},
    'Volume24hrAllCurrencies': {'type': 'string', 'required': False},
    'PreSettlement': {'type': 'string', 'required': False},
    'Bid': {'type': 'float', 'required': False},
    'Ask': {'type': 'float', 'required': False},
    'LastPrice': {'type': 'float', 'required': False},
}

    
def validate_input_data(data,schema = schema):
    v = Validator(schema, allow_unknown=True, purge_unknown=True, error_handler=cerberus_error_handler)
    if v.validate(data):
        return v.document
    else:
        raise ValueError(v.errors)

