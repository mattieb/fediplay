from os import environ, umask
import shlex
from subprocess import run
from threading import Thread, Lock

from lxml.etree import HTML
import mastodon
Mastodon = mastodon.Mastodon
from youtube_dl import YoutubeDL

class Queue(object):
    def __init__(self):
        self.lock = Lock()
        self.playing = False
        self.queue = []

    def add(self, url):
        filename = Getter().get(url)
        
        with self.lock:
            self.queue.append(filename)
            if not self.playing:
                self._play(self.queue.pop(0), self._play_finished)

    def _play(self, filename, cb_complete):
        self.playing = True

        def run_thread(filename, cb_complete):
            print('==> Playing', filename)
            play_command = build_play_command(filename)
            print('[executing]', play_command)
            run(play_command, shell=True)
            print('==> Playback complete')
            cb_complete()

        thread = Thread(target=run_thread, args=(filename, cb_complete))
        thread.start()

    def _play_finished(self):
        with self.lock:
            self.playing = False
            if len(self.queue) > 0:
                self._play(self.queue.pop(0), self._play_finished)

class Getter(object):
    def _progress_hook(self, progress):
        if progress['status'] == 'finished':
            self.filename = progress['filename']

    def get(self, url):
        options = {
            'format': 'mp3/mp4',
            'nocheckcertificate': 'FEDIPLAY_NO_CHECK_CERTIFICATE' in environ,
            'progress_hooks': [self._progress_hook]
        }
        with YoutubeDL(options) as downloader:
            downloader.download([url])

        return self.filename

class StreamListener(mastodon.StreamListener):
    def __init__(self):
        self.queue = Queue()

    def on_update(self, status):
        tags = extract_tags(status)
        if 'fediplay' in tags:
            links = extract_links(status)
            if links:
                self.queue.add(links[0])

def register(api_base_url):
    old_umask = umask(0o77)
    Mastodon.create_app('fediplay', api_base_url=api_base_url, to_file='clientcred.secret')
    umask(old_umask)

def login(api_base_url, email, password):
    client = Mastodon(client_id='clientcred.secret', api_base_url=api_base_url)
    old_umask = umask(0o77)
    client.log_in(email, password, to_file='usercred.secret')
    umask(old_umask)

def stream(api_base_url):
    client = Mastodon(client_id='clientcred.secret', access_token='usercred.secret', api_base_url=api_base_url)
    listener = StreamListener()
    print('==> Streaming from', api_base_url)
    client.stream_user(listener)

def extract_tags(toot):
    return [tag['name'] for tag in toot['tags']]

def link_is_internal(link):
    classes = link.attrib.get('class', '').split(' ')
    if classes:
        return 'mention' in classes

    return False

def extract_links(toot):
    html = HTML(toot['content'])
    all_links = html.cssselect('a')
    return [link.attrib['href'] for link in all_links if not link_is_internal(link)]

def build_play_command(filename):
    escaped_filename = shlex.quote(filename)
    template = environ.get(
        'FEDIPLAY_PLAY_COMMAND',
        'ffplay -v 0 -nostats -hide_banner -autoexit -nodisp {filename}'
    )
    return template.format(filename=escaped_filename)

def main():
    from getpass import getpass
    from os import path
    from sys import exit

    api_base_url = environ.get('FEDIPLAY_API_BASE_URL')
    if not api_base_url:
        print('FEDIPLAY_API_BASE_URL environment variable not set')
        exit(1)

    if not path.exists('clientcred.secret'):
        print('==> No clientcred.secret; registering application')
        register(api_base_url)

    if not path.exists('usercred.secret'):
        print('==> No usercred.secret; logging in')
        email = input('Email: ')
        password = getpass('Password: ')
        login(api_base_url, email, password)

    stream(api_base_url)

if __name__ == '__main__':
    main()
