'''Environment variable management.'''

from os import getenv

from dotenv import load_dotenv, find_dotenv


def no_check_certificate():
    '''Returns whether fediplug should check TLS certificates.'''

    return bool(getenv('FEDIPLAY_NO_CHECK_CERTIFICATE'))

def play_command():
    '''Returns the play command fediplug should use to play a file.'''

    return (getenv('FEDIPLAY_PLAY_COMMAND') or
            'ffplay -v 0 -nostats -hide_banner -autoexit -nodisp {filename}')

load_dotenv(find_dotenv())
