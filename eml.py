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

smtp = smtplib.SMTP()
smtp.connect("smtp.163.com")
smtp.login(args.user, args.passwd)
