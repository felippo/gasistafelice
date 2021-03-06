# Quickstart

    $ git clone https://github.com/befair/gasistafelice && cd gasistafelice
    $ make up

Then you could use the test database:

    $ make dbtest

Or you could initialize an empty database:

    $ make dbinit

Further, you may want to dump the database (on `gasistafelice/fixtures/test.sql`):

    $ make dbdump

Now go on:

* [`localhost:8080/`](http://localhost:8080/) for UI
* [`localhost:8080/gasistafelice/`](http://localhost:8080/gasistafelice/) for old UI
* [`localhost:8080/gasistafelice/admin/`](http://localhost:8080/gasistafelice/admin/) for Django Admin UI

and login with `admin`/`admin`.

For debugging purpose, you could use the backend directly at:

* [`localhost:7000/gasistafelice/`](http://localhost:7000/gasistafelice/)
* [`localhost:7000/gasistafelice/admin/`](http://localhost:7000/gasistafelice/admin/)

If you want to change any (default) configuration, please edit the `settings.env` file.

## Test

To launch all the tests:

    $ make test

Additionally, you can visualize the end-to-end tests running in the browsers via a VNC client:

- `localhost:5900` for Firefox
- `localhost:5901` for Chrome

## Debugging

To see the tracebacker (this requires `uwsgi` installed on your host machine):

    $ uwsgi --connect-and-read /tmp/gf_tracebacker1

For further info, you can see the [docs](https://uwsgi-docs.readthedocs.org/en/latest/Tracebacker.html).

## Profiling

Enable profiling adding the following line in your `settings.env`:

    APP_PROFILING=true

Then see `/tmp/gf_profiling` on your host machine.
