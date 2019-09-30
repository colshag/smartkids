"""
Smart Kids by NeuroJump games
Special Thanks to Keith Galli for help understanding python Alexa coding!
https://www.youtube.com/channel/UCq6XkhO5SZ66N04IcPbqNcw
"""

from __future__ import print_function
import random
from facts import myFacts
from sounds import sounds

# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "SSML",
            "ssml": __build_ssml_speech(output)
        },
        "card": {
            "type": "Simple",
            "title": "SessionSpeechlet - " + title,
            "content": "SessionSpeechlet - " + __remove_ssml_speech(output)
        },
        "reprompt": {
            "outputSpeech": {
                "type": "SSML",
                "ssml":  __build_ssml_speech(output)
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def __build_ssml_speech(text):
    """Build the SSML to include sound effects which are captioned by ()
    replace any soundkey (eg. (door) with a random audio clip from amazon clips based on sounds dict of list of clips"""
    for soundkey in sounds.keys() :
        if soundkey in text :
            print(soundkey)
            print(text)
            newString = random.choice(sounds[soundkey])
            newString = newString + '<break time="1s"/>'
            text = text.replace(soundkey, newString)
            print(text)
    
    t = '<speak>' + text + '</speak>'
    return t
    
def __remove_ssml_speech(text):
    """Remove sound clips captioned by () if not appropriate"""
    for soundkey in sounds.keys() :
        if soundkey in text :
            text = text.replace(soundkey, '')

    return text

def __pass_session_attributes(session):
    """Get the current session attributes and pass them back as a dictionary for the session_attributes dictionary
    to keep the session attributes active"""
    d = {}
    if session.get('attributes', {}):
        pass
        # current_id = session['attributes']['id']
        # d['crew_morale'] = session['attributes']['crew_morale'] + scenarios[current_id]['CREW_MORALE'] # update morale
        # d['ship_strength'] = session['attributes']['ship_strength'] + scenarios[current_id]['SHIP_STRENGTH'] # update ship strength
        # d['intel'] = session['attributes']['intel'] + scenarios[current_id]['INTEL'] # update intel
        # d['id'] = session['attributes']['id']
    
    print('pass_session_attributes====>')
    print(d)
    return d

def get_fact_response(intent, session, category):
    """ Give player a fact based on category given
    """
    print("get_fact_response(%s)===>" % category)
    print(session)
    session_attributes = __pass_session_attributes(session)
    speech_output = "I'm sorry there has been an error, please contact neurojump forums"
    
    # if session.get('attributes', {}):
    if category != "":
        speech_output = random.choice(myFacts[category]) + ", please choose from these categories: Culture, Animals, Geography, and Space"
        
    card_title = "Your %s Fact" % category
    reprompt_text = speech_output
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}

    card_title = "Welcome"
    speech_output = "Welcome to our learning game called. Did You Know. We hope you enjoy some random facts from four categories. Please say: Culture, Animals, Geography, or Space, to learn some interesting facts!"
    reprompt_text = speech_output
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def get_help_response():
    """ Give the player some information
    """
    session_attributes = {}

    card_title = "Help"
    speech_output = "No Problem. I would love to share some facts with you, please choose from these categories: Culture, Animals, Geography, and Space"
    reprompt_text = speech_output
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying did you know, we hope you learned something new! " \
                    "Have a great day! "
                    
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific 
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass
    

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']


    # Dispatch to your skill's intent handlers
    if intent_name == "cultureFact":
        return get_fact_response(intent, session, "CULTURE")
    elif intent_name == "animalFact":
        return get_fact_response(intent, session, "ANIMALS")
    elif intent_name == "geographyFact":
        return get_fact_response(intent, session, "GEOGRAPHY")
    elif intent_name == "spaceFact":
        return get_fact_response(intent, session, "SPACE")
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        # raise ValueError("Invalid intent")
        return get_status_response(intent, session)


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
