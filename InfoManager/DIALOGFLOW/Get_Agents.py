import os
import re
import dialogflow_v2
import sys
import zipfile

def getAgent(KEY_PATH: str, agent: str):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH

    client = dialogflow_v2.AgentsClient()
    parent = client.project_path(agent)

    # Imprime agentes dentro del proyecto (por si existen mas)
    for element in client.search_agents(parent):
        print(element)

    response = client.export_agent(parent)

    def callback(operation_future):
        result = operation_future.result()

        with open(agent + ".zip", "wb") as f:
            f.write(result.agent_content)

    response.add_done_callback(callback)
    zip_ref = zipfile.ZipFile(agent + '.zip', 'r')
    zip_ref.extractall("../../chatbots/")
    zip_ref.extractall("../../chatbots/%s" % agent + "-03-09-2018")

_DICT_AGENT_CLIENT = {
    "facturasvoz-estable": "/home/ramon/Ebraintec/Keys_DF/facturasvoz-estable-19c1a9fdc200_admin.json",
    "hs-preguntasrespuestas-fac0e": "/home/ramon/Ebraintec/Keys_DF/hs-preguntasrespuestas-fac0e-8f92fd138c11_admin.json"
}

if __name__ == "__main__":
    for key, path in _DICT_AGENT_CLIENT.items():
        getAgent(path, key)
