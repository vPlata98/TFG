import sys
import json
import argparse
import random

from google.cloud import dialogflow as dialogflow_v2
from read import readXMLFile

trainingSaludos = ["Hola", "Saludos", "Que tal", "hey"]
textoAvisame = ["hola, cuando estes listo, avisame y comenzara el test de trivia"]
textoListo = ["listo", "preparado", "vamos", "comencemos"]
textoDespedida = ["El trivia ha terminado, gracias por jugar."]


def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts, hijo=False, father=None):
    """Create an intent of the given intent type."""

    intents_client = dialogflow_v2.IntentsClient()

    parent = dialogflow_v2.AgentsClient.agent_path(project_id)
    print("padre: " + parent)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow_v2.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow_v2.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    responses = []
    # for message in message_texts:

    message_response_txt = dialogflow_v2.Intent.Message.Text(text=message_texts)

    print("ANTES DE NADA ")
    print(message_response_txt)

    message_response = dialogflow_v2.Intent.Message(text=message_response_txt)

    print("DESPUES ")
    print(message_response)
    responses.append(message_response)
    print("RESPONSES")
    print(responses)
    print("id", father)
    if hijo:
        followup = dialogflow_v2.Intent.FollowupIntentInfo(followup_intent_name="custom")
        intent = dialogflow_v2.Intent(
            display_name=display_name,
            training_phrases=training_phrases,
            messages=responses,
            output_contexts=[
                dialogflow_v2.Context(
                    name=dialogflow_v2.ContextsClient.context_path(display_name, "-", "next-output"),
                    lifespan_count=1)],
            # input_context_names=["projects/" + project_id + "/agent/sessions/-/contexts/name"],
            webhook_state=dialogflow_v2.Intent.WebhookState.WEBHOOK_STATE_ENABLED,
            # is_fallback=True,
            parent_followup_intent_name=father,
            followup_intent_info=[followup]

        )
    else:
        intent = dialogflow_v2.Intent(
            display_name=display_name,
            training_phrases=training_phrases,
            messages=responses,
            output_contexts=[
                dialogflow_v2.Context(
                    name=dialogflow_v2.ContextsClient.context_path(display_name, "-", "next-output"),
                    lifespan_count=1)],
            # input_context_names=["projects/" + project_id + "/agent/sessions/-/contexts/name"],
            webhook_state=dialogflow_v2.Intent.WebhookState.WEBHOOK_STATE_ENABLED,
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
    intents_client = dialogflow_v2.IntentsClient()

    parent = dialogflow_v2.AgentsClient.agent_path(project_id)
    intents = intents_client.list_intents(request={'parent': parent})
    intent_names = [
        intent.name for intent in intents
        if intent.display_name == display_name]

    intent_ids = [
        intent_name.split('/')[-1] for intent_name
        in intent_names]

    return intent_ids


def formIntent(preguntas):
    intent1 = create_intent(sys.argv[1], sys.argv[2], trainingSaludos, textoAvisame)
    intent2 = create_intent(sys.argv[1], preguntas[0][0][0], textoListo, [preguntas[0][0][0] + "\n-->"
                                                                          + "\n-->".join(
        random.sample(preguntas[0][1], len(preguntas[0][1])))],
                            True, intent1.name)
    intentAnt = intent2
    for indx, pregunta in enumerate(preguntas):
        if pregunta[0] == preguntas[-1][0]:
            create_intent(sys.argv[1],
                          "Despedida",
                          pregunta[1],
                          textoDespedida,
                          True, intentAnt.name)
        else:
            intent = create_intent(sys.argv[1],
                                   preguntas[(indx + 1) % len(preguntas)][0][0],
                                   pregunta[1],
                                   [preguntas[(indx + 1) % len(preguntas)][0][0] + "\n-->"
                                    + "\n-->".join(random.sample(preguntas[(indx + 1) % len(preguntas)][1],
                                                                 len(preguntas[(indx + 1) % len(preguntas)][1])))],
                                   True, intentAnt.name)
            intentAnt = intent
            print(indx, pregunta)


def main():
    formIntent(readXMLFile(sys.argv[3]))


if __name__ == "__main__":
    main()
