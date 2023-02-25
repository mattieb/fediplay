'''The play queue.'''

from os import path, listdir, makedirs, remove, utime
from time import time, localtime
from threading import Thread, Lock

import click
import asyncio

from fediplug.cli import options
import fediplug.env as env
import fediplug.buttplugio as buttplugio




'''--deprecated--'''
class Queue(object):
    '''The play queue.'''

    # pylint: disable=too-few-public-methods

    def __init__(self, plug_client):
        self.lock = Lock()
        self.playing = False
        self.queue = []
        self.plug_client = plug_client

    def add(self, buttplug_instructions):
        '''adds the buttplug instructions to the play queue.'''

        with self.lock:
            self.queue.extend(buttplug_instructions)
            if not self.playing:
                self._play(self.queue.pop(0), self._play_finished)

    def _play(self, buttplug_instructions, cb_complete):
        self.playing = True

        def _run_thread(buttplug_instructions, cb_complete):
            play_command = build_play_command(buttplug_instructions)
            if options['debug']:
                click.echo(f'==> Playing {buttplug_instructions} with {play_command}')
            else:
                click.echo(f'==> Playing {buttplug_instructions}')
            """ 
            loop = asyncio.new_event_loop
            asyncio.run_coroutine_threadsafe(buttplugio.trigger_actuators(self.plug_client, play_command), loop)
            # run command THIS DOES NOT WORK RIGHT NOW ##### THIS REALLY NEEDS TO BE FIXED
            #loop = asyncio.events._get_running_loop()
            #print(loop) """
            
            print('foo')
            
            click.echo('==> Playback complete')
            cb_complete()

        thread = Thread(target=_run_thread, args=(buttplug_instructions, cb_complete))
        thread.start()


    def _play_finished(self):
        with self.lock:
            self.playing = False
            if self.queue:
                self._play(self.queue.pop(0), self._play_finished)


def build_play_command(buttplug_instructions):
    '''Builds a play command for the given filename.'''
    # hardcoded for now 
    # return tuple with ( strength [0.0-1.0] , duration [in s] )

    return (0.5, 1)
