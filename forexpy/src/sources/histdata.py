"""
Get forex data from HistData
See link for more info: www.histdata.com
Author  : Zetra
Date    : 20230518
License : MIT
"""

import datetime
import glob
import logging
import os
import pandas as pd 
import requests
import sys 
import zipfile38 as zipfile


from bs4 import BeautifulSoup
from pathlib import Path
from typing import List, Tuple 
RESAMPLE_DICT = {"1m":"1Min","5m":"5Min", "15m":"15Min", "30m":"30Min", "1h":"1H", "4h":"4H", "1d":"1D"}

# Set the logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

# CONSTANTS
HISTDATA_URL    = 'https://www.histdata.com/'
ASCII_1M        = 'https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/'
ASCII_TICK_DATA = 'https://www.histdata.com/download-free-forex-historical-data/?/ascii/tick-data-quotes/'
ONE_MINUTE      = 'M1'
TICK_DATA       = 'T'
HEADERS         = {'Host': 'www.histdata.com',
                    'Connection': 'keep-alive',
                    'Content-Length': '104',
                    'Cache-Control': 'max-age=0',
                    'Origin': 'https://www.histdata.com',
                    'Upgrade-Insecure-Requests': '1',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept'      : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Referer'     : ''}

PLATFORM = 'ASCII'
GET_HISTDATA_URL = "https://www.histdata.com/get.php"



def unzip_files(files: List[str], path: str = "") -> bool:
    """
    Unzip the given list of files to the given directory. The function will create 
    a `files` folder and save the extracted files in there.


    :params files is a list of zip files to extract 
    :type :List[str]

    :params path is where to save the extracted files 
    :type :str 


    :return: (bool)
    """

    if path == "":
        path = os.path.join(os.path.abspath(''), "hist_files")

        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except:
            logging.error("> Could not create `hist_files` folder. All files will be saved here.")
            path = os.path.abspath('')

        
    for file in files:
        try:
            zip_file = zipfile.ZipFile(file)
            fn       = os.path.basename(file).split(".")[0]
            zip_file.extractall(os.path.join(path, fn))
            logging.info(f"> Unzipped file {fn}")
        except Exception as e:
            logging.error(f"> Could not unzip file {file}")

    return True 


def download(symbol: str, tf:str, date: str, path: str ="") -> Tuple[bool,str]:
    """
    Download the zip file from HistData

    :params symbol is the currency pair
    :type :str 

    :params tf is the timeframe 
    :type  :str

    :params date is the for the data of interest
    :type :str 

    :params path where to save the zip file and final output
    :type :str 
    """

    dt = datetime.datetime.strptime(date, "%Y%m%d")


    # Select the appropriate referer url
    if tf == "tick":
        referer_url = f"{ASCII_TICK_DATA}{symbol.lower()}/{dt.year}/{dt.month}"
        time_frame  = 'T'
    else:
        referer_url = f"{ASCII_1M}{symbol.lower()}/{dt.year}/{dt.month}"
        time_frame  = 'M1'

    # Set the referer in the headers
    HEADERS["Referer"] = referer_url

    # Get the token for the request
    resp = requests.get(referer_url, allow_redirects=True)

    if resp.status_code != 200:
        logging.warning("HistData may not be online...go to www.histdata.com and check.")
    
    soup = BeautifulSoup(resp.content, "html.parser")

    try:
        token = soup.find('input', {'id':'tk'}).attrs["value"]
    except Exception as e: 
        logging.error("There is no token...exiting")
        sys.exit(1)


    # Submit the request
    post_data = {'tk': token,
            'date': str(dt.year),
            'datemonth': f'{dt.year}{dt.month:02d}',
            'platform': PLATFORM,
            'timeframe': time_frame,
            'fxpair': symbol.upper()}


    resp = requests.post(url = GET_HISTDATA_URL, data=post_data, headers=HEADERS )

    if len(resp.content) == 0:
        logging.info("> No data was found")

        return (False, path) 


    # Create the filename 
    filename   = f"HISTDATA_COM_{PLATFORM}_{symbol}_{time_frame}{dt.year}{dt.month}.zip"
    
    # Create the save directory if no path provided
    if path == "":
        path = os.path.join(os.path.abspath(''), "temp_hist")

        # Check if `temp_hist` does not already exist
        if not os.path.isdir(path):
            try:
                os.makedirs(path)
            except:
                logging.error("> Unable to create the `temp_hist` folder")
                logging.info("> All zip files will be saved in this folder")
                path = os.path.abspath('')
               

    # Save the zip file     
    local_name = os.path.join(path, filename)
    with open(local_name, "wb") as f: 
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    
    return (True, path)


