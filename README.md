# fediplay

A Mastodon client that automatically plays your friends' music as they toot links to it.

## What's new in 2.2

If you've been using fediplay before, the all-new version 2.2 will be a little different!

-   You now specify the instance you want to stream from on the command line, instead of setting it in the environment. fediplay has been upgraded with the power of [Click](http://click.pocoo.org/) to give it a more modern command-line interface.

-   We use [appdirs](https://pypi.org/project/appdirs/) to keep downloaded music files in your operating system's user cache directory.

-   We use [keyring](https://pypi.org/project/keyring/) to store your client credentials and access token, securely if your operating system supports it. If you already have `.secret` files from an earlier version, we'll migrate them automatically for you.

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

Since version 2.2, thanks to [@bbonf](https://github.com/bbonf), if there's a recent #fediplay toot in your timeline, it'll be pulled up and played before the stream starts. Great if you just missed a song before starting your stream!

### Filtering

Since version 2.2, you can also, thanks to [@Jenkyrados](https://github.com/Jenkyrados), specify users to filter! Just add them to the command line after the server name, e.g. `fediplay stream example.com @user @otheruser@example.net`.

