import smtplib
from email.mime.text import MIMEText #MIMEtext allows us to send text & HTML email


def send_mail(customer, dealer, rating, comments): #function to send email taking in the data to be mailed
    port = 2525 #mailtrap port
    smtp_server = 'smtp.mailtrap.io' #mailtrap server
    login = 'a45f14d227ef4f' #username
    password = 'ae600915998187' #passowrd
    #formatted string as a message
    message = f"<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Dealer: {dealer}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'email1@example.com' #sender email
    receiver_email = 'email2@example.com' #receiver email
    msg = MIMEText(message, 'html') #email variable with message and type HTML mail
    msg['Subject'] = 'Tata Feedback' #subject of email
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server: #passing server and port to SMTPlib to send the email
        server.login(login, password) #username and password to login into server
        server.sendmail(sender_email, receiver_email, msg.as_string()) #send the email

