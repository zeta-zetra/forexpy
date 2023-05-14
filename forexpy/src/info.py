"""
List the major forex pairs that can be downloaded

Author  : Zetra
Date    : 20230514
License : MIT
"""
import click 

@click.command()
def info():
    """
    List all forex pairs that are available
    """

    # List the data sources
    sources = ["Dukascopy", "MetaTrader5", "Alpha Advantage", "HistData"]
    click.echo(click.style("\n> Here are the available sources: ", fg="blue"))
    for i, source in enumerate(sources):
        click.echo(click.style(f"{i+1}. {source}", fg="blue"))     

    # List the available currency pairs 
    pairs = ["AUDUSD","EURUSD", "GBPUSD", "NZDUSD", "USDCAD", "USDCHF", "USDJPY"]
    click.echo(click.style("\n> Here are the available pairs: ", fg="blue"))
    for i, pair in enumerate(pairs):
        click.echo(click.style(f"{i+1}. {pair}", fg="blue"))

    # List the timeframes
    timeframes = ["tick","1m","5m", "15m", "30m", "1h", "4h", "1d"]
    click.echo(click.style("\n> Here are the available timeframes: ", fg="blue"))
    for i, tf in enumerate(timeframes):
        click.echo(click.style(f"{i+1}. {tf}", fg="blue"))



if __name__ == "__main__":
    info()