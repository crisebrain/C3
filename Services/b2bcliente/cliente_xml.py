import requests
from requests_xml import XML
import ast
import json


def fillReq(fieldsdict):
    import xml.etree.ElementTree
    et = xml.etree.ElementTree.parse("request_template.xml")
    et.getroot()
    root = et.getroot()
    body = root.getchildren()[1]
    consultarfactura = body.getchildren()[0]
    for children in consultarfactura.getchildren():
        children.text = fieldsdict[children.tag]
        print("%s : %s" %(children.tag, children.text))
    # esta instruccion es para convertir el objeto tipo elementTree a texto
    xmlreq = xml.etree.ElementTree.tostring(et.getroot()).decode()
    # ---------------------------------------------------------------------
    headers = {'Content-Type': 'application/xml'}
    req = requests.post("http://169.48.112.198:9000/mockB2BFacturaSOAP?WSDL",
                        data=xmlreq, headers=headers)
    return req

def getResponseValues(responsedict):
    responsedict = [item for item in responsedict.values()]
    # responsedict = [item for item in responsedict.values()]
    responsedict = [item for item in responsedict[0].values()]
    responsedict = [item for item in responsedict[1].values()]
    responsedict = [item for item in responsedict[0].values()]
    return responsedict

if __name__ == "__main__":
    dictfields = {"Empresa": "RICOH",
                  "Periodo": "Hoy",
                  "FechaEmisionInicio": "2017-07-12",
                  "FechaEmisionFin": "2017-07-12",
                  "Status": "Recibido",
                  "NumeroFactura": "RCA20202ABFL",
                  "Factura": "???",
                  "Cuenta": "1209ABC",
                  "Cuenta": "1209ABC",
                  "Prefijo": "AAAA,99AA",
                  "FolioInicio": "900082982",
                  "FolioFin" : "900082990",
                  "Acuse": "Aceptado",
                  "NITAdquiriente": "88888821"}
    # funciona con un diccionario
    req = fillReq(dictfields)
    xml = XML(xml=req.content)
    # el request lo convierto a texto, en seguida a xml y de xml a diccionario
    diccionario_respuesta = ast.literal_eval(xml.json())
    diccionario_respuesta = getResponseValues(diccionario_respuesta)
    for elem in diccionario_respuesta:
        print(elem)
