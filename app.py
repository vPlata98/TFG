import os
from logging import INFO
from werkzeug.utils import secure_filename
from typing import Dict
from read import conseguirNotas, readXMLFile
from flask import Flask, request, jsonify, render_template
from flask.logging import create_logger
from bot import formIntent
from google.cloud import storage
from dialogflow_fulfillment import WebhookClient, QuickReplies

# Create Flask app and enable info level logging
app = Flask(__name__)
logger = create_logger(app)
logger.setLevel(INFO)
preguntasUsuario = []
nota = [[0]]
respuestas = conseguirNotas("preguntasXML.xml")
currentQuestion = 0
flag = False
uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)


def calculoNota(respuestasUsuario):
    global nota, respuestas
    for index, respuesta in enumerate(respuestasUsuario):
        respuestasCorrectas = [x for x in respuestas.keys() if x.lower() == respuesta.lower()]
        nota.append([respuestas[puntuacion] / 100 for puntuacion in respuestasCorrectas])
        print(nota)
    nota = sum(nota, [])
    nota = sum(nota)


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
def webhook():
    """Handle webhook requests from Dialogflow."""
    global nota, flag, currentQuestion, respuestas
    data = request.get_json(silent=True)
    # print(data)

    if data['queryResult']['queryText'].lower() in ["listo", "preparado", "vamos", "comencemos", "ya", "adelante", "empieza", "comienza"]:
        flag = True
    if flag:
        currentQuestion += 1
    if data['queryResult']['queryText'].lower() in ["adiós","adios", "hasta luego", "chao", "nos vemos"]:
        print(preguntasUsuario[2:])
        calculoNota(preguntasUsuario[2:])
        numRespuestas = len([key for key, value in respuestas.items() if value == 100])
        reply = {
            "fulfillmentText": "Tu nota es la siguiente " + str(nota) + "/" + str(numRespuestas),
        }
        preguntasUsuario.clear()
        nota = [[0]]
        return jsonify(reply)
    agent = WebhookClient(data)
    agent.handle_request(handler)
    preguntasUsuario.append(data['queryResult']['queryText'])
    # print(agent.response)
    print(agent.response)
    return jsonify(agent.response)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        print(request.files.getlist("file"))
        fileQuestions = ""
        secureJSON = ""
        for file in request.files.getlist("file"):
            print(file.filename)
            filename, file_extension = os.path.splitext(file.filename)
            file.save(os.path.join(uploads_dir, secure_filename(file.filename)))
            if file_extension == ".xml":
                fileQuestions = file.filename
            elif file_extension == ".json":
                secureJSON = file.filename
        explicit(os.path.join(uploads_dir, secure_filename(secureJSON)))

        # f = request.files["file"]
        # f.save(secure_filename(f.filename))
        formIntent(request.form["projectFile"], request.form["bot"], readXMLFile(fileQuestions))
        return render_template("index.html", send=True)
    else:
        return render_template('index.html')


def explicit(file):
    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        file)
    # os.system("export GOOGLE_APPLICATION_CREDENTIALS=" + file)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = file
    print(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    # Make an authenticated API request
    # buckets = list(storage_client.list_buckets())
    # print(buckets)
    return storage_client


if __name__ == '__main__':
    app.run(debug=True)
