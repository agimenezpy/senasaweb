# -*- coding: iso-8859-1 -*-
from django.contrib.gis import gdal
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "senasaweb.settings"
from django.db import connection
from parametros.models import Distrito,Departamento
if os.name == "nt":
    ROOT_DIR = "Z:/Desktop/mapas/SGM/"
else:
    ROOT_DIR = "/home/agimenez/Desktop/mapas/SGM/"
MODULE = "parametros"

LOCS = ("00_Asuncion/Departamental/asunwloc.shp",
"01_Concepcion/Departamental/conceloc.shp",
"02_Sanpedro/Departamental/sanpeloc.shp",
"03_Cordillera/Departamental/cordiloc.shp",
"04_Guaira/Departamental/guairaloc.shp",
"05_Caaguazu/Departamental/caaguloc.shp",
"06_Caazapa/Departamental/caazaloc.shp",
"07_Itapua/Departamental/itapuloc.shp",
"08_Misiones/Departamental/misioloc.shp",
"09_Paraguari/Departamental/paragloc.shp",
"10_Alto_Parana/Departamental/alpaloc.shp",
"11_Central/Departamental/centraloc.shp",
r"12_Neembucu/Departamental/neeloc.shp",
"13_Amambay/Departamental/amamloc.shp",
"14_Canindeyu/Departamental/caninloc.shp",
"15_Pte_Hayes/Departamental/ptehayesloc.shp",
"16_Boqueron/Departamental/boqueloc.shp",
"17_Alto_Paraguay/Departamental/altopyloc.shp")

DISTRITOS = "Nacional/pydto.shp"
DEPARTAMENTOS = "Nacional/pydpto.shp"

def dump_file(filename,funcion,name,pk1=None,pk2=None,pk3=None,idx=0):
    fn = gdal.DataSource(filename)
    print filename
    codigo = ""
    rownum = 1
    k1,k2,k3 = None,None,None
    for row in fn[0]:
        if pk1 != None and pk1 not in row.fields:
            pk1 = False

        if pk1 == None:
            codigo = "%02d" % idx
        else:
            try:
                if pk1:
                    value = str(row.get(pk1))
                    if value:
                        value = int(value.strip(), 10)
                    else:
                        d = Departamento.objects.get(geom__contains=row.geom.geos.centroid)
                        value = d.pk
                else:
                    d = Departamento.objects.get(geom__contains=row.geom.geos.centroid)
                    value = d.pk
                k1 = value
            except Exception,e:
                print row,connection.queries[-1]['sql'],e
                value = idx
                k1 = idx
            codigo = "%02d" % value

        if pk2 != None and pk2 not in row.fields:
            pk2 = False

        if pk2 != None:
            try:
                if pk2:
                    value = str(row.get(pk2))
                    if value:
                        value = int(value.strip(), 10)
                    else:
                        g = row.geom
                        d = Distrito.objects.filter(departamento_id__exact=idx).get(geom__contains=g.geos.centroid)
                        value = int(d.pk[2:],10)
                else:
                    g = row.geom
                    d = Distrito.objects.filter(departamento_id__exact=idx).get(geom__contains=g.geos.centroid)
                    value = int(d.pk[2:], 10)
                k2 = value
            except Exception, e:
                print row,connection.queries[-1]['sql'],e
                value = rownum
                k2 = None
            codigo += "%02d" % value

        if pk3 != None and pk3 not in row.fields:
            pk3 = False

        if pk3 != None:
            if pk3:
                value = str(row.get(pk3))
                if value:
                    value = int(value.strip(), 10)
                    k3 = value
                else:
                    value = rownum
            else:
                value = rownum
            codigo += "%03d" % value
        #print row.fields
        fnams = name.split("|")
        if len(fnams) > 1:
            for itm in fnams:
                if itm in row.fields:
                    name = itm
                    break
        nombre = row.get(name)
        if not nombre:
            nombre = 'LOC %d' % rownum
        try:
            row.geom
        except:
            continue
            rownum += 1
        funcion(idx,codigo,nombre,row.geom,k1,k2,k3)
        rownum += 1

def procesar_departamento(*args,**kwargs):
    idx,codigo,nombre,geom,k1 = args[:5]
    DEP.write(r"""- model: %s.Departamento
  pk: %d
  fields:
    nombre: %s
    geom: %s
""" % (MODULE,k1,nombre.decode("latin-1").encode("UTF-8"),geom.hex))

def procesar_distrito(*args,**kwargs):
    idx,codigo,nombre,geom,k1,k2 = args[:6]
    DIST.write("""- model: %s.Distrito
  pk: '%s'
  fields:
    nombre: %s
    departamento: %s
    geom: %s
""" % (MODULE,codigo,nombre.decode("latin-1").encode("UTF-8"),k1,geom.hex))

def procesar_localidad(*args,**kwargs):
    idx,codigo,nombre,geom,k1,k2,k3 = args[:7]
    ##print k1,k2,k3,codigo,nombre#,geom
    if k1 == None:
        k1 = 0
    if k2 == None:
        k2 = 0
    LOC.write("""- model: %s.Localidad
  pk: '%s'
  fields:
    nombre: %s
    distrito: '%s'
    geom: %s
""" % (MODULE,codigo,nombre.decode("latin-1").encode("UTF-8"),"%02d%02d" % (k1,k2),geom.hex))

DEP = None
DIST = None
LOC = None

def do_dep():
    global DEP
    DEP = open('%s/fixtures/departamento.yaml' % MODULE,'w')
    dump_file(os.path.join(ROOT_DIR,DEPARTAMENTOS),procesar_departamento,"DEPARTAMEN","COD_DPTO")
    DEP.close()

def do_dist():
    global DIST
    DIST = open('%s/fixtures/distrito.yaml' % MODULE,'w')
    dump_file(os.path.join(ROOT_DIR,DISTRITOS),procesar_distrito,"DISTRITO","COD_DPTO","COD_DTO")
    DIST.close()

def do_loc():
    global LOC
    LOC = open('%s/fixtures/localidad.yaml' % MODULE,'w')
    dump_file(os.path.join(ROOT_DIR,LOCS[0]), procesar_localidad,"NOMBRE",None,None,"BARRIO",0)
    for idx in range(1, len(LOCS)):
        dump_file(os.path.join(ROOT_DIR,LOCS[idx]),procesar_localidad,"DESCLOCA|DESCLOC", "DEPARTAMEN", "DISTRITO", "BARRIO", idx)
    DEP.close()

if __name__ == "__main__":
    #do_dep()
    #do_dist()
    do_loc()
