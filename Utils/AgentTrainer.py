import os
import dialogflow_v2 as dialogflow
import json
import sys

class Agent_Handler:
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
        self.entityclient = dialogflow.EntityTypesClient()
        self.entity_parent = self.entityclient.project_agent_path(project_id)

    def search_element_by_name(self, displayName, list_elements):
        elems = [{field[0].camelcase_name: field[1]
                  for field in element.ListFields()}
                 for element in list_elements]
        mask = [True if element["displayName"] == displayName else False
                for element in elems]
        if any(mask):
            index = mask.index(True)
            name = elems[index]["name"]
        else:
            name = None
        return name

    def delete_entity_type(self, displayName):
        """Delete entity type with the given entity type name."""
        list_types = self.entityclient.list_entity_types(self.entity_parent)
        path_entity_type = self.search_element_by_name(displayName,
                                                       list_types)
        if path_entity_type:
            self.entityclient.delete_entity_type(path_entity_type)
        else:
            print("The entity type {0} doesn't exists".format(displayName))

    def create_entity_type(self, displayName, kind):
        """Create an entity type."""
        entity_type = dialogflow.types.EntityType(display_name=displayName,
                                                  kind=kind)
        try:
            response = self.entityclient.create_entity_type(self.entity_parent,
                                                            entity_type)
        except Exception as error:
            if type(error).__name__ == "FailedPrecondition":
                print("updating entity type {0} ...".format(displayName))
                self.delete_entity_type(displayName)
                response = self.entityclient.create_entity_type(
                    self.entity_parent, entity_type)
            else:
                print(type(error).__name__, error)
                response = None
        print('Entity type created: \n{}'.format(response))

    def create_entity(self, displayNameType, entity_value, synonyms):
        """Create an entity of the given entity type."""
        list_types = self.entityclient.list_entity_types(self.entity_parent)
        path_entity_type = self.search_element_by_name(displayNameType,
                                                       list_types)
        synonyms = synonyms or [entity_value]
        # Note: synonyms must be exactly [entity_value] if the
        # entity_type's kind is KIND_LIST
        if path_entity_type:
            entity = dialogflow.types.EntityType.Entity()
            entity.value = entity_value
            entity.synonyms.extend(synonyms)
            response = self.entityclient.batch_create_entities(
                path_entity_type, [entity])
            print('Entity created: {}'.format(response))
        else:
            print("The entity type {0} doesn't exists".format(displayNameType))
            print("please create first the entity type with create_entity_type")

    def delete_intent(self, display_name):
        project_id = self.project_id
        list_intents = self.intents_client.list_intents(self.parent)
        name_intent = self.search_element_by_name(display_name,
                                                  list_intents)
        if name_intent:
            self.intents_client.delete_intent(name_intent)
        else:
            print("The intent {0} doesn't exists".format(display_name))

    def create_intent(self, display_name, training_phrases_parts,
                      message_texts, action=None, webhook_state=False,
                      input_context_names=[], output_contexts=[],
                      displayNameType=None):
        """Create an intent of the given intent type."""
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
            training_phrase = dialogflow.types.Intent.TrainingPhrase(
                parts=parts)
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
        try:
            response = self.intents_client.create_intent(self.parent, intent)
        except Exception as error:
            if type(error).__name__ == "FailedPrecondition":
                print("updating intent ...")
                self.delete_intent(display_name)
                response = self.intents_client.create_intent(self.parent,
                                                             intent)
            else:
                print(type(error).__name__, error)
                response = None
        print('Intent created: {}'.format(response))
        return response

if __name__ == "__main__":
    project_id = "hs-preguntasrespuestas-fac0e"
    # handler = Agent_Handler("facturasvoz-estable")
    # handler = Agent_Handler("preguntasrespuestas-humansite")
    handler = Agent_Handler(project_id)

    # Nombre de tipo de entity
    display_name = "comida"
    # Tipo de entity (hay listas 2, maps 1 o enumerables 3)
    kind= 1  # KIND_MAP
    # Valor de la entity
    entity_value1 = "garnacha"
    # Sinonimos para la entity
    synonyms1 = ["huarache", "torta", "enfrijolada", "sope", "taco", "tacos",
                 "quesadilla"]
    # lo mismo
    entity_value2 = "platillo"
    synonyms2 = ["mole", "aguachile", "birria", "pancita", "cochinita",
                 "barbacoa"]
    entity_value3 = "golosina"
    synonyms3 = ["cocada", "palanqueta", "gomitas", "cacahuates", "pepitas",
                 "pistaches"]

    # Frases de entrenamiento
    tphrases = [[
                    {"text": "Quiero unos "},
                    {"text": "tacos ", "entity_type": display_name},
                    {"text": "de "},
                    {"text": "cochinita", "entity_type": display_name}
               ],
               [
                    {"text": "se me antoja una "},
                    {"text": "torta", "entity_type": display_name}
               ],
               [
                    {"text": "Voy a preparar "},
                    {"text": "mole", "entity_type": display_name}
               ],
               [
                    {"text": "voy a preparar "},
                    {"text": "aguachile", "entity_type": display_name}
               ],
               [
                    {"text": "Me das unas "},
                    {"text": "enfrijoladas", "entity_type": display_name}
               ],
               [
                    {"text": "Tengo antojo de una "},
                    {"text": "birria", "entity_type": display_name}
               ],
               [
                    {"text": "Tengo antojo de comerme un "},
                    {"text": "pozole", "entity_type": display_name}
               ],
               [
                    {"text": "Tengo mucha hambre y quiero "},
                    {"text": "barbacoa", "entity_type": display_name}
               ]]
    # Mensaje de respuesta
    message_texts = ["Sale ${0}.original para el joven!!!".format(display_name)]
    # Nombre de intent
    display_name_intent = "auto-comer"
    # action
    action = "hambre"
    # comunicacion con webhook
    webhook_state = False
    # crear el tipo de entity
    handler.create_entity_type(display_name, kind)
    # crear los posibles valores junto con sinonimos
    handler.create_entity(display_name, entity_value1, synonyms1)
    handler.create_entity(display_name, entity_value2, synonyms2)
    handler.create_entity(display_name, entity_value3, synonyms3)

    # Crear intent con especificaciones, si el intent ya existe
    # lo borra y crea uno nuevo con las nuevas especificaciones
    handler.create_intent(display_name_intent, tphrases, message_texts,
                          webhook_state=webhook_state, action=action)
