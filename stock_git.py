from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import ssl
import smtplib

sender_email = ""
sender_password = ""
receiver_email = ""


url = "https://www.microcenter.com/product/623606/creality-ender-3-v2-3d-printer"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")
text = ""
for script in soup(["span"]):
    text += str (script.extract())

res = re.search("inventoryCnt\">([\S ]{5,15})<\/span>", text)

print(res.group(1))
if (res.group(1) != "Sold Out"):
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
    server.login(sender_email, sender_password)

    msg = MIMEMultipart()
    msg['Subject'] = "Microcenter Stock"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    content = "The item is in Stock!\n" + res.group(1)
    mtext = MIMEText(content)
    msg.attach(mtext)
    server.sendmail(sender_email, receiver_email, msg.as_string())
