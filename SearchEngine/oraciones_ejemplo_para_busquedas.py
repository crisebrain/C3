import sys
from SearchEngine import Regexseaker
from Utils import constantesFacturas as cf

def pruebasFolios():
    reg = Regexseaker()

    expsMalas = [
        # "y con folio de inicio igual a 1234",
        # "y con folio de inicio igual a xxxxx",
        # "con rango de folio  entre el inicial de AAAAA",
        "rojo es el folio de inicio",
        "carro es el folio de inicio",
        "qerwet es el folio de inicio",
        "dsfda como folio de inicio",
        "El folio de inicio es el ERWERWREWT",
        "En folio de inicio asignamos el QWEERE",
        "Para folio de inicio el valor de QWERWERWER",
        "cuyo folio de inicio es el WQERRTW",
        "folio de inicio igual a QWERRT",
        "El folio de inicio definido en QWERTTW",
    ]

    expsBuenas_FolioInicio = [
        "facturas donde el folio de inicial es 0123",
        "y con folio de inicio igual a 000012",
        "con rango de folio  entre el inicial de 123456789",
        "9037432  es el folio de inicio",
        "El folio de inicio es el 002930200",
        "En folio de inicio asignamos el 2373893",
        "Para folio de inicio el valor de 11111111",
        "cuyo folio de inicio es el 222222",
        "folio de inicio igual a 78923430",
        "El folio de inicio definido en 23432",
        "con folio inicial igual a 568768",
        "con folio inicial  de  709898798",
        "el folio inicial es el  689778",
        "folio inicial de 6987687",
        "folio Inicial definido en 79876767878 ",
        "23432 es el folio de inicio",
        "y asignamos 56987 como folio inicial",
        "cuyo folio mas reciente de inicio es el 5687",
        "6987898 es el ultimo folio de inicio",
        "el folio inicial es el 6987879",
        "tenemos un folio de inicialización de 679876",
        "y donde 6987867 es el folio de inicio definido",
        "con folio inicial asignado de 569876",
        "folio de inicialización de 69879879",
        "folio de inicio asignado a 5986987",
        "dame las facturas con folio de inicio igual a 6987987",
        "con comienzo de folio en 69887",
        "con inicialización de folio o folio de inicio de 69979",
        "Ademas de que el folio de comienzo de serie es el 60978",
        "el folio de comienzo es el 7098",
        "y un folio inicial o de inicio de 709098",
        "con folio con principio de serie de 698987",
        "dame las facturas que principian con el folio 09900909",
        "Quiero las facturas con inicialización de folio en 97980990",
        "Requiero las facturas cerradas pero que inicien con el folio 6899879",
        "por favor factoras con inicialización de folio en 89989",
        "notas de credito cuyo folio inicial es el 9889897979",
        "908908908 como folio de inicialización",
        "908908908 como folio de inicio",
        "908908908 es el folio de inicio",
        "dame las facturas que inician con el folio 987879797897",
        "quiero facturas con folio inicial o de inicio definido en  6999897979",
        "necesito las facturas donde el folio de comienzo es 433554",
        "necesito las facturas que comienzan con el folio 7998989",
        "solicito las facturas cuo folio de inicia empieza en 7898908",
        "quiero facturas que empiezan con el folio 68799889",
        "el folio 79898798 es el de inicio"
    ]

    expsBuenas_FolioFin = [
            "con folio de finalización igual a 69898",
            "el folio de finalizado es 6980987",
            "el folio de fin es el 698798",
            "con folio de fin en 6987",
            "el folio de finalizacion es 98798787",
            "en folio de finalización asignamos 6988",
            "con folio de finalizado igual a 232343",
            " y el folio final de 65656",
            "el folio de finalización es el 12342",
            "con folio de finalización de 98573",
            "en folio de finalización ponemos 2334",
            "y 87664 como folio de finalización",
            "el folio final es 42445",
            "con folio de finalización definido en 42455",
            "el folio de finalización es 62564",
            "en folio de finalización asignamos el 9873",
            "9877 es el folio de finalización",
            "53457 es el folio de finalizado",
            "y con folio de finalización o de fin en 69887",
            "el folio final es igual a 2334544",
            "el folio termina en 6798",
            "con folio final definido a 698787",
            "y un folio de finalización igual a 23443",
            "asi como un folio de fin de 6797898989",
            "56987987 es el folio de finalización",
            "56987987 es el folio de finalización",
            "56987987 es el folio de cierre",
            "como folio de cierre o de fin ponemos el 698987",
            "el folio de fin es el 798988",
            "679897 es el ultimo folio de finalizado",
            "el reciente folio de finalizado es el 9898787",
            "el folio 79898798 es el de finalización",
            "como finalización de folio ponemos el 698988",
            "y con folio de fin definido en 69887",
            "como folio de finalizado se tiene el 69898",
            "en folio de finalizado asignamoe el valor 609898",
            "para el folio de finalizado ponemos 435665",
            "9880708 es el valor del folio de final",
            "11111 es nuestro folio de finalización",
            "11111 es mi folio de finalización",
            "mi folio de finalización es el 222222",
            "nuestro valor de finalización en folio es el 697988",
            "folio de finalizado es 689080880",
            "para folio de finalizado asignamos el 67879799",
            "en el cierre de folio ponemos el 68808080808",
        ]



            # for phrase in expsBuenas_FolioInicio:
            #     resultado = folios(phrase, "Inicio")
            #     if resultado[1] == 0:
            #         print("Resulado: {1}\n{0}\n\n".format(str(resultado[0:2]), resultado[2]))
            #
            # for phrase in expsBuenas_FolioFin:
            #     resultado = folios(phrase, "Fin")
            #     if resultado[1] == 0:
            #         print("Resulado: {1}\n{0}\n\n".format(str(resultado[0:2]), resultado[2]))

            # for phrase in expsBuenas_FolioFin:
            #     print("Resulado: {0}\n".format(str(folios(phrase, "Fin"))))
    for phrase in expsBuenas_FolioInicio: #+ expsBuenas_FolioInicio:
        resultado = reg.seakexpresion(phrase, cf.FOLIO_INICIAL.value)
        #if resultado[1] == 0:
        print("{0}\nResulado: {1}\n{2}\n".format(
        phrase, str(resultado[:2]),resultado[3]))


def pruebasFechas():
    reg = Regexseaker()
    exps = [
            # "con fecha inicial del 15 de Febrero del 2017 , es todo gracias",
            # " cuya fecha inicial es desde el 1 de febrero del 2017",
            # "posteriores al primero de febrero del 2018",
            # "entre el 15 de noviembre del 17",
            # "con periodo del 1 de Marzo del 2017 ",
            # " desde marzo del 2017",
            # "posteriores al 24 de Septiembre",
            # "de Marzo primero del 2017",
            # "de noviembre ",
            # "desde Abril del 2017 ",
            # "a partir de la segunda semena de enero del año pasado",
            # "comprendidas en el periodo de Enero del 2017",
            # " generadas a partir del 6 de Noviembre del año pasado",
            # "generados desde el 8 de Abril del presente año",
            # " generadas desde el 5 del presente mes",
            # "con fecha del 5 de Abril del 2017",
            # "que oscilen entre el 4 de Junio",
            # "comprendidos entre Abril 7",
            # "con rango de fechas comprendido entre Abril 5",
            # "que datan del 4 de Abril del 2018",
            # "desde el último de marzo del 2017",
            # "entre el 23 de Junio del 2016",
            # "con fecha de inicio del 12 de Marzo del 2016",
            # "pero emitidas en Noviembre 17 del año pasado",
            # "pero cuyas fechas se encuentren entre el 1 de Diciembre",
            # "Del 1 de marzo",
            # "Del 3 de Mayo del año pasado ",
            # " entre el 5 de Marzo del 2018",
            # "que esten entre el día actual ",
            # "pero que tambien sean anteriores al 12 de Marzo del 18, esta claro",
            # "pero que sean anteriores al 14 de Junio",
            # "y el 24 de Febrero del 2018",
            # "al 5 de Noviembre",
            # "al mes actual",
            # "anteriores al 7 de Noviembre",
            # "hasta el mes pasado",
            # "anteriores a Enero del presente año",
            # "a Marzo del mismo año",
            # " al 6 de Noviembre del año pasado",
            # "y Septiembre 14 del año pasado",
            # "y Marzo 19 del presente año",
            # "previos al 15 de Enero del 2018",
            # "anteriores a Abril 9 de este año",
            # "hasta el día de hoy",
            # "y el primero de Marzo del año pasado",
            # "y fecha de fin del 13 de Noviembre del presente año",
            # "anteriores al 5 de Marzo del 2017",
            # "pero que sean previas al 15 de Marzo de este año.",
            # " y el 15 de Febrero del año pasado",
            # " y que sean previas al 6 de Noviembre de este año",
            # "al 9 de Noviembre del 2016",
            # "al 19 de Enero del presente año",
            # " previas al 5 de noviembre de este año",
            # "y el 6 de Enero del 2017",
            # "y posteriores al 14 de Diciembre"
            "facturas con fecha de inicio es 21 de febrero del 2009 y de fin 15 de marzo del 2018, gracias. y fecha de fin 24 de diciembre del 2000"
        ]

    expsAcordadas = [
            "5 de septiembre 2 de noviembre octubre 5",
            "fecha inicial del 5 de enero del 2015",
            "fecha inicial del 9 de Diciembre del 2013",
            "fecha de inicio al 12 de Marzo del 2013",
            "fecha de inicio al 12 de Noviembre del 2015",
            "fecha de comienzo del primero de enero del 2015",
            "fecha de comienzo del 21 de Enero del 2013",
            "fecha inicio de marzo del 2015",
            "fecha principio en Julio del 2015",
            "con periodo de inicio de Septiembre 23 del 2016",
            "iniciando en Septiembre 27 del 2012",
            "Con comienzo en Julio 23",
            "Con comienzo en Julio 45",
            "Iniciando el 14 de Mayo",
            "iniciando el 12 de Febrero",
            "inicia Del primero de enero",

            "Fecha final del 3 de Noviembre del 2017",
            "y finalizando al 4 de Marzo del 2014",
            "finalizando el 12 de Agosto de 1980",
            "concluyendo el 23 de Febrero de 1988",
            "y terminando el 12 de Julio de 1990",
            "concluyendo en Octubre 23",
            "con fecha de finalización a Septiembre del 2016",
            "hasta el 12 de Marzo",
            "la fecha de fin es el 12 de Abril",
            "terminando el 23 de diciembre del 2030",
            "y la fecha final es el 23 de Octubre",
            "fecha de conclusión de Noviembre 18",
            "Terminando el 12 Marzo del 2015",
            "y fecha de conclusión de documentos al 23 de Noviembre"
        ]

    expsCasos = [
            "quiero mi facturas con fecha de inicio 3 de septiembre del 2017",
            "quiero mi facturas con fecha de fin 3 de septiembre del 2017",
            "quiero mi facturas con fecha de inicio 3 de septiembre del 2017 y fin de diciembre del 2018",
            "quiero mi facturas con fecha de 3 de septiembre del 2017",
            "quiero mi facturas con fecha de inicio 3 de septiembre del 2017 y fin de diciembre del 2018 además 1 de enero del 2018",
            "quiero mi facturas con fecha de inicio 3 de septiembre del 2017 además 1 de enero del 2018 y fin de diciembre del 2018",
            "quiero mi facturas además 1 de enero del 2018 con fecha de inicio 3 de septiembre del 2017 y fin de diciembre del 2018",
            "quiero mi facturas además 1 de enero del 2018 con 3 de septiembre del 2017 y de diciembre del 2018",
            "quiero mi facturas con además 1 de enero del 2018 y fin de diciembre del 2018",
            "quiero mi facturas con y fin de diciembre del 2018 además 1 de enero del 2018",
    ]

    for i, phrase in enumerate(expsAcordadas + expsCasos):
        resultado = reg.seakexpresion(phrase, "fecha")
        #if resultado[1] == 0:
        print("{0}: {1} \nResultado:{2} \nEstado:{3}".format(
            i + 1, phrase, str(resultado[0]), resultado[1]))
        for tree in resultado[2]:
            print(str(tree) + "\n" + "-" * 10)
            print("\n")


    # reg = Regexseaker()
    # expr = [
    #     "Quiero facturas de estado aceptado con número de documento 33443 y el prefijo es x",
    #     "Quiero facturas de estado recibido con número de documento 33443 y el prefijo es x",
    #     "Quiero facturas de estado error con número de documento 33443 y el prefijo es x",
    #     "Quiero facturas de estado firmado con número de documento 33443 y el prefijo es x",
    #     "Quiero facturas de estado enviado con número de documento 33443 y el prefijo es x",
    #     "Quiero facturas de estado xsdsfds con número de documento 33443 y el prefijo es x",
    #     "Quiero facturas de estado 12321 con número de documento 33443 y el prefijo es x",
    #     "Quiero facturas de estado es recibido con número de documento 33443 y el prefijo es x",
    #     "Quiero facturas de estado es el que sea con número de documento 33443 y el prefijo es x",
    #     "Facturas de hoy con recibido como estado y prefijo algo",
    #     "Facturas de hoy con recibido es estado y prefijo algo",
    #     "Facturas de hoy con recibido estado y prefijo algo",
    #     "Facturas de hoy con recibido es el estado y prefijo algo"
    #     ]
    # print("\n")
    #
    # print("\n")
    # for e in expr:
    #     resultado = reg.seakexpresion(e.lower(), "Estado", nl=5)
    #     print("{0}\nEstado: {1}\n".format(e, resultado))
    # # print("NoDocumento: ", reg.seakexpresion(expr.lower(), "NoDocumento", nl=3))

    # pruebasFolios()
    # pruebasFechas()

reg = Regexseaker("SearchEngine/facturaskeys.json")
campos = [attr for attr in dir(cf) if '__' not in attr]
campos = [(getattr(cf, campo)).value for campo in campos]
campos.pop(3)
campos.pop(3)

frases = ["numero de cuenta abc345",
          "facturas de hoy",
          "notas de ayer",
          "facturas del año pasado",
          "facturas del mes pasado",
          "facturas de la semana",
          "facturas del dia",
          """Dame las facturas desde el 30 de junio del 2016 al 3 de octubre
             del 2017 con acuse rechazado prefijo igual a x numero de documento 3232
             folio inicial 3221 y folio final 21 estado cerrado, el numero de cuenta
             es ssa981 y nit adquiriente AAGR860628s4""",
          "el número de cuenta es Sad345",
          "con número de cuenta 5555",
          "cuenta con número xsa243",
          "cuenta de numero aaxr243210S01",
          "cuenta de clave 22",
          "cuenta con matrícula igual a x243421",
          "número de cuenta con número igual a aagr223455",
          "número de cuenta con 1214125 como numero",
          "cuenta 342243x",
          "la cuenta es 234342s",
          "cuenta de numero 32422a",
          "con cuenta igual a WWD224",
          "con cuenta de matricula 3424232s",
          "cuenta con numeración igual 2342211",
          "Con prefijo número 23",
          "Prefijo con matricula 1223",
          "Cuyo prefijo es werw",
          "donde se lea que el prefijo es 2a42",
          "para serie igual a x",
          "y donde el prefijo es a4",
          "y tambien con est como prefijo",
          "23a es el prefijo",
          "la serie está asignada a z443",
          "para la asignacón del prefijo tenemos al z43",
          "3343 se lee como prefijo",
          "prefijo igual a 4343",
          "prefijo ass",
          "prefijo sea x",
          "nit con clave fafafll",
          "nit con número AAGR860628S34",
          "NIT de número x243421",
          "NIT de numero aaxr243210S01",
          "adquiriente es el 3424242",
          "nit de clave 22",
          "nit adquiriente con numero igual a x243421",
          "nit adquiriente con número igual a aagr223455",
          "nit adquiriente con aaagg como numero",
          "nit con x como número",
          "nit clave aagr342243",
          "nit es 100",
          "nit x",
          "con nit igual a WWDA912122r44",
          "con nit adquiriente igual a aagr860628s34",
          "el nit adquiriente es y",
          "rfc con clave fafafll",
          "rfc con número AAGR860628S34",
          "rfc de número x243421",
          "rfc de numero aaxr243210'S01",
          "rfc de clave 22",
          "rfc adquiriente con numero igual a x243421",
          "rfc adquiriente con número igual a aagr223455",
          "rfc adquiriente con aaagg como numero",
          "rfc con x como número",
          "rfc clave aagr342243",
          "rfc es 100",
          "en donde el rfc sea x",
          "con rfc igual a WWDA912122r44",
          "con rfc adquiriente igual a aagr860628s34",
          "con 51521 como nit adquiriente",
          "6623 es el nit adquiriente",
          "x igual al nit adquiriente",
          "2 está asignado como nit",
          "el rfc adquiriente es y",
          "documento con numero x",
          "documento con número y",
          "documento de numero x",
          "documento de número 22",
          "documento con numero igual a x",
          "documento con número igual a e",
          "documento con aaagg como numero",
          "documento con x como número",
          "numero de documento es 100",
          "número de documento es 100",
          "con número de documento x",
          "con numero de documento a",
          "el numero de documento es y",
          "12 es el numero de documento",
          "factura con numero de",
          "factura con número a",
          "nota de numero x",
          "nota de número 22",
          "factura con numero igual a x",
          "factura con número igual a e",
          "crédito con aaagg como numero",
          "crédito con A3 como número",
          "número de crédito es 100",
          "numero de crédito es 100",
          "con número de crédito x",
          "con numero de crédito a",
          "el numero de la nota es y2",
          "12 es el numero de la nota",
          "matricula de documento sea casa",
          "Con número de documento número 23",
          "con número de documento al calce de 443",
          "y también con 424545 como número de documento",
          "2342545 es el número de documento",
          "el numero de documento está asignado como 34433443",
          "el numero de documento está asignado a CU",
          "el numero de documento asignado a CU",
          "para la asignacón del numero de documento tenemos al 433344343",
          "434343 se lee como numero de documento",
          "Con numero de documento 23",
          "documento cuyo numero es werwer",
          "con numero al calce de 443",
          "donde se lea que el numero es 23423542",
          "y donde el numero es 232434",
          "y tambien con 424545 como numero de documento",
          "2342545 es el numero de documento",
          "para la asignación del numero tenemos al 433344343",
          "434343 se lee como numero",
          "numero igual a 34434343",
          "numero de factura 4334433",
          "numero de facturas 1311324",
          "documento sea inicializando",
          "Dame las facturas",
	      "de tipo factura",
	      "quiero las notas",
          "quiero notas de credito con tipo de documento factura",
          "dame las notas con prefijo factura",
          "las facturas con número de documento nota",
          "dame las facturas con prefijo notas",
          "quiero las notas de credito con prefijo factura",
          "quiero las facturas que digan nota como prefijo",
          "dame los documentos facturas",
          "necesito documentos de tipo factura que sean notas",
          "Dame los documentos de tipo factura con acuse pendiente",
          "quiero las notas con estado aceptado",
          "quiero las facturas con estado abierto",
          "dame los documentos de tipo notas de credito",
          "documentos que sean facturas",
          "los documentos que sean de tipo nota",
          "los documentos que sean notas",
          "tipo de documento nota",
          "documento tipo facturas",
          "los documentos son notas",
          "documentos que son facturas",
          "el documento de tipo nota",
          "los documentos son facturas",
          "el tipo de documento es nota",
          "son facturas con prefijo nota",
          "son facturas con prefijo son notas",
          "son facturas con prefijo es nota",
          "es factura con prefijo nota",
          "es nota con prefijo la factura",
          "es nota con prefijo factura",
          "para nota con prefijo factura",
          "de nota con prefijo de factura",
          "para nota con prefijo de factura",
          "para nota con prefijo es factura",
          "para nota con prefijo factura"]

for exp in frases:
    print(exp)
    res = [reg.seakexpresion(exp, field)[0] for field in campos]
    res2 = {campo:resi for (campo, resi) in zip(campos, res) if not isinstance(resi, dict) and resi is not None}
    res3 = {campo:resi for (campo, resi) in zip(campos, res) if (isinstance(resi, dict) and all([True if val is not None else False for val in resi.values()]))}
    print(res2)
    print(res3)
    # print(["{0}: {1}".format(field, resi) for field, resi in zip(campos, res)
        #    if resi is not None])
    print("\n")

pruebasFolios()
pruebasFechas()
