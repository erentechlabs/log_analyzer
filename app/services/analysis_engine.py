from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .. import crud, models

BRUTE_FORCE_THRESHOLD = 10  # 10 try
BRUTE_FORCE_TIMEFRAME_MINUTES = 5  # In 5 minutes


def analyze_for_brute_force(db: Session, parsed_log: dict):
    ip = parsed_log['ip_address']

    # Last 5 minutes, IP failed logins count for this IP
    time_limit = datetime.utcnow() - timedelta(minutes=BRUTE_FORCE_TIMEFRAME_MINUTES)
    failed_attempts_count = crud.count_recent_failed_logins(db, ip_address=ip, since=time_limit)

    if failed_attempts_count >= BRUTE_FORCE_THRESHOLD:
        # Before creating an alert for this IP, check if an alert has been created recently
        if not crud.has_recent_alert(db, ip_address=ip, reason="Brute-force"):
            details = f"{failed_attempts_count} failed attempts within {BRUTE_FORCE_TIMEFRAME_MINUTES} minutes."
            alert = crud.create_alert(db, reason="Brute-force", ip_address=ip, details=details)
            return alert
    return None