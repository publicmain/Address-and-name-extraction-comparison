import smtplib
from email.mime.text import MIMEText
import subprocess
import time
import logging
import os

APP_PATH = "python3 app.py"
APP_NAME = "app.py"
EMAIL_SENDER = "jiangnan971205@163.com"
EMAIL_PASSWORD = "RHQp7XXmJRnt9eEs"
EMAIL_RECEIVER = "jiangnan971205@163.com"
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 587  # SMTP 服务器的端口


# 配置日志
logging.basicConfig(filename="monitor.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s: %(message)s")


def send_email(subject, message):
    """发送警告邮件"""
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # 启用加密传输
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

def is_app_running():
    try:
        # result = subprocess.check_output(f'tasklist /FI "IMAGENAME eq {APP_NAME}"', shell=True)
        result = subprocess.check_output(f"pgrep -f {APP_NAME}", shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def start_app():
    logging.info(f"{APP_NAME} is not running. Starting it now...")
    subprocess.Popen(APP_PATH, shell=True)

def monitor_app():
    while True:
        try:
            if not is_app_running():
                start_app()
                send_email(
                    subject=f"{APP_NAME} stopped!",
                    message=f"The application {APP_NAME} has unexpectedly stopped and will be restarted."
                )
        except Exception as e:
            logging.error(f"Error occurred: {e}")
        time.sleep(5)

if __name__ == "__main__":
    logging.info("Starting the monitoring of app.py")
    monitor_app()