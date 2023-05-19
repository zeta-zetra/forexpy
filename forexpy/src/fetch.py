"""
Main function that calls the other functions

Author  : Zetra
Date    : 20230514
License : MIT
"""

import click 
import datetime
import os
from pathlib import Path
import sys

# Own modules
from sources.metatrader_5 import fetch_from_metatrader
from sources.dukascopy import fetch_from_dukascopy
from sources.histdata import fetch_from_hist
from utils import sanitize_inputs

@click.command()
@click.option("--source", default="dukas", help="Source for the forex data")
@click.option("--symbol", default="EURUSD", help="Currency pair to download")
@click.option("--start", default=datetime.datetime.now().strftime('%Y%m%d'), help="Start date to download the data")
@click.option("--end", default="", help="End date to download the data")
@click.option("--tf", default="tick", help="Timeframe to download")
@click.option("--n", default=10, help="Number of candles to download")
@click.option("--output", default="csv", help="Type of output for the data")
@click.option("--path", default="", help="Full Path to save the data")
@click.option("--keep", default="F", help="Keep the .bi5 from Dukascopy or the zip files from HistData. To keep the files set: --keep T ")
def main(source, symbol, start, end, tf, n, output, path, keep):

    # `Clean` the input 
    sanitize_results = sanitize_inputs(source, symbol, start, end, tf, output, path)

    if sanitize_results["error"] == 1:
        msg   = sanitize_results["body"]
        click.echo(click.style(f"{msg}", fg="red"))
        sys.exit(1)
    else:
        source, symbol, start, end, tf, output, path = sanitize_results["body"]


    n_candles = int(n)
    
    if source == "dukas":
        # Get the data from Dukascopy 
        results = fetch_from_dukascopy(symbol, start, end, tf=tf, keep=keep)
    elif source == "metatrader":

        # Get the data from MetaTrader5
        results = fetch_from_metatrader(symbol, start, tf, n, end)
        
    elif source == "hist":
        # Get the data from HistData
        results = fetch_from_hist(symbol, start, end, tf, path=path, keep=keep)
    else:
        click.echo(click.style(f"> The data source `{source}` does not exist. Sources: [dukas, metatrader]", fg="red"))
        sys.exit(1)

    # Save the results if available
    if len(results) == 0:
        click.echo(click.style("> No results found.", fg="red"))
        sys.exit(1)

    # Set the directory to save the data
    if path == "":
        dir_     = Path(os.path.abspath("")).parents[0]
        dir_data = os.path.join(dir_, "data")
    else:
        dir_data = os.path.join(path, "data")

    # Set the filename
    filename = f"{symbol}-{source}-{tf}-{start}.csv"
    
    # Create a data folder if possible to save the file
    # If not possible, save the file in the current folder
    if os.path.exists(dir_data):
        results.to_csv(os.path.join(dir_data,filename))
        click.echo(click.style(f"File saved in the data folder under {path}", fg="green"))
    else:
        try:
            os.makedirs(dir_data)
        except Exception as e:
            
            click.echo(click.style("> Failed to create the data folder.", fg="red"))
            click.echo(click.style("> File will be saved in the current folder", fg="blue"))
            dir_data = os.path.abspath("")

        results.to_csv(os.path.join(dir_data,filename))
        click.echo(click.style("File saved successfully", fg="green"))

if __name__ == "__main__":
    main()