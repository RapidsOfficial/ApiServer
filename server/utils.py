import requests
import config
import math
import json

def dead_response(message="Invalid Request", rid=config.rid):
    return {"error": {"code": 404, "message": message}, "id": rid}

def response(result, error=None, rid=config.rid):
    return {"error": error, "id": rid, "result": result}

def make_request(method, params=[]):
    headers = {"content-type": "text/plain;"}
    data = json.dumps({"id": config.rid, "method": method, "params": params})

    try:
        return requests.post(config.endpoint, headers=headers, data=data).json()
    except Exception:
        return dead_response()

def satoshis(value):
    return int(value * math.pow(10, 8))

def amount(value):
    return round(value / math.pow(10, 8), 8)
