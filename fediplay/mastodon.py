'''Mastodon interface.'''

from os import umask

import click
from lxml.etree import HTML # pylint: disable=no-name-in-module
import mastodon
from youtube_dl.utils import DownloadError

from fediplay.queue import Queue

Mastodon = mastodon.Mastodon

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

def register(api_base_url):
    '''Register fediplay to a Mastodon server and save the client credentials.'''

    old_umask = umask(0o77)
    Mastodon.create_app('fediplay', api_base_url=api_base_url, to_file='clientcred.secret')
    umask(old_umask)

def login(client, grant_code):
    '''Log in to a Mastodon server and save the user credentials.'''

    old_umask = umask(0o77)
    client.log_in(code=grant_code, to_file='usercred.secret')
    umask(old_umask)

def stream(api_base_url):
    '''Stream statuses and add them to a queue.'''

    client = Mastodon(client_id='clientcred.secret', access_token='usercred.secret',
                      api_base_url=api_base_url)
    listener = StreamListener(Queue())
    click.echo('==> Streaming from {}'.format(api_base_url))
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
