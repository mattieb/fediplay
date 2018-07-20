'''Mastodon interface.'''

from os import umask

import click
from lxml.etree import HTML # pylint: disable=no-name-in-module
import mastodon
from youtube_dl.utils import DownloadError

from fediplay.queue import Queue

Mastodon = mastodon.Mastodon


def api_base_url(instance):
    '''Create an API base url from an instance name.'''

    return 'https://' + instance

class StreamListener(mastodon.StreamListener):
    '''Listens to a Mastodon timeline and adds links the given Queue.'''

    def __init__(self, queue):
        self.queue = queue

    def on_update(self, status):
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

def register(instance, clientcred):
    '''Register fediplay to a Mastodon server and save the client credentials.'''

    saved_umask = umask(0o77)
    Mastodon.create_app('fediplay',
                        scopes=['read'],
                        api_base_url=api_base_url(instance),
                        to_file=clientcred)
    umask(saved_umask)

def build_client(instance, clientcred, usercred=None):
    '''Builds a Mastodon client.'''

    return Mastodon(client_id=clientcred, access_token=usercred, api_base_url=api_base_url(instance))

def get_auth_request_url(client):
    '''Gets an authorization request URL from a Mastodon instance.'''

    return client.auth_request_url(scopes=['read'])

def login(client, grant_code, usercred):
    '''Log in to a Mastodon server and save the user credentials.'''

    saved_umask = umask(0o77)
    client.log_in(code=grant_code, scopes=['read'], to_file=usercred)
    umask(saved_umask)

def stream(instance, clientcred, usercred):
    '''Stream statuses and add them to a queue.'''

    url = api_base_url(instance)
    client = Mastodon(client_id=clientcred, access_token=usercred, api_base_url=url)
    listener = StreamListener(Queue())
    click.echo('==> Streaming from {}'.format(url))
    client.stream_user(listener)

def extract_tags(toot):
    '''Extract tags from a toot.'''

    return [tag['name'] for tag in toot['tags']]

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
