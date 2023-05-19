
import datetime
import pytest

# Own modules
from ..src.utils import (sanitize_inputs, OUTPUT, SOURCES, SYMBOLS, TIMEFRAMES)


def test_path_existence():
    """
    Test if the given path exists
    """

    results = sanitize_inputs(d,"EURUSD", "20230104", "20230105", path="datatemp")

    assert results["error"] == 1


@pytest.mark.parametrize("d", SOURCES )
def test_sanitize_input_sources(d):
    """
    Test if source is correct
    """

    results = sanitize_inputs(d,"EURUSD", "20230104", "20230105")

    assert results["error"] == 0


@pytest.mark.parametrize("s", SYMBOLS )
def test_sanitize_input_symbols(s):
    """
    Test if the symbol is correct
    """

    results = sanitize_inputs("dukas",s, "20230104", "20230104")

    assert results["error"] == 0   



@pytest.mark.parametrize("t", TIMEFRAMES )
def test_sanitize_input_timeframe(t):
    """
    Test if the timeframe is correct
    """

    results = sanitize_inputs("dukas","EURUSD", "20230104", "20230104", tf=t)

    assert results["error"] == 0   


@pytest.mark.parametrize("o", OUTPUT )
def test_sanitize_input_output(o):
    """
    Test if the output is correct
    """

    results = sanitize_inputs("dukas","EURUSD", "20230104", "20230104", tf="tick", output=o)

    assert results["error"] == 0   


def test_sanitize_input_start_incorrect():
    """
    Test if the start date is incorrect
    """
    results = sanitize_inputs("dukas","EURUSD", "2023", "20230104")

    assert results["error"] == 1


@pytest.mark.parametrize("st", [datetime.datetime.now().strftime('%Y%m%d'), "20230411"] )
def test_sanitize_input_start_correct(st):
    """
    Test if the start date is correct
    """
    end = datetime.datetime.now() + datetime.timedelta(days=1)
    results = sanitize_inputs("dukas","EURUSD",st, end.strftime('%Y%m%d') )

    assert results["error"] == 0


@pytest.mark.parametrize("e", ["",datetime.datetime.now().strftime('%Y%m%d'), "20230413"] )
def test_sanitize_input_end_correct(e):
    """
    Test if the end date is correct
    """
    results = sanitize_inputs("dukas","EURUSD","20230412", e)

    assert results["error"] == 0


@pytest.mark.parametrize("e", ["2023","202304","2023041","2023045555"] )
def test_sanitize_input_end_incorrect(e):
    """
    Test if the end date is incorrect
    """
    results = sanitize_inputs("dukas","EURUSD", "20230414", e)

    assert results["error"] == 1


def test_sanitize_input_end_start_incorrect():
    """
    Test if start date is less than end date
    """
    results = sanitize_inputs("dukas","EURUSD", "20230414", "20230413")

    assert results["error"] == 1
