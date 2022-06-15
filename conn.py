import sqlite3
from datetime import datetime

def conn():
    db = "databases/pandas.sqlite"
    conn = sqlite3.connect(db)
    return conn

def sysdate():
    fmt = '%Y_%m_%d_%H_%M_%S'
    fecha  = datetime.now()
    fecha = fecha.strftime(fmt)
    return fecha