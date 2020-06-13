from server import config
from server import sio
from server import app

if __name__ == "__main__":
    sio.run(app, debug=config.debug, host=config.host, port=config.port)
