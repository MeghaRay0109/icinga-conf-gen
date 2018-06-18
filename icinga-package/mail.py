'''
    A module to send email.
'''
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders

import settings
import logging
import logging.handlers
mailserver=settings.MAIL_HOST

def sendEmail(mail_text,attachment_name,frm,to,subject):
    global mailserver    
    if type(to) is str:
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = frm
        msg['To'] = to
        msg = create_attachemnt(msg,attachment_name)
        msg.attach(MIMEText(mail_text))
        s = smtplib.SMTP(mailserver)   
        s.sendmail(frm , [to], msg.as_string())
        s.quit()
    elif type(to) is list:
        for sendee in to:
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = frm
            msg['To'] = sendee
            msg.attach(MIMEText(mail_text))
            msg = create_attachemnt(msg,attachment_name)
            s = smtplib.SMTP(mailserver)   
            s.sendmail(frm , [sendee], msg.as_string())
            s.quit()

def send_email(mail_text, sender, recipient, subject, content_type="text/plain"):
    '''
        email function.
    '''
    mailserver = settings.MAIL_HOST
    msg = MIMEText(mail_text)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    msg.add_header('Content-Type', content_type)
    server = smtplib.SMTP(mailserver)
    if type(recipient) is str:
        server.sendmail(sender, [recipient], msg.as_string())
    else:
        server.sendmail(sender, recipient, msg.as_string())
    server.quit()

def create_attachemnt(msg,attachment_name):
    if attachment_name:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(attachment_name,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % settings.ERROR_FILE)
        msg.attach(part)
    return msg



class TitledSMTPHandler(logging.handlers.SMTPHandler):
    def getSubject(self, record):
        formatter = logging.Formatter(fmt=self.subject)
        return formatter.format(record)
