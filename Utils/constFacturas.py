from enum import Enum

class constantesFacturas(Enum):
    TIPO_DOCUMENTO = "tipoDocumento"
    PERIODO = "periodo"
    STATUS = "status"
    PREFIJO = "prefijo"
    ACUSE = "acuse"
    FOLIO_INICIAL = "folioInicial"
    FOLIO_FINAL = "folioFinal"
    NIT = "nit"
    CUENTA = "cuenta"
    FECHA = "fecha"
    NO_DOCUMENTO = "noDocumento"
    FECHA_INICIAL = "fechaInicial"
    FECHA_FINAL = "fechaFinal"


class constGenericas(Enum):
    RECIBIDO = "Recibido"
    ERROR =  "Error"
    FIRMADO = "Firmado"
    RECHAZADO = "Rechazado"
    ACEPTADO = "Aceptado"
    ENVIADO = "Enviado"
    PENDIENTE = "Pendiente"


if __name__ == "__main__":
    c = constantesFacturas
    print(c.TIPO_DOCUMENTO.value)
    print(c.TIPO_DOCUMENTO.name)