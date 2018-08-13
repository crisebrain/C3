from enum import Enum

class constantesFacturas(Enum):
    PREFIJO = "prefijo"
    NIT = "nit"
    CUENTA = "cuenta"
    NO_DOCUMENTO = "noDocumento"
    STATUS = "status"
    ACUSE = "acuse"
    TIPO_DOCUMENTO = "tipoDocumento"
    FOLIO_INICIAL = "folioInicial"
    FOLIO_FINAL = "folioFinal"
    PERIODO = "periodo"
    FECHA = "fecha"
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
