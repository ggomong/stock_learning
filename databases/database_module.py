import os as os
import sqlite3 as sql


# 데이터베이스 연결을 얻음
def get_finance_db_connection():
    try:
        db_conn = sql.connect(os.path.dirname(os.path.realpath(__file__)) + "/finance_data.db")
        return db_conn
    except sql.Error as e:
        print(e)
    
    return db_conn


# 주식 일간데이터 테이블이 없으면 생성
def create_stock_daily_series_table(db_conn):
    db_conn.execute(
        "CREATE TABLE IF NOT EXISTS stock_daily_series("
            "code TEXT, "
            "date DATE, "
            "open INTEGER, "
            "high INTEGER, "
            "low INTEGER, "
            "close INTEGER, "
            "volume INTEGER, "
            "hold_foreign REAL, "
            "st_purchase_inst REAL, "
            "PRIMARY KEY(code, date)"
            ")"
        )
        

# 환율 일간데이터 테이블이 없으면 생성
def create_exchange_daily_series_table(db_conn):
    db_conn.execute(
        "CREATE TABLE IF NOT EXISTS exchange_daily_series("
            "code TEXT, "
            "date DATE, "
            "open REAL, "
            "high REAL, "
            "low REAL, "
            "close REAL, "
            "PRIMARY KEY(code, date)"
            ")"
        )
