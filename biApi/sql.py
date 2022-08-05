import psycopg2
import sys

con = None



def createTable():
        -- DROP TABLE IF EXISTS public."BTCUSDT_F_15m";

    CREATE TABLE IF NOT EXISTS public."BTCUSDT_F_15m"
    (
        open_time bigint NOT NULL,
        open numeric,
        high numeric,
        low numeric,
        close numeric,
        volume numeric,
        close_time bigint,
        qav numeric,
        "not" numeric,
        tbbav numeric,
        tbqav numeric,
        ignore numeric,
        CONSTRAINT "BTCUSDT_F_15m_pkey" PRIMARY KEY (open_time)
    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS public."BTCUSDT_F_15m"
        OWNER to postgres;