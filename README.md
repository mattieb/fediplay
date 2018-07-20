# fediplay

A Mastodon client that automatically plays your friends' music as they toot links to it.

## What's new in 2.0

If you've been using fediplay before, the all-new version 2.0 will be a little different!

-   You now specify the instance you want to stream from on the command line, instead of setting it in the environment. fediplay has been upgraded with the power of [Click](http://click.pocoo.org/) to give it a more modern command-line interface.

-   We use [appdirs](https://github.com/ActiveState/appdirs) to store your credentials in your operating system's user config directory, and downloaded music files in your operating system's user cache directory. If you already have `.secret` files from an earlier version, we'll move and rename them automatically for you.

Be sure to follow all the instructions, including re-running `pipenv install` to update the installed dependencies.

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

