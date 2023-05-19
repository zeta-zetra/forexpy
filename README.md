# forexpy - Collect forex data with Python

`forexpy` is a python command-line package that can download currency exchange rates from multiple soruces. The
package can provide forex data for storage, strategy development, etc.

Table of Contents
=================

* [Data Sources](#data-sources) 
* [Usage](#usage)
* [Disclaimer](#disclaimer)
* [Contact](#contact)


## Data Sources

Here is a list of data sources:

 - [x] MetaTrader5

 - [x] Dukascopy

 - [x] Histdata.com 



## Usage

There is one main function in the library which is `fetch.py`.  The function does all the heavy lifting of calling all the other functions
to get the given task accomplished. The `fetch.py` has options. To get a view of the options, run `python fetch.py --help`:

    Usage: fetch.py [OPTIONS]

    Options:
    --source TEXT  Source for the forex data
    --symbol TEXT  Currency pair to download
    --start TEXT   Start date to download the data
    --end TEXT     End date to download the data
    --tf TEXT      Timeframe to download
    --n INTEGER    Number of candles to download
    --output TEXT  Type of output for the data
    --path TEXT    Full Path to save the data
    --keep TEXT    Keep the .bi5 from Dukascopy or the zip files from HistData.
                    To keep the files set: --keep T
    --help         Show this message and exit.

 ### Available Currency pairs

   - AUDUSD 
  
   - EURUSD 
   
   - GBPUSD 
   
   - NZDUSD 
   
   - USDCAD 
   
   - USDCHF  
   
   - USDJPY

 ### Available TimeFrames 

   - Tick
   
   - 1 Min
   
   - 5 Min
   
   - 15 Min 
   
   - 30 Min 
   
   - 1 Hour 
   
   - 4 Hour 
   
   - 1 Day 

### Dukascopy


### Metatrader5


### HistData 



## Disclaimer

I have no affiliation with the data sources used in the package. 

## Contact

If you want to contact me: info@zetra.io



