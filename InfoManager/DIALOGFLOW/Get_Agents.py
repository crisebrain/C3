import os
import json
import dialogflow_v2
import sys
import zipfile
import shutil
import datetime
import gc

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

def getAgent(key_path, agent, chatbots_folder = "chatbots"):
    """Downloads the agent zip file and paste the folder on chatbots.

    Parameters:
    key_path - key file path to get admin permissons of GC.
    agent - agent name.

    returns:
    None
    """
    if os.path.exists(key_path):
        if sys.platform == 'linux':
            zip_folder = "/tmp/DF_cb_zips"
            extracted_folder = "/tmp/DF_cb_extracted"
        elif sys.platform.startswith('win'):
            zip_folder = "d:/DF_cb_zips"
            extracted_folder = "d:/DF_cb_extracted"
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
                print("Check differences on {0} and {1}".format(previousVer,
                                                                newVercopied))
                print("Keeping both files")
                print("********************************\n")
            else:
                print("The agent {0} is already up-to-date".format(agent))
                shutil.rmtree(newVercopied)
        else:
            shutil.copytree(newVer, previousVer)

    else:
        print("file %s not founded" % key_path)


def update_Agents(key_directory_folder='metadata', key_type='admin'):
    """Iterates the AgentId to download them from DF with getAgent function.
    Uses the keyfiles_path.json file on metadata folder to know the current
    keyfile for each agent used in project.
    Parameters:
    key_directory_folder - Is the keyfiles_path.json container folder, e.g.
                           "metada".
    type - Is the type of keyfile used, i.e., "admin" to download the agent.

    Returns:
    None - if the key files folder doesn't enlisted on keyfiles_path.json
           doesn't exists.
    """
    keydirpath = os.path.join(key_directory_folder, "keyfiles_path.json")
    keys_directory = json.load(open(keydirpath, 'r'))
    # Usa el directorio que haya sido asignado en keyfiles_path.json
    # según el sistema operativo
    dir_location = keys_directory.get("DirLocation").get(sys.platform, "")
    if dir_location == "":
        print("\nThere is not path assigned for {0} \
               add the path on keyfiles_path.json\n".format(sys.platform))
        return 0
    elif not os.path.exists(dir_location):
        print("\nThe directory {} doesn't exists\n".format(dir_location))
        return 0
    for element in keys_directory['Agents'][key_type]:
        pathfile = os.path.join(dir_location, element["keyfile"])
        getAgent(pathfile, element["project_id"])
    gc.collect()
    return 1