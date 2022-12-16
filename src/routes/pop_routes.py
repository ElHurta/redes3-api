import re
from flask import Blueprint, request, jsonify
import poplib

pop_routes = Blueprint('pop_routes', __name__)

@pop_routes.route('/pop', methods=['POST'])
def pop():
    user = request.json.get('user')
    # Connect to the mail box 
    try:
        Mailbox = poplib.POP3_SSL('redesmails.com', '995') 
        Mailbox.user(user) 
        Mailbox.pass_(request.json.get('password')) 
        NumofMessages = len(Mailbox.list()[1])
        messagesList = []
        for i in range(NumofMessages):
            fullMessage = "" 
            for msg in Mailbox.retr(i+1)[1]:
                # Serialize the message as json
                fullMessage += msg.decode('utf-8') +"\n"
            messagesList.append(email_to_json(fullMessage))
                
        Mailbox.quit()
        return messagesList

    except:
        return jsonify(message="POP3 failed"), 401

@pop_routes.route('/login', methods=['POST'])
def login():
    user = request.json.get('user')
    # Connect to the mail box 
    Mailbox = poplib.POP3_SSL('redesmails.com', '995') 
    try:
        Mailbox.user(user) 
        Mailbox.pass_(request.json.get('password'))
        Mailbox.quit()
        return jsonify(message="Login success"), 200
    except: 
        return jsonify(message="Login failed"), 401
    

def email_to_json(email_string):
    # Use regular expressions to extract the relevant information
    delivered_to_match = re.search(r'Delivered-To: (.*)', email_string)
    delivered_to = delivered_to_match.group(1) if delivered_to_match else None
    message_id_match = re.search(r'Message-Id: (.*)', email_string)
    message_id = message_id_match.group(1) if message_id_match else None
    date_match = re.search(r'Date: (.*)', email_string)
    date = date_match.group(1) if date_match else None
    from_match = re.search(r'Return-Path: (.*)', email_string)
    sender = from_match.group(1) if from_match else None
    subject_match = re.search(r'Subject: (.*)', email_string)
    subject = subject_match.group(1) if subject_match else None
    body_match = re.search(r'\n\n(.*)', email_string)
    body = body_match.group(1) if body_match else None

    # Remove the angle brackets from the message ID and sender
    message_id = message_id.strip("<>") if message_id else None
    sender = sender.strip("<>") if sender else None

    # Create a dictionary with the extracted information
    info = {
        "delivered_to": delivered_to,
        "sender": sender,
        "subject": subject,
        "body": body
    }

    # Convert the dictionary to JSON

    return info