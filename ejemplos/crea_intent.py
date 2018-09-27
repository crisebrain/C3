import os
import dialogflow_v2 as dialogflow

def create_intent(display_name, training_phrases_parts,
                  message_texts, action=None, webhook_state=False,
                  input_context_names=[], output_contexts=[],
                  displayNameType=None):
    """Create an intent of the given intent type."""
    intents_client = dialogflow.IntentsClient()
    parent = intents_client.project_agent_path(project_id)

    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        parts = []
        for element in training_phrases_part:
            if element.get("entity_type") is not None:
                part = dialogflow.types.Intent.TrainingPhrase.Part(
                    text=element.get("text"),
                    entity_type="@{0}".format(element.get("entity_type")),
                    alias=element.get("entity_type"))
            else:
                part = dialogflow.types.Intent.TrainingPhrase.Part(
                    text=element.get("text"))
            parts.append(part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=parts)
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)
    # Mas informacion
    # https://dialogflow-python-client-v2.readthedocs.io/en/latest/gapic/ \
    # v2/types.html#dialogflow_v2.types.Intent
    # el tema de los contextos tambien tiene que tratarse
    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message],
        action=action,
        webhook_state=webhook_state,
        input_context_names=input_context_names,
        output_contexts=output_contexts)
    response = intents_client.create_intent(parent, intent)
    print('Intent created: {}'.format(response))
    return response

filename = "hs-preguntasrespuestas-fac0e-8f92fd138c11_admin.json"
home = os.environ["HOME"]
path = os.path.join(home, "Ebraintec/Keys_DF", filename)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path

project_id = "hs-preguntasrespuestas-fac0e"

tphrases = [[
                {"text": "Quiero unos "},
                {"text": "tacos ", "entity_type": "comida"},
                {"text": "de "},
                {"text": "cochinita", "entity_type": "comida"}
           ],
           [
                {"text": "se me antoja una "},
                {"text": "torta", "entity_type": "comida"}
           ],
           [
                {"text": "Voy a preparar "},
                {"text": "mole", "entity_type": "comida"}
           ],
           [
                {"text": "voy a preparar "},
                {"text": "aguachile", "entity_type": "comida"}
           ],
           [
                {"text": "Me das unas "},
                {"text": "enfrijoladas", "entity_type": "comida"}
           ],
           [
                {"text": "Tengo antojo de una "},
                {"text": "birria", "entity_type": "comida"}
           ],
           [
                {"text": "Tengo antojo de comerme un "},
                {"text": "pozole", "entity_type": "comida"}
           ],
           [
                {"text": "Tengo mucha hambre y quiero "},
                {"text": "barbacoa", "entity_type": "comida"}
           ]]

message_texts = ["Sale $comida.original para el joven!!!"]
# Nombre de intent
display_name_intent = "auto-comer"
# action
action = "hambre"
# comunicacion con webhook
webhook_state = False
# Nombre de tipo de entity
display_name = "comida"

create_intent(display_name_intent, tphrases, message_texts,
              displayNameType=display_name, webhook_state=webhook_state,
              action=action)
