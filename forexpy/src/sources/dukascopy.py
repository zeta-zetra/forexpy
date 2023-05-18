
import datetime
import glob
import logging
import lzma 
import os 
import random
import requests
import struct 
import sys 
import time

import pandas as pd 

from typing import Dict, List, Union

from utils import RESAMPLE_DICT

# Set logging config
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

# CONSTANTS
BASE_URL = "https://datafeed.dukascopy.com/datafeed"


def format_dates(df: pd.DataFrame, symbol: str,  filename: str) -> pd.DataFrame:
    """
    Format the dates 
    """

    if 'h' in filename:
        hour = int(filename.split('h')[0][-2:])
        date = filename.split('h')[0][:-2]
        dt   = datetime.datetime.strptime(date, "%Y%m%d")
        updated_dt = dt + datetime.timedelta(hours=hour)

    dates = [ updated_dt+t  for t in pd.TimedeltaIndex(df.iloc[:,0])  ]

    df["date"] = dates
    
    return df

def format_prices(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    """
    Format the bid and ask prices 
    """

    if "JPY" in symbol:
        point = 1000
    else:
        point = 100000

    df.iloc[:,1] = df.iloc[:,1]/point
    df.iloc[:,2] = df.iloc[:,2]/point

    return df 


def format_volume(df: pd.DataFrame) -> pd.DataFrame:
    """
    Format the bid and ask volume 
    """

    df.iloc[:,3] = df.iloc[:,3]*1000000
    df.iloc[:,4] = df.iloc[:,4]*1000000

    return df 

def format_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Format columns
    """

    df.rename(columns={0: "secs", 1: "ask", 2:"bid", 3:"ask_vol", 4: "bid_vol"}, inplace=True)

    df = df[["ask", "bid", "ask_vol", "bid_vol", "date"]]

    df.set_index("date", inplace=True)

    return df



def decompress(filename: str) -> pd.DataFrame:
    """
    Decompress the .bi5 files, if any, and construct a dataframe
   
   
    :params filename  
    :type :str 

    :return: (pd.DataFrame)
    """

    fmt = '>3i2f'
    chunk_size = struct.calcsize(fmt)

   
    data = []
    try:
        with lzma.open(filename) as f:
            while True:
                chunk = f.read(chunk_size)
                if chunk:
                    data.append(struct.unpack(fmt, chunk))
                else:
                    break

        df = pd.DataFrame(data)

        
    except Exception as e:
        logging.error(e)

        df = pd.DataFrame()


    return df

def download_file(url: str) -> Dict[str, Union[str, int]]:
    """
    Download the .bi5 file and save in a temp file

    :params url to download from 
    :type :str 

    :return: Dict[str, Union[str, int]]
    """
    try:
        filename = "".join(url.split("/")[-4:])

        if not os.path.isdir(os.path.join(os.path.abspath(''), "datatemp")):
            os.mkdir(os.path.join(os.path.abspath(''), "datatemp"))

        local_filename = os.path.join(os.path.abspath(''), "datatemp", filename)
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)    

        # Check if file exists
        if os.path.isfile(local_filename):
            return {"error":0}
        else:
            return {"error":1}
    except Exception as e:
        logging.error(f"> ERROR - {e}")
        return {"error":1}
        


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
   
        
            if tf == "" or tf == "tick":

                    filename = f"h_ticks.bi5"
                    for h in range(0,24):
                        url = f"{BASE_URL}/{symbol}/{start_year}/{start_month}/{start_day}/{h:02d}{filename}"
                        all_urls.append(url)
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
                        for h in range(0,24):
                            url = f"{BASE_URL}/{symbol}/{start_year}/{start_month}/{start_day}/{h:02d}{filename}"
                            all_urls.append(url)
                else:
                        filename = "BID_candles_min_1.bi5"
                        url = f"{BASE_URL}/{symbol}/{start_year}/{start_month}/{start_day}/{filename}"
                        all_urls.append(url)

                
    
    return all_urls

def resample_ohlc(df: pd.DataFrame, tf: str) -> pd.DataFrame:
    """
    Resample the ohlc data 

    :params df dataframe with ohlcv data 
    :type :pd.DataFrame 

    :params tf timeframe 
    :type :str 

    :return: (pd.DataFrame) 
    """
    rule = RESAMPLE_DICT[tf]

    # set the index 
    df["Local time"] = pd.to_datetime(df["Local time"])
    df.set_index("Local time", inplace=True)

    # Resample 
    ohlcv = df[["Open","High","Low","Close"]]
    ohlcv = ohlcv.resample(rule, closed = 'right',label = 'right').agg({'Open': 'first', 
                                 'High': 'max', 
                                 'Low': 'min', 
                                 'Close': 'last',
                                 'Volume':'sum'})

    return ohlcv

def fetch_from_dukascopy(symbol: str, start: str, end: str, tf: str="", keep="F") -> pd.DataFrame:
    """
    Downloading Dukascopy data
    """

    # Get the urls 
    urls = get_urls(symbol, start, end, tf=tf)

    # Download the files 
    list_not_found  = []

    for url in urls:
        download_result = download_file(url)
        
        if download_result["error"] == 1:
            list_not_found.append(url)

        sleep_time = random.randint(6, 10)
        logging.info(f"Waiting {sleep_time} seconds before continuing...")
        time.sleep(sleep_time)

    if len(list_not_found) > 0:
        logging.info("Links to download manually: ")
        for n in list_not_found:
            print(n)


    # Check if any files were downloaded from Dukascopy
    files = glob.glob(os.path.join(os.path.abspath(''), "datatemp","*.bi5"))
    
    if len(files) == 0:
        return []
    
    # Decompress and create dataframe
    final_df = pd.DataFrame()
    for file in files:
         result_df = decompress(file)
         if len(result_df) > 0:
             if tf == "tick":
                filename  = os.path.basename(file)
                
                # Format the dates 
                result_df = format_dates(result_df, symbol, filename)

                # Format the prices 
                result_df  = format_prices(result_df, symbol)

                # Format the volume
                result_df  = format_volume(result_df)

                # Format the columns  
                final_df = format_columns(final_df)

                # Save latest result
                final_df = pd.concat([final_df, result_df])

             else:

                result_df = pd.read_csv(filename)

                # Save latest result
                final_df = pd.concat([final_df, result_df])


    # Check if resample is needed and index the date
    if tf != "tick" and tf != "1m":
            # Resample the data 
            final_df = resample_ohlc(final_df, tf)
    


    # Delete the `datatemp` folder
    if keep in ['F', 'f']:
        try:
            os.remove(os.path.join(os.path.abspath(''), "datatemp"))
            logging.info("> Deleting the `datatemp` folder")
        except Exception as e:
            logging.error("> Could not delete the `datatemp` folder")
            
    return final_df


def main():

    # Read data 
    
    dir_ = os.path.abspath('').split('app')[0]
    print(os.path.join(dir_, "data"))
    filename = os.path.join(dir_, "data", "EURUSD-dukas-tick-20230315.csv")

    df  = pd.read_csv(filename)    
    now = datetime.datetime.now()
    print()
    print(now + pd.TimedeltaIndex(df.iloc[:,1]))

    # s = [ now+t  for t in pd.TimedeltaIndex(df.iloc[:,1])  ]
    # df["date"] = s 
    filename = ["2023031500h_ticks.bi5", "2023031501h_ticks.bi5"]
    print(int(filename.split('h')[0][-2:]))
    
if __name__ == "__main__":
    # main()
    fetch_from_dukascopy("EURUSD", "", "")
