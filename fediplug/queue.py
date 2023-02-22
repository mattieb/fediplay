'''The play queue.'''

from os import path, listdir, makedirs, remove, utime
from time import time, localtime
from subprocess import Popen, run
from threading import Thread, Lock

import click
from youtube_dl import YoutubeDL, utils

from fediplug.cli import options
import fediplug.env as env


class Queue(object):
    '''The play queue.'''

    # pylint: disable=too-few-public-methods

    def __init__(self, cache_dir):
        self.lock = Lock()
        self.playing = False
        self.queue = []
        self.cache_dir = cache_dir

    def add(self, url):
        '''Fetches the url and adds the resulting audio to the play queue.'''

        filenames = Getter(self.cache_dir).get(url)

        with self.lock:
            self.queue.extend(filenames)
            if not self.playing:
                self._play(self.queue.pop(0), self._play_finished)

    def _play(self, filename, cb_complete):
        self.playing = True

        def _run_thread(filename, cb_complete):
            play_command = build_play_command(filename)
            if options['debug']:
                click.echo(f'==> Playing {filename} with {play_command}')
            else:
                click.echo(f'==> Playing {filename}')
            run(play_command)

            click.echo('==> Playback complete')
            cb_complete()

        thread = Thread(target=_run_thread, args=(filename, cb_complete))
        thread.start()

    def _play_finished(self):
        with self.lock:
            self.playing = False
            if self.queue:
                self._play(self.queue.pop(0), self._play_finished)

class Getter(object):
    '''Fetches music from a url.'''

    # pylint: disable=too-few-public-methods
    def __init__(self, cache_dir):
        self.filename = None
        self.filenames = []
        self.cache_dir = cache_dir

    def _progress_hook(self, progress):
        if options['debug']:
            print('progress hook: status {!r}, filename {!r}'.format(progress['status'], progress['filename']))

        if (progress['status'] in ('downloading', 'finished') and 
            progress['filename'] not in self.filenames):
            self.filenames.append(progress['filename'])

    def get(self, url):
        '''Fetches music from the given url.'''

        '''deleting files here'''
        auto_delete_files(self.cache_dir)

        ytdl_options = {
            'format': 'mp3/mp4',
            'nocheckcertificate': env.no_check_certificate(),
            'outtmpl': path.join(self.cache_dir, utils.DEFAULT_OUTTMPL),
            'progress_hooks': [self._progress_hook],
            'restrictfilenames': True,
            'quiet': True,
            'no_warnings': True
        }

        if options['debug']:
            ytdl_options['quiet'] = False
            ytdl_options['no_warnings'] = False

        with YoutubeDL(ytdl_options) as downloader:
            downloader.download([url])

        for file in self.filenames:
            utime(file)

        return self.filenames

def build_play_command(filename):
    '''Builds a play command for the given filename.'''

    filename = rf"{filename}"
    
    command_args = env.play_command().split()
    command_args.append(filename)
    return command_args

def auto_delete_files(cache_dir):
    for the_file in listdir(cache_dir):
        file_path = path.join(cache_dir, the_file)
        if path.isfile(file_path):
            file_time = path.getmtime(file_path)
            if file_time + 604800 < time():
                remove(file_path)