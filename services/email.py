import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_otp_email(to_email: str, otp: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_USERNAME
        msg["To"] = to_email
        msg["Subject"] = "Finable"

        body = f"Your OTP is: {otp}"
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        print("Logging in with:", SMTP_USERNAME)  # Debugging
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
        server.quit()

        return {"message": "✅ OTP email sent successfully"}
    except Exception as e:
        raise Exception(f"Error sending email: {e}")
    

def send_reset_password_email(to_email: str, reset_link: str):
    subject = "Password Reset Request"
    body = f"""
    <html>
    <body>
        <p>Hello,</p>
        <p>You requested to reset your password. Click the link below to set a new password:</p>
        <p><a href="{reset_link}">{reset_link}</a></p>
        <p>This link will expire in 30 minutes. If you did not request a password reset, please ignore this email.</p>
        <br>
        <p>Best regards,</p>
        <p>Finable Team</p>
    </body>
    </html>
    """

    # Create MIME object
    message = MIMEMultipart()
    message["From"] = SMTP_USERNAME
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, to_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        raise Exception(f"Error sending email: {str(e)}")
