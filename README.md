# Binance Websocket

This repository has the source code to deploy a Server with two main functions

## 1. Serve a Websocket

The websocket has only `/` enpoint, and everytime a connection is established, the server response is the last 10 records for the 5 main criptos (05/05/2024)

- BTC
- BNB
- ETH
- SOL
- XRP

### Response format:
Every response from this endpoint has the following structure
```json
  {
    "coin": "coinName", 
    "values": [v1, v2, ..., v10], // Float 
    "operations": [o1, o2, ..., o10], // String 
    "time": [t1, t2, ..., t10] // String (HH:MM)
  }
```

## 2 Get and Insert data
### Get data from binance
We consume the following ws endpoint from binance:

```
  wss://fstream.binance.com/stream?streams=
    btcusdt@kline_1m/
    bnbusdt@kline_1m/
    ethusdt@kline_1m/
    solusdt@kline_1m/
    xrpusdt@kline_1m
```
### Inserting data

Everytime the stock operation is close, we store the value into Mongo Database, in other words, each time we have a response from the `data['k']['x']` key equal to `True` we store data

```json
{
  "e": "kline",     // Event type
  "E": 1638747660000,   // Event time
  "s": "BTCUSDT",    // Symbol
  "k": {
    "t": 1638747660000, // Kline start time
    "T": 1638747719999, // Kline close time
    "s": "BTCUSDT",  // Symbol
    "i": "1m",      // Interval
    "f": 100,       // First trade ID
    "L": 200,       // Last trade ID
    "o": "0.0010",  // Open price
    "c": "0.0020",  // Close price
    "h": "0.0025",  // High price
    "l": "0.0015",  // Low price
    "v": "1000",    // Base asset volume
    "n": 100,       // Number of trades
    "x": false,     // Is this kline closed?
    "q": "1.0000",  // Quote asset volume
    "V": "500",     // Taker buy base asset volume
    "Q": "0.500",   // Taker buy quote asset volume
    "B": "123456"   // Ignore
  }
}

```

On the script we can see this like the following snippet

```python
isClose = data['data']['k']['x']
```

# Local installation and execution

If you want to run this program you need to follow this steps:

1. Install all prerequisites

    ```bash
      pip install -r requirements.txt
    ```

2. Create a `.env` file to store your credentials

    ```python
      # Mongo URI
      MONGO_URI="String"
      # Mongo DataBase name
      MONGO_DATABASE="String"
      # Mongo Collection name
      MONGO_COLLECTION="String"

    ```

# Live

The endpoint is online on Railways and can be consume using the following url:

### [wss://binace-websocket-production.up.railway.app](wss://binace-websocket-production.up.railway.app)