# forexpy - Collect forex data with Python

`forexpy` is a python command-line package that can download currency exchange rates from multiple soruces. The
package can provide forex data for storage, strategy development, etc.

Table of Contents
=================

* [Data Sources](#data-sources) 
* [Usage](#usage)
   * [Available Currency pairs](#available-currency-pairs)
   * [Available TimeFrames](available-timeFrames)
   * [Dukascopy](#dukascopy)
   * [Metatrader5](#metatrader5)
   * [HistData](#histdata)
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

When you run `python info.py`, you will get information about available source, pairs, etc. Here is a sample output:

    > Here are the available sources:
        1. dukas
        2. metatrader
        3. hist
    > Here are the available pairs:
        1. AUDUSD
        2. EURUSD
        3. GBPUSD
    > Here are the available timeframes:
        1. tick
        2. 1m
        3. 5m
    > Here are the available output types:
        1. csv

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

   *Note*: To arrive at some timeframes, 1 minute data is downloaded and resampled to the desired timeframe. 



### Dukascopy

By default if no source is provided, the data will be fetched from [Dukascopy](https://www.dukascopy.com/trading-tools/widgets/quotes/historical_data_feed). 

When you run the code below:

    python fetch.py 

you are asking data for EURUSD tick from Dukascopy for today. **No data will be downloaded.**. Dukascopy does not provide real-time data, try [Metatrader5](#metatrader5).

For Dukascopy make sure your start and/or end dates are at least a month before the current date. This will download EURUSD tick data for 2022-10-02 only. 

    python fetch.py --start 20221002  

You can download data between a range of dates. This will download EURUSD tick between 2022-10-02 and 2022-11-10

    python fetch.py --start 20221002 --end 20221110  

You can download for different timeframes as well:

1. **1 Min**

        python fetch.py --start 20221002 --tf 1m 

2. **5 Min** 

        python fetch.py --start 20221002 --end 20221015 --tf 5m

3. **15 Min** 

        python fetch.py --start 20221102 --end 20221115 --tf 15m

4. **30 Min**

        python fetch.py --start 20221002 --end 20221015 --tf 30m

5. **1 Hour** 

        python fetch.py --symbol USDJPY --start 20221002 --end 20221015 --tf 1h

6. **1 Day** 

        python fetch.py --symbol GBPUSD  --start 20221002 --end 20221015 --tf 1d

When downloading data from Dukascopy, `.bi5` are saved in a folder and then used to create the final csv file. The `--keep` argument is used to 
tell forexpy if these files should be deleted or not. By default there are deleted. To keep them, run:

    python fetch.py --start 20221002 --end 20221015 --tf 1d --keep T 


If you have a folder of `.bi5` files then you can use `decompressor.py` to decompress them. Simply run:

    python decompressor.py --path XXXX 

You can also state where the final output should be saved:

    python decompressor.py --path XXXX --save XXXX

### Metatrader5


### HistData 



## Disclaimer

I have no affiliation with the data sources used in the package. 

## Contact

If you want to contact me: info@zetra.io



