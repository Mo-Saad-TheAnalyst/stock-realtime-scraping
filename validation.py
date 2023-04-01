import cerberus

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

v = cerberus.Validator(schema)

record_dict = {
    'stock_name': 'AAPL',
    'timestamp': '2022-04-01T10:00:00',
    'regular_market_price': 144.72,
    'regular_market_change': -1.23,
    'regular_market_change_percent': -0.84,
    'type': 0,
    'PreviousClose': 1000.0,
    'KeyMetric2': 2000.0,
    'KeyMetric3': 3000.0,
    'KeyMetric4': 4000.0,
}

if v.validate(record_dict):
    print("Data is valid!")
else:
    print("Data is invalid:", v.errors)