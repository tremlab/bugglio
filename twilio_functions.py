from twilio import twiml
from twilio.rest import Client
import os


AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
CALLER_ID = os.environ.get("TWILIO_CALLER_ID")
TWILIO_APP_SID = os.environ.get("TWILIO_TWIML_APP_SID")


def eval_phone(phone_raw):
    """make sure mobile # is correctly formatted for twilio.
        From form - user input will be a string of only digits.
    """
    if phone_raw[0] != "1":
        phone_raw = "1" + phone_raw

    if len(phone_raw) == 11:
        phone_raw = "+" + phone_raw
        response = phone_raw
    else:
        response = "not a valid phone number.  try again!"

    return response


def send_sms(mobile):
    """sends text to requested number."""

    if mobile[0] != "+":
        confirm_string = None
    else:
        # sms_string = markov.get_quote("buffy_speechify.txt")
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            to=mobile,
            from_=CALLER_ID,
            body=sms_string,
            # media_url="https://climacons.herokuapp.com/clear.png",
        )
        confirm_string = sms_string

    return confirm_string
