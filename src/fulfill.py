from flask import Flask, request, jsonify
from datetime import datetime as dt
import pytz

tz = pytz.timezone('Canada/Eastern')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def student_number():
    # return student number
    return jsonify(student_number="200575834")

@app.route('/webhook', methods=['POST'])
def webhook():
    # Parse the incoming JSON request
    req = request.get_json(force=True)
    
    # Get the intent name from queryResult -> intent-> displayName
    intent_name = req.get('queryResult', {}).get('intent', {}).get('displayName', '')
    
    # Prepare a response to the intent
    if intent_name == 'Get Current Datetime':
        # Response of the request or use a static response
        now = dt.now(tz)
        response_text = f"Today's Date is {now.strftime('%d-%b-%Y')} and current time is {now.strftime('%I:%M %p')} in Torronto."
        
        # Create a fulfillment response in Dialogflow's expected format
        fulfillment_response = {
            "fulfillmentText": response_text,
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [response_text]
                    }
                }
            ]
        }
    else:
        # Default response if the intent is not recognized
        fulfillment_response = {
            "fulfillmentText": "Sorry, I didn't got you.",
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": ["Sorry, I didn't got you."]
                    }
                }
            ]
        }

    # Return the response in JSON format
    return jsonify(fulfillment_response)

if __name__ == '__main__':
    app.run()  # Turn off debug mode when deploying