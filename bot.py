import sys
import json
import argparse
import random

from dialogflow_fulfillment import QuickReplies
from google.cloud import dialogflow as dialogflow_v2_beta
from google.cloud import dialogflow_v2beta1 as dialogflow_v2_beta
from read import readXMLFile

trainingSaludos = ["Hola", "Saludos", "Que tal", "hey"]
trainingDespedida = ["Adios", "Hasta luego", "Chao", "Nos vemos"]
textoAvisame = ["Hola, cuando estes listo, avisame y comenzara el test de trivia"]
textoListo = ["listo", "preparado", "vamos", "comencemos", "ya", "adelante", "empieza", "comienza"]
textoDespedida = ["El trivia ha terminado, gracias por jugar. Despidete para obtener tu nota. Por favor, evalúame "
                  "haciendo esta encuesta: "
                  "https://docs.google.com/forms/d/e/1FAIpQLSeBg3ydhTGIRkVAXu3SwZxu2zVlQ3DYKb3SFqLvvJxQMAxb7g"
                  "/viewform?usp=sf_link"]


def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts, type, imgInfo=None, hijo=False, father=None):
    """Create an intent of the given intent type."""

    intents_client = dialogflow_v2_beta.IntentsClient()

    parent = dialogflow_v2_beta.AgentsClient.agent_path(project_id)
    print("padre: " + parent)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow_v2_beta.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow_v2_beta.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    responses = []
    # for message in message_texts:

    print("ANTES DE NADA 1 ")
    print(message_texts)
    if type == "trueFalse" and len(max(message_texts, key=len)) < 20:
        message_response_txt = dialogflow_v2_beta.Intent.Message.QuickReplies(title=message_texts[0][0],
                                                                              quick_replies=message_texts[1])
        message_response = dialogflow_v2_beta.Intent.Message(quick_replies=message_response_txt)
    elif type in ["multichoice", "trueFalse", "gapSelect"]:
        message_response_txt = dialogflow_v2_beta.Intent.Message.Card(title=message_texts[0][0],
                                                                      buttons=creadorBotones(message_texts[1]),
                                                                      image_uri=imgInfo[0],
                                                                      subtitle='\n '.join(message_texts[1]))
        message_response = dialogflow_v2_beta.Intent.Message(card=message_response_txt)

    elif type == "normal":
        message_response_txt = dialogflow_v2_beta.Intent.Message.Text(text=message_texts)
        message_response = dialogflow_v2_beta.Intent.Message(text=message_response_txt)
    else:
        message_response_txt = dialogflow_v2_beta.Intent.Message.Text(text=['\n--> '.join(sum(message_texts, []))])
        message_response = dialogflow_v2_beta.Intent.Message(text=message_response_txt)

    responses.append(message_response)

    if hijo:
        followup = dialogflow_v2_beta.Intent.FollowupIntentInfo(followup_intent_name="custom")
        intent = dialogflow_v2_beta.Intent(
            display_name=display_name,
            training_phrases=training_phrases,
            messages=responses,
            output_contexts=[
                dialogflow_v2_beta.Context(
                    name=dialogflow_v2_beta.ContextsClient.context_path(display_name, "-", "next-output"),
                    lifespan_count=1)],
            # input_context_names=["projects/" + project_id + "/agent/sessions/-/contexts/name"],
            webhook_state=dialogflow_v2_beta.Intent.WebhookState.WEBHOOK_STATE_ENABLED,
            # is_fallback=True,
            parent_followup_intent_name=father,
            followup_intent_info=[followup]

        )
    else:
        intent = dialogflow_v2_beta.Intent(
            display_name=display_name,
            training_phrases=training_phrases,
            messages=responses,
            output_contexts=[
                dialogflow_v2_beta.Context(
                    name=dialogflow_v2_beta.ContextsClient.context_path(display_name, "-", "next-output"),
                    lifespan_count=1)],
            # input_context_names=["projects/" + project_id + "/agent/sessions/-/contexts/name"],
            webhook_state=dialogflow_v2_beta.Intent.WebhookState.WEBHOOK_STATE_ENABLED,
            # is_fallback=True,
            # parent_followup_intent_name=parent + "/intents/" + id[0],
            # followup_intent_info=[followup]

        )

    print(intent)
    response = intents_client.create_intent(request={'parent': parent, 'intent': intent})

    print('Intent created: {}'.format(response))
    return response


def _get_intent_ids(project_id, display_name):
    # from google.cloud import dialogflow
    intents_client = dialogflow_v2_beta.IntentsClient()

    parent = dialogflow_v2_beta.AgentsClient.agent_path(project_id)
    intents = intents_client.list_intents(request={'parent': parent})
    intent_names = [
        intent.name for intent in intents
        if intent.display_name == display_name]

    intent_ids = [
        intent_name.split('/')[-1] for intent_name
        in intent_names]

    return intent_ids


def rangeQuestions(message):
    for indx, msg in enumerate(message[1:]):
        message[indx] = str(indx) + ")" + msg
    print(message)
    return message


def formIntent(projectCode, projectName, preguntas):
    intent1 = create_intent(projectCode, projectName, trainingSaludos, textoAvisame, "normal")
    message = [preguntas[0][0]] + [random.sample(preguntas[0][1], len(preguntas[0][1]))]
    print(message)
    intent2 = create_intent(projectCode, preguntas[0][0][0], textoListo, message,
                            preguntas[0][2],
                            preguntas[0][3],
                            True, intent1.name)
    intentAnt = intent2
    for indx, pregunta in enumerate(preguntas):
        if pregunta[0] == preguntas[-1][0]:
            intent = create_intent(projectCode,
                                   "Despedida",
                                   pregunta[1],
                                   textoDespedida,
                                   "normal",
                                   pregunta[3],
                                   True, intentAnt.name)
            intentAnt = intent
            create_intent(projectCode,
                          "Despedida Usuario",
                          trainingDespedida,
                          [],
                          "normal",
                          None,
                          True, intentAnt.name)
        else:
            intent = create_intent(projectCode,
                                   preguntas[(indx + 1) % len(preguntas)][0][0],
                                   pregunta[1],
                                   [preguntas[(indx + 1) % len(preguntas)][0]] +
                                   [random.sample(preguntas[(indx + 1) % len(preguntas)][1],
                                                  len(preguntas[(indx + 1) % len(preguntas)][1]))],
                                   preguntas[(indx + 1) % len(preguntas)][2],
                                   preguntas[(indx + 1) % len(preguntas)][3],
                                   True, intentAnt.name)
            intentAnt = intent
            print(indx, pregunta)


def creadorBotones(bot):
    botones = []
    for indx, b in enumerate(bot):
        botones.append({'text': b})
    return botones


def main():
    if sys.argv[2] == "download":
        download = dialogflow_v2_beta.services.agents.AgentsAsyncClient.export_agent(parent=sys.argv[1])
        print(download)
    else:
        formIntent(sys.argv[1], sys.argv[2], readXMLFile(sys.argv[3]))


if __name__ == "__main__":
    main()
