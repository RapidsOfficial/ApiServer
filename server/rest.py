from server.methods.transaction import Transaction
from flask_restful import Resource, reqparse
from server.methods.general import General
from server.methods.address import Address
from server.methods.block import Block
from server import stats
from server import utils

class GetInfo(Resource):
    @stats.rest
    def get(self):
        return General().info()

class GetPrice(Resource):
    @stats.rest
    def get(self):
        return General().price()

class BlockByHeight(Resource):
    @stats.rest
    def get(self, height):
        parser = reqparse.RequestParser()
        parser.add_argument("offset", type=int, default=0)
        args = parser.parse_args()

        data = Block().height(height)
        if data["error"] is None:
            data["result"]["tx"] = data["result"]["tx"][args["offset"]:args["offset"] + 10]

        return data

class HashByHeight(Resource):
    @stats.rest
    def get(self, height):
        return Block().get(height)

class BlocksByRange(Resource):
    @stats.rest
    def get(self, height):
        parser = reqparse.RequestParser()
        parser.add_argument("offset", type=int, default=30)
        args = parser.parse_args()

        if args["offset"] > 100:
            args["offset"] = 100

        result = Block().range(height, args["offset"])
        return utils.response(result)

class BlockByHash(Resource):
    @stats.rest
    def get(self, bhash):
        parser = reqparse.RequestParser()
        parser.add_argument("offset", type=int, default=0)
        args = parser.parse_args()

        data = Block().hash(bhash)
        if data["error"] is None:
            data["result"]["tx"] = data["result"]["tx"][args["offset"]:args["offset"] + 10]

        return data

class BlockHeader(Resource):
    @stats.rest
    def get(self, bhash):
        return utils.make_request("getblockheader", [bhash])

class TransactionInfo(Resource):
    @stats.rest
    def get(self, thash):
        return Transaction().info(thash)

class AddressBalance(Resource):
    @stats.rest
    def get(self, address):
        return Address().balance(address)

class AddressHistory(Resource):
    @stats.rest
    def get(self, address):
        parser = reqparse.RequestParser()
        parser.add_argument("offset", type=int, default=0)
        args = parser.parse_args()

        data = Address().history(address)
        if data["error"] is None:
            data["result"]["tx"] = data["result"]["tx"][args["offset"]:args["offset"] + 10]

        return data

class AddressMempool(Resource):
    @stats.rest
    def get(self, address):
        return Address().mempool(address)

class AddressUnspent(Resource):
    @stats.rest
    def get(self, address):
        parser = reqparse.RequestParser()
        parser.add_argument("amount", type=int, default=0)
        args = parser.parse_args()

        return Address().unspent(address, args["amount"])

class MempoolInfo(Resource):
    @stats.rest
    def get(self):
        return General().mempool()

class DecodeRawTx(Resource):
    @stats.rest
    def get(self, raw):
        return Transaction().decode(raw)

class EstimateFee(Resource):
    @stats.rest
    def get(self):
        return General().fee()

class Broadcast(Resource):
    @stats.rest
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("raw", type=str, default="")
        args = parser.parse_args()

        return Transaction().broadcast(args["raw"])

def init(api):
    api.add_resource(GetInfo, "/info")
    api.add_resource(GetPrice, "/price")
    api.add_resource(BlockByHeight, "/height/<int:height>")
    api.add_resource(HashByHeight, "/hash/<int:height>")
    api.add_resource(BlockByHash, "/block/<string:bhash>")
    api.add_resource(BlockHeader, "/header/<string:bhash>")
    api.add_resource(BlocksByRange, "/range/<int:height>")
    api.add_resource(AddressBalance, "/balance/<string:address>")
    api.add_resource(AddressMempool, "/mempool/<string:address>")
    api.add_resource(AddressUnspent, "/unspent/<string:address>")
    api.add_resource(AddressHistory, "/history/<string:address>")
    api.add_resource(TransactionInfo, "/transaction/<string:thash>")
    api.add_resource(DecodeRawTx, "/decode/<string:raw>")
    api.add_resource(MempoolInfo, "/mempool")
    api.add_resource(EstimateFee, "/fee")
    api.add_resource(Broadcast, "/broadcast")
