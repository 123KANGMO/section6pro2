import psycopg2
import configparser
import sys

import pandas as pd
import os
config = configparser.ConfigParser()    
config.read(os.path.join(os.path.dirname(__file__) +'/../config.ini'), encoding='utf-8') 

def getAllToCSV():
    try:
        conn = psycopg2.connect(host='localhost', dbname='binance',user='postgres',password=str(config['db']['password']),port=5432)
        cur = conn.cursor()

        sql = """Select * from BTCUSDT_F_15m"""
        cur.execute(sql)
        df = pd.DataFrame(cur.fetchall(),columns =['open_time','open','high', 'low', 'close', 'volume', 'close_time', 'qav', 'num_t', 'tbbav', 'tbqav', 'ignore'])
        df.to_csv('./f_15m.csv')
        cur.close()
        print('hi')
    except  (Exception, psycopg2.DatabaseError)  as e:
        print(f'Error {e}')
        sys.exit(1)

    finally:
        if conn:
            conn.close()

getAllToCSV()

