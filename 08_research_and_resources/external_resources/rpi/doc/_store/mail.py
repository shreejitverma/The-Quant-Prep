#
# Sending emails in combination
# with Motion surveillance software
#
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#

import smtplib
from datetime import datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


def prompt(prompt):
    return raw_input(prompt).strip()

fromaddr = 'rpi@hilpisch.com' # prompt("From: ")
toaddrs  = 'yves@hilpisch.com' # prompt("To: ")
subject = 'Security Alert.' # prompt("Subject: ")

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddrs
msg['Subject'] = subject


# Add the From: and To: headers at the start!
# msg = ("From: %s\r\nTo: %s\r\n\r\nSubject: %s\r\n"
#       % (fromaddr, ", ".join(toaddrs), subject))

# print "Enter message, end with ^D (Unix) or ^Z (Windows):"

# body = ''
#while 1:
#    try:
#        line = raw_input()
#    except EOFError:
#        break
#    if not line:
#        break
#    body = body + line

body = 'A motion has been detected.\nTime: %s' % str(datetime.now())
msg.attach(MIMEText(body, 'plain'))

print "Message length is " + repr(len(msg))

smtp = smtplib.SMTP()
# smtp.starttls()
smtp.set_debuglevel(1)
smtp.connect('smtp.hilpisch.com', 587)
smtp.login('hilpisch13', 'henrynikolaus06')
text = msg.as_string()
smtp.sendmail(fromaddr, toaddrs, text)
smtp.quit()
print text
