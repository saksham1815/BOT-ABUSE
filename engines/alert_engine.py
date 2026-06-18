from core.config import settings
from core.database import SessionLocal, AlertEvent
from datetime import datetime


def check_threshold(category: str, value: float):
    if value >= settings.ALERT_THRESHOLD:
        db = SessionLocal()
        evt = AlertEvent(category=category, value=value, threshold=settings.ALERT_THRESHOLD, created_at=datetime.utcnow())
        db.add(evt)
        db.commit()
        db.close()
        return True
    return False