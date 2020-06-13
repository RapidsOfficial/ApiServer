from datetime import timedelta
import server as state
import time

def socket(func):
    def wrapper(*args, **kwargs):
        state.socket_counter += 1
        return func(*args, **kwargs)

    return wrapper

def rest(func):
    def wrapper(*args, **kwargs):
        state.rest_counter += 1
        return func(*args, **kwargs)

    return wrapper

def info():
    uptime = timedelta(seconds=time.monotonic() - state.start_time)
    return {
        "uptime": str(uptime),
        "subscriptions": {
            "connections": state.connections,
            "subscribers": len(state.subscribers),
            "watch": len(state.watch_addresses)
        },
        "requests": {
            "socket": state.socket_counter,
            "rest": state.rest_counter
        }
    }
