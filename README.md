# fediplay

A Mastodon client that automatically plays your friends' music as they toot links to it.

You'll need `ffplay` from [FFmpeg](https://ffmpeg.org/) to actually play music.

On macOS, `ffplay` is part of the Homebrew ffmpeg package, but you need to build it with `brew install ffmpeg --with-sdl2`.

Use pip to install the Python dependencies, then edit `stream` so it points to your Mastodon instance and run it. You'll need to log in the first time.

Toots that include the hashtag #fediplay and have as their first link something that [youtube-dl](https://rg3.github.io/youtube-dl/) can play, will!

If new #fediplay toots come in while music is playing, they'll be downloaded immediately and queued to be played later.
