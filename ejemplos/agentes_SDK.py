import os
import dialogflow_v2

def getAgent(KEY_PATH: str, agent: str):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH

    client = dialogflow_v2.AgentsClient()
    parent = client.project_path(agent)

    # Imprime agentes dentro del proyecto (por si existen más)
    # for element in client.search_agents(parent):
    #     print(element)

    response = client.export_agent(parent)

    def callback(operation_future):
        result = operation_future.result()

        with open(agent + ".zip", "wb") as f:
            f.write(result.agent_content)

    response.add_done_callback(callback)


if __name__ == "__main__":
    KEY_PATH = "/home/gabriel/Documentos/Keys_DF/facturasvoz-estable-19c1a9fdc200_admin.json"
    getAgent(KEY_PATH, "facturasvoz-estable")

