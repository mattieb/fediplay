'''Mastodon interface.'''

LISTEN_TO_HASHTAG = 'fediplug'

from os import umask

import click
import lxml.html as lh
from lxml.html.clean import clean_html
import mastodon
import asyncio

from fediplug.cli import options
import fediplug.keyring as keyring
from fediplug.queue import Queue
from fediplug.buttplugio import trigger_actuators

Mastodon = mastodon.Mastodon


def api_base_url(instance):
    '''Create an API base url from an instance name.'''

    return 'https://' + instance

class StreamListener(mastodon.StreamListener):
    '''Listens to a Mastodon timeline and adds buttplug instructions the given queue.'''

    def __init__(self, plug_client, instance, users, event_loop):
        self.plug_client = plug_client
        self.instance = instance
        self.users = users
        self.event_loop = event_loop

        if options['debug']:
            print(rf'listener initialized with users={self.users}')

    def on_update(self, status):
        if options['debug']:
            print(rf'incoming status: acct={status.account.acct}')

        if self.users and normalize_username(status.account.acct, self.instance) not in self.users:
            if options['debug']:
                print('skipping status due to username filtering')
            return

        tags = extract_tags(status)
        if options['debug']:
            print(rf'expecting: {LISTEN_TO_HASHTAG}, extracted tags: {tags}')

        if LISTEN_TO_HASHTAG in tags:
            ''' Here we extract the instructions for the butplug'''
            # TODO: still need to write extraction code
            buttplug_instructions = extract_buttplug_instructions(status)
            click.echo('queueing instructions')
            self.event_loop.run_until_complete(trigger_actuators(self.plug_client, buttplug_instructions))



'''
            if options['debug']:
                print(rf'instructions: {buttplug_instructions}')

            for link in links:
                try:
                    click.echo(rf'==> Trying {link}')
                    self.queue.add(link)
                    return
                except DownloadError:
                    pass
'''

def register(instance):
    '''Register fediplug to a Mastodon server and save the client credentials.'''

    client_id, client_secret = Mastodon.create_app('fediplug', scopes=['read'], api_base_url=api_base_url(instance))
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

def stream(instance, users, client_id, client_secret, access_token, plug_client, event_loop):
    '''Stream statuses and add them to a queue.'''

    client = build_client(instance, client_id, client_secret, access_token)
    users = [normalize_username(user, instance) for user in users]
    listener = StreamListener(plug_client, instance, users, event_loop)
    

    existing_statuses = client.timeline_hashtag(LISTEN_TO_HASHTAG, limit=1)

    if options['debug']:
        print(rf'existing_statuses: {existing_statuses}')

    for status in existing_statuses:
        listener.on_update(status)

    click.echo(f'==> Streaming from {instance}')
    client.stream_user(listener)

def extract_tags(toot):
    '''Extract tags from a toot.'''

    return [tag['name'] for tag in toot['tags']]

def normalize_username(user, instance):
    user = user.lstrip('@')
    parts = user.split('@')
    if options['debug']:
        print(rf'parts: {parts}')

    if len(parts) == 1 or parts[1] == instance:
        return parts[0]
    else:
        return user

def extract_buttplug_instructions(toot):
    '''Extract buttplug instruction informations from a toot.'''
    doc_list = []
    doc = lh.fromstring(toot['content'])
    doc = clean_html(doc)
    doc_list.append(doc.text_content())
    print(rf'extracted buttplug_instruction: {doc_list}')
    return doc_list