import requests
from requests_xml import XML
import xml.etree.ElementTree as ET
import ast
import json


def sendReq(fieldsdict):
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
    headers = {"Content-Type": "text/xml",
               "charset": "UTF-8",
               "SOAPAction": "http://www.enl.com.mx/B2BFactura/consultarFactura"}
    req = requests.post("http://169.48.112.198:9000/mockB2BFacturaSOAP?WSDL",
                        data=xmlreq, headers=headers)
    return req

def getResponseValues(xmlstring):
    tree = ET.ElementTree(ET.fromstring(xmlstring))
    root = tree.getroot()
    body = root.getchildren()[1]  # body
    facturas = body.getchildren()[0].getchildren()  # responsebody
    facturaslista = [factura.getchildren() for factura in facturas]
    lista_dicc = []
    for fields in facturaslista:
        diccionario = {}
        for field in fields:
            diccionario.update({field.tag:field.text})
        lista_dicc.append(diccionario)
    return lista_dicc


if __name__ == "__main__":
    dictfields = {"Empresa": "RICOH",
                  "Periodo": "Mes",
                  "FechaEmisionInicio": "",
                  "FechaEmisionFin": "",
                  "Status": "",
                  "NumeroFactura": "",
                  "Factura": "Factura",
                  "Cuenta": "",
                  "Cuenta": "",
                  "Prefijo": "",
                  "FolioInicio": "",
                  "FolioFin" : "",
                  "Acuse": "Aceptado",
                  "NITAdquiriente": ""}
    # funciona con un diccionario
    req = sendReq(dictfields)
    lista_dicc = getResponseValues(req.content)
    print(lista_dicc)
