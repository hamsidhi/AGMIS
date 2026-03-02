import os
import smtplib
from email.mime.text import MIMEText


class Emailer:
    def __init__(self):
        self.enabled = os.environ.get("EMAIL_NOTIFICATIONS", "0").strip().lower() in ("1", "true", "yes", "on")
        self.smtp_host = os.environ.get("SMTP_HOST", "")
        self.smtp_port = int(os.environ.get("SMTP_PORT", "587") or 587)
        self.smtp_user = os.environ.get("SMTP_USER", "")
        self.smtp_pass = os.environ.get("SMTP_PASS", "")
        self.from_email = os.environ.get("FROM_EMAIL", self.smtp_user or "no-reply@example.com")

    def is_configured(self):
        return self.enabled and self.smtp_host and self.from_email

    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        if not self.is_configured():
            return False
        if not to_email:
            return False
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.from_email
        msg["To"] = to_email
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                if self.smtp_user and self.smtp_pass:
                    server.login(self.smtp_user, self.smtp_pass)
                server.sendmail(self.from_email, [to_email], msg.as_string())
            return True
        except Exception:
            return False


emailer = Emailer()