def create_df(path: str, tf:str) -> pd.DataFrame:
    """
    Create a dataframe from all the csv files from HistData

    :params path is where the csv files are located 
    :type :str 

    :params tf is the timeframe
    :type :str 


    :return: (pd.DataFrame)
    """

    if tf == "tick":
        csv_files = [  p  for p in Path(path).rglob('*T*.csv')]
    else:
        csv_files = [  p  for p in Path(path).rglob('*M1*.csv')]

    if len(csv_files) == 0:
        logging.error("> No files found")
        sys.exit(1)

    logging.info(f"> Found {len(csv_files)} files")

    all_df = pd.DataFrame()
    for csv in csv_files:
        df = pd.read_csv(csv, header=None)
        all_df = pd.concat([all_df, df])

    # Convert str to datetime
    logging.info("Formatting the dates")
    ms  = all_df.iloc[:,0].apply(lambda x: x.split(" ")[1].strip() )
    ymd = all_df.iloc[:,0].apply(lambda x: datetime.datetime.strptime(x.split(" ")[0].strip(), "%Y%m%d") )
    dt  = ymd + pd.TimedeltaIndex(ms.astype(int), unit='ms')
    
    # Create the datetime column 
    all_df["date"] = dt 

    # Rename the columns 
    all_df.rename(columns={0:"time", 1:"bid", 2:"ask", 3: "volume"}, inplace=True)
    
    # Drop the time column 
    all_df.drop(["time", "volume"], axis=1, inplace=True)

    # Set the index 
    all_df.set_index("date", inplace=True)

    return all_df 


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

    # Resample 
    ohlc = df.drop(["ask"], axis=1)
    ohlc = ohlc.resample(rule).ohlc()

    # Drop the multiindex column
    ohlc.columns = ohlc.columns.droplevel(0)
    
    return ohlc



def fetch_from_hist(symbol: str, start:str, end:str, tf:str, path: str="", keep:str ="") -> pd.DataFrame:
    """
    Fetch the data from Histdata

    :params symbol is the currency pair 
    :type :str 

    :params start is the start date 
    :type :str 

    :params end is the end date 
    :type :str 

    :params tf is the timeframe
    :type :str 

    :params path is where the files need to be saved 
    :type :str 

    :params keep the zip files?
    :type :str  

    :return: (pd.DataFrame)
    """

    # Get the date range, if any 
    if end != "":
        start_dt   = datetime.datetime.strptime(start, "%Y%m%d")
        end_dt     = datetime.datetime.strptime(end, "%Y%m%d")
        date_range = list(pd.date_range(start_dt, end_dt, freq="1d"))

        date_range = [ d.strftime("%Y%m%d") for d in date_range]

    else:
        date_range = [start]

    # Download the zip file(s)
    for dt in date_range:
        try:
            res, path = download(symbol, tf, dt) 
            if res:
                logging.info("> File downloaded successfully")
        except Exception as e:
            logging.error(f"> {e}")
            sys.exit(1)

    # Unzip the files 
    zip_files = glob.glob(os.path.join(path,"*.zip"))
    zip_result = unzip_files(zip_files, path)


    # create one dataframe 
    price_df = create_df(path, tf)

    # Resample if needed 
    if tf != "tick" and tick != "1m":
        ohlc = resample_ohlc(price_df)

        # Output 
        return ohlc 

    # Clean up if necessary 
    if keep != "F" or keep == "":
        pass 

    return price_df

def main():
    """
    """
    pass


if __name__ == "__main__":
    main()

