"""
    Includes the main event loop that continuously pings the email
"""
import time
# Should perhaps write all to logs, instead of to stdout
from src.email_ingest.gmail import EmailWrapper
from src.filereaders.pdf2text import PDF2Text
from src.filereaders.xls2text import XLS2Text
from src.resources.union_special_excel import USExcelTemplate
from src.resources.union_special_list import usp_price_list


def handle_datasources(datasources):
    """
    :param datasources: a python list of tuples (name, bytestring)
    :return:
    """
    out = []
    for filename, content_str in datasources:
        if filename == "plaintext":
            out.append(content_str)
            pass
        elif filename.endswith('.pdf'):
            text = PDF2Text().pdf_bytestring_to_text(content_str)
            out.append(text)
        elif filename.endswith('.xls') or filename.endswith('.xlsx'):
            text = XLS2Text().xls_bytestring_to_text(content_str)
            out.append(text)
        else:
            print("Not supported type!", filename)

    out = "".join(out)

    # Returns a fulltext string including text from all these sources
    # We can then use this to extract individual strings

    return out

def extract_union_special_items(fulltext):
    fulltext = set(fulltext.split())
    matching_parts = fulltext.intersection(usp_price_list.get_partlist_as_set)
    out = []
    for part in matching_parts:
        part_json = usp_price_list.get_partnumber_json(part_no=part)
        print("Part json is")
        print(part_json)
        print("Part json is", type(part_json), len(part_json))
        out.append(part_json)
    return out


if __name__ == "__main__":
    print("Starting program...")

    TIME_INTERVAL = 5

    email_service = EmailWrapper()

    # Write all errors into GCP stackdriver
    while True:
        ###############################
        # GET UNREAD EMAILS
        ###############################
        print(f"Getting e-mails...")
        messages = email_service.get_unread_messages()
        print(f"---- Retrieved {len(messages)} emails ----")

        ###############################
        # ANSWER FOR EACH INDIVIDUAL MAIL
        ###############################
        print("Extracting all text and recognising all parts...")
        for message in messages:
            message_idx = message['id']

            ###############################
            # EXTRACT FULL PLAINTEXT
            ###############################
            print("Retrieving OCR or fulltext")
            attachments = email_service.get_message_with_attachments(msg_id=message_idx)

            if attachments is None:
                continue

            plaintext = handle_datasources(attachments)
            print(f"---- Extracted {len(plaintext)} characters starting with {plaintext[:100]} ----")

            ###############################
            # EXTRACT FULL PLAINTEXT
            ###############################
            print("Creating answer to RFP Excel...")
            matching_parts = extract_union_special_items(plaintext)
            print("Matching parts are")
            print(matching_parts)

            excel = USExcelTemplate()
            for part_json in matching_parts:
                print("Inserting")
                print(part_json)
                excel.insert_item(
                    partnumber=part_json['Partnumber'],
                    description=part_json['Description'],
                    listprice=part_json['Price'],
                    stock=part_json['Stock'],
                    status=part_json['Status'],
                    weight=part_json['Weight'],
                    replaced=part_json['Replaced']
                )

            # Instead of saving to disk, we need to send the email ....
            excel.save_to_disk()

            print("Sending e-mail and marking as read...")

            exit(0)

            # We might want to mark individual items as read before,
            # just in case it creates a crash in the server...

            # mark_as_read(service, 'me', message_idx)
            # email_wrapper.get_message(msg_id=message_idx)


        time.sleep(TIME_INTERVAL)
