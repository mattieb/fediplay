# fediplay

A Mastodon client that automatically plays your friends' music as they toot links to it.

## Getting started

You'll need `ffplay` from [FFmpeg](https://ffmpeg.org/) to actually play music. On macOS, `ffplay` is part of the Homebrew ffmpeg package, but you need to build it with `brew install ffmpeg --with-sdl2`.

Edit `stream.py` so it points to your Mastodon instance.

Use `pipenv install --dev` from [Pipenv](https://docs.pipenv.org/) to install the Python dependencies and set up the package with a `stream` executable.

## Streaming

Use `pipenv run stream` to start the stream. You'll need to log in the first time.

Toots that include the hashtag #fediplay and have as their first link something that [youtube-dl](https://rg3.github.io/youtube-dl/) can play, will!

If new #fediplay toots come in while music is playing, they'll be downloaded immediately and queued to be played later.

