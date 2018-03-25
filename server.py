from flask import Flask, jsonify, render_template, redirect, request, Response, flash, session
import sys
import os
import json
from twilio import twiml
from twilio.twiml.messaging_response import MessagingResponse
import bugsnag
from bugsnag.flask import handle_exceptions
import twilio_functions

app = Flask(__name__)
handle_exceptions(app) # bugsnag config
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "s0Then!stO0dth34ean9a11iw4n7edto9ow4s8ur$7!ntOfL*me5")
# app.jinja_env.endefined = StrictUndefined

AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
CALLER_ID = os.environ.get("TWILIO_CALLER_ID")
TWILIO_APP_SID = os.environ.get("TWILIO_TWIML_APP_SID")

bugsnag.configure(
    api_key=os.environ.get("BUGSNAG_BUGGLIO_KEY"),
    project_root="/",
)

@app.route("/", methods=['GET', 'POST'])
def homepage():
    """display homepage.
    """
    # build homepage, fomr to submit phone #
    return render_template("index.html")

@app.route("/bugsnag", methods=['GET', 'POST'])
def process_notif():
    """this route responds to notifications from the Bugsnag webhook.
    """
    data = json.loads(request.header)
    print("Bugsnag notification: {}".format(data))
    return "OK"



@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """this route responds to incoming texts.
    """
    resp = MessagingResponse()

    sms_msg = "Everything's perfectly all right now. We're fine. We're all fine here, now, thank you. How are you?"

    resp.message(sms_msg)

    return str(resp)

    # twiml = """
    # <Reposnse>
    #     <Message>
    #         Heyo
    #     </Message>
    # </Response>
    # """"


# @app.route("/message", methods=['POST'])
# def ask_for_msg():
#     phone_raw = request.form.get("mobile")
#
#     mobile = twilio_functions.eval_phone(phone_raw)
#
#     buffy_txt = twilio_functions.send_sms(mobile)
#
#     twitter_functions.tweet_text(buffy_txt)
#
#     confirm_string = """Marzipan! '%s' was texted to %s
#     """ % (buffy_txt, mobile)
#
#     return render_template("confirm_sms.html", confirm_string=confirm_string)


if __name__ == "__main__":
    bugsnag.notify(Exception("Test Error"))
    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
