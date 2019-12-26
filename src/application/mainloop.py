"""
    Includes the main event loop that continuously pings the email
"""
import time
# Should perhaps write all to logs, instead of to stdout

if __name__ == "__main__":
    print("Starting program...")

    TIME_INTERVAL = 5

    # Write all errors into GCP stackdriver
    while True:
        print("Getting e-mails...")

        print("Extracting all text and recognising all parts...")

        print("Creating answer to RFP Excel...")

        print("Sending e-mail and marking as read...")

        time.sleep(TIME_INTERVAL)
