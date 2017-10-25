import bottle
# specific
from beaker.middleware import SessionMiddleware

import bxforms.api


class Webserver():

    """Abstract our webserver so its outside the core app folder."""

    def __init__(self, host, port):
        """Load the server up locally."""
        local_app = SessionMiddleware(bottle.app())
        bottle.run(app=local_app, server='cherrypy', host=host,
                   port=port, reloader=True)
