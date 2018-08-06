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
file = "audios/guion_5.flac"
languageCode = "es-419"
letras = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
		  "n", "ñ", "o", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
phraseHints = ["acuse pendiente", "nit", "nit adquiriente", "rfc",]
phraseHints += letras
print(phraseHints)
# file = "audios/shwazil_hoful.flac"
# languageCode = "en-US"
# phraseHints = ["shwazil hoful day"]
token = obtenemosToken()
audioBase64 = encode_audio64_DF(file)

# Actualizar los valores dependiendo el audio a procesar
# https://dialogflow.com/docs/reference/api-v2/rest/v2/projects.agent.sessions/detectIntent
# sample rate ideal en 16000
valores = {
            "queryInput":{
                "audioConfig": {
                    # FLAC: AUDIO_ENCODING_FLAC, WAV: AUDIO_ENCODING_LINEAR_16
                    "audioEncoding": "AUDIO_ENCODING_FLAC",
                    "sampleRateHertz": 16000,
                    "languageCode": languageCode,
                    "phraseHints": phraseHints
                }
            },
            "inputAudio": audioBase64
        }


# Petición
res = getIntent(valores, token)
resJson = json.dumps(res.json(), indent=4)
print(resJson.encode('ascii').decode('unicode-escape')) # Imprime correctamente los caracteres
