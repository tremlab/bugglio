from flask import Flask, jsonify, render_template, redirect, request, abort, Response, flash, session
# from flask_sqlalchemy import SQLAlchemy
import sys
import os
# from model import ()
# from sqlalchemy.orm.exc import NoResultFound
import json
from twilio import twiml
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from flask_cors import CORS, cross_origin
import bugsnag
from bugsnag.flask import handle_exceptions
import psycopg2

bugsnag.configure(
    api_key=os.environ.get("BUGSNAG_BUGGLIO_KEY"),
    project_root="/",
)

app = Flask(__name__)
handle_exceptions(app) # bugsnag config
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "s0Then!stO0dth34ean9a11iw4n7edto9ow4s8ur$7!ntOfL*me5")
# db = SQLAlchemy(app)
# conn = psycopg2.connect(DATABASE_URL, sslmode='require')

AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
CALLER_ID = os.environ.get("TWILIO_CALLER_ID")
TWILIO_APP_SID = os.environ.get("TWILIO_TWIML_APP_SID")
ON_DUTY = os.environ.get("ON_DUTY")


# In the simplest case, initialize the Flask-Cors extension with default arguments in order to allow CORS for all domains on all routes.
CORS(app)
# app.config['Access-Control-Allow-Origin'] = '*'

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
    # this app route should only accept requests from Bugsnag's IP addresses
    headers_list = request.headers.getlist("X-Forwarded-For")
    request_ip = headers_list[0] if headers_list else request.remote_addr
    print(request_ip)
    if request_ip in ['104.196.245.109', '104.196.254.247']:
        data = json.loads(request.data)
        sms_msg = parse_bugsnag(data)

        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            to=ON_DUTY,
            from_=CALLER_ID,
            body=sms_msg,
        )

        return "OK"

    else:
         abort(403)  # Forbidden


def parse_bugsnag(data):
    """accepts a dictionary of data from the JSON payload from Bugsnag's notification.
    """
    # catch if not formatted right
    try:
        notif_type = data['trigger']['type']
        message = data['trigger']['message']
        project = data['project']['name']
    except Exception as e:
        bugsnag.notify(e)
        return "Couldn't parse notification data. Check app.bugsnag.com"

    sms_msg = message + " on " + project

    if notif_type == 'exception':
        sms_msg = sms_msg + " details: " + data['error']['exceptionClass'] + " " + data['error']['message']

        # // The type of trigger sent (always present)
        # // - "firstException"         A new error is created from a new exception
        # // - "powerTen"               An error occurs frequently
        # // - "exception"              Every time an exception is received
        # // - "reopened"               An error is automatically reopened
        # // - "projectSpiking"         A spike in exception in a project has been detected
        # // - "comment"                A comment is added to an error
        # // - "errorStateManualChange" A user has manually changed the state of an error

    return sms_msg


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """this route responds to incoming texts.
    """
    resp = MessagingResponse()

    sms_msg = "Everything's perfectly all right now. We're fine. We're all fine here, now, thank you. How are you? --bugglio.herokuapp.com"

    resp.message(sms_msg)

    return str(resp)

    # twiml = """
    # <Reposnse>
    #     <Message>
    #         Heyo
    #     </Message>
    # </Response>
    # """"



if __name__ == "__main__":
    DEBUG = "NO_DEBUG" not in os.environ
    # connect_to_db(app, os.environ.get("DATABASE_URL"))
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
