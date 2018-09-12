import os
import dialogflow_v2

def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    """Create an intent of the given intent type."""
    import dialogflow_v2 as dialogflow
    intents_client = dialogflow.IntentsClient()

    parent = intents_client.project_agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])

    response = intents_client.create_intent(parent, intent)

    print('Intent created: {}'.format(response))

if __name__ == "__main__":
    _HOME = os.environ['HOME']
    keypath = _HOME + "/Ebraintec/Keys_DF/preguntasrespuestas-humansite-e221cd6b345a_admin.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = keypath
    tphrases = ["comete mis calzones", "chupame el pie"]
    message_texts = ["Mejor tu comete los tuyos"]
    project_id = "preguntasrespuestas-humansite"
    display_name = "prueba"
    create_intent(project_id, display_name,
                  tphrases, message_texts)
