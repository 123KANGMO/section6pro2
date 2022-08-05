# https://api3.binance.com



import requests
import json
import time
from datetime import datetime
import pandas as pd
import psycopg2


lasttimestamp = 0
df_5m = pd.DataFrame({'open_time':[],'open':[],'high':[], 'low':[], 'close':[], 'volume':[], 'close_time':[], 'qav':[], 'not':[], 'tbbav':[], 'tbqav':[] })
#qav : Quote asset volume : btc/usdt 라면 usdt volume을 의미 
#tbbav : Taker buy base asset volume :   maker가 아닌 taker가 buy 인 코인의 볼륨
#tbqav : Taker buy quote aasset volume :   동일 하게 taker가 buy 인 계산화폐의 볼륨, 

# 1M 월봉 1m 분봉
klen = 500 # 500개씩 받아오는데 마지막은 500이 아니겠지, 최소 0이겠지. 
criticalError = False

# while klen ==500:
#   response = requests.get("https://api2.binance.com/api/v3/klines?symbol=BTCUSDT&interval=5m&startTime=150315480000")
#   bit = json.loads(response.content)
n = 1
t = 1503092400000
while klen ==500:
  response = requests.get(f"https://api2.binance.com/api/v3/klines?symbol=BTCUSDT&interval=5m&startTime={t}")
  bit = json.loads(response.content)
  bit_df = pd.DataFrame(bit, columns=['open_time','open','high', 'low', 'close', 'volume', 'close_time', 'qav', 'not', 'tbbav', 'tbqav', 'ignore'])
  if len(df_5m) == 0 :
    df_5m = bit_df.copy()
  elif df_5m.iloc[-1]['close_time']+1 == bit_df.iloc[0]['open_time'] :
    df_5m = pd.concat([df_5m,bit_df], ignore_index=True)
  else:
    criticalError= True
    break
  t = bit_df.iloc[-1]['close_time']+1
  time.sleep(1)
  print(f"done {n}", df_5m.iloc[-1]['close_time']+1, bit_df.iloc[0]['open_time'] )
  n+=1
  
  klen = len(bit)


if criticalError:
  print('what the xxxx, something wrong')
else: 
  df_5m.to_csv('outt.csv',index=False)

# breakpoint()
'''
'''