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

email_whitelist = [
    'david.yenicelk@gmail.com',
    'segaslp@gmail.com',
    'baker@bakermagnetics.com.tr',
    'auguryenicelik@hotmail.com',
    'mcyenicelik@hotmail.com',
    'mcyenicelik@bakermagnetics.com.tr',
    'unionspecialbags@bakermagnetics.com.tr',
    'unionspecial@bakermagnetics.com.tr',
    'baker@bakermagnetics.com.tr',
]

def handle_datasources(datasources):
    """
    :param datasources: a python list of tuples (name, bytestring)
    :return:
    """
    out = []
    for filename, content_str in datasources:
        print("Filename is: ", filename)
        if filename == "plaintext":
            out.append(content_str)
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

def _is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def extract_union_special_items(fulltext):
    union_special_item_set = usp_price_list.get_partlist_as_set

    # Must be a partition of the set, i.e. a full case distinction
    simple_union_special_item_seet = [x for x in union_special_item_set if _is_number(x)]
    complex_union_special_item_seet = [x for x in union_special_item_set if not _is_number(x)]

    # q = [set(x) for x in union_special_items]
    acceptable_chars = set()
    print("Iterating")
    for word in union_special_item_set:
        if ' ' in word:
            print(word)
        wordset = set(word)
        acceptable_chars = acceptable_chars.union(wordset)


    print("Union special parts")
    print(union_special_item_set)

    featureset1 = fulltext
    featureset2 = fulltext.replace(" ", "")
    featureset3 = fulltext.replace(" ", "-")
    featureset4 = fulltext.replace("-", "")
    featureset5 = fulltext.replace("-", " ")

    # This is the advanced set. Only search complex names in this advanced set
    full_featureset = featureset1 + featureset2 + featureset3 + featureset4 + featureset5
    simple_featureset = fulltext.split()

    # For all parts, detect if they are included
    found_items_simple = [x for x in list(simple_union_special_item_seet)if x in simple_featureset]
    found_items_complex = [x for x in list(complex_union_special_item_seet) if x in full_featureset]
    found_items = found_items_simple + found_items_complex

    # fulltext = fulltext.
    print("Fulltext is", full_featureset)

    print("Acceptable characters are", acceptable_chars)

    print("Found items are")
    print(found_items)

    exit(0)

    fulltext = set(fulltext.split())
    matching_parts = fulltext.intersection(usp_price_list.get_partlist_as_set)
    out = []
    for part in matching_parts:
        part_json = usp_price_list.get_partnumber_json(part_no=part)
        out.append(part_json)
    return out

def _represents_int(s):
    try:
        return int(s)
    except ValueError:
        return 1

def get_unit_number(fulltext_string, part_number):
    # Split the fulltext by whitespaces
    tokens = fulltext_string.split(" ")
    # Identify index of occurence
    idx = tokens.index(part_number)
    if idx == -1:
        return 0
    # move from idx and find best occuring number (2 digits)
    # do not move past 20 tokens away from the unit for the unit number
    for i in range(1, 50):
        # You could probably implement this in a more efficient manner using convolutions...
        # Convolution 1
        candidate1 = str(tokens[idx + i])
        # Convolution 2
        candidate2 = str(tokens[idx - i])
        # print("Candidate 1 and 2 are", candidate1, candidate2)
        if len(candidate1) <= 2:
            units = _represents_int(candidate1)
            if units < 30:
                return units
        if len(candidate2) <= 2:
            units = _represents_int(candidate1)
            if units < 30:
                return units

    return 1


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
            sender = email_service.get_email_sender(msg_id=message_idx)
            if sender is None:
                assert False, ("No sender found! Cannot respond to anyone ...", sender)
            email_service.set_email_to(sender)

            # Continue if email from is not whitelisted..
            if not (email_service.email_to in email_whitelist):
                print("Email not whitelisted!!!", email_service.email_to)
                continue

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
            matching_parts = list(sorted(matching_parts, key=lambda x: x['Partnumber']))
            for part_json in matching_parts:

                # Identify the unit number
                units = get_unit_number(plaintext, part_json['Partnumber']) # Will comment out for now because not very stable

                excel.insert_item(
                    partnumber=part_json['Partnumber'],
                    description=part_json['Description'],
                    listprice=part_json['Price'],
                    requested_units=units,
                    stock=part_json['Stock'],
                    status=part_json['Status'],
                    weight=part_json['Weight'],
                    replaced=part_json['Replaced']
                )

            excel.update_date()

            # Instead of saving to disk, generate a new email...
            message = email_service.create_message_with_attachment(
                content_bytestr=excel.get_bytestring()
            )

            print("Sending e-mail and marking as read...")
            email_service.send_message(message=message)
            email_service.mark_as_read(msg_id=message_idx)

        time.sleep(TIME_INTERVAL)
