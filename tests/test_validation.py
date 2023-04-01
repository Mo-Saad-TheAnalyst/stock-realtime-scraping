import pytest
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.validation import validate_input_data

@pytest.mark.parametrize("data,expected",
[({'stock_name': 'AAPL','timestamp': '2022-05-01 15:00:00','regular_market_price': '145.45','regular_market_change': '-2.33','regular_market_change_percent': '-1.58%','type': 1},
  {'stock_name': 'AAPL','timestamp': '2022-05-01 15:00:00','regular_market_price': '145.45','regular_market_change': '-2.33','regular_market_change_percent': '-1.58%','type': 1}),

({'stock_name': 'AAPL','timestamp': '2022-05-01 15:00:00','regular_market_price': '145.45','regular_market_change': '-2.33','regular_market_change_percent': '-1.58%','type': 1,'unknown_field': 'some value'},
 {'stock_name': 'AAPL','timestamp': '2022-05-01 15:00:00','regular_market_price': '145.45','regular_market_change': '-2.33','regular_market_change_percent': '-1.58%','type': 1})
])
def test_valid_input(data,expected):
    assert validate_input_data(data) == expected

def test_missing_required_field():
    data = {
        'stock_name': 'AAPL',
        'timestamp': '2022-05-01 15:00:00',
        'regular_market_price': '145.45',
        'regular_market_change': '-2.33',
        'regular_market_change_percent': '-1.58%'
    }
    with pytest.raises(ValueError):
        validate_input_data(data)


def test_invalid_string_field():
    data = {
        'stock_name': 'AAPL',
        'timestamp': '2022-05-01 15:00:00',
        'regular_market_price': 145.45,
        'regular_market_change': '-2.33',
        'regular_market_change_percent': '-1.58%',
        'type': 1
    }
    with pytest.raises(ValueError):
        validate_input_data(data)

def test_invalid_integer_field():
    data = {
        'stock_name': 'AAPL',
        'timestamp': '2022-05-01 15:00:00',
        'regular_market_price': '145.45',
        'regular_market_change': '-2.33',
        'regular_market_change_percent': '-1.58%',
        'type': '1'
    }
    with pytest.raises(ValueError):
        validate_input_data(data)

