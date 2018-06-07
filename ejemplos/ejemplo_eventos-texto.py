import requests
import json
import subprocess


def obtenemosToken():
    # Obtenemos token de google (Ver documentación de como generar el token)
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"])
    token = token.decode("utf-8").strip()
    return token


def sendEvent(jdata, token):
    # ---------------------------------------------------------------------
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer " + token,
               "charset": "UTF-8"}
    req = requests.post("https://dialogflow.googleapis.com/v2/projects/transferenciaautomatica2/agent/sessions/4fe0f059:detectIntent",
                        data=json.dumps(jdata, indent=4), headers=headers)
    return req



# Programa principal
token = obtenemosToken()

# Actualizar los valores dependiendo el evento a procesar
# https://dialogflow.com/docs/reference/api-v2/rest/v2/projects.agent.sessions/detectIntent
valores = {
            "queryInput": {
                # Aquí puede descomentarse cualquiera de los dos bloques de
                # código. Sirve para enviar eventos o textos.
                # "event": {
                #     'name': 'e_prueba',
                #     'parameters': { 'nombre': 'Gabriel' },
                #     'languageCode': 'en'
                # }
                "text": {
                    "text": "Prueba Gabriel",
                    "languageCode": "es"
                }
            },
            "queryParams": {
                "timeZone": "America/Mexico_City"
            }
        }

# Salta al evento
res = sendEvent(valores, token)
resJson = json.dumps(res.json(), indent=4)
print(resJson.encode('ascii').decode('unicode-escape')) # Imprime correctamente los caracteres
