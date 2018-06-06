import requests
import json
import subprocess


def sendReq(jdata, token):
    # ---------------------------------------------------------------------
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer " + token,
               "charset": "UTF-8"}
    req = requests.post("https://dialogflow.googleapis.com/v2/projects/transferenciaautomatica2/agent/sessions/4fe0f059:detectIntent",
                        data=json.dumps(jdata, indent=4), headers=headers)
    return req



# Obtenemos token de google (Ver documentación de como generar el token)
token = subprocess.check_output(["gcloud", "auth", "print-access-token"])
token = token.decode("utf-8").strip()


data = {"queryInput":{"event": { 'name': 'e_prueba',
                                 'parameters': { 'nombre': 'Gabriel' },
                                 'languageCode': 'en'}},
        "queryParams":{
            "timeZone": "America/Mexico_City"}
#'parameters': { 'nombre': 'Gabriel' },

        }

# llamamos petición
req = sendReq(data, token)
print(req.json())
