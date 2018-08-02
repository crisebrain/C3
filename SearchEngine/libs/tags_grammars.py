def choose_grammar(field, cg, cf):
    dgramm = {cf.PREFIJO.value: r""" Q: {<dato|Nums|unknown|(nc[fm][sp]000)|Singlel>}
                                     AUX1 : {<vmip1p0> <spcms|cs>}
                                     AUX2 : {<spcms> <Calce> <sps00>}
                                     AUX3 : {<aq0cs0> <sps00|spcms>}
                                     AUX4 : {<p0300000> <vmip3s0> <cs>}
                                     AUX5 : {<vmip3s0>? <Asignar> <sps00|cs>}
                                     AUX6 : {<vsip3s0|vssp3s0|cs> <da0ms0>?}
                                     AUX : {<AUX1|AUX2|AUX3|AUX4|AUX5|AUX6>}
                                     NP: {<%(sg)s> <AUX|sps00|da0ms0>? <Sustnum>? <Q|sps00>}
                                     NP: {<Q|sps00|vsip3s0> <AUX> <%(sg)s>}
                                 """  % {'sg': cf.PREFIJO.value},
              cf.NO_DOCUMENTO.value: r""" Q: {<Singlel|cc|dato|Nums|(nc[mf][sp]000)>}
                                          AUX1 : {<vmip1p0> <spcms|cs>}
                                          AUX2 : {<spcms> <Calce> <sps00>}
                                          AUX3 : {<aq0cs0> <sps00|spcms>}
                                          AUX4 : {<p0300000> <vmip3s0> <cs>}
                                          AUX5 : {<vmip3s0>? <Asignar> <sps00|cs>}
                                          AUX6 : {<vsip3s0|vssp3s0|cs> <da0ms0>?}
                                          AUX : {<AUX1|AUX2|AUX3|AUX4|AUX5|AUX6>}
                                          NP: {<Sustnum> <sps00> <da0fs0>? <%(sg)s> <AUX|Sustnum>? <Q|sps00>}
                                          NP: {<%(sg)s> <sps00|Pronrelativo> <Sustnum> <AUX>? <Q|sps00>}
                                          NP: {<%(sg)s> <sps00> <Q|sps00> <AUX> <Sustnum>}
                                          NP: {<Q> <AUX> <Sustnum> <sps00> <da0fs0>? <%(sg)s>}
                                      """ % {'sg': cf.NO_DOCUMENTO.value},
              cf.NIT.value: r""" Q: {<unknown|dato|Z|Singlel|datoNitCol>}
                                 AUX1 : {<vmip1p0> <spcms|cs>}
                                 AUX2 : {<aq0cs0> <sps00|spcms>}
                                 AUX3 : {<vmip3s0>? <Asignar> <sps00|cs>}
                                 AUX4 : {<vsip3s0|vssp3s0|cs> <da0ms0>?}
                                 AUX: {<AUX1|AUX2|AUX3|AUX4>}
                                 NP: {<%(sg)s> <%(sg)s>? <sps00> <Sustnum> <AUX>? <Q|cc>}
                                 NP: {<%(sg)s> <%(sg)s>? <sps00> <Q> <AUX> <Sustnum>}
                                 NP: {<%(sg)s> <%(sg)s>? <AUX|sps00> <Q|cc>}
                                 NP: {<%(sg)s> <%(sg)s>? <Sustnum|(vs\w+)>? <da0ms0>? <Q|cc>}
                                 NP: {<Q> <AUX> <%(sg)s> <%(sg)s>?}
                             """ % {'sg': cf.NIT.value},
              cf.CUENTA.value: r""" Q: {<unknown|dato|Z|Singlel>}
                                    NP: {<%(sg)s> <sps00>? <Sustnum>? (<aq0cs0|sps00|Es>){0,2} <Q>}
                                    NP: {<(da0\w+)>? <Sustnum>? <sps00|da0fs0>? <%(sg)s> <(vs\w+)>? <Q>}
                                    NP: {<Sustnum> <sps00> <%(sg)s> <sps00> <Sustnum> <aq0cs0> <sps00> <Q>}
                                    NP: {<Sustnum> <sps00> <%(sg)s> <sps00> <Q> <cs> <Sustnum>}
                                    NP: {<sps00> <%(sg)s> <aq0cs0> <sps00> <Q>}
                                """ % {'sg': cf.CUENTA.value},
              cf.STATUS.value: r""" Q: {<Recibido|Error|Firmado|Rechazado|Aceptado|Enviado>}
                                    NP: {<%(sg)s> <vssp3s0|sps00|vsis3s0|Es|Valor|da0ms0|cs>{0,3} <Q>}
                                    NP: {<Q> <vssp3s0|sps00|vsis3s0|Es|Valor|da0ms0|cs>{1,3} <%(sg)s>}
                                    NP: {<%(sg)s> <vssp3s0|sps00|vsis3s0|Es|Valor|da0ms0|cs>{0,3} <.*>}
                                    NP: {<.*> <vssp3s0|sps00|vsis3s0|Es|Valor|da0ms0|cs>{1,3} <%(sg)s>}
                                """ % {'sg': cf.STATUS.value},
              cf.ACUSE.value: r""" Q: {<Rechazado|Aceptado|Pendiente>}
                                   NP: {<%(sg)s> <vssp3s0|sps00|vsis3s0|Es|Valor|da0ms0|cs>{0,3} <Q>}
                                   NP: {<Q> <vssp3s0|vsis3s0|Es|da0ms0|cs>{1,3} <%(sg)s>}
                                   NP: {<%(sg)s> <vssp3s0|sps00|vsis3s0|Es|Valor|da0ms0|cs>{0,3} <.*>}
                                   NP: {<.*> <vssp3s0|vsis3s0|Es|da0ms0|cs>{1,3} <%(sg)s>}
                               """ % {'sg': cf.ACUSE.value},
              "Folio": r""" Q: {<Es|sps00|da0ms0|unknown|Valor|cs|cc|Reciente|p0300000|dp1msp|spcms|dp1css>}
                            NP: {<Folio> <Q>{0,3} (<tipoFolio> <Q|Prefijo>*){1,2} <dato>}
                            NP: {<Folio> <Q>{0,3} (<dato> <Q|Prefijo>*){1,2} <tipoFolio>}
                            NP: {<dato> <Q>{1,3} <Folio> <Q>{0,3} <tipoFolio>}
                            NP: {<tipoFolio> <Q>{1,3} <Folio> <Q>{0,3} <dato>}

                            NP: {<Folio> <Q>{0,3} (<tipoFolio> <Q|Prefijo>*){1,2} <.*>}
                            NP: {<.*> <Q>{1,3} <Folio> <Q>{0,3} <tipoFolio>}
                            NP: {<tipoFolio> <Q>{1,3} <Folio> <Q>{0,3} <.*>}
                        """,
              cf.PERIODO.value: r""" DP: {<semana|dia|mes|año>}
                                     NP1: {<presente|pasado> <DP>}
                                     NP2: {<DP> <sps00>? <presente|pasado>}
                                     NP3: {<sps00> <presente|pasado>}
                                     NP4: {<spcms|da0fs0|%(sg)s> <DP>}
                                 """ % {'sg': cf.PERIODO.value},
              cf.TIPO_DOCUMENTO.value: r""" Q: {<TFactura|TNota>}
                                            NP: {<%(sg)s> <sps00> <TDocumento> <pr0cn000>? <(vs\w+)>? <Q>}
                                            NP: {<TDocumento>? <pr0cn000>? <(vs\w+)>? <sps00>? <%(sg)s> <Q>}
                                            NP: {<TDocumento> <pr0cn000>? <(vs\w+)>? <Q>}
                                            NP: {<Imperativo|vmip1s0|Requiero> <(da0\w+)|dp1c[p|s]s>? <Q> <sps00>? <TCredito>?}
                                            NP: {<(da0\w+)|(vs\w+)|sps00> <Q>}
                                                }<prefijo> <(vs\w+)|sps00>?{
                                            NP: {<%(sg)s> <sps00> <TDocumento> <pr0cn000>? <(vs\w+)>? <(.*)>}
                                            NP: {<TDocumento>? <pr0cn000>? <(vs\w+)>? <sps00>? <%(sg)s> <(.*)>}
                                            NP: {<Q> <sps00>? <TCredito>?}
                                                }(<prefijo> <Q>)|(<prefijo> <Q> <sps00>? <TCredito>?){
                                        """ % {'sg': cf.TIPO_DOCUMENTO.value},
              cf.FECHA.value: r""" Q: {<De|Articulos|spcms|sps00|Es>}
                                   I: {<Inicio|Fin> <Q>{0,2} <sps00>?}
                                   NP: {<I>? <DiasNum|ao0ms0> <Q>{0,2} <%(sg)s> <Q>{0,2} <AniosNum>?}
                                   NP: {<I>? <%(sg)s> <Q>{0,2} <DiasNum|ao0ms0> <Q>{0,2} <AniosNum>?}
                                   NP: {<I>? <%(sg)s> <Q>{0,2} <AniosNum>}
                                   NP: {<I>? <%(sg)s>}
                               """ % {'sg': cf.FECHA.value}
             }
    return dgramm[field]

