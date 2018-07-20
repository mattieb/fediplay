'''Entry point for command-line interface.'''

import os
import sys

import appdirs
import click
from mastodon import Mastodon

import fediplay.mastodon as mastodon

path = os.path

dirs = appdirs.AppDirs('fediplay', 'zigg')


def build_usercred_filename(instance):
    '''Generate a usercred filename from an instance name.'''

    return path.join(dirs.user_config_dir, instance + '.usercred.secret')

def build_clientcred_filename(instance):
    '''Generate a clientcred filename from an instance name.'''

    return path.join(dirs.user_config_dir, instance + '.clientcred.secret')

def ensure_dirs():
    '''Make sure the application directories exist.'''

    if not path.exists(dirs.user_config_dir):
        os.makedirs(dirs.user_config_dir)

    if not path.exists(dirs.user_cache_dir):
        os.makedirs(dirs.user_cache_dir)

def ensure_usercred(instance):
    '''Ensure the usercred file exists.'''

    usercred = build_usercred_filename(instance)

    if path.exists(usercred):
        return usercred

    if path.exists('usercred.secret'):
        click.echo('==> Migrating usercred.secret to ' + usercred)
        os.rename('usercred.secret', usercred)
        return usercred

    click.echo(usercred + ' does not exist; try `fediplay login`')
    sys.exit(1)

def ensure_clientcred(instance):
    '''Ensure the clientcred file exists.'''

    clientcred = build_clientcred_filename(instance)

    if path.exists(clientcred):
        return clientcred

    if path.exists('clientcred.secret'):
        click.echo('==> Migrating clientcred.secret to ' + clientcred)
        os.rename('clientcred.secret', clientcred)
        return clientcred

    click.echo(clientcred + ' does not exist; try `fediplay register`')
    sys.exit(1)

@click.group()
def cli():
    '''Command-line interface group.'''

    ensure_dirs()

    pass

@cli.command()
@click.argument('instance')
def register(instance):
    '''Register fediplay to the instance.'''

    clientcred = build_clientcred_filename(instance)

    if path.exists(clientcred):
        click.echo(clientcred + ' already exists')
        sys.exit(1)

    mastodon.register(instance, clientcred)

@cli.command()
@click.argument('instance')
def login(instance):
    '''Log in to the instance.'''

    clientcred = ensure_clientcred(instance)

    usercred = build_usercred_filename(instance)
    if path.exists(usercred):
        click.echo(usercred + ' already exists')
        sys.exit(1)

    client = mastodon.build_client(instance, clientcred)

    click.echo('Open this page in your browser and follow the instructions.')
    click.echo('Paste the code here.')
    click.echo('')
    click.echo(mastodon.get_auth_request_url(client))
    click.echo('')

    grant_code = input('Code: ')
    mastodon.login(client, grant_code, usercred)

@cli.command()
@click.argument('instance')
def stream(instance):
    '''Stream music from the instance.'''

    clientcred = ensure_clientcred(instance)
    usercred = ensure_usercred(instance)

    mastodon.stream(instance, clientcred, usercred, cache_dir=dirs.user_cache_dir)
