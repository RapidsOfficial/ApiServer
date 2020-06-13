from flask_socketio import SocketIO
from flask_caching import Cache
from flask_restful import Api
from flask_cors import CORS
from flask import Flask
import config
import time

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SECRET_KEY"] = config.secret
cache = Cache(config={"CACHE_TYPE": "simple"})
sio = SocketIO(app, cors_allowed_origins="*")
cache.init_app(app)
api = Api(app)
CORS(app)

start_time = time.monotonic()
socket_counter = 0
rest_counter = 0

watch_addresses = {}
connections = 0
subscribers = {}
thread = None
mempool = []

from server import routes
from server import socket
from server import rest

routes.init(app)
socket.init(sio)
rest.init(api)
