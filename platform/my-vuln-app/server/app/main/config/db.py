import pymysql
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

username = 'my-vuln-app-user' #os.getenv('DB_ROOT')
password = 'pw' #os.getenv('DB_ROOT_PASSWORD')
userpass = 'mysql+pymysql://' + username + ':' + password + '@'
server = 'platform_db_1/'
dbname = 'my-vuln-app-db' #os.getenv('DB')
socket = '/var/run/mysqld/mysqld.sock'
SQLALCHEMY_DATABASE_URI = userpass + server + dbname

os.environ['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

os.environ['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

db_sqlAlchemy = SQLAlchemy()