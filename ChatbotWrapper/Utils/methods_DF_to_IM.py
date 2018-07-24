IM_FIELDS = "IM_fields"

def updateIM(req:dict, fields: dict):
    req.update({IM_FIELDS: fields})
    print(req)

