from .. import celery
from .models import Post
from flask import current_app, render_template
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, time
from datetime import timedelta

@celery.task()
def log(msg):
    return msg

@celery.task(
    bind=True,
    ignore_result=True,
    default_retry_delay=300,
    max_retries=5
)
def digest(self):
    #get the current day at midnight for calculating start and end date filter
    current_day = datetime.combine(datetime.now.today(), time.min)

    posts = Post.query.filter(
        Post.created_date >= current_day - timedelta(days=7),
        Post.created_date <= current_day
    ).all()

    if (len(posts) == 0):
        return

    msg = MIMEText(render_template("../templates/email/digest.html", posts=posts), 'html')

    msg['Subject'] = "Weekly Digest"
    msg['From'] = current_app.config['SMTP_FROM']

    try:
        smtp_server = smtplib.SMTP(current_app.config['SMTP_SERVER'])
        smtp_server.starttls()
        smtp_server.login(current_app.config['SMTP_USER'], 
        current_app.config['SMTP_PASSWORD'])
        smtp_server.sendmail("", [""], msg.as_string())
        smtp_server.close()
        return

    except Exception as e:
        self.retry(exc=e)