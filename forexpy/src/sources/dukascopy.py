
import datetime
import logging
import lzma 
import requests
import struct 
import sys 

import pandas as pd 

from typing import List

import os 


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')


BASE_URL = "https://datafeed.dukascopy.com/datafeed"

def get_urls(symbol: str, start: str, end: str ="", tf: str = "") -> List[str]:
    """
    Get all the urls to download the data
    
    :params symbol 
    :type :str 

    :params start date 
    :type :str 

    :params end date 
    :type :str

    :params tf is the timeframe
    :type :str

    :return: (List[str]) 
    """

    # Format the symbol
    symbol = symbol.upper()

    # Convert str to datetime object
    start_dt    = datetime.datetime.strptime(start,"%Y%m%d")
    
    if end == "":
      end_dt  = ""
    else:
      end_dt  = datetime.datetime.strptime(end,"%Y%m%d")


    start_year  = start_dt.year
    start_month = start_dt.month if start_dt.month >= 10 else f"0{start_dt.month}"
    start_day   = start_dt.day if start_dt.day >= 10 else f"0{start_dt.day}"

    # Don't run if start or end dates greater than cutoff 
    cutoff_dt   = datetime.datetime.now() - datetime.timedelta(days=31) 

    if start_dt > cutoff_dt:
        logging.error(f"ERROR - Start and/or end date has to be less than {cutoff_dt.strftime('%Y-%m-%d')}")
        sys.exit()


    # Create the urls 
    all_urls = []

    if end_dt == "":
   
        for h in range(0,24):
            if tf == "" or tf == "tick":
                    filename = f"h_ticks.bi5"
                    url = f"{BASE_URL}/{symbol}/{start_year}/{start_month}/{start_day}/{h:02d}{filename}"
            else:
                    filename = "BID_candles_min_1.bi5"
                    url = f"{BASE_URL}/{symbol}/{start_year}/{start_month}/{start_day}/{filename}"
        
            all_urls.append(url)
    else:

        date_range = list(pd.date_range(start_dt, end_dt, freq="1d"))

        for dt in date_range:
                start_year  = dt.year 
                start_month = dt.month if dt.month >= 10 else f"0{dt.month}"
                start_day   = dt.day if dt.day >= 10 else f"0{dt.day}"            
                
                if tf == "" or tf == "tick":
                        filename = f"h_ticks.bi5"
                        url = f"{BASE_URL}/{symbol}/{start_year}/{start_month}/{start_day}/{h:02d}{filename}"
                else:
                        filename = "BID_candles_min_1.bi5"
                        url = f"{BASE_URL}/{symbol}/{start_year}/{start_month}/{start_day}/{filename}"


                all_urls.append(url)
    
    return all_urls

def fetch_from_dukascopy(symbol: str, start: str, end: str, tf: str="") -> pd.DataFrame:
    """
    Downloading Dukascopy data
    """

    # Get the urls 
    urls = get_urls(symbol, start, end, tf=tf)

    # Download the files 

    # Format the data 

    # Output the data

    return []


def main():
    # start_dt    = datetime.datetime.strptime("20230505","%Y%m%d")
    # cutoff_dt   = datetime.datetime.now() - datetime.timedelta(days=31) 
    # print(f"{start_dt} {cutoff_dt} {start_dt > cutoff_dt}")

    print(get_urls("EURUSD","20230416"))
    # local_filename = os.path.join(os.path.abspath(''),'save.bi5')
    # url = "https://datafeed.dukascopy.com/datafeed/EURUSD/2023/04/18/00h_ticks.bi5"
    # # url = "https://datafeed.dukascopy.com/datafeed/EURUSD/2023/04/01/BID_candles_min_1.bi5"
    # # url = "https://datafeed.dukascopy.com/datafeed/eurusd/2021/05/11/23h_ticks.bi5"
    # # url   = "https://datafeed.dukascopy.com/datafeed/EURUSD/2023/04/08/00h_ticks.bi5"
    # res = requests.get(url)
    # res_body = res.content

    # with requests.get(url, stream=True) as r:
    #     r.raise_for_status()
    #     with open(local_filename, 'wb') as f:
    #         for chunk in r.iter_content(chunk_size=8192): 
    #             # If you have chunk encoded response uncomment if
    #             # and set chunk_size parameter to None.
    #             #if chunk: 
    #             f.write(chunk)


    # fmt = '>3i2f'
    # chunk_size = struct.calcsize(fmt)
    # data = []
    # with lzma.open(local_filename) as f:
    #     while True:
    #         chunk = f.read(chunk_size)
    #         if chunk:
    #             data.append(struct.unpack(fmt, chunk))
    #         else:
    #             break
    # df = pd.DataFrame(data)

    # print(df)

if __name__ == "__main__":
    main()
    # fetch_from_dukascopy()
