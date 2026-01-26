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


fromaddr = 'rpi@hilpisch.com'
toaddrs  = 'yves@hilpisch.com'  # can be list of strings
subject = 'Security Alert.'

#
# Email object
# 
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddrs
msg['Subject'] = subject

#
# Email body
#
body = 'A motion has been detected.\nTime: %s' % str(datetime.now())
msg.attach(MIMEText(body, 'plain'))

#
# Connecting to SMTP server and
# sending the email
#
smtp = smtplib.SMTP()
smtp.set_debuglevel(1)
smtp.connect('smtp.hilpisch.com', 587)
smtp.login('hilpisch13', 'henrynikolaus06')
text = msg.as_string()
smtp.sendmail(fromaddr, toaddrs, text)
smtp.quit()

#
# Output
#
print "Message length is " + repr(len(msg))
print text
