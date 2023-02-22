'''Entry point for command-line interface.'''

options = {'debug': False}

import os
path = os.path
import sys

import appdirs
import click
import atexit
from mastodon import Mastodon

from fediplug.dirs import DIRS
import fediplug.mastodon as mastodon
import fediplug.keyring as keyring

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
        click.echo('user credential for {} does not exist; try `fediplug login`'.format(instance))
        sys.exit(1)

    return keyring.get_credential(instance, keyring.CREDENTIAL_ACCESS_TOKEN)

def get_client_credentials(instance):
    '''Ensure the client credentials exist.'''

    keyring.migrate_client_credentials(instance)

    if not (keyring.has_credential(instance, keyring.CREDENTIAL_CLIENT_ID) and
            keyring.has_credential(instance, keyring.CREDENTIAL_CLIENT_SECRET)):
        click.echo('client credentials for {} do not exist; try `fediplug register`'.format(instance))
        sys.exit(1)

    return (
        keyring.get_credential(instance, keyring.CREDENTIAL_CLIENT_ID),
        keyring.get_credential(instance, keyring.CREDENTIAL_CLIENT_SECRET)
    )

@click.group()
@click.option('-d', '--debug', is_flag=True, help='Print debug messages.')
def cli(debug):
    '''A program to play music your friends post on Mastodon.'''

    options['debug'] = debug

    ensure_dirs()

@cli.command()
@click.argument('instance')
def register(instance):
    '''Register fediplug on your Mastodon instance.'''

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
@click.argument('users', nargs=-1)
@click.option('--clean-up-files', is_flag=True)
def stream(instance, users, clean_up_files):
    '''Stream music from your timeline.'''
    if ( clean_up_files ):
        atexit.register(delete_files)

    client_id, client_secret = get_client_credentials(instance)
    access_token = get_access_token(instance)

    mastodon.stream(instance, users, client_id, client_secret, access_token, cache_dir=DIRS.user_cache_dir)

def delete_files():
    cache_dir = DIRS.user_cache_dir
    for the_file in os.listdir(cache_dir):
        file_path = os.path.join(cache_dir, the_file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print('deleted ' + the_file)

@cli.command()  
def clean_up_files():
    delete_files()


