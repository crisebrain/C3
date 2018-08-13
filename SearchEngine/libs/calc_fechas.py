from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def preparaFechas(entity, cf):
    import datetime
    from datetime import date

    def buildDate(fechaDic):
        diasNum = {
            "primero": 1,
            "segundo": 2,
            "tercero": 3,
            "cuarto": 4,
            "quinto": 5,
            "sexto": 6,
            "séptimo": 7,
            "octavo": 8,
            "noveno": 9
        }

        y = today.year if fechaDic.get("AniosNum") is None else int(fechaDic["AniosNum"])
        m = today.month if fechaDic.get(cf.FECHA.value) is None else fechaDic[cf.FECHA.value]
        m = numberMonth[m]

        d = fechaDic.get("DiasNum")
        if d is None:
            d = 1
        elif d in diasNum:
            d = diasNum[d]
        else:
            d = int(d)

        # Establece la fecha al día, si no se puede la corrige.
        try:
            date = datetime.date(y, m, d)
            statusCode = 1
        except ValueError:
            date = datetime.date(y, m, 1)
            statusCode = 0  # Establece código

        # Evalúamos años posteriores
        if date.year > today.year:
            date = date.replace(year=today.year)

        return date, statusCode

    def selectCaseDate():
        nonlocal fechaInicio, fechaFin, fechaEspecifica, firstSpecificDate

        if not firstSpecificDate:
            # Caso 1: dan fecha fin, pero no de inicio.
            if fechaFin and fechaInicio is None:
            # if "fechaFin" in dicDates and not "fechaInicio" in dicDates:
                fechaInicio = None, 1
            # Caso 2: dan fecha de inicio, pero no de fin
            elif fechaInicio and fechaFin is None:
            # elif "fechaInicio" in dicDates and not "fechaFin" in dicDates:
                fechaFin = today, 1
        else:
            # Caso 3: fecha específica
            fechaInicio = fechaEspecifica
            fechaFin = fechaEspecifica

    def orderDate():
        nonlocal  fechaFin, fechaInicio

        # Validamos que existan las fechas y las ordenamos.
        if fechaInicio[0] and fechaFin[0] and \
                fechaFin[0] < fechaInicio[0]:
            dateSwap = fechaInicio
            fechaInicio = fechaFin
            fechaFin = dateSwap

    fechaFin = None
    fechaInicio = None
    fechaEspecifica = None
    firstSpecificDate = False
    today = date.today()
    numberMonth = {
        "enero": 1,
        "febrero": 2,
        "marzo": 3,
        "abril": 4,
        "mayo": 5,
        "junio": 6,
        "julio": 7,
        "agosto": 8,
        "septiembre": 9,
        "octubre": 10,
        "noviembre": 11,
        "diciembre": 12
    }

    if len(entity) == 0:
        statusCode = 1
        fechaInicio = [None]
        fechaFin = [None]
    else:
        # Obtenemos fechas de las Entitys
        # Invertimos para interar desde el último elemento.
        entity.reverse()
        for fecha in entity:
            if "Fin" in fecha and fechaFin is None:
                fechaFin = buildDate(fecha)
            elif "Inicio" in fecha and fechaInicio is None:
                fechaInicio = buildDate(fecha)
            elif fechaEspecifica is None:
                # Validamos si fecha específica fue la primera en ocurrir.
                if fechaInicio is None and fechaFin is None:
                    firstSpecificDate = True
                fechaEspecifica = buildDate(fecha)

        selectCaseDate()
        orderDate()

        # Evalúa código final
        statusCode = 0
        if fechaInicio[1] and fechaFin[1]:
            statusCode = 1
    result = [value.strftime("%Y-%m-%d") if value is not None else value
              for value in [fechaInicio[0], fechaFin[0]]]

    return (dict(zip([cf.FECHA_INICIAL.value, cf.FECHA_FINAL.value],
                     result)), statusCode)


def time_period(period, cf):
    result = {cf.FECHA_INICIAL.value: None, cf.FECHA_FINAL.value: None}
    if period["interval"] == 1 and period["time"] == 0:
        result[cf.FECHA_INICIAL.value] = datetime.now().date()
        result[cf.FECHA_FINAL.value] = datetime.now().date()
    if period["interval"] == 1 and period["time"] == 1:
        timed = timedelta(days=1)
        result[cf.FECHA_INICIAL.value] = (datetime.now() - timed).date()
        result[cf.FECHA_FINAL.value] = datetime.now().date()
    if period["interval"] == 2 and period["time"] == 0:
        diacorriente = datetime.isoweekday(datetime.now())
        timed = timedelta(days=diacorriente)
        result[cf.FECHA_INICIAL.value] = (datetime.now() - timed).date()
        result[cf.FECHA_FINAL.value] = datetime.now().date()
    if period["interval"] == 2 and period["time"] == 1:
        diacorriente = datetime.isoweekday(datetime.now())
        timed = timedelta(days=diacorriente+7)
        result[cf.FECHA_INICIAL.value] = (datetime.now() - timed).date()
        result[cf.FECHA_FINAL.value] = result[cf.FECHA_INICIAL.value]
        result[cf.FECHA_FINAL.value] += timedelta(days=6)
    if period["interval"] == 3 and period["time"] == 0:
        diames = datetime.now().day - 1
        timed = timedelta(days=diames)
        result[cf.FECHA_INICIAL.value] = (datetime.now() - timed).date()
        result[cf.FECHA_FINAL.value] = datetime.now().date()
    if period["interval"] == 3 and period["time"] == 1:
        diames = datetime.now().day - 1
        rdelta = relativedelta(months=1)
        primero = datetime.now() - timedelta(days=diames) - rdelta
        result[cf.FECHA_INICIAL.value] = primero.date()
        timed = timedelta(days=diames + 1)
        result[cf.FECHA_FINAL.value] = (datetime.now() - timed).date()
    if period["interval"] == 4 and period["time"] == 0:
        year, weeks, weekday = datetime.isocalendar(datetime.now())
        timed = timedelta(weeks=weeks-1, days=weekday - 1)
        result[cf.FECHA_INICIAL.value] = (datetime.now() - timed).date()
        result[cf.FECHA_FINAL.value] = datetime.now().date()
    if period["interval"] == 4 and period["time"] == 1:
        year, weeks, weekday = datetime.isocalendar(datetime.now())
        rdelta = relativedelta(weeks=weeks-1, days=weekday - 1, years=1)
        result[cf.FECHA_INICIAL.value] = (datetime.now() - rdelta).date()
        rdelta2 = relativedelta(days=364)
        result[cf.FECHA_FINAL.value] = result[cf.FECHA_INICIAL.value]
        result[cf.FECHA_FINAL.value] += rdelta2
    for key, value in result.items():
        if value is not None:
            result[key] = value.strftime("%Y-%m-%d")
    return result
