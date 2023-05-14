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



@click.command()
@click.option("--source", default="dukas", help="Source for the forex data")
@click.option("--symbol", default="EURUSD", help="Currency pair to download")
@click.option("--start", default=datetime.datetime.now().strftime('%Y%m%d'), help="Start date to download the data")
@click.option("--end", default="", help="End date to download the data")
@click.option("--tf", default="tick", help="Timeframe to download")
@click.option("--n", default=10, help="Number of candles to download")
@click.option("--output", default="csv", help="Type of output for the data")
@click.option("--path", default="", help="Full Path to save the data")
def main(source, symbol, start, end, tf, n, output, path):

    # `Clean` the input 
    symbol    = symbol.upper()
    n_candles = int(n)
    tf        = tf.lower()

    if source == "dukas":
        pass 
    elif source == "metatrader":

        # Get the data from MetaTradeer5
        results = fetch_from_metatrader(symbol, start, tf, n, end)
        
        if len(results) == 0:
            click.echo(click.style("> No results found.", fg="red"))
            sys.exit(1)

        # Set the directory to save the data
        dir_     = Path(os.path.abspath("")).parents[0]
        dir_data = os.path.join(dir_, "data")

        # Set the filename
        filename = f"{symbol}-{source}-{tf}-{start}.csv"
        
        # Create a data folder if possible to save the file
        # If not possible, save the file in the current folder
        if os.path.exists(dir_data):
            results.to_csv(os.path.join(dir_data,filename))
            click.echo(click.style("File saved in the data directory", fg="green"))
        else:
            try:
                os.makedirs(dir_data)
            except Exception as e:
                
                click.echo(click.style("> Failed to create the data directory.", fg="red"))
                click.echo(click.style("> File will be saved in the current folder", fg="blue"))
                dir_data = os.path.abspath("")

            results.to_csv(os.path.join(dir_data,filename))

    elif source == "alpha":
        pass
    elif source == "hist":
        pass 
    else:
        click.echo(click.style(f"> The data source `{source}` does not exist. Sources: [dukas, metatrader]", fg="red"))

if __name__ == "__main__":
    main()