from os import path
from csv import reader
MODULE = "parametros"
# -*- coding: iso-8859-1 -*-

PROYECTOS = {
    "Aecid/Bid":"Banco Interamericano de Desarrollo",
    "BIRF":"BIRF",
    "Cepra":"CEPRA",
    "Focem":"FOCEM",
    "Fondos locales":"Fondos Locales",
    "Proyectos especiales":"Proyectos Especiales"
}

if __name__ == '__main__':
    LIST = open("scripts/grupos.txt", "r")
    #PRO = open("%s/fixtures/proyectos.yaml" % MODULE, "w")
    GRU = open("%s/fixtures/grupo_obra.yaml" % MODULE, "w")
    proj = []
    proy_id = 0
    group_id = 1
    LIST.next()
    rd = reader(LIST,'excel-tab')
    for arr in rd:
        print arr
        codigo, grupo, proyecto = arr[:3]
        proyecto = proyecto.strip()
        grupo = grupo.strip()
        codigo.strip()
#            if not proyecto in proj:
#                proy_id += 1
#                proj.append(proyecto)
        GRU.write("""- model: %s.Grupo
  pk: %d
  fields:
    codigo: %s
    descripcion: %s
    proyecto: %d
""" % (MODULE, group_id,
       codigo,
       grupo.decode("latin-1").encode("UTF-8"),
       int(proyecto,10)))
        group_id += 1
#    proy_id = 1
#    for pr in proj:
#        PRO.write("""- model: %s.Proyecto
#  pk: %d
#  fields:
#    nombre: %s
#    descripcion: %s
#    presupuesto: 0
#    ejecutado: 0
#    moneda: USD
#""" % (MODULE, proy_id, pr, PROYECTOS[pr].decode("latin-1").encode("UTF-8")))
#        proy_id += 1
#    PRO.close()
    GRU.close()