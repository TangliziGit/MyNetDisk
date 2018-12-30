import time
import hashlib
import config

def get_date():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def get_password_salted(password):
    return hashlib.sha256((password+config.salt).encode()).digest()
