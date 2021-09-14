from logging import INFO
from typing import Dict
from read import readXMLFile
from flask import Flask, request, jsonify
from flask.logging import create_logger

from dialogflow_fulfillment import WebhookClient, QuickReplies

# Create Flask app and enable info level logging
app = Flask(__name__)
logger = create_logger(app)
logger.setLevel(INFO)


def handler(agent: WebhookClient) -> None:
    """
    Handle the webhook request.

    This handler sends a text message along with a quick replies
    message back to Dialogflow, which uses the messages to build
    the final response to the user.
    """
    #agent.add('How are you feeling today?')
    #agent.add(QuickReplies(quick_replies=['Happy :)', 'Sad :(']))


@app.route('/webhook', methods=['GET','POST'])
def webhook() -> Dict:
    """Handle webhook requests from Dialogflow."""
    data = request.get_json(silent=True)
    #print(data)
    preguntas = readXMLFile("preguntasXML.xml")
    if data['queryResult']['queryText'] == 'hola':
        reply = {
            "fulfillmentText": "Tu nota es la siguiente",
        }
        return jsonify(reply)
    agent = WebhookClient(data)
    agent.handle_request(handler)
    print(agent.response)
    return agent.response


@app.route('/')
def index():
    return 'Hello, Flask!'


if __name__ == '__main__':
    app.run(debug=True)
