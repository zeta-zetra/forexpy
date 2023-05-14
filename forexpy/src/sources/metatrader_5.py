"""
This is the MetaTrader5 file that gets the rates and ticks

Author  : Zetra
Date    : 20230514
License : MIT
"""

import emoji
import datetime
import logging
import MetaTrader5 as mt5
import pandas as pd
import pytz
import sys

from typing import Union


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

TIMEFRAMES = {"1m": mt5.TIMEFRAME_M1,"5m":mt5.TIMEFRAME_M5 ,
             "15min":mt5.TIMEFRAME_M15, "30min":mt5.TIMEFRAME_M30, "1h": mt5.TIMEFRAME_H1,
              "4h": mt5.TIMEFRAME_H4, "1d": mt5.TIMEFRAME_D1}


def fetch_from_metatrader(symbol: str, start: str, tf:str= "tick", n: int = 10, end: str="") -> pd.DataFrame:
    """
    Fetch forex data from a connected Metatrader5 broker

    :params symbol 
    :type :str

    :params start - start date
    :type :str

    :params end - end date
    :type :str

    :params tf - The timeframe: [ticks, 1m, 5m, 15m, 30m, 1h, 4h, 1d]
    :type :str

    :params n - number of look back period.
    :type :int

    :return pd.DataFrame
    """

    if tf == "tick":
        if end == "":
            ticks = get_ticks(symbol, n)

        elif end != "":
            ticks = get_ticks_range(symbol, start, end)
 
        return ticks 
    else:
        timeframe = TIMEFRAMES[tf]
        if end == "":
            rates = get_rates(symbol, n, timeframe=timeframe)
        elif end != "" :
            rates = get_rates_range(symbol, timeframe, start, end)

        return rates 

def get_ticks_range(symbol: str, start: str, end: str):
    """
    Get ticks based on date range
    """
    # connect to MetaTrader 5
    if not mt5.initialize():
        logging.error(emoji.emojize(":red_circle: MT5 initialize() failed"))
        mt5.shutdown()
        quit()

    try:
        from_date  = datetime.datetime.strptime(start,"%Y%m%d")
        to_date    =  datetime.datetime.strptime(end,"%Y%m%d")
    except Exception as e:
        logging.error(emoji.emojize(":red_circle: Error with the date format. Make sure to format is YYYYMMDD"))
        sys.exit(1)


    # Get the ticks from the broker
    ticks = mt5.copy_ticks_range(symbol, from_date, to_date, mt5.COPY_TICKS_ALL)

    # Convert the tuple to df
    ticks_frame = pd.DataFrame(ticks)

    # Check if empty
    if len(ticks_frame) == 0:
        return ticks_frame

    # Convert the seconds to datetime
    ticks_frame["time"] = pd.to_datetime(ticks_frame["time"], unit="s")

    # Set time as index
    ticks_frame.set_index("time", inplace=True)

    # Shutdown MT5
    mt5.shutdown()

    return ticks_frame

def get_rates_range(symbol: str, timeframe:str, start: str, end: str):
    """
    Get rates based on date range
    """

     # connect to MetaTrader 5
    if not mt5.initialize():
        logging.error(emoji.emojize(":red_circle: MT5 initialize() failed"))
        mt5.shutdown()
        quit()
    
    try:
        from_date  = datetime.datetime.strptime(start,"%Y%m%d")
        to_date    =  datetime.datetime.strptime(end,"%Y%m%d")
    except Exception as e:
        print("Error with the date format. Make sure to format is YYYYMMDD")
        sys.exit(1)

    # Get rates 
    rates = mt5.copy_rates_range(symbol, timeframe, from_date, to_date)

    # Convert tuple to dataframe
    rates_frame = pd.DataFrame(rates)

    # Check if empty
    if len(rates_frame) == 0:
        return rates_frame

    # Format the time
    rates_frame["time"] = pd.to_datetime(rates_frame['time'], unit='s')

    # Convert time to right format
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], format='%Y-%m-%d')

    # Set column time as index
    rates_frame.set_index('time', inplace=True)

    # Shutdown MT5
    mt5.shutdown()

    return rates_frame   


def get_ticks(symbol: str, n_ticks: int)-> pd.DataFrame:
    """
    Get ticks from MetaTrader 5 broker from today 

    :params symbol 
    :type :str

    :params n_ticks
    :type :int

    return ticks 
    """
    # connect to MetaTrader 5
    if not mt5.initialize():
        logging.error(emoji.emojize(":red_circle: MT5 initialize() failed"))
        mt5.shutdown()
        quit()

    # Get the current utc time
    from_date = datetime.datetime.now()

    # Get the ticks from the broker
    ticks = mt5.copy_ticks_from(symbol, from_date, n_ticks, mt5.COPY_TICKS_ALL)

    # Convert the tuple to df
    ticks_frame = pd.DataFrame(ticks)
    print(ticks_frame)
    # Check if empty
    if len(ticks_frame) == 0:
        return ticks_frame


    # Convert the seconds to datetime
    ticks_frame["time"] = pd.to_datetime(ticks_frame["time"], unit="s")

    # Set time as index
    ticks_frame.set_index("time", inplace=True)

    # Shutdown MT5
    mt5.shutdown()

    return ticks_frame


def get_rates(symbol: str, n_candles: int, timeframe = mt5.TIMEFRAME_D1) -> pd.DataFrame:
    """
    Function to get data from MetaTrader 5 broker
    """

    # connect to MetaTrader 5
    if not mt5.initialize():
        logging.error(emoji.emojize(":red_circle: MT5 initialize() failed"))
        mt5.shutdown()
        quit()


    # Current date extract 
    utc_from = datetime.datetime.now()

    # Get rates 
    rates = mt5.copy_rates_from(symbol, timeframe, utc_from, n_candles)

    # Convert tuple to dataframe
    rates_frame = pd.DataFrame(rates)

    # Check if empty
    if len(rates_frame) == 0:
        return rates_frame

    # Format the time
    rates_frame["time"] = pd.to_datetime(rates_frame['time'], unit='s')

    # Convert time to right format
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], format='%Y-%m-%d')

    # Set column time as index
    rates_frame.set_index('time', inplace=True)

    # Shutdown MT5
    mt5.shutdown()

    return rates_frame