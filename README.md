# fediplug

A Mastodon client that automatically vibrates your buttplug.io devices as people on your timeline toot instructions.

## getting started

Use `pipenv install` from [Pipenv](https://docs.pipenv.org/) to install the Python dependencies and set up the fediplug script inside the virtual environment.

You can use the fediplug script with either `pipenv run fediplug` or by entering the Pipenv shell with `pipenv shell` and just running `fediplug`.

## registering and logging in

To register fediplug to your instance, use `fediplug register example.com`.

To log in to your instance, use `fediplug login example.com`.

## streaming

Use `fediplug stream example.com` to start the stream. You'll need to log in the first time.

Toots that include the hashtag #fediplug will trigger the buttplug.io device.

If new #fediplug toots come in while instructions are being executed, they will be queued and executed later.

If there's a recent #fediplug toot in your timeline, it'll be pulled up and executed before the stream starts.

### filtering

You can also filter instructions by user, so only their instructions are executed. Just add them to the command line after the server name, e.g. `fediplug stream example.com @user @otheruser@example.net`.