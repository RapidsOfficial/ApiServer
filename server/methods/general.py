from server import utils

class General():
    @classmethod
    def info(cls):
        data = utils.make_request("getblockchaininfo")

        if data["error"] is None:
            nethash = utils.make_request("getnetworkhashps", [6, data["result"]["blocks"]])
            if nethash["error"] is None:
                data["result"]["nethash"] = int(nethash["result"])

        return data

    @classmethod
    def fee(cls):
        return utils.response({
            "feerate": utils.satoshis(0.00001),
            "blocks": 6
        })

    @classmethod
    def mempool(cls):
        data = utils.make_request("getmempoolinfo")

        if data["error"] is None:
            if data["result"]["size"] > 0:
                mempool = utils.make_request("getrawmempool")["result"]
                data["result"]["tx"] = mempool
            else:
                data["result"]["tx"] = []

        return data
