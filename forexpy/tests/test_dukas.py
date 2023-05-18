import os 
import pytest 

# Own modules
from ..src.sources.dukascopy import (get_urls, download_file, decompress)

def test_decompress_fail():
    """
    Test decompressing a non-existent .bi5 file 
    """
    
    result = decompress("")

    assert len(result) == 0

def test_decompress():
    """
    Test decompressing a .bi5 file
    """
    data_dir = os.path.join(os.path.abspath(""), "forexpy", "tests", "data")
    result = decompress(os.path.join(data_dir, "2023031702h_ticks.bi5"))

    assert len(result) == 3096

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

    assert len(result) == 1

def test_get_urls_start_end_by_tf():
    """
    Get the Dukas urls that will download the data when start and end dates are given with timeframe
    """

    result = get_urls("EURUSD", "20230414","20230416", tf="1m")

    assert len(result) == 3


def test_download_file_fail():
    """
    Test if a file is not downloaded
    """
    
    result = download_file("https://datafeed.dukascopy.com/datafeed")

    assert result["error"] == 1


def test_download_file():
    """
    Test if a file can be downloaded
    """

    result = download_file("https://datafeed.dukascopy.com/datafeed/EURUSD/2023/03/17/00h_ticks.bi5")

    assert result["error"] == 0


def test_format_volume():
    """
    Test formatting the volume
    """

    pass 

def test_format_prices():
    """
    Test formatting prices 
    """
    pass 


def test_format_columns():
    """
    Test formatting columns    
    """

    pass 