"""
List the major forex pairs that can be downloaded

Author  : Zetra
Date    : 20230514
License : MIT
"""
import click 

from utils import OUTPUT, SOURCES, SYMBOLS ,TIMEFRAMES

@click.command()
def info():
    """
    List all forex pairs that are available
    """

    # List the data sources
    sources = SOURCES   
    click.echo(click.style("\n> Here are the available sources: ", fg="blue"))
    for i, source in enumerate(sources):
        click.echo(click.style(f"{i+1}. {source}", fg="blue"))     

    # List the available currency pairs 
    pairs = SYMBOLS 
    click.echo(click.style("\n> Here are the available pairs: ", fg="blue"))
    for i, pair in enumerate(pairs):
        click.echo(click.style(f"{i+1}. {pair}", fg="blue"))

    # List the timeframes
    timeframes = TIMEFRAMES 
    click.echo(click.style("\n> Here are the available timeframes: ", fg="blue"))
    for i, tf in enumerate(timeframes):
        click.echo(click.style(f"{i+1}. {tf}", fg="blue"))

    # List available output
    output = OUTPUT 
    click.echo(click.style("\n> Here are the available output types: ", fg="blue"))
    for i, out in enumerate(output):
        click.echo(click.style(f"{i+1}. {out}", fg="blue"))    

if __name__ == "__main__":
    info()