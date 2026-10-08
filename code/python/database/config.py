from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://demo:CHANGE_ME_BEFORE_RUNNING@127.0.0.1:3306/djy?charset=utf8mb4"
engine = create_engine(SQLALCHEMY_DATABASE_URI)

db = SQLAlchemy()
