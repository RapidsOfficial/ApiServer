# Getting started

This is RESTful API which will allow you to interact with Sugarchain blockchain.

# How to use it?

First of all you have to create `config.py` file in root of project directory with following content:

```
rid = "api-server"
cache = 3600  # Cache request for 1 hour
secret = 'YOU SHOULD HAVE A VERY STRONG PASSWORD HERE'
endpoint = "http://rpcuser:rpcpassword@127.0.0.1:34229/" # RPC 34229 or 44229
host = "0.0.0.0"
port = 1234
debug = False
block_page = 10
tx_page = 25
```

# Install dependencies
```
$ sudo apt-get install python3-pip
$ pip3 install -r requirements.txt
```

# Run
```
$ python3 app.py
```

All request should be send to this endpoint: `https://api.sugarchain.org/`

Responce have following fields:

- `result`: list or object which contains requested data.
- `error`: this field contains error message in case something went wrong.
- `id`: api server identifier which is set in `config.py` file.

P.s. keep in mind, that all amounts in this API should be in **Satoshis**.
