'''Entry point for command-line interface.'''

from os import path
import sys

import click
from mastodon import Mastodon

import fediplay.mastodon as mastodon


def build_usercred_filename(instance):
    '''Generate a usercred filename from an instance name.'''

    return instance + '.usercred.secret'

def build_clientcred_filename(instance):
    '''Generate a clientcred filename from an instance name.'''

    return instance + '.clientcred.secret'

@click.group()
def cli():
    '''Command-line interface group.'''

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

    usercred = build_usercred_filename(instance)
    clientcred = build_clientcred_filename(instance)

    if path.exists(usercred):
        click.echo(usercred + ' already exists')
        sys.exit(1)

    if not path.exists(clientcred):
        click.echo(clientcred + ' does not exist; try `fediplay register`')
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

    clientcred = build_clientcred_filename(instance)
    usercred = build_usercred_filename(instance)

    if not path.exists(clientcred):
        click.echo(clientcred + ' does not exist; try `fediplay register`')
        sys.exit(1)

    if not path.exists(usercred):
        click.echo(usercred + ' does not exist; try `fediplay login`')
        sys.exit(1)

    mastodon.stream(instance, clientcred, usercred)
