'''Entry point for command-line interface.'''

from os import path
import sys

import click
from mastodon import Mastodon

import fediplay.env as env
import fediplay.mastodon as mastodon

def api_base_url_from_instance(instance):
    return 'https://' + instance

@click.group()
def cli():
    '''Command-line interface group.'''

    pass

@cli.command()
@click.argument('instance')
def register(instance):
    '''Register fediplay to the instance.'''

    api_base_url = api_base_url_from_instance(instance)

    if path.exists('clientcred.secret'):
        click.echo('clientcred.secret already exists')
        sys.exit(1)

    mastodon.register(api_base_url)

@cli.command()
@click.argument('instance')
def login(instance):
    '''Log in to the instance.'''

    api_base_url = api_base_url_from_instance(instance)

    if path.exists('usercred.secret'):
        click.echo('usercred.secret already exists')
        sys.exit(1)

    if not path.exists('clientcred.secret'):
        click.echo('clientcred.secret does not exist; try `fediplay register`')
        sys.exit(1)

    client = Mastodon(client_id='clientcred.secret', api_base_url=api_base_url)

    click.echo('Open this page in your browser and follow the instructions.')
    click.echo('Paste the code here.')
    click.echo('')
    click.echo(client.auth_request_url())
    click.echo('')

    grant_code = input('Code: ')
    mastodon.login(client, grant_code)

@cli.command()
@click.argument('instance')
def stream(instance):
    '''Stream music from the instance.'''

    api_base_url = api_base_url_from_instance(instance)

    if not path.exists('clientcred.secret'):
        click.echo('clientcred.secret does not exist; try `fediplay register`')
        sys.exit(1)

    if not path.exists('usercred.secret'):
        click.echo('usercred.secret does not exist; try `fediplay login`')
        sys.exit(1)

    mastodon.stream(api_base_url)
