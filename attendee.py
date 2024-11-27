import sqlite3;
import re
import hashlib

def isValidEmail(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+$', email)

def standartName(name):
    return name.lower().capitalize()

def hashingPassw(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

