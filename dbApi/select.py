import psycopg2
import configparser
import sys


import os
config = configparser.ConfigParser()    
config.read(os.path.join(os.path.dirname(__file__) +'/../config.ini'), encoding='utf-8') 

def inserttest():
    try:
        conn = psycopg2.connect(host='localhost', dbname='binance',user='postgres',password=str(config['db']['password']),port=5432)
        cur = conn.cursor()
        # create table one by one
        # cursor.executemany(sql_str, your_dataframe.values.tolist())
        cur.execute(
            "INSERT INTO BTCUSDT_F_15m (open_time, openp, highp, lowp, closep, volume, close_time, qav, num_t, tbbav, tbqav, ign)  VALUES(%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s ,%s)",
             (1577836800000, 7189.43, 7190.52,7172.94, 7176.2, 1037.337, 1577837699999, 7447960.0213, 1560, 383.751, 2755105.07629, 0)
            )                # close communication with the PostgreSQL database server
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
