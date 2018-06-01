import requests
import xml.etree.ElementTree as ET
import ast
import json
import pandas as pd

def sendReq(fieldsdict):
    import xml.etree.ElementTree
    #et = xml.etree.ElementTree.parse("request_template.xml")
    et = xml.etree.ElementTree.parse("Services/b2bcliente/request_template.xml")
    et.getroot()
    root = et.getroot()
    body = root.getchildren()[1]
    consultarfactura = body.getchildren()[0]
    for children in consultarfactura.getchildren():
        children.text = fieldsdict[children.tag]
        print("%s : %s" % (children.tag, children.text))
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
            diccionario.update({field.tag: field.text})
        lista_dicc.append(diccionario)
    return lista_dicc  # HumanResult(lista_dicc)

def superPandasRespuesta(lista_dicc):
    columns = ['NumeroDocumento', 'FechaEmision', 'Monto', 'NITAdquiriente',
               'NombreAdquiriente', 'NITFacturador', 'Estatus', 'Acuse',
               'Referencia']
    df = pd.DataFrame(columns=columns)
    for dicc in lista_dicc:
        dicpeq = dict()
        for key, value in dicc.items():
            if (value is None) or (value == "?"):
                dicpeq.update({key:"&nbsp;"})
            else:
                dicpeq.update({key:value})
        df = df.append(dicpeq, ignore_index=True)
    df.to_html("temp.html", table_id="t01")
    stringout = open("temp.html", "rb").read()
    return stringout

def HumanResult(lista_dicc):
    mensajote = ""
    counter = 0
    for resultado in lista_dicc:
        almenos1 = 0
        for key, value in resultado.items():
            keystr = '{:-<20}:'.format(key)
            va = True
            if value is not None:
                if value == "?":
                    va = False
                    valuestr = '{:->20}'.format("&nbsp;")
                else:
                    valuestr = '{:->30}'.format(value)
            else:
                va = False
                valuestr = '{:->20}'.format('&nbsp;')
            msgfield = keystr + valuestr
            if va:
                mensajote += msgfield + "\n"
                almenos1 += 1
        if almenos1 > 0:
            endline = '{:*^49}'.format('Factura') + "\n"
            mensajote += endline
            counter += 1
    if counter > 0:
        return(mensajote)
    else:
        return("No se encontraron coincidencias")

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
                  "FolioFin": "",
                  "Acuse": "Aceptado",
                  "NITAdquiriente": ""}
    # funciona con un diccionario
    req = sendReq(dictfields)
    listadicc = getResponseValues(req.content)
    browsertable = superPandasRespuesta(listadicc)
    print(browsertable)
