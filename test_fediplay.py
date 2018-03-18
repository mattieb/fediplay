from os import environ

from fediplay.mastodon import extract_links
from fediplay.queue import build_play_command

def test_extract_links():
    toot = {
        'content': "<p><a href=\"https://cybre.space/tags/nowplaying\" class=\"mention hashtag\" rel=\"tag\">#<span>nowplaying</span></a> <a href=\"https://cybre.space/tags/fediplay\" class=\"mention hashtag\" rel=\"tag\">#<span>fediplay</span></a> Grimes ft. Janelle Mon\u00e1e - Venus Fly <a href=\"https://www.youtube.com/watch?v=eTLTXDHrgtw\" rel=\"nofollow noopener\" target=\"_blank\"><span class=\"invisible\">https://www.</span><span class=\"ellipsis\">youtube.com/watch?v=eTLTXDHrgt</span><span class=\"invisible\">w</span></a></p>"
    }
    urls = extract_links(toot)
    assert urls == ['https://www.youtube.com/watch?v=eTLTXDHrgtw']

def test_build_play_command_default():
    environ.pop('FEDIPLAY_PLAY_COMMAND')
    play_command = build_play_command('Awesome Music.mp3')
    assert play_command == 'ffplay -v 0 -nostats -hide_banner -autoexit -nodisp \'Awesome Music.mp3\''

def test_build_play_command_specified():
    environ.update(FEDIPLAY_PLAY_COMMAND='afplay {filename}')
    play_command = build_play_command('Awesome Music.mp3')
    assert play_command == 'afplay \'Awesome Music.mp3\''
