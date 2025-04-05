from datetime import datetime, timedelta
from backports.zoneinfo import ZoneInfo

from src.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_korea_now():
    kst = ZoneInfo("Asia/Seoul")
    return datetime.now(kst)


def get_today_range():
    kst = ZoneInfo("Asia/Seoul")
    now = get_korea_now()
    today_start = datetime(now.year, now.month, now.day, tzinfo=kst)
    tomorrow_start = today_start + timedelta(days=1)
    return today_start, tomorrow_start


def get_recent_days_range(days: int):
    now = get_korea_now()
    days_before = now - timedelta(days=days)
    return days_before, now
