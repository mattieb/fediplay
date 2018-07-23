'''Secret storage.'''

import os
path = os.path

import appdirs
import click
from keyring import get_password, set_password


SERVICE_NAME = 'fediplay'
CREDENTIAL_CLIENT_ID = 'client_id'
CREDENTIAL_CLIENT_SECRET = 'client_secret'
CREDENTIAL_ACCESS_TOKEN = 'access_token'

dirs = appdirs.AppDirs('fediplay', 'zigg')

def build_username(instance, credential_kind):
    return credential_kind + '@' + instance

def set_credential(instance, credential_kind, credential):
    set_password(SERVICE_NAME, build_username(instance, credential_kind), credential)

def get_credential(instance, credential_kind):
    return get_password(SERVICE_NAME, build_username(instance, credential_kind))

def has_credential(instance, credential_kind):
    return get_credential(instance, credential_kind) is not None

def migrate_client_credentials(instance):
    def migrate_and_unlink(filename):
        if path.exists(filename):
            click.echo('==> Migrating client credentials to keyring from ' + filename)

            with open(filename, 'r', encoding='utf-8') as infile:
                client_id = infile.readline().strip()
                client_secret = infile.readline().strip()

            set_credential(instance, CREDENTIAL_CLIENT_ID, client_id)
            set_credential(instance, CREDENTIAL_CLIENT_SECRET, client_secret)

            os.unlink(filename)

    migrate_and_unlink('clientcred.secret')
    migrate_and_unlink(path.join(dirs.user_config_dir, instance + '.clientcred.secret'))

def migrate_access_token(instance):
    def migrate_and_unlink(filename):
        if path.exists(filename):
            click.echo('==> Migrating access token to keyring from ' + filename)

            with open(filename, 'r', encoding='utf-8') as infile:
                access_token = infile.readline().strip()

            set_credential(instance, CREDENTIAL_ACCESS_TOKEN, access_token)

            os.unlink(filename)

    migrate_and_unlink('usercred.secret')
    migrate_and_unlink(path.join(dirs.user_config_dir, instance + '.usercred.secret'))
