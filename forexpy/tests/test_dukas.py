


# Own modules
from ..src.sources.dukascopy import (get_urls)

def test_get_urls_start_only():
    """
    Get the Dukas urls that will download the data when only start date is given
    """

    result = get_urls("EURUSD", "20230416")

    assert len(result) == 24


def test_get_urls_start_end():
    """
    Get the Dukas urls that will download the data when start and end dates are given
    """

    result = get_urls("EURUSD", "20230414","20230416")

    assert len(result) == 72


def test_get_urls_start_only_by_tf():
    """
    Get the urls for the start date only for the given timeframe
    """

    result = get_urls("EURUSD", "20230416", tf="1m")

    assert len(result) == 24

def test_get_urls_start_end_by_tf():
    """
    Get the Dukas urls that will download the data when start and end dates are given with timeframe
    """

    result = get_urls("EURUSD", "20230414","20230416", tf="1m")

    assert len(result) == 72