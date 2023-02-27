'''Entry point for command-line interface.'''

options = {'debug': False}

import os
path = os.path
import sys

import atexit
import appdirs
import click as click
import atexit
from mastodon import Mastodon
import asyncio

from fediplug.dirs import DIRS
import fediplug.mastodon as mastodon
import fediplug.keyring as keyring
import fediplug.buttplugio as buttplugio

def get_access_token(instance):
    '''Ensure the user credential exists.'''

    keyring.migrate_access_token(instance)

    if not keyring.has_credential(instance, keyring.CREDENTIAL_ACCESS_TOKEN):
        click.echo(f'user credential for {instance} does not exist; try `fediplug login`')
        sys.exit(1)

    return keyring.get_credential(instance, keyring.CREDENTIAL_ACCESS_TOKEN)

def get_client_credentials(instance):
    '''Ensure the client credentials exist.'''

    keyring.migrate_client_credentials(instance)

    if not (keyring.has_credential(instance, keyring.CREDENTIAL_CLIENT_ID) and
            keyring.has_credential(instance, keyring.CREDENTIAL_CLIENT_SECRET)):
        click.echo(f'client credentials for {instance} do not exist; try `fediplug register`')
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
def stream(instance, users):
    '''Control buttplug.io device from your timeline.'''

    event_loop = asyncio.get_event_loop()
    plug_client = event_loop.run_until_complete(buttplugio.connect_plug_client())
    plug_client = event_loop.run_until_complete(buttplugio.scan_devices(plug_client))

    client_id, client_secret = get_client_credentials(instance)
    access_token = get_access_token(instance)

    mastodon.stream(instance, users, client_id, client_secret, access_token, plug_client, event_loop)
