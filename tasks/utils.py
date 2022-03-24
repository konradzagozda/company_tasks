import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email = 'oasdkoasd2123@gmail.com'
password = 'usifjisaf'


def send_mail(subject, text, from_email=email, to_emails=[]):
    assert isinstance(to_emails, list)
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)
    msg_str = msg.as_string()

    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(email, password)
    server.sendmail(from_email, to_emails, msg_str)
    server.quit()
