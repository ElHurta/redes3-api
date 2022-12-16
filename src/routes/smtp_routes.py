import re
from flask import Blueprint, request
import smtplib, ssl

smtp_routes = Blueprint('smtp_routes', __name__)

@smtp_routes.route('/smtp', methods=['POST'])
def sendMessage():
    # Get the email data from the request
    data = request.get_json()
    sender = data['sender']
    recipients = data['recipients']
    subject = data['subject']
    message = data['message']

    # Create the email message
    msg = f"Subject: {subject}\n\n{message}"

    # Send the email
    with smtplib.SMTP('redesmails.com', 25) as server:
        server.sendmail(sender, recipients, msg)

    return "Email sent!"
