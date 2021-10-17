import json
import pprint

import websocket

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
closes = []


def on_open(ws):
    print('opened connection')


def on_close(ws):
    print('closed connection')


def on_message(ws, message):
    json_message = json.loads(message)
    pprint.pprint(json_message)
    candle = json_message["k"]
    is_candled_closed = json_message["x"]
    close = json_message["c"]

    if is_candled_closed:
        print(f"candle closed at {close}")
        closes.append(float(close))
        print("closes")
        print(closes)


ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
