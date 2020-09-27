from server import utils
import requests

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
            data["result"]["tx"] = []
            if data["result"]["size"] > 0:
                mempool = utils.make_request("getrawmempool")["result"]
                data["result"]["tx"] = mempool

        return data

    @classmethod
    def price(cls):
        link = "https://api.coingecko.com/api/v3/simple/price?ids=rapids&vs_currencies=usd,btc,gbp,eur"
        return requests.get(link).json()
