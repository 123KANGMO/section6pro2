        # cursor.executemany(sql_str, your_dataframe.values.tolist())

import psycopg2
import configparser
import sys


import os
config = configparser.ConfigParser()    
config.read(os.path.join(os.path.dirname(__file__) +'/../config.ini'), encoding='utf-8') 


def insert_test():
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

def insert_test(listData):
    try:
        conn = psycopg2.connect(host='localhost', dbname='binance',user='postgres',password=str(config['db']['password']),port=5432)
        cur = conn.cursor()
        # create table one by one
        # cursor.executemany(sql_str, your_dataframe.values.tolist())
        insert_sql = '''INSERT INTO BTCUSDT_F_15m (open_time, openp, highp, lowp, closep, volume, close_time, qav, num_t, tbbav, tbqav, ign)
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

def delete_test(part_id):
    """ delete part by part id """
    conn = None
    rows_deleted = 0
    try:
        # read database configuration
        conn = psycopg2.connect(host='localhost', dbname='binance',user='postgres',password=str(config['db']['password']),port=5432)
        cur = conn.cursor()

        # execute the UPDATE  statement
        cur.execute("DELETE FROM BTCUSDT_F_15m WHERE open_time = %s", (part_id,))
        # get the number of updated rows
        rows_deleted = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
        print('well done')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted


delete_test(1577836800000)