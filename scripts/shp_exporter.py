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

def dump_file(filename,funcion,name,pk1=None,pk2=None,pk3=None,idx=0,fpath=""):
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
                        value = int(d.codigo,10)
                else:
                    d = Departamento.objects.get(geom__contains=row.geom.geos.centroid)
                    value = int(d.codigo,10)
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
                        d = Distrito.objects.filter(departamento_id__exact="%02d" % idx).get(geom__contains=g.geos.centroid)
                        value = int(d.codigo[2:],10)
                else:
                    g = row.geom
                    d = Distrito.objects.filter(departamento_id__exact="%02d" % idx).get(geom__contains=g.geos.centroid)
                    value = int(d.codigo[2:], 10)
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
        funcion(idx,codigo,nombre,row.geom,k1,k2,k3,fpath=fpath,fid=row.fid)
        rownum += 1

def procesar_departamento(*args,**kwargs):
    idx,codigo,nombre,geom,k1 = args[:5]
    DEP.write(r"""- model: %s.Departamento
  pk:
  fields:
    codigo: '%s'
    nombre: %s
    geom: %s
""" % (MODULE,"%02d" % k1,nombre.decode("latin-1").encode("UTF-8"),geom.hex))
    CSV.write("DEPARTAMENTO\t%s\t%s\t%s\t%d\t%s\t\n" % ("%02d" % k1,nombre,"",kwargs["fid"],kwargs["fpath"]))

def procesar_distrito(*args,**kwargs):
    idx,codigo,nombre,geom,k1,k2 = args[:6]
    DIST.write("""- model: %s.Distrito
  pk:
  fields:
    codigo: '%s'
    nombre: %s
    departamento: '%s'
    geom: %s
""" % (MODULE,codigo,nombre.decode("latin-1").encode("UTF-8"),"%02d" % k1,geom.hex))
    CSV.write("DISTRITO\t%s\t%s\t%s\t%d\t%s\t\n" % (codigo,nombre,"%02d" % k1,kwargs["fid"],kwargs["fpath"]))

def procesar_localidad(*args,**kwargs):
    idx,codigo,nombre,geom,k1,k2,k3 = args[:7]
    ##print k1,k2,k3,codigo,nombre#,geom
    if geom.geom_type != 'Polygon':
        #print k1,k2,k3,codigo,nombre,geom.geom_count,[geom[i].area for i in range(0, geom.geom_count)]
        marea = max([geom[i].area for i in range(0, geom.geom_count)])
        geom = filter(lambda it: it.area == marea, geom)[0]
#        locs = ""
#        for  i in range(0, geom.geom_count):
#            locs += "<gml:featureMember fid='%d'>%s</gml:featureMember>\n" % (i, geom[i].gml)
#        tf = open(ROOT_DIR + "/tmp/" + codigo + ".gml", "w")
#        tf.write("""<?xml version="1.0" encoding="UTF-8"?>
#<gml:FeatureCollection xmlns:gml="http://www.opengis.net/gml">
#%s
#</gml:FeatureCollection>
#            """ % locs)
        #tf.close()
    if k1 == None:
        k1 = 0
    if k2 == None:
        k2 = 0
    LOC.write("""- model: %s.Localidad
  pk:
  fields:
    codigo: '%s'
    nombre: %s
    distrito: '%s'
    geom: %s
""" % (MODULE,codigo,nombre.decode("latin-1").encode("UTF-8"),"%02d%02d" % (k1,k2),geom.hex))
    CSV.write("LOCALIDAD\t%s\t%s\t%s\t%d\t%s\tRURAL\n" % (codigo,nombre,"%02d%02d" % (k1,k2),kwargs["fid"],kwargs["fpath"]))

DEP = None
DIST = None
LOC = None
CSV = None

def do_dep():
    global DEP
    global CSV
    CSV = open("scripts/division_politica.csv","w")
    DEP = open('%s/fixtures/departamento.yaml' % MODULE,'w')
    dump_file(os.path.join(ROOT_DIR,DEPARTAMENTOS),procesar_departamento,"DEPARTAMEN","COD_DPTO",fpath=DEPARTAMENTOS)
    DEP.close()
    CSV.close()

def do_dist():
    global DIST
    global CSV
    CSV = open("scripts/division_politica.csv","a")
    DIST = open('%s/fixtures/distrito.yaml' % MODULE,'w')
    dump_file(os.path.join(ROOT_DIR,DISTRITOS),procesar_distrito,"DISTRITO","COD_DPTO","COD_DTO",fpath=DISTRITOS)
    DIST.close()
    CSV.close()

def do_loc():
    global LOC
    global CSV
    CSV = open("scripts/division_politica.csv","a")
    LOC = open('%s/fixtures/localidad.yaml' % MODULE,'w')
    dump_file(os.path.join(ROOT_DIR,LOCS[0]), procesar_localidad,"NOMBRE",None,None,"BARRIO",0,fpath=LOCS[0])
    for idx in range(1, len(LOCS)):
        dump_file(os.path.join(ROOT_DIR,LOCS[idx]),procesar_localidad,"DESCLOCA|DESCLOC", "DEPARTAMEN", "DISTRITO", "BARRIO", idx,fpath=LOCS[idx])
    LOC.close()
    CSV.close()

if __name__ == "__main__":
    do_dep()
    do_dist()
    do_loc()
