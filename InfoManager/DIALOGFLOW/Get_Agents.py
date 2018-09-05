import os
import re
import dialogflow_v2
import sys
import zipfile
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
                    SHAhash.update(hashlib.md5(buf).hexdigest())
                f1.close()

    except:
        import traceback
        # Print the stack traceback
        traceback.print_exc()
        return -2

    return SHAhash.hexdigest()

def getAgent(key_path, agent):
    """Downloads the agent zip file and paste the folder on chatbots.

    Parameters:
    key_path - key file path to get admin permissons of GC.
    agent - agent name.

    returns:
    None
    """
    if os.path.exists(key_path):
        zip_folder = "../../DF_cb_zips"
        chatbots_folder = "../../chatbots"
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
        client = dialogflow_v2.AgentsClient()
        parent = client.project_path(agent)
        # Imprime agentes dentro del proyecto (por si existen mas)
        for element in client.search_agents(parent):
            print(element)
        response = client.export_agent(parent)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        downloaded = agent + "_" + timestamp
        zip_path = os.path.join(zip_folder, agent + ".zip")
        if not os.path.exists(zip_folder):
            os.mkdir(zip_folder)
        def callback(operation_future):
            result = operation_future.result()
            with open(zip_path, "wb") as f:
                f.write(result.agent_content)
        response.add_done_callback(callback)
        zip_ref = zipfile.ZipFile(zip_path, 'r')
        zip_ref.extractall("../../chatbots/%s" % downloaded)
    else:
        print("file %s not founded" % key_path)

_HOME = os.environ['HOME']
_DICT_AGENT_CLIENT = {
    "facturasvoz-estable": os.path.join(_HOME, "Ebraintec/Keys_DF/facturasvoz-estable-19c1a9fdc200_admin.json"),
    "hs-preguntasrespuestas-fac0e": os.path.join(_HOME, "Ebraintec/Keys_DF/hs-preguntasrespuestas-fac0e-8f92fd138c11_admin.json"),
    "preguntasrespuestas-humansite": os.path.join(_HOME, "Ebraintec/Keys_DF/preguntasrespuestas-humansite-e221cd6b345a_admin.json")
}

if __name__ == "__main__":
    for key, path in _DICT_AGENT_CLIENT.items():
        getAgent(path, key)
