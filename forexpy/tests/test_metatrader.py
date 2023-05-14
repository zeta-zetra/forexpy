import datetime
import MetaTrader5 as mt5
import pytest 

# Own modules
from ..src.sources.metatrader_5 import (fetch_from_metatrader, get_rates, get_ticks, 
                                get_rates_range, get_ticks_range)



def test_get_ticks():
    """
    Test getting tick data 
    """

    results = get_ticks("EURUSD", 5)

    assert results.shape[0] == 0


def test_get_ticks_range():
    """
    Test getting tick data based on date range
    """

    results = get_ticks_range("EURUSD", "20230501","20230506")

    assert results.shape[0] > 0


def test_get_rates():
    """
    Test getting rates on timeframe 
    """

    results = get_rates("EURUSD", 10)

    assert results.shape[0] == 10


def test_get_rates_range():
    """
    Test getting rates based on date range
    """

    results = get_rates_range("EURUSD", mt5.TIMEFRAME_D1, "20230501", "20230510")

    assert results.shape[0] == 8


def test_get_ticks_max():
    """
    Maximum ticks have been extracted 
    """

    with pytest.raises(SystemError):
        results = get_ticks_range("EURUSD", "19700101", "20230510")

def test_get_rates_max():
    """
    Maximum rates that can be extracted 
    """

    with pytest.raises(SystemError):
        results = get_rates_range("EURUSD", mt5.TIMEFRAME_D1, "19700101", "20230510")

    # assert results.shape[0] == 1582


