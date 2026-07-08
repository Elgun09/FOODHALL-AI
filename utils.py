from datetime import datetime

def now():
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")

def success(text: str):
    return f"✅ {text}"

def error(text: str):
    return f"❌ {text}"
