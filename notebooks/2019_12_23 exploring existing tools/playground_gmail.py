"""
    Tests how the Gmail-email client is working
"""

# If modifying these scopes, delete the file token.pickle.
from googleapiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from email.mime.text import MIMEText
import base64
from google.oauth2 import service_account

# Email variables. Modify this!
EMAIL_FROM = 'david@theaicompany.com'
EMAIL_TO = 'seegaslp@gmail.com'
EMAIL_SUBJECT = 'Hello  from Lyfepedia!'
EMAIL_CONTENT = 'Hello, this is a test\nhttps://david@theaicompany.com'

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
  print(message)
  print(message.as_string())
  # print(base64.urlsafe_b64encode(message.as_string().encode('utf-8')))
  return {'raw': message.as_string()}

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
    print('Message Id: %s' % message['id'])
    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def service_account_login():
  SCOPES = ['https://www.googleapis.com/auth/gmail.send']
  SERVICE_ACCOUNT_FILE = '/Users/david/xtractor/.keys/procurement-263106-10748d7d6fd5.json'

  credentials = service_account.Credentials.from_service_account_file(
          SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  delegated_credentials = credentials.with_subject(EMAIL_FROM)
  service = build('gmail', 'v1', credentials=delegated_credentials)
  return service

if __name__ == "__main__":
    print("Seind e-mails")
    service = service_account_login()
    # Call the Gmail API
    message = create_message(EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT, EMAIL_CONTENT)
    sent = send_message(service,'me', message)
