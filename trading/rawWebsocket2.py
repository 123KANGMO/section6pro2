
import websocket
import datetime
import json

REST_testnet = "https://testnet.binancefuture.com"
Websocket_testnet = "wss://stream.binancefuture.com"

def on_message(ws, message):
    print()
    # print(str(datetime.datetime.now()) + ": ")
    print(type(message))
    message2 = json.loads(message)
    print(message2['data'])

def on_error(ws, error):
    print(error)

def on_close(close_msg):
    print("### closed ###" + close_msg)
    streamKline()

'''
Combined streams are accessed at 
/stream?streams=<streamName1>/<streamName2>/<streamName3>
'''

def streamKline(currency, interval):
    websocket.enableTrace(False) 
    #/stream?streams=<streamName1>/<streamName2>/<streamName3>
    # socket = f'{Websocket_testnet}/stream?streams={currency}@kline_{interval}/'
    socket = f'wss://fstream.binance.com/stream?streams=btcusdt@kline_3m'
    ws = websocket.WebSocketApp(socket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()

streamKline('solusdt', '1m')
1659412620000

1659412799999