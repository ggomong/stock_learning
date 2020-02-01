import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import databases.database_module as db


# 하이퍼파라미터
input_data_column_cnt = 6   # 입력데이터의 컬럼 개수(Variable 개수)
output_data_column_cnt = 1  # 결과데이터의 컬럼 개수

seq_length = 60             # 1개 시퀀스의 길이(시계열데이터 입력 개수)
rnn_cell_hidden_dim = 20    # 각 셀의 (hidden)출력 크기
forget_bias = 1.0           # 망각편향(기본값 1.0)
num_stacked_layers = 1      # stacked LSTM layers 개수
keep_prob = 1.0             # dropout할 때 keep할 비율

epoch_num = 1000            # 에폭 횟수(학습용전체데이터를 몇 회 반복해서 학습할 것인가 입력)
learning_rate = 0.01        # 학습률


# 상수
train_rate = 0.7            # 전체 데이터에서 train/test 데이터 비율
validation_rate = 0.2       # train 데이터에서 validation 데이터 비율


def get_codes(db_conn):
    backup_row_factory = db_conn.row_factory
    db_conn.row_factory = lambda cursor, row: row[0]
    cursor = db_conn.cursor()
    cursor.execute(
        "SELECT DISTINCT code "
            "FROM stock_daily_series"
        )
    codes = cursor.fetchall()
    db_conn.row_factory = backup_row_factory
    return codes


def get_code_datas(db_conn, code):
    cursor = db_conn.cursor()
    cursor.execute(
        "SELECT open, high, low, close, volume, hold_foreign, st_purchase_inst "
            "FROM stock_daily_series "
            "WHERE code = ? AND volume > 0",
        (code,)
        )
    datas = cursor.fetchall()
    return datas


def make_learning_datas(datas, split_rate):
    dataMin = datas.min()
    dataMax = datas.max()


db_conn = db.get_finance_db_connection()
codes = get_codes(db_conn)
db_conn.close()
