from flask import render_template, redirect, url_for, request, session, flash
from ivr_phone_tree_python import app
import twilio.twiml
from ivr_phone_tree_python.view_helpers import twiml


@app.route('/')
@app.route('/ivr')
def home():
    return render_template('index.html')


@app.route('/ivr/welcome', methods=['POST'])
def welcome():
    response = twilio.twiml.Response()
    with response.gather(timeout=30, finishOnKey="#", action=url_for('menu'), method="POST") as g:
        g.say("how much wood would a woodchuck chuck if a woodchuck could chuck wood?  "+
              "Enter your response, followed by the pound key")
    return twiml(response)


@app.route('/ivr/menu', methods=['POST'])
def menu():
    selected_option = request.form['Digits']
    option_actions = {'700': _give_instructions}

    if option_actions.has_key(selected_option):
        response = twilio.twiml.Response()
        option_actions[selected_option](response)
        return twiml(response)

    return _redirect_welcome()


@app.route('/ivr/planets', methods=['POST'])
def planets():
    selected_option = request.form['Digits']
    option_actions = {'2': "+12024173378",
                      '3': "+12027336386",
                      "4": "+12027336637"}

    if option_actions.has_key(selected_option):
        response = twilio.twiml.Response()
        response.dial(option_actions[selected_option])
        return twiml(response)

    return _redirect_welcome()


# private methods

def _give_instructions(response):
    response.say("This item is indoors, but is normally found flashing orange in the wild",
                 voice="alice", language="en-GB")

    response.say("Thank you for playing")

    response.hangup()
    return response


def _list_planets(response):
    with response.gather(numDigits=1, action=url_for('planets'), method="POST") as g:
        g.say("To call the planet Broh doe As O G, press 2. To call the planet " +
              "DuhGo bah, press 3. To call an oober asteroid to your location, press 4. To " +
              "go back to the main menu, press the star key ",
              voice="alice", language="en-GB", loop=3)

    return response


def _redirect_welcome():
    response = twilio.twiml.Response()
    response.say("Returning to the main menu", voice="alice", language="en-GB")
    response.redirect(url_for('welcome'))

    return twiml(response)
