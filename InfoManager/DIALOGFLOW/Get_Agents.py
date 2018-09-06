import os
import re
import json
import dialogflow_v2
import sys
import zipfile
import shutil
import datetime

def GetHashofDirs(directory, verbose=0):
    """Walks on the specified directory to retrieve the cheksum of contents.

    Parameters:
    directory - str with the directory's path.
    verbose - 0 by defualt to not print.

    Returns:
    hex checksum if the process was successful.
    """
    import hashlib, os
    SHAhash = hashlib.md5()
    if not os.path.exists (directory):
        return -1
    try:
        for root, dirs, files in os.walk(directory):
            for names in files:
                if verbose == 1:
                    print('Hashing', names)
                filepath = os.path.join(root,names)
                try:
                    f1 = open(filepath, 'rb')
                except:
                    # You can't open the file for some reason
                    f1.close()
                    continue

                while 1:
                    # Read file in as little chunks
                    buf = f1.read(4096)
                    if not buf : break
                    hashstr = hashlib.md5(buf).hexdigest()
                    SHAhash.update(hashstr.encode('utf-8'))
                f1.close()

    except:
        import traceback
        # Print the stack traceback
        traceback.print_exc()
        return -2

    return SHAhash.hexdigest()

def modify_agent_name(folder_path, agent):
    """Modifies the agent field in agent.json.

    Parameters:
    folder_path - string path of the agent folder in  C3/chatbots/
    agent - string agent name
    """
    file_path = os.path.join(folder_path, "agent.json")
    diccionario = json.load(open(file_path, 'r'))
    diccionario['googleAssistant']['project'] = agent
    with open(file_path, 'w') as fil:
        fil.write(json.dumps(diccionario, indent=2))

def getAgent(key_path, agent):
    """Downloads the agent zip file and paste the folder on chatbots.

    Parameters:
    key_path - key file path to get admin permissons of GC.
    agent - agent name.

    returns:
    None
    """
    if os.path.exists(key_path):
        zip_folder = "/tmp/DF_cb_zips"
        extracted_folder = "/tmp/DF_cb_extracted"
        chatbots_folder = "chatbots"
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
        client = dialogflow_v2.AgentsClient()
        parent = client.project_path(agent)
        print("********************************\n")
        # Imprime agentes dentro del proyecto (por si existen mas)
        for element in client.search_agents(parent):
            print(element)
        response = client.export_agent(parent)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        # Paths
        zip_path = os.path.join(zip_folder, agent + ".zip")
        newVer = os.path.join(extracted_folder, agent)
        previousVer = os.path.join(chatbots_folder, agent)
        if not os.path.exists(zip_folder):
            os.mkdir(zip_folder)
        if not os.path.exists(extracted_folder):
            os.mkdir(extracted_folder)
        def callback(operation_future):
            result = operation_future.result()
            with open(zip_path, "wb") as f:
                f.write(result.agent_content)
        response.add_done_callback(callback)
        zip_ref = zipfile.ZipFile(zip_path, 'r')
        zip_ref.extractall(newVer)
        modify_agent_name(newVer, agent)
        # copiando a chatbots folder
        if os.path.exists(previousVer):
            newVercopied = previousVer + timestamp
            shutil.copytree(newVer, newVercopied)
            hashPrevious = GetHashofDirs(previousVer)
            hashNew = GetHashofDirs(newVercopied)
            if hashNew != hashPrevious:
                print(hashNew, " not equal ", hashPrevious)
                print("Check the differences between {0} and {1}".format(previousVer, newVercopied))
                print("Keeping both files")
                print("********************************\n")
            else:
                print("The agent {0} is already up-to-date".format(agent))
                shutil.rmtree(newVercopied)
        else:
            shutil.copytree(newVer, previousVer)

    else:
        print("file %s not founded" % key_path)


def update_Agents():
    _HOME = os.environ['HOME']
    # Para elegir el nombre del agente, usar el project id presenta dialogflow en la consola
    _DICT_AGENT_CLIENT = {
        "facturasvoz-estable": os.path.join(_HOME, "Ebraintec/Keys_DF/facturasvoz-estable-19c1a9fdc200_admin.json"),
        "hs-preguntasrespuestas-fac0e": os.path.join(_HOME, "Ebraintec/Keys_DF/hs-preguntasrespuestas-fac0e-8f92fd138c11_admin.json"),
        # "preguntasrespuestas-humansite": os.path.join(_HOME, "Ebraintec/Keys_DF/preguntasrespuestas-humansite-e221cd6b345a_admin.json")
    }
    for key, path in _DICT_AGENT_CLIENT.items():
        getAgent(path, key)
