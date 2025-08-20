from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models

# --- LogEntry CRUD Functions ---

def create_log_entry(db: Session, parsed_log: dict):
    """Adds a new log entry to the database."""
    db_log = models.LogEntry(
        ip_address=parsed_log.get('ip_address'),
        username=parsed_log.get('username'),
        timestamp=parsed_log.get('timestamp', datetime.utcnow()),
        log_type=parsed_log.get('type'),
        raw_log=parsed_log.get('raw_log')
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_log_entries(db: Session, skip: int = 0, limit: int = 100):
    """Lists log entries in the database."""
    return db.query(models.LogEntry).offset(skip).limit(limit).all()

def count_recent_failed_logins(db: Session, ip_address: str, since: datetime):
    """Counts failed login attempts from a specific IP since a given time."""
    return db.query(models.LogEntry).filter(
        models.LogEntry.ip_address == ip_address,
        models.LogEntry.log_type == 'ssh_failed_login',
        models.LogEntry.timestamp >= since
    ).count()


# --- Alert CRUD Functions ---

def create_alert(db: Session, reason: str, ip_address: str, details: str):
    """Adds a new alert record to the database."""
    db_alert = models.Alert(
        reason=reason,
        ip_address=ip_address,
        details=details,
        timestamp=datetime.utcnow()
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

def get_alerts(db: Session, skip: int = 0, limit: int = 100):
    """Lists alerts in the database."""
    return db.query(models.Alert).order_by(models.Alert.timestamp.desc()).offset(skip).limit(limit).all()

def has_recent_alert(db: Session, ip_address: str, reason: str, time_frame_minutes: int = 60):
    """Checks whether an alert for the same reason was recently created for a given IP."""
    since = datetime.utcnow() - timedelta(minutes=time_frame_minutes)
    count = db.query(models.Alert).filter(
        models.Alert.ip_address == ip_address,
        models.Alert.reason == reason,
        models.Alert.timestamp >= since
    ).count()
    return count > 0