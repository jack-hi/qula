#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
import argparse
from email.message import EmailMessage


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--user", help="smtp user")
parser.add_argument("-p", "--passwd", help="smtp password")
parser.add_argument("-r", "--receiver", help="Receiver e-mail address.")
args = parser.parse_args()

msg = EmailMessage()
msg['Subject'] = 'email test 001'
msg['From'] = 'hjj414@163.com'
msg['To'] = 'hjj414@163.com'
msg.set_content('anything')

smtp = smtplib.SMTP()
smtp.connect("smtp.163.com")
smtp.login('hjj414@163.com', args.passwd)
smtp.send_message(msg)
smtp.quit()
