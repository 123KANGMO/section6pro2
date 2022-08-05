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

cm_futures_client = CMFutures()
um_futures_client = UMFutures()


def getData(interval: str, symbol: str) -> list:
    params = {
        'symbol': symbol,# 'BTCUSDT'
        'interval': interval, #'1d' '15m'
        'startTime': 1577836800000,# 20 01 01 12 00 am
        # 'endTime': 1513092400000,
        'limit': 500
        }
    response = um_futures_client.klines(**params)
    return response

def changeDType(data: list) -> list:
    df = pd.DataFrame(data, columns =['open_time','open','high', 'low', 'close', 'volume', 'close_time', 'qav', 'num_t', 'tbbav', 'tbqav', 'ignore'])
    for col in ['open', 'high','low', 'close', 'volume','qav','tbbav','tbqav','ignore']:
        df[col] = df[col].astype(float)
    return df.values.tolist()




def initTable(listData:list, table_name:str):
    try:
        conn = psycopg2.connect(host='localhost', dbname='binance',user='postgres',password=config['db']['password'],port=5432)
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


def tableInit(): # 이걸 잘 ... 
    clist=getData(interval = '1d', symbol= 'BTCUSDT') 
    print('API worked')
    clist = changeDType(clist)
    initTable(listData = clist, table_name='BTCUSDT_F_1d')

