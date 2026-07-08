from datetime import datetime

def now():
    return datetime.now()

def log(text):
    print(f"[{now()}] {text}")
