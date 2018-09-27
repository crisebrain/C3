import dialogflow_v2 as dialogflow
import os

class Entity_Handler:
    def __init__(self, project_id):
        self.project_id = project_id
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
            print("The entity type {0} doesn't exists".format(display_name))

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
                response = self.entityclient.create_entity_type(self.entity_parent,
                                                                entity_type)
            elif type(error).__name__ == "InvalidArgument":
                print(type(error).__name__, error)
                response = None
        print('Entity type created: \n{}'.format(response))
        return response

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



filename = "facturas-fasedos-mio-b9db6285b172.json"
home = os.environ["HOME"]
path = os.path.join(home, "Ebraintec/Keys_DF", filename)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path

project_id = "facturas-fasedos-mio"
display_name = "comida"
kind= 1
entity_value1 = "garnacha"
synonyms1 = ["huarache", "torta", "enfrijolada", "sope", "taco", "tacos", "quesadilla"]
entity_value2 = "platillo"
synonyms2 = ["mole", "aguachile", "birria", "pancita", "cochinita", "barbacoa"]

handler = Entity_Handler(project_id)
handler.create_entity_type(display_name, kind)
handler.create_entity(display_name, entity_value1, synonyms1)
handler.create_entity(display_name, entity_value2, synonyms2)
