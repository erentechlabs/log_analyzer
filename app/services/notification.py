import smtplib
import os
from app import models


def send_email_alert(alert: models.Alert):
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    message = f"""Subject: SECURITY ALERT: {alert.reason}

    Suspicious activity has been detected on the server.

    Details:
    - Reason: {alert.reason}
    - IP Address: {alert.ip_address}
    - Time: {alert.timestamp}
    - Description: {alert.details}
    """
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Example for Gmail
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.encode('utf-8'))
        server.quit()
        print("Alert email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")