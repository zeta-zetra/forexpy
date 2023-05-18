"""
Decompress .bi5 files from Dukascopy
"""


import click 
import datetime
import glob
import os
from pathlib import Path
import sys

from sources.dukascopy import decompress 

@click.command()
@click.option("--path", default="", help="Full Path to the .bi5 file(s)")
@click.option("--save", default="", help="Full Path to save the .bi5 file(s)")
def decompress_data(path: str, save: str):
    """
    Decompress .bi5 file(s) from Dukascopy 

    The output will be csv file(s)

    :params path to where the .bi5 file(s) are located
    :type :str 

    :params save path for the csv files
    :type :str
    """

    if path == "":
        click.echo(click.style("> No path provided. Provide --path XXXX", fg="red"))
        sys.exit(1)

    files = glob.glob(os.path.join(path, "*.bi5"))

    dir_ =  os.path.join(os.path.abspath(''), "temp") if save == "" else save 

    if save != "":
        if not os.path.isdir(dir_): 
            click.echo(click.style("> --save directory non-existent. ", fg="red"))
            sys.exit(1)

    try:
        if save == "":
            os.makedirs(dir_)
        
        click.echo(click.style("> Folder `temp` has been created to save the files", fg="blue"))
    except:
        click.echo(click.style("> Failed to create the `temp` directory.", fg="red"))
       

    for filename in files:
        result = decompress(filename)

        if len(result) > 0 :
            fn = os.path.basename(filename)
            fn = fn.split(".")[0]
            if save == "":
                click.echo(click.style(f"> {fn} will be saved in the current folder under `temp`", fg="blue"))
            else:
                click.echo(click.style(f"> {fn} will be saved in the specified folder", fg="blue")) 

            result.to_csv(os.path.join(dir_, f"{fn}.csv"))
     


if __name__ == "__main__":
    decompress_data()