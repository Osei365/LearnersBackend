import pymysql
import os

host = os.getenv('DATABASEHOST')
password = os.getenv('DATABASEPASSWORD')
user = os.getenv('DATABASEUSERNAME')
conn = pymysql.connect(host=host, user=user, password=password)

cur = conn.cursor()

cur.execute('CREATE DATABASE IF NOT EXISTS learners')

conn.close()
