# fediplay

A Mastodon client that automatically plays your friends' music as they toot links to it.

## Getting started

fediplay comes configured to use `ffplay` from [FFmpeg](https://ffmpeg.org/) to actually play music.

-   On macOS, `ffplay` is part of the [Homebrew](https://brew.sh/) `ffmpeg` package, but you need to build it with `brew install ffmpeg --with-sdl2`.

-   On Windows, `ffplay` is part of the [Scoop](http://scoop.sh/) `ffmpeg` package.

Use `pipenv install` from [Pipenv](https://docs.pipenv.org/) to install the Python dependencies and set up the fediplay script inside the virtual environment.

You can use the fediplay script with either `pipenv run fediplay` or by entering the Pipenv shell with `pipenv shell` and just running `fediplay`.

## Registering and logging in

To register fediplay to your instance, use `fediplay register example.com`.

To log in to your instance, use `fediplay login example.com`.

## Streaming

Use `fediplay stream example.com` to start the stream. You'll need to log in the first time.

Toots that include the hashtag #fediplay and have as their first link something that [youtube-dl](https://rg3.github.io/youtube-dl/) can play, will!

If new #fediplay toots come in while music is playing, they'll be downloaded immediately and queued to be played later.

