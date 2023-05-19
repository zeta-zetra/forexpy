import pytest 


# Own modules
from ..src.sources.histdata import (download)


@pytest.mark.parametrize('d', ["tick", "1m"])
def test_download_data(d):
    """
    Test downloading a zip file from histdata.com
    Note: This requires network connection
    """

    result = download("EURUSD", d, "20220501")

    assert result == True