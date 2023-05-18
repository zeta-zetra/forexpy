"""
Extra functionality
"""

import datetime

from typing import Dict, Tuple, Union


SOURCES    = ["dukas", "metatrader", "alpha", "hist"]
SYMBOLS    = ["AUDUSD","EURUSD", "GBPUSD", "NZDUSD", "USDCAD", "USDCHF", "USDJPY"]
TIMEFRAMES = ["tick","1m","5m", "15m", "30m", "1h", "4h", "1d"]
RESAMPLE_DICT = {"1m":"1Min","5m":"5Min", "15m":"15Min", "30m":"30Min", "1h":"1H", "4h":"4H", "1d":"1D"}
OUTPUT     = ["csv"]

def sanitize_inputs(source: str, symbol: str, start: str, end: str, tf: str="tick", output: str ="csv") -> Union[Dict[str, Union[int, str]] ,Dict[str, Union[int, Tuple[str, str, str, str, str, str] ]]]:
    """
    Check if all inputs by the user are allowed.
    

    :params source is data source 
    :type :str 

    :params symbol is the currency pair
    :type :str 

    :params start is the from date 
    :type :str 

    :params end is the end date 
    :type :str 

    :params tf is the timeframe
    :type :str 

    :params output is the type of file output
    :type :str 


    :return: Union[Dict[str, Union[int, str]] ,Dict[str, Union[int, Tuple[str, str, str, str, str, str] ]]]
    """

    if source.lower() not in SOURCES:
        msg = "> Provided source does not exist. Please run the `info.py` to see sources"
        return {"error": 1, "body": msg}

    if symbol.upper() not in SYMBOLS:
        msg = "> Provided symbol does not exist. Please run the `info.py` to see symbols"
        return {"error": 1, "body": msg}

    if tf.lower() not in TIMEFRAMES:
        msg = "> Provided timeframe does not exist. Please run the `info.py` to see timeframe"
        return {"error": 1, "body": msg}       

    if output.lower() not in OUTPUT:
        msg = "> Provided output does not exist. Please run the `info.py` to see timeframe"
        return {"error": 1, "body": msg}          

    if start == "" or len(start) < 8 or len(start) > 8:
        msg = "> Start date is empty or not in correct format. Enter start date as YYYYMMDD"
        return {"error": 1, "body": msg}        
    
    if end != "":
        if len(end) > 8 or len(end) < 8:
                 msg = "> End date not in correct format. Enter end date as YYYYMMDD"
                 return {"error": 1, "body": msg}    

    if end != "" and start !="":
        # Check if start date is less than end date 
        start_dt    = datetime.datetime.strptime(start,"%Y%m%d")
        end_dt      = datetime.datetime.strptime(end,"%Y%m%d")
        
        if start_dt > end_dt:
                 msg = "> Start date must be LESS than End date."
                 return {"error": 1, "body": msg}  

    return {"error": 0, "body": (source.lower(), symbol.upper(), start, end, tf.lower(), output.lower())}

