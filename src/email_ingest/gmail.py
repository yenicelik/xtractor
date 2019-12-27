"""
    Tests how the Gmail-email client is working
"""

# If modifying these scopes, delete the file token.pickle.
import datetime
import mimetypes
import os
import base64
import email
import random
import re
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from googleapiclient.discovery import build
from apiclient import errors
from google.oauth2 import service_account
from unidecode import unidecode

load_dotenv()


class EmailWrapper:
    """
        Includes and logic which gets and send e-mails.
    """

    def get_email_sender(self, msg_id):
        message = self.service.users().messages().get(userId=self.user_id, id=msg_id).execute()
        payload = message['payload']  # get payload of the message
        header = payload['headers']  # get header of the payload

        for item in header:  # getting the Sender
            if item['name'] == 'From':
                msg_from = item['value']
                msg_from = msg_from[msg_from.find("<")+1:msg_from.find(">")]
                return msg_from
            else:
                # Perhaps fallback to david@theaicompany.com?
                pass

        assert False, ("No sender found! Cannot respond to anyone ...", header)

    def _service_account_login(self):
        """
        :return: service: Authorized Gmail API service instance.
        """
        SCOPES = [
            'https://mail.google.com/'
        ]
        # Change this to an env variable
        SERVICE_ACCOUNT_FILE = os.getenv('CREDENTIALS')

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        delegated_credentials = credentials.with_subject(self.email_from)
        _service = build('gmail', 'v1', credentials=delegated_credentials)
        return _service

    def set_email_to(self, email_to):
        self._email_to = email_to

    @property
    def email_to(self):
        """
        :return: to: Email address of the receiver.
        """
        return self._email_to

    def set_email_subject(self, email_subject):
        self._email_subject = email_subject

    @property
    def email_subject(self):
        """
        :return: subject: The subject of the email message.
        """
        return self._email_subject

    def set_email_content(self, email_content):
        self._email_content = email_content

    @property
    def email_content(self):
        return self._email_content

    @property
    def email_from(self):
        """
            sender: Email address of the sender.
        """
        return 'david@theaicompany.com'

    @property
    def user_id(self):
        """
        :return: user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
        """
        return 'me'

    def __init__(self):
        # Email variables. Modify this!
        self.service = self._service_account_login()

        # Should be email to whoever is the sender
        self._email_to = 'segaslp@gmail.com'
        self._email_subject = 'Seasons greetings!'
        self._email_content = 'Teklif is attached'

    # def create_message(self, message_text, attachments):
    #     """Create a message for an email.
    #     :param message_text: The text of the email message.
    #     :param message_text: A list of attachments to be sent by email.
    #     :returns: An object containing a base64url encoded email object.
    #     """
    #     message = MIMEText(message_text)
    #     message['to'] = self.email_to
    #     message['from'] = self.email_from
    #     message['subject'] = self.email_subject
    #     # How to encode attachments ?
    #     b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
    #     b64_string = b64_bytes.decode()
    #     return {'raw': b64_string}

    def create_message_with_attachment(
            self,
            content_bytestr
    ):
        """Create a message for an email.

        Args:
          sender: Email address of the sender.
          to: Email address of the receiver.
          subject: The subject of the email message.
          message_text: The text of the email message.
          file: The path to the file to be attached.

        Returns:
          An object containing a base64url encoded email object.
        """
        message = MIMEMultipart()
        message['to'] = self.email_to
        message['from'] = self.email_from
        message['subject'] = self.email_subject
        message.add_header('User-Agent', 'Apple Mail OSX Email Client gzip')
        message.add_header('Accept-Encoding', 'gzip')

        message_text = random.choice([
                "Merhabalar. Excel'i ek dosyada bul.",
                "Selam Cengiz Bey."
        ])

        msg = MIMEText(message_text)
        message.attach(msg)

        print("File is")
        print(content_bytestr)
        print(type(content_bytestr))

        content_type = 'application/vnd.ms-excel'
        main_type, sub_type = content_type.split('/', 1)

        # msg = MIMEBase(main_type, sub_type)
        # msg.set_payload(content_bytestr)
        # msg.add_header('Content-Disposition', 'attachment', filename='BM_{}.xlsx'.format(datetime.date.today().strftime("%d.%m.%Y")))
        # message.attach(msg)

        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    def send_message(self, message):
        """Send an email message.
        Args:
          message: Message to be sent.
        Returns:
          Sent Message.
        """
        print("Email to is set to", self.email_to)
        print(message)
        try:
            message = self.service.users().messages().send(userId=self.user_id, body=message)
            message.execute()
            # print('Message Id: %s' % message['id'])
            print("Sent ", message)
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    def get_unread_messages(self):
        """List all Messages of the user's mailbox with label_ids applied.
        Returns:
          List of Messages that have all required Labels applied. Note that the
          returned list contains Message IDs, you must use get with the
          appropriate id to get the details of a Message.
        """
        labelIds = ["INBOX", "UNREAD"]  # ["INBOX"]
        # Finally, perhaps have to mark the email as READ
        try:
            response = self.service.users().messages().list(userId=self.user_id, labelIds=labelIds).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.service.users().messages().list(
                    userId=self.user_id,
                    labelIds=labelIds,
                    pageToken=page_token
                ).execute()
                messages.extend(response['messages'])

            return messages
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    def get_mime_message(self, msg_id):
        try:
            message = self.service.users().messages().get(
                userId=self.user_id,
                id=msg_id,
                format='raw'
            ).execute()
            print('Message snippet: %s' % message['snippet'])
            msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
            mime_msg = email.message_from_string(msg_str)

            return mime_msg

        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    def mark_as_read(self, msg_id):
        """Add labels to a Thread.
        Args:
          msg_id: The message id to be retrievad and whose contents are to be read.
        Returns:
          Message contents to be read, including any attachments.
        """
        try:
            message = self.service.users().messages().modify(user_id=self.user_id, id=msg_id,
                                                             body={"removeLabelIds": ['UNREAD']})
            message.execute()

            print('Message make read snippet: %s' % message)

            return message

        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    def parse_body_plaintext(self, payload):
        """
            From the given e-mail, parse all parts into one bytestring, to then convert this bytestring into utf-8
        :return:
        """
        # Fetching message body
        message_parts = payload['parts']  # fetching the message parts
        out = []
        for message_part in message_parts:
            part_body = message_part['body']  # fetching body of the message
            if 'data' not in part_body:
                continue
            part_data = part_body['data']  # fetching data from the body
            clean_one = part_data.replace("-", "+")  # decoding from Base64 to UTF-8
            clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
            clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))  # decoding from Base64 to UTF-8
            soup = BeautifulSoup(clean_two, "lxml")  # This is completely unnecessary and hacky haha
            message_body = unidecode(' '.join(map(lambda p: p.text, soup.find_all('p')))).lower()
            out.append(message_body)

        return "".join(out)

    def get_message_with_attachments(self, msg_id):
        """Get and store attachment from Message with given id.
        :param msg_id: ID of Message containing attachment.
        """
        try:
            message = self.service.users().messages().get(userId=self.user_id, id=msg_id).execute()

            print("Message is: ")
            print(message)

            if not ('payload' in message):
                return None

            if not ('parts' in message['payload']):
                return None

            out = []

            # Get the body
            plaintext = self.parse_body_plaintext(payload=message['payload'])
            out.append(
                ('plaintext', plaintext)
            )

            print("Does payload have parts?")
            print(message['payload'])
            print(message['payload']['parts'])

            print("Now treating single attachments ... ")

            # Do it for single-itemed attachments ...
            for _part in message['payload'].get('parts', ''):
                print("Yes!")
                print(_part)
                print("Continuing")
                part = _part
                # turn into a dict...
                if part['filename']:
                    if 'data' in part['body']:
                        print("Getting body data11")
                        data = part['body']['data']
                    else:
                        print("Retrieving attachment11")
                        att_id = part['body']['attachmentId']
                        att = self.service.users().messages().attachments().get(
                            userId=self.user_id,
                            messageId=msg_id,
                            id=att_id
                        ).execute()
                        data = att['data']

                    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                    path = part['filename']

                    out.append((path, file_data))

            print("Now treating multiple attachments ... ")

            for _part in message['payload'].get('parts', ''):
                if 'parts' not in _part:
                    continue
                parts = _part['parts']
                for part in parts:
                    if part['filename']:
                        if 'data' in part['body']:
                            print("Getting body data11")
                            data = part['body']['data']
                        else:
                            print("Retrieving attachment11")
                            att_id = part['body']['attachmentId']
                            att = self.service.users().messages().attachments().get(
                                userId=self.user_id,
                                messageId=msg_id,
                                id=att_id
                            ).execute()
                            data = att['data']

                        file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                        path = part['filename']

                        out.append((path, file_data))

            # also try to get any other attachment type...

            print("All found resource are: ")
            for i in out:
                print(i)
            return out

        except errors.HttpError as error:
            print('An error occurred: %s' % error)


if __name__ == "__main__":
    print("Sending e-mails")

    email_wrapper = EmailWrapper()

    # Call the Gmail API
    # message = create_message(EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT, EMAIL_CONTENT)
    # sent = send_message(service,'me', message)
    messages = email_wrapper.get_unread_messages()
    # for each message, get the ID and send a response ...
    print("Received message is")
    print(messages)

    for message in messages:
        message_idx = message['id']
        print("Id is", message_idx)
        # mark_as_read(service, 'me', message_idx)
        # email_wrapper.get_message(msg_id=message_idx)
        email_wrapper.get_message_with_attachments(msg_id=message_idx)