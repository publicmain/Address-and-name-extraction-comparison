import subprocess
import time
import sys
import smtplib
from email.mime.text import MIMEText

EMAIL_SENDER = "yaokexiang1bc@gmail.com"
EMAIL_PASSWORD = "200111cs"
EMAIL_RECEIVER = "yaokexiang1bc@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # SMTP 服务器的端口

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

def start_flask_app():
    process = subprocess.Popen([sys.executable, 'app.py'])
    print(f"Flask 应用已启动,进程 ID 为 {process.pid}")
    return process

def monitor_flask_app(process):
    while True:
        time.sleep(5)  # 每隔 5 秒检查一次
        if process.poll() is not None:
            print("Flask 应用已退出,正在重新启动...")
            send_email(
                subject="Flask 应用停止运行",
                message="Flask 应用已意外停止,监控脚本将自动重启应用。"
            )
            process = start_flask_app()

if __name__ == "__main__":
    flask_process = start_flask_app()
    try:
        monitor_flask_app(flask_process)
    except KeyboardInterrupt:
        print("监控脚本已终止。")
        flask_process.terminate()