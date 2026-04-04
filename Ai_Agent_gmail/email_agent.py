import imaplib
import email
from email.header import decode_header
from idlelib.iomenu import errors
from sre_constants import error

from google import genai

import os
from dotenv import load_dotenv
from pyasn1.codec.ber.decoder import decode
from pydantic_core.core_schema import is_instance_schema

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_API_PASSWORD = os.getenv("GMAIL_API_PASSWORD")

client = genai.Client(api_key="GEMINI_API_KEY")

def connect_to_gmail():
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(GMAIL_EMAIL, GMAIL_API_PASSWORD)
        print("Connected to Gmail")
        return mail
    except Exception as e:
        print(f"Error connecting tp Gmail: {e}")
        return None

def decode_email_subject(subject):
    if not subject:
        return "Without subject"


    decoded_parts = decode_header(subject)

    decoded_subject = ""

    try:
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                decoded_subject += part.decode(encoding or "utf-8" , errors = "ignore")
            else:
                decoded_subject += part
        return decoded_subject

    except Exception as e:
        print(f"Error decoding subject: {e}")
        return subject if isinstance(subject, str) else "Error decoding subject"

def get_email_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                try:
                    body = msg.get_payload(decode= True).decode("utf-8", errors="ignore")
                    break
                except:
                    body = "Can't decode part"

    else:
        try:
            body = msg.get_payload(decode= True).decode("utf-8", errors="ignore")
        except:
            body = "Can't decode "



def get_emails(mail, max_emails=5):
    try:
        mail.select("INBOX") # "SPAM"
        status, messages = mail.search(None, "all")  # "SEEN" , "UNSEEN"
        email_ids = messages[0].split()
        email_ids = email_ids[-max_emails:]
        #Ex. 100 -> emails_ids = [96, 97, 98, 99, 100]
        #If there are 100 letters,the 100th is the newest

        emails = []

        for email_id in reversed(email_ids):
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    subject = decode_email_subject(msg.get("Subject", "Без теми"))
                    sender = msg.get("From", "Невідомий")
                    date = msg.get("Date", "Невідома дата")
                    body = get_email_body(msg)

                    emails.append({
                        "subject": subject,
                        "sender": sender,
                        "date": date,
                        "body": body[:500]
                    })
        return emails
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return []

def analyze_emails_with_ai():
    pass

def main():
    mail = connect_to_gmail()
    if not mail:
        print("Something wrong")
        return
    print("Getting emails")
    emails = get_emails(mail, max_emails=5)

    mail.close()
    mail.logout()

    print(emails)

if __name__ == '__main__':
    main()