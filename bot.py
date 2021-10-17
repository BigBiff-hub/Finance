import json
import pprint

import websocket, talib, numpy

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYM = 'ETHUSD'
TRADE_QUANTITIY = 0.05
closes = []
in_position = False


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

        if len(closes) > RSI_PERIOD:
            num_closes = numpy.array(closes)
            rsi = talib.RSI(num_closes, RSI_PERIOD)
            print('all rsis calculated so far')
            print(rsi)
            last_rsi = rsi[-1]
            print(f'the current rsi is {last_rsi}')

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print('sell now ethereum is overbought')
                    # TODO: put binance sell logic here
                else:
                    print("No shares currently available cannot do anything")
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("its oversold, but you already own it cannot do anything")
                else:
                     print('Buy now as ethereum is over sold')
                    #TODO: put binance logic here



ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
