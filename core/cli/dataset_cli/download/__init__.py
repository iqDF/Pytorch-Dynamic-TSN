import os
import requests

import click
from click import echo

from .clients import (
    URLClient,
    Kaggle
)

__all__ = ['api_download', 'url_download']

API_HANDLER_MAP = {
    'KAGGLE': Kaggle,
}


"""
API Download

See/edit above lists of supported API where 
data can be downloaded.
"""

@click.command()
@click.argument(
    'api',
    envvar = 'API',
    type = click.Choice(
        [api for api in API_HANDLER_MAP.keys()],
        case_sensitive = False
    )
)
@click.argument(
    'dataset',
    envvar = 'DATASET',
    type = click.STRING
)
@click.argument(
    'save_folder',
    envvar = 'SAVE_FOLDER',
    type = click.Path(exists=False, dir_okay=True)
)
@click.option(
    '--credential_file',
    default = "",
    type = click.File(mode='w', lazy=False)
)
@click.option(
    '--unzip/--dont_unzip',
    default = False
)
def api_download(
    api, 
    dataset, 
    save_folder, 
    credential_file,
    unzip
):
    """
    Usage: 
        > dataset_cli api_download API={YOUR_API} DATASET={YOUR_DATASET} \ 
            SAVE_FOLDER={YOUR_SAVE_DIR} [--OPTIONS]
    """
    api_client = API_HANDLER_MAP[api](
        dataset, save_folder,
        credential_file, unzip
    )
    api_client()  # __call__ to authenticate and download dataset


"""
URL Download
Download manually using HTTP requests.
"""

@click.command()
@click.argument(
    'url',
    type = click.STRING
)
@click.argument(
    'save_folder',
    type = click.Path(exists=False, dir_okay=True)
)
@click.option('--unzip/--dont_unzip', default=False)
def url_download(ctx):
    client = URLClient(url, save_folder, unzip)
    client()  # __call__ to authenticate and download dataset
