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
preguntasUsuario = []
nota = 0


def calculoNota(respuestasUsuario):
    global nota
    preguntasQuiz = readXMLFile("preguntasXML.xml")
    for index, pregunta in enumerate(preguntasQuiz):
        if pregunta[1][0].lower() == respuestasUsuario[index].lower():
            nota += 1


def handler(agent: WebhookClient) -> None:
    """
    Handle the webhook request.

    This handler sends a text message along with a quick replies
    message back to Dialogflow, which uses the messages to build
    the final response to the user.
    """
    # agent.add('How are you feeling today?')
    # agent.add(QuickReplies(quick_replies=['Happy :)', 'Sad :(']))


@app.route('/webhook', methods=['POST'])
def webhook() -> Dict:
    """Handle webhook requests from Dialogflow."""
    global nota
    data = request.get_json(silent=True)
    # print(data)
    preguntas = readXMLFile("preguntasXML.xml")
    if data['queryResult']['queryText'] == 'adios':
        print(preguntasUsuario[2:])
        calculoNota(preguntasUsuario[2:])
        reply = {
            "fulfillmentText": "Tu nota es la siguiente " + str(nota) + "/" + str(len(preguntasUsuario[2:])),
        }
        preguntasUsuario.clear()
        nota = 0
        return jsonify(reply)
    agent = WebhookClient(data)
    agent.handle_request(handler)
    preguntasUsuario.append(data['queryResult']['queryText'])
    # print(preguntasUsuario)
    return agent.response


@app.route('/')
def index():
    return 'Hello, Flask!'


if __name__ == '__main__':
    app.run(debug=True)
