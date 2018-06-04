import requests
import json

def sendReq(jdata):
    # ---------------------------------------------------------------------
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer ya29.c.El_QBQWnd2RGa4q3OlSFseyRPS_NBrH3D40iWeALXy6goUq4I05M0uIrWuTaWcolTxg27zozBNX5rCqdCI6jSukvTyrKIUc8zXi6dJwBucgdsmwEXbe7U9lAburX6xVliA",
               "charset": "UTF-8"}
    req = requests.post("https://dialogflow.googleapis.com/v2/projects/chatfase1/agent/sessions/4fe0f059:detectIntent",
                        data=json.dumps(jdata, indent=4), headers=headers)
    return req


data = {"queryInput":{"event": {"name": "salida","parameters": {"prueba": "1"},
                                "languageCode": "es"}},
        "queryParams":{ "timeZone": "America/Mexico_City"}}

req = sendReq(data)
print(req.json())
