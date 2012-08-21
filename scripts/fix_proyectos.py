from os import path
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
    LIST = open("scripts/proyectos_grupos.txt", "r")
    PRO = open("%s/fixtures/proyectos.yaml" % MODULE, "w")
    GRU = open("%s/fixtures/grupo_obra.yaml" % MODULE, "w")
    proj = []
    proy_id = 0
    group_id = 1
    try:
        while True:
            arr = LIST.readline().strip().split("\t")
            print arr
            proyecto, grupo = arr[:2]
            proyecto = proyecto.strip()
            grupo = grupo.strip()
            if not proyecto in proj:
                proy_id += 1
                proj.append(proyecto)
            GRU.write("""- model: %s.Grupo
  pk: %d
  fields:
    nombre: %s
    descripcion: %s
    proyecto: %d
""" % (MODULE, group_id,
       grupo[:100].decode("latin-1").encode("UTF-8"),
       grupo.decode("latin-1").encode("UTF-8"),
       proy_id))
            group_id += 1
    except Exception, e:
        print e
    proy_id = 1
    for pr in proj:
        PRO.write("""- model: %s.Proyecto
  pk: %d
  fields:
    nombre: %s
    descripcion: %s
    presupuesto: 0
    ejecutado: 0
    moneda: USD
""" % (MODULE, proy_id, pr, PROYECTOS[pr].decode("latin-1").encode("UTF-8")))
        proy_id += 1
    PRO.close()
    GRU.close()