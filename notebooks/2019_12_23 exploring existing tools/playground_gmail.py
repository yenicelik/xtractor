"""
    Tests how the Gmail-email client is working
"""

# If modifying these scopes, delete the file token.pickle.
import email

from googleapiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from email.mime.text import MIMEText
import base64
from google.oauth2 import service_account

# Email variables. Modify this!
EMAIL_FROM = 'david@theaicompany.com'
EMAIL_TO = 'segaslp@gmail.com'
EMAIL_SUBJECT = 'Testing GMail API!'
EMAIL_CONTENT = 'Hello, this is a test3'


def create_message(sender, to, subject, message_text):
    """Create a message for an email.
    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.
    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    print("Message is")
    b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
    b64_string = b64_bytes.decode()
    return {'raw': b64_string}

    # print(message)
    # print(message.as_string())
    # # print(base64.urlsafe_b64encode(message.as_string().encode('utf-8')))
    # # print(base64.urlsafe_b64encode(message.as_string()))
    # return {'raw': message.as_string()}


def send_message(service, user_id, message):
    """Send an email message.
    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.
    Returns:
      Sent Message.
    """
    try:
        message = service.users().messages().send(userId=user_id, body=message)
        message.execute()
        # print('Message Id: %s' % message['id'])
        print("Sent ", message)
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


# def get_unread_messages(service, user_id):
#   """Get all unread email messages.
#   Args:
#     service: Authorized Gmail API service instance.
#     user_id: User's email address. The special value "me"
#     can be used to indicate the authenticated user.
#   Returns:
#     Unread e-mail messages
#   """
#   try:
#       # labels.get(id="INBOX")
#     message = service.users().messages().list(userId=user_id, labelIds="INBOX")
#
#         # .get(userId=user_id, id=msg_id).send(userId=user_id, body=message)
#     message.execute()
#     # print('Message Id: %s' % message['id'])
#     print("Sent ", message)
#     return message
#   except errors.HttpError as error:
#     print('An error occurred: %s' % error)
#
def service_account_login():
    SCOPES = [
        # 'https://www.googleapis.com/auth/gmail.send',
        # 'https://www.googleapis.com/auth/gmail.compose',
        # 'https://www.googleapis.com/auth/gmail.labels',
        # 'https://www.googleapis.com/auth/gmail.modify',
        # 'https://www.googleapis.com/auth/gmail.readonly',
        # 'https://www.googleapis.com/auth/gmail.send'
        'https://mail.google.com/'
    ]
    SERVICE_ACCOUNT_FILE = '/Users/david/xtractor/.keys/procurement-263106-10748d7d6fd5.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    delegated_credentials = credentials.with_subject(EMAIL_FROM)
    service = build('gmail', 'v1', credentials=delegated_credentials)
    return service


def get_unread_messages(service, user_id):
    """List all Messages of the user's mailbox with label_ids applied.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      label_ids: Only return Messages with these labelIds applied.

    Returns:
      List of Messages that have all required Labels applied. Note that the
      returned list contains Message IDs, you must use get with the
      appropriate id to get the details of a Message.
    """
    labelIds = ["INBOX", "UNREAD"]  # ["INBOX"]
    # Finally, perhaps have to mark the email as READ
    try:
        response = service.users().messages().list(userId=user_id, labelIds=labelIds).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, labelIds=labelIds,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def get_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        print('Message snippet: %s' % message['snippet'])

        return message

    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def get_mime_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id,
                                                 format='raw').execute()
        print('Message snippet: %s' % message['snippet'])
        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        mime_msg = email.message_from_string(msg_str)

        return mime_msg

    except errors.HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == "__main__":
    print("Seind e-mails")
    service = service_account_login()
    # Call the Gmail API
    # message = create_message(EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT, EMAIL_CONTENT)
    # sent = send_message(service,'me', message)
    messages = get_unread_messages(service, 'me')
    # for each message, get the ID and send a response ...
    print("Received message is")
    print(messages)

    for message in messages:
        message_idx = message['id']
        print("Id is", message_idx)
        get_message(service, 'me', message_idx)