def get_posibles(field, cg, cf):
    if field in [cf.PREFIJO.value, cf.NO_DOCUMENTO.value,
                 cf.NIT.value, cf.CUENTA.value]:
        return ['Fz', 'Y', 'Z', 'cc', 'dato', 'nccn000', "ncms000",
                'ncfs000', 'sps00', 'Singlel', 'unknown', "Nums", "Es"]
    elif field == "Folio":
        return ['Fz', 'Y', 'Z', 'cc', 'dato', 'nccn000', "ncms000",
                'ncfs000', 'Singlel', 'unknown', "Nums", "aq0ms0"]
    elif field in [cf.STATUS.value, cf.ACUSE.value]:
        return ["dato", "vmp00sm", "ncms000", "aq0msp", "unknown", "Fz", "Y"
                "Z", "cc"]
    elif field == cf.TIPO_DOCUMENTO.value:
        return ['Fz', 'Y', 'Z', 'cc', 'dato', 'nccn000', "ncms000",
                'ncfs000', 'sps00', 'Singlel', 'unknown', "Nums", "Es"]
    elif field == cf.FECHA.value:
        return [cf.FECHA.value, "AniosNum", "DiasNum", "Inicio", "Fin"]

def get_tags(field, cg, cf):
    if field == cf.PREFIJO.value:
        return ["Singlel", "Calce", "Asignar", "Sustnum"]
    elif field == cf.NO_DOCUMENTO.value:
        return ["Singlel", "Inicio", "Sustnum", cf.PREFIJO.value, 'Folio',
                "Fin", 'Valor', 'Reciente', cf.STATUS.value, 'Recibido',
                'Error', 'Firmado', 'Rechazado', 'Aceptado', 'Enviado',
                'Pendiente', cf.ACUSE.value, "Pronrelativo", "Calce",
                "Asignar"]
    elif field == cf.NIT.value:
        return ["Singlel", "Sustnum", "Asignar", "Calce"]
    elif field == cf.CUENTA.value:
        return ["Singlel", "Sustnum"]
    elif field == "Folio":
        return ["Inicio", "Fin", "Es", "Valor", cf.PREFIJO.value, "Reciente"]
    elif field == cf.STATUS.value:
        return ["Es", "Valor", cg.RECIBIDO.value, cg.ERROR.value,
                cg.FIRMADO.value, cg.RECHAZADO.value, cg.ACEPTADO.value,
                cg.ENVIADO.value, "Factura"]
    elif field == cf.ACUSE.value:
        return ["Es", "Valor", cg.RECHAZADO.value, cg.ACEPTADO.value,
                cg.PENDIENTE.value]
    elif field == cf.PERIODO.value:
        return ["pasado", "presente", "semana", "dia", "mes", "año"]
    elif field == cf.TIPO_DOCUMENTO.value:
        return [cf.PREFIJO.value, cf.NO_DOCUMENTO.value, "Sustnum",
                "Requiero", "Imperativo", "TDocumento", "TFactura",
                "TNota", "TCredito"]
    elif field == cf.FECHA.value:
        return  ["Inicio", "De", "Es", "Fin", "Articulos"]

def regex_taglist(field, cg, cf):
    if field == cf.NIT.value:
        return ["datoNitCol"]
    elif field == cf.NO_DOCUMENTO.value:
        return ["Nums"]
    elif field == cf.PREFIJO.value:
        return ["Nums"]
    elif field == cf.FECHA.value:
        return ["AniosNum", "DiasNum"]
    else:
        return []
