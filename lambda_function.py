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
        d['ID'] = session['attributes']['ID']
        d['category'] = session['attributes']['category']
        d['completed'] = session['attributes']['completed']
        d['correct'] = session['attributes']['correct']
        d['donelist'] = session['attributes']['donelist']
        
    print('pass_session_attributes====>')
    print(d)
    return d

def get_question(intent, session, category):
    """ Give player a fact question based on category given
    """
    print("get_question(%s)===>" % category)
    print(session)
    session_attributes = __pass_session_attributes(session)
    speech_output = "I'm sorry there has been an error, please contact neurojump forums"
    
    if session.get('attributes', {}):
        if session_attributes["ID"] == -1:
            if len(session_attributes['donelist'][category]) >= len(myFacts[category]):
                # all questions in category have been asked
                speech_output = "Great work! You have asked for all the questions in the %s category, please choose another category." % category
            else:
                # category has questions left from this selected category
                selectedID = -2
                count = 0
                while selectedID == -2:
                    count += 1
                    item = random.choice(myFacts[category])
                    if item["ID"] not in session_attributes['donelist'][category]:
                        selectedID = item["ID"]
                        speech_output = "From the %s category: " % category
                        speech_output = speech_output + "Here is your True or False Question: " + item["QUESTION"]
                        print("TRY ITEMID = %d" % item["ID"])
                        session_attributes["category"] = category
                        session_attributes["ID"] = selectedID
                    if count > 100:
                        speech_output = "Sorry there was an error selecting a question, please try again!"
                        break
        else:
            category = session_attributes['category']
            categoryList = myFacts[category]
            item = categoryList[session_attributes['ID']]
            speech_output = "From the %s category: " % session_attributes['category']
            print("STORE ITEMID = %d" % item["ID"])
            speech_output = speech_output + "Here is a your True or False Question: " + item['QUESTION']
            
    card_title = "Your %s Question" % category
    reprompt_text = speech_output
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_response(intent, session, response):
    """ A player says response = TRUE or FALSE"""
    print("get_response===>%s" % response)
    print(session)
    session_attributes = __pass_session_attributes(session)
    speech_output = "I'm sorry there has been an error, please contact neurojump forums"
    
    if session.get('attributes', {}):
        if session_attributes['ID'] == -1:
            speech_output = "Please choose a category from: Culture, Animals, Geography, and Space. " 
        else:
            completed = session_attributes['completed'] + 1
            category = session_attributes['category']
            correct = session_attributes['correct']
            item = myFacts[category][session_attributes['ID']]
            
            if item["TRUE OR FALSE"] == response:
                correct += 1
            
            if completed == 0:
                score = 0
            else:
                score = (float(correct) / float(completed)) * 100
                
            speech_output = item["RESPONSE %s" % response] + ". Your score is %d percent from %d questions asked, Please chose from: Culture, Animals, Geography, and Space. " % (score, completed)
            session_attributes['correct'] = correct
            session_attributes['completed'] = completed
            donelist = session_attributes['donelist']
            donelist[category].append(session_attributes['ID'])
            session_attributes['donelist'] = donelist
            session_attributes['ID'] = -1
        
    card_title = response
    reprompt_text = speech_output
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {'ID':-1,
                          'category':'CULTURE',
                          'completed':0,
                          'correct':0,
                          'donelist':{'CULTURE':[],'ANIMALS':[],'GEOGRAPHY':[],'SPACE':[]}
                          }

    card_title = "Welcome"
    speech_output = "Welcome to Smart Kids, where we ask you 10 True or False questions, on your journey of learning. Please choose your first category, from Culture, Animals, Geography, or Space."
    reprompt_text = speech_output
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def get_help_response(intent, session):
    """ Give the player some information
    """
    session_attributes = __pass_session_attributes(session)

    card_title = "Help"
    speech_output = "Please choose from these categories: Culture, Animals, Geography, and Space"
    reprompt_text = speech_output
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying smart kids, we hope you learned something new! " \
                    "Have a great day! "
                    
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def end_game(intent, session):
    card_title = "Game Complete"
                    
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    session_attributes = __pass_session_attributes(session)
    speech_output = "I'm sorry there has been an error, please contact neurojump forums"
    
    if session.get('attributes', {}):
        correct = session_attributes['correct']
        completed = session_attributes['completed']
        score = (float(correct) / float(completed)) * 100
        speech_output = "Great Job! You finished 10 questions from smart kids, nice work! Your final score was %d percent. See you again soon for more learning with Neuro Jump Games!" % score
    
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
    session_attributes = __pass_session_attributes(session)

    # check status of game
    if session.get('attributes', {}):
        if session_attributes['completed'] == 10:
            return end_game(intent, session)

    # Dispatch to your skill's intent handlers
    if intent_name == "cultureFact":
        return get_question(intent, session, "CULTURE")
    elif intent_name == "animalFact":
        return get_question(intent, session, "ANIMALS")
    elif intent_name == "geographyFact":
        return get_question(intent, session, "GEOGRAPHY")
    elif intent_name == "spaceFact":
        return get_question(intent, session, "SPACE")
    elif intent_name == "true":
        return get_response(intent, session, "TRUE")
    elif intent_name == "false":
        return get_response(intent, session, "FALSE")
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response(intent, session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        # raise ValueError("Invalid intent")
        return get_help_response(intent, session)


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
