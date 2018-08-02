from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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
