from server.methods.transaction import Transaction
from server.methods.general import General
from server.methods.block import Block
from flask import request
from server import stats
from server import utils
from server import sio
import server as state
import flask_socketio

def subscription_loop():
    bestblockhash = None

    while True:
        print("Subscription loop")
        print(f"Watching for {len(state.watch_addresses)} addresses")
        print(f"Watching for {len(state.watch_addresses)} addresses")

        data = General().info()
        if "bestblockhash" in data["result"]:
            if data["result"]["bestblockhash"] != bestblockhash:
                print("New block")

                bestblockhash = data["result"]["bestblockhash"]
                sio.emit("block.update", utils.response({
                    "height": data["result"]["blocks"],
                    "hash": bestblockhash
                }), room="blocks")

                updates = Block().inputs(bestblockhash)
                for address in updates:
                    mempool = list(set(state.mempool) - set(updates[address]))
                    if address in state.watch_addresses:
                        print(f"Sending update to address: {address}")

                        sio.emit("address.update", utils.response({
                            "address": address,
                            "tx": updates[address],
                            "height": data["result"]["blocks"],
                            "hash": bestblockhash
                        }), room=address)

            data = General().mempool()
            updates = Transaction().addresses(data["result"]["tx"])
            temp_mempool = []
            for address in updates:
                updates[address] = list(set(updates[address]) - set(mempool))
                temp_mempool += updates[address]
                if address in state.watch_addresses:
                    if len(updates[address]) > 0:
                        print(f"Sending mempool update to address: {address}")

                        sio.emit("address.update", utils.response({
                            "address": address,
                            "tx": updates[address],
                            "height": None,
                            "hash": None
                        }), room=address)

            mempool = list(set(mempool + temp_mempool))

        print("Subscription loop is done, waiting delay")
        sio.sleep(0.5)

@stats.socket
def Connect():
    state.connections += 1
    if state.thread is None:
        state.thread = sio.start_background_task(target=subscription_loop)

@stats.socket
def Disconnect():
    state.connections -= 1
    if request.sid in state.subscribers:
        for address in state.subscribers[request.sid]:
            if request.sid in state.watch_addresses[address]:
                state.watch_addresses[address].remove(request.sid)
                flask_socketio.leave_room(address, request.sid)
                if len(state.watch_addresses[address]) == 0:
                    state.watch_addresses.pop(address)

        state.subscribers.pop(request.sid)

@stats.socket
def SubscribeBlocks():
    flask_socketio.join_room("blocks", request.sid)
    return True

@stats.socket
def UnsubscribeBlocks():
    flask_socketio.leave_room("blocks", request.sid)
    return True

@stats.socket
def SubscribeAddress(address):
    if request.sid not in state.subscribers:
        state.subscribers[request.sid] = []

    if address not in state.watch_addresses:
        state.watch_addresses[address] = [request.sid]
    else:
        state.watch_addresses[address].append(request.sid)

    state.subscribers[request.sid].append(address)
    flask_socketio.join_room(address, request.sid)

    return True

@stats.socket
def UnubscribeAddress(address):
    if request.sid in state.watch_addresses[address]:
        state.watch_addresses[address].remove(request.sid)
        flask_socketio.leave_room(address, request.sid)
        if len(state.watch_addresses[address]) == 0:
            state.watch_addresses.pop(address)

        return True
