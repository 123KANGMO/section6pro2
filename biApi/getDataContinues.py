from re import T
from binance.spot import Spot 
from binance.cm_futures import CMFutures
from binance.um_futures import UMFutures
import pandas as pd

import psycopg2
import sys
import os
import configparser
config = configparser.ConfigParser()    
config.read(os.path.join(os.path.dirname(__file__) +'/../config.ini'), encoding='utf-8') 
db_pw= config['db']['password']

cm_futures_client = CMFutures()
um_futures_client = UMFutures()

import time  
tnow = time.time()-86400 
tnow = int(tnow*1000)


def getData(interval: str, symbol: str, startTime: int) -> list:
    params = {
        'symbol': symbol,# 'BTCUSDT'
        'interval': interval, #'1d' '15m'
        'startTime': startTime, #1577836800000 = 20 01 01 12 00 am
        'limit': 1500
        }
    response = um_futures_client.klines(**params)
    return response

def changeDType(data: list) -> list:
    df = pd.DataFrame(data, columns =['open_time','open','high', 'low', 'close', 'volume', 'close_time', 'qav', 'num_t', 'tbbav', 'tbqav', 'ignore'])
    for col in ['open', 'high','low', 'close', 'volume','qav','tbbav','tbqav','ignore']:
        df[col] = df[col].astype(float)
    return df.values.tolist()




def savaDataToDB(listData:list, table_name:str):
    try:
        conn = psycopg2.connect(host='localhost', dbname='binance',user='postgres',password=db_pw,port=5432)
        cur = conn.cursor()
        insert_sql = f'''INSERT INTO {table_name} (open_time, openp, highp, lowp, closep, volume, close_time, qav, num_t, tbbav, tbqav, ign)
          VALUES(%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s ,%s)'''
        cur.executemany(insert_sql, listData)                # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        print('done insert')
    except  (Exception, psycopg2.DatabaseError)  as e:
        print(f'Error {e}')
        sys.exit(1)
    finally:
        if conn:
            conn.close()
    

def lastDataTimestamp( table_name:str): 
    try:
        conn = psycopg2.connect(host='localhost', dbname='binance',user='postgres',password=db_pw,port=5432)
        cur = conn.cursor()
        # insert_sql = f'''SELECT MAX(open_time) FROM {table_name}'''
        insert_sql= f'''SELECT close_time 
        FROM {table_name}
        ORDER BY open_time DESC 
        LIMIT 1'''
        cur.execute(insert_sql)                # close communication with the PostgreSQL database server
        onerow = cur.fetchone()
        # fetchall() => [(num)]    [0]으로 접근 불가.
        # fetchone() => (num,)         
        print(f'what i got is : {onerow} , type: {type(onerow)}')
        cur.close()

    except  (Exception, psycopg2.DatabaseError)  as e:
        print(f'Error {e}')
        sys.exit(1)

    finally:
        if conn:
            conn.close()
    return onerow[0]
'''
현제시간 마지막 데이터 시간 비교.
마지막 데이터 시간
'''




def candleDataUpdate(table_name: str, symbol:str, interval:str):
    cycle = 0
    lastData = lastDataTimestamp( table_name=table_name)
    while tnow > lastData :
        clist=getData(interval = interval, symbol= symbol, startTime = lastData+1) 
        clist = changeDType(clist)
        savaDataToDB(listData = clist, table_name=table_name)
        lastData = lastDataTimestamp( table_name=table_name)
        cycle+=1
        print(cycle)


candleDataUpdate(table_name='BTCUSDT_F_15m', symbol='BTCUSDT', interval='15m')