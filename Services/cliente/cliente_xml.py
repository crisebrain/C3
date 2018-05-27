import requests
from xml.dom.minidom import parse
from requests_xml import XML
import ast
import json

# xml = """<soapenv:Envelope
# xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
# xmlns:b2b="http://www.enl.com.mx/B2BFactura/">
#    <soapenv:Header/>
#    <soapenv:Body>
#       <b2b:consultarFactura>
#          <Empresa>RICOH</Empresa>
#          <Periodo>Hoy</Periodo>
#          <FechaEmisionInicio>2017-07-12</FechaEmisionInicio>
#          <FechaEmisionFin>2017-07-12</FechaEmisionFin>
#          <Status>Recibido</Status>
#          <NumeroFactura>RCA20202ABFL</NumeroFactura>
#          <Factura>???</Factura>
#          <Cuenta>1209ABC</Cuenta>
#          <Cuenta>1209ABC</Cuenta>
#          <Prefijo>AAAA,99AA</Prefijo>
#          <FolioInicio>900082982</FolioInicio>
#          <FolioFin>900082990</FolioFin>
#          <Acuse>Aceptado</Acuse>
#          <NITAdquiriente>88888821</NITAdquiriente>
#       </b2b:consultarFactura>
#    </soapenv:Body>
# </soapenv:Envelope>
# """

fil = open("request_xml.xml", "r")
headers = {'Content-Type': 'application/xml'}
req = requests.post("http://169.48.112.198:9000/mockB2BFacturaSOAP?WSDL",
                    data=fil.read(), headers=headers)
print(req.text)

xml = XML(xml=req.content)
print(json.dumps(ast.literal_eval(xml.json()), indent=4))



# from xml.dom.minidom import parse
# filepath = "request_xml.xml"
# fileobj = parse(filepath)
# tags = ["Empresa", "Periodo", "FechaEmisionInicio",
#         "FechaEmisionFin", "Status",
#         "NumeroFactura", "Factura", "Cuenta",
#         "Cuenta", "Prefijo", "FolioInicio", "FolioFin",
#         "Acuse", "NITAdquiriente"]
# dictfields = dict()
# for node in fileobj.childNodes:
#     for tag in tags:
#         dictfields[tag] = node.getElementsByTagName(tag)[0].firstChild.data
# print(dictfields)
