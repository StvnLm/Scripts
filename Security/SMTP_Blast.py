import smtplib

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()   # optional
    # ...send emails
    sent_from = "mikelovesoreos@gmail.com"
    to = ["stevenlammailbox@gmail.com", '']
    subject = "Test email from python"
    body = "This is a successful email!"

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    gmail_user = "mikelovesoreos@gmail.com"
    gmail_pass = "Sheridan1"
    server.login(gmail_user, gmail_pass)
    server.sendmail(sent_from, to, email_text)
    server.close()

except Exception as E:
    print("Something went wrong")
    print(E)
