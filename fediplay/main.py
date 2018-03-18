'''Entry point for command-line interface.'''

from os import path
import sys

from mastodon import Mastodon

import fediplay.env as env
from fediplay.mastodon import stream, register, login

def main():
    '''Run fediplay command-line interface.'''

    api_base_url = env.api_base_url()
    if not api_base_url:
        print('FEDIPLAY_API_BASE_URL environment variable not set')
        sys.exit(1)

    if not path.exists('clientcred.secret'):
        print('==> No clientcred.secret; registering application')
        register(api_base_url)

    if not path.exists('usercred.secret'):
        print('==> No usercred.secret; logging in')
        client = Mastodon(client_id='clientcred.secret', api_base_url=api_base_url)

        print('Open this page in your browser and follow the instructions.')
        print('Paste the code here.')
        print('')
        print(client.auth_request_url())
        print('')

        grant_code = input('Code: ')
        login(client, grant_code)

    stream(api_base_url)
