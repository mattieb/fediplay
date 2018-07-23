'''Entry point for command-line interface.'''

import os
path = os.path
import sys

import appdirs
import click
from mastodon import Mastodon

from fediplay.dirs import DIRS
import fediplay.mastodon as mastodon
import fediplay.keyring as keyring


def ensure_dirs():
    '''Make sure the application directories exist.'''

    if not path.exists(DIRS.user_config_dir):
        os.makedirs(DIRS.user_config_dir)

    if not path.exists(DIRS.user_cache_dir):
        os.makedirs(DIRS.user_cache_dir)

def get_access_token(instance):
    '''Ensure the user credential exists.'''

    keyring.migrate_access_token(instance)

    if not keyring.has_credential(instance, keyring.CREDENTIAL_ACCESS_TOKEN):
        click.echo('user credential for {} does not exist; try `fediplay login`'.format(instance))
        sys.exit(1)

    return keyring.get_credential(instance, keyring.CREDENTIAL_ACCESS_TOKEN)

def get_client_credentials(instance):
    '''Ensure the client credentials exist.'''

    keyring.migrate_client_credentials(instance)

    if not (keyring.has_credential(instance, keyring.CREDENTIAL_CLIENT_ID) and
            keyring.has_credential(instance, keyring.CREDENTIAL_CLIENT_SECRET)):
        click.echo('client credentials for {} do not exist; try `fediplay register`'.format(instance))
        sys.exit(1)

    return (
        keyring.get_credential(instance, keyring.CREDENTIAL_CLIENT_ID),
        keyring.get_credential(instance, keyring.CREDENTIAL_CLIENT_SECRET)
    )

@click.group()
def cli():
    '''A program to play music your friends post on Mastodon.'''

    ensure_dirs()

@cli.command()
@click.argument('instance')
def register(instance):
    '''Register fediplay on your Mastodon instance.'''

    mastodon.register(instance)

@cli.command()
@click.argument('instance')
def login(instance):
    '''Log in to your Mastodon instance.'''

    client_id, client_secret = get_client_credentials(instance)

    click.echo('Open this page in your browser and follow the instructions.')
    click.echo('Paste the code here.')
    click.echo('')
    click.echo(mastodon.get_auth_request_url(instance, client_id, client_secret))
    click.echo('')

    grant_code = input('Code: ')
    mastodon.login(instance, client_id, client_secret, grant_code)

@cli.command()
@click.argument('instance')
def stream(instance):
    '''Stream music from your timeline.'''

    client_id, client_secret = get_client_credentials(instance)
    access_token = get_access_token(instance)

    mastodon.stream(instance, client_id, client_secret, access_token, cache_dir=DIRS.user_cache_dir)
