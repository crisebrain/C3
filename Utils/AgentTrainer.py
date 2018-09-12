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
        self.intents_client = dialogflow.IntentsClient()
        self.parent = self.intents_client.project_agent_path(project_id)

    def delete_intent(self, display_name):
        project_id = self.project_id
        intents = [{field[0].camelcase_name: field[1]
                    for field in intent.ListFields()}
                   for intent in self.intents_client.list_intents(self.parent)]
        intent_mask = [True if intent["displayName"] == display_name else False
                       for intent in intents]
        if any(intent_mask):
            index = intent_mask.index(True)
            name = intents[index]["name"]
            self.intents_client.delete_intent(name)
        else:
            print("The intent {0} doesn't exists".format(display_name))

    def create_intent(self, display_name, training_phrases_parts,
                      message_texts):
        """Create an intent of the given intent type."""
        training_phrases = []
        for training_phrases_part in training_phrases_parts:
            part = dialogflow.types.Intent.TrainingPhrase.Part(
                text=training_phrases_part)
            # Here we create a new training phrase for each provided part.
            training_phrase = dialogflow.types.Intent.TrainingPhrase(
                parts=[part])
            training_phrases.append(training_phrase)

        text = dialogflow.types.Intent.Message.Text(text=message_texts)
        message = dialogflow.types.Intent.Message(text=text)

        intent = dialogflow.types.Intent(
            display_name=display_name,
            training_phrases=training_phrases,
            messages=[message])
        try:
            response = self.intents_client.create_intent(self.parent, intent)
        except Exception as error:
            if type(error).__name__ == "FailedPrecondition":
                print("updating intent ...")
                self.delete_intent(display_name)
                response = self.intents_client.create_intent(self.parent,
                                                             intent)
            else:
                response = None
        # print('Intent created: {}'.format(response))
        return response

if __name__ == "__main__":
    atr = AgentTrainer("preguntasrespuestas-humansite")
    tphrases = ["Jarvis", "Oye Jarvis", "Te hablo a tí",
                "Jarvis me escuchas", "Jarvis dime algo"]
    message_texts = ["Vete a molestar a otro lado, pinche escuincle!!!"]
    atr.create_intent("prueba", tphrases, message_texts)
