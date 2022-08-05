import psycopg2
import configparser
import sys


import os
config = configparser.ConfigParser()    
config.read(os.path.join(os.path.dirname(__file__) +'/../config.ini'), encoding='utf-8') 


conn = None
def create_table(sql):
    try:
        conn = psycopg2.connect(host='localhost', dbname='binance',user='postgres',password=str(config['db']['password']),port=5432)
        cur = conn.cursor()
        # create table one by one
        cur.execute(sql)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        print('done')

    except  (Exception, psycopg2.DatabaseError)  as e:
        print(f'Error {e}')
        sys.exit(1)

    finally:
        if conn:
            conn.close()

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



'''
DROP TABLE IF EXISTS BTCUSDT_F_1d;
'''
csql = [
'''
CREATE TABLE IF NOT EXISTS BTCUSDT_F_1d
(
    open_time bigint NOT NULL,
    openp numeric,
    highp numeric,
    lowp numeric,
    closep numeric,
    volume numeric,
    close_time bigint,
    qav numeric,
    num_t bigint,
    tbbav numeric,
    tbqav numeric,
    ign numeric,
    CONSTRAINT "BTCUSDT_F_1d_pkey" PRIMARY KEY (open_time)
)
''',

# '''
# TABLESPACE pg_default;
# ''',

# '''
# ALTER TABLE IF EXISTS public."BTCUSDT_F_15m"
#     OWNER to postgres;
# '''
]

# 테이블 생성 하려면 밑에 주석을 ....
for x in csql:
    create_table(x)
# inserttest()

