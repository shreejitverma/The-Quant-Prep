#
# Sending emails in combination
# with Motion surveillance software
#
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#

import argparse
import smtplib
from datetime import datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders

def prompt(prompt):
    return raw_input(prompt).strip()

fromaddr = 'rpi@hilpisch.com' # prompt("From: ")
toaddrs  = 'yves@hilpisch.com' # prompt("To: ")
subject = 'Video Evidence.' # prompt("Subject: ")

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddrs
msg['Subject'] = subject


parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='Input file')
args = parser.parse_args()


part = MIMEBase('application', "octet-stream")
part.set_payload(open(args.input_file, "rb").read())
Encoders.encode_base64(part)

part.add_header('Content-Disposition', 'attachment; filename="%s"' % args.input_file)

msg.attach(part)

body = 'This video has been recorded due to a motion in your home office.\nTime: %s' % str(datetime.now())
msg.attach(MIMEText(body, 'plain'))

print "Message length is " + repr(len(msg))

smtp = smtplib.SMTP()
smtp.set_debuglevel(1)
smtp.connect('smtp.hilpisch.com', 587)
smtp.login('hilpisch12', 'henrynikolaus06')
text = msg.as_string()
smtp.sendmail(fromaddr, toaddrs, text)
smtp.quit()
print text
