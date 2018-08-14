'''Mastodon interface.'''

from os import umask

import click
from lxml.etree import HTML # pylint: disable=no-name-in-module
import mastodon
from youtube_dl.utils import DownloadError

import fediplay.keyring as keyring
from fediplay.queue import Queue

Mastodon = mastodon.Mastodon


def api_base_url(instance):
    '''Create an API base url from an instance name.'''

    return 'https://' + instance

class StreamListener(mastodon.StreamListener):
    '''Listens to a Mastodon timeline and adds links the given Queue.'''

    def __init__(self, queue, users):
        self.queue = queue
        self.users = users

    def on_update(self, status):
        if self.users and status.account.username not in self.users:
            return
        tags = extract_tags(status)
        if 'fediplay' in tags:
            links = extract_links(status)
            for link in links:
                try:
                    click.echo('==> Trying {}'.format(link))
                    self.queue.add(link)
                    return
                except DownloadError:
                    pass

def register(instance):
    '''Register fediplay to a Mastodon server and save the client credentials.'''

    client_id, client_secret = Mastodon.create_app('fediplay', scopes=['read'], api_base_url=api_base_url(instance))
    keyring.set_credential(instance, keyring.CREDENTIAL_CLIENT_ID, client_id)
    keyring.set_credential(instance, keyring.CREDENTIAL_CLIENT_SECRET, client_secret)

def build_client(instance, client_id, client_secret, access_token=None):
    '''Builds a Mastodon client.'''

    return Mastodon(api_base_url=api_base_url(instance),
                    client_id=client_id, client_secret=client_secret, access_token=access_token)

def get_auth_request_url(instance, client_id, client_secret):
    '''Gets an authorization request URL from a Mastodon instance.'''

    return build_client(instance, client_id, client_secret).auth_request_url(scopes=['read'])

def login(instance, client_id, client_secret, grant_code):
    '''Log in to a Mastodon server and save the user credentials.'''

    client = build_client(instance, client_id, client_secret)
    access_token = client.log_in(code=grant_code, scopes=['read'])
    keyring.set_credential(instance, keyring.CREDENTIAL_ACCESS_TOKEN, access_token)

def stream(instance, users, client_id, client_secret, access_token, cache_dir='.'):
    '''Stream statuses and add them to a queue.'''

    client = build_client(instance, client_id, client_secret, access_token)
    users = [normalize_username(u, instance) for u in users]
    listener = StreamListener(Queue(cache_dir), users)
    click.echo('==> Streaming from {}'.format(instance))
    client.stream_user(listener)

def extract_tags(toot):
    '''Extract tags from a toot.'''

    return [tag['name'] for tag in toot['tags']]

def normalize_username(user, instance):
    # If user was specified with an @ at beggining, remove it
    user = user.lstrip('@')
    tmp = user.split('@')
    # remove instance if it is our own instance
    return user if (len(tmp) == 1 or tmp[1] != instance) else tmp[0]


def link_is_internal(link):
    '''Determines if a link is internal to the Mastodon instance.'''

    classes = link.attrib.get('class', '').split(' ')
    if classes:
        return 'mention' in classes

    return False

def extract_links(toot):
    '''Extract all external links from a toot.'''

    html = HTML(toot['content'])
    all_links = html.cssselect('a')
    return [link.attrib['href'] for link in all_links if not link_is_internal(link)]
