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

fromaddr = 'rpi@mydomain.net'
toaddrs  = 'me@mydomain.net'  # can be list of strings
subject = 'Video Recorded.'

#
# Email object
# 
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddrs
msg['Subject'] = subject


#
# Email attachement
#
parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='Input file')
args = parser.parse_args()

part = MIMEBase('application', "octet-stream")
part.set_payload(open(args.input_file, "rb").read())
Encoders.encode_base64(part)

part.add_header('Content-Disposition',
                'attachment; filename="%s"' % args.input_file)

msg.attach(part)

#
# Email body
#
body = 'This video has been recorded due to a motion just detected.'
body += '\nTime: %s' % str(datetime.now())
msg.attach(MIMEText(body, 'plain'))

#
# Connecting to SMTP server and
# sending the email
#
smtp = smtplib.SMTP()
smtp.set_debuglevel(1)
smtp.connect('smtp.mydomain.net', 587)
smtp.login('username', 'password')
text = msg.as_string()
smtp.sendmail(fromaddr, toaddrs, text)
smtp.quit()

# Shell output
print "Message length is " + repr(len(msg))
print text
