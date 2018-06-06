import requests
import json
import subprocess
import base64


def encode_audio64_DF(archivo):
    audio = open(archivo, "rb")
    audio_content = audio.read()
    return str(base64.b64encode(audio_content), "ascii", "ignore") # Borra saltos de linea


def obtenemosToken():
    # Obtenemos token de google (Ver documentación de como generar el token)
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"])
    token = token.decode("utf-8").strip()
    return token


def getIntent(valoresAudio, token):
    # ---------------------------------------------------------------------
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer " + token,
               "charset": "UTF-8"}
    req = requests.post("https://dialogflow.googleapis.com/v2/projects/transferenciaautomatica2/agent/sessions/4fe0f059:detectIntent",
                        data=json.dumps(valoresAudio, indent=4), headers=headers)
    return req


# Inicialización
token = obtenemosToken()
audioBase64 = encode_audio64_DF("saldo8.wav")

# Actualizar los valores dependiendo el audio a procesar
# https://dialogflow.com/docs/reference/api-v2/rest/v2/projects.agent.sessions/detectIntent
valores = {
            "queryInput":{
                "audioConfig": {
                    "audioEncoding": "AUDIO_ENCODING_LINEAR_16",
                    "sampleRateHertz": 8000,
                    "languageCode": "es"
                }
            },
            "inputAudio": audioBase64
        }


# Petición
res = getIntent(valores, token)
resJson = json.dumps(res.json(), indent=4)
print(resJson.encode('ascii').decode('unicode-escape')) # Imprime correctamente los caracteres
