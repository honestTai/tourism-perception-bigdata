import os

from sqlalchemy import create_engine

db_config = {
    'user': 'djy',
    'password': 'CHANGE_ME_BEFORE_RUNNING',
    'host': '127.0.0.1:3306',
    'database': 'djy'
}

# Create database engine
engine = create_engine( f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}?charset=utf8mb4")

path = os.getcwd()
data_path = path + '/static/data'
static_path = path + '/static'
