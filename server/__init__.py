from flask_socketio import SocketIO
from flask_caching import Cache
from flask_restful import Api
from flask_cors import CORS
from flask import Flask
import eventlet
import config
import time

eventlet.monkey_patch()

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SECRET_KEY"] = config.secret
cache = Cache(config={"CACHE_TYPE": "simple"})
sio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")
cache.init_app(app)
api = Api(app)
CORS(app)

start_time = time.monotonic()
socket_counter = 0
rest_counter = 0

watch_addresses = {}
subscribers = {}
connections = 0
thread = None

from server import routes
from server import socket
from server import rest

routes.init(app)
socket.init(sio)
rest.init(api)
