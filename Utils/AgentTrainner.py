import os
import dialogflow_v2 as dialogflow
import json
import sys

class AgentTrainer:
    def __init__(self, project_id, key_directory_folder="metadata",
                 key_type="admin"):
        self.project_id = project_id
        keydirpath = os.path.join(key_directory_folder, "keyfiles_path.json")
        keys_directory = json.load(open(keydirpath, 'r'))
        # Usa el directorio que haya sido asignado en keyfiles_path.json
        # según el sistema operativo
        dir_location = keys_directory.get("DirLocation").get(sys.platform, "")
        alert1 = '''There is not path assigned for {0},
        please add the path on keyfiles_path.json'''.format(sys.platform)
        alert2 = "\nThe directory {} doesn't exists\n".format(dir_location)
        assert dir_location != "", alert1
        assert os.path.exists(dir_location), alert2
        agentsArray = keys_directory['Agents'][key_type]
        agentexist = [True if element["project_id"] == project_id else False
                      for element in agentsArray]
        if any(agentexist):
            keyfile = agentsArray[agentexist.index(True)]["keyfile"]
            keyfile = os.path.join(dir_location, keyfile)
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = keyfile
        else:
            msgerr = "Key for project {0} doesn't exists".format(project_id)
            raise FileNotFoundError(msgerr)

    def delete_intent(self, intent_id):
        project_id = self.project_id
        intents_client = dialogflow.IntentsClient()
        intent_path = intents_client.intent_path(project_id, intent_id)
        intents_client.delete_intent(intent_path)

    def create_intent(self, display_name, training_phrases_parts,
                      message_texts):
        """Create an intent of the given intent type."""
        project_id = self.project_id
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
        try:
            response = intents_client.create_intent(parent, intent)
        except:
            print(intents_client.get_intent(display_name))
        # print('Intent created: {}'.format(response))

if __name__ == "__main__":
    atr = AgentTrainer("preguntasrespuestas-humansite")
    tphrases = ["comete mis calzones", "chupame el pie"]
    message_texts = ["Mejor tu comete los tuyos"]
    atr.create_intent("prueba", tphrases, message_texts)
