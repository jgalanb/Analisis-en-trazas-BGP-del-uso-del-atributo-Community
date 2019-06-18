#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Importación de librerias empleadas en el codigo:
"""
import sys, re;
from os import *
import pandas as pd
import numpy as np
from time import time,localtime, asctime
import collections

""" ============================= FUNCIONES ================================ """
"""
La función 'get_tag' me volverá una etiqueta nunca/alguna vez/casi siempre/siempre
dependiendo del valor de entrada en dicha función:
"""
def get_tag(porcentaje):

    if porcentaje == 0.0:
        tag = 'Nunca';
    elif porcentaje == 100.0:
        tag = 'Siempre';
    elif porcentaje >= 90.0:
        tag = 'Casi siempre'
    else:
        tag = 'Alguna vez'

    return tag;

"""
'get_clasificacion_ASes' devolverá un string de tal forma que para cada AS que forma
el ASPATH veremos si el AS es monitor, tránsito u origen:
"""
def get_clasificacion_ASes(ASes_different):

    clasi_AS = [];
    for AS in range(0,len(ASes_different)):
        if AS == 0:
            clasificacion = ASes_different[AS] + '-Monitor'
        elif AS == len(ASes_different)-1:
            clasificacion = ASes_different[AS] + '-Origen'
        else:
            clasificacion = ASes_different[AS] + '-Transito'

        clasi_AS.append(clasificacion)

    clasificacion_ASes = ' ' + " ".join(clasi_AS) + ' '

    return clasificacion_ASes;

"""
'get_communities' devolverá un string con todas aquellas communities distintas
anunciadas bajo el ASPATH que le pasaremos como entrada a la función:
"""
def get_communities(df_aspath_comm):

    communities = [];
    list_ASescomm = [];
    for seq_communities in list(df_aspath_comm.ASesValuesComm.unique()):
        ASesValues = seq_communities.split(" ")
        for ASValue in ASesValues:
            if not ASValue in communities:
                communities.append(ASValue)

            AS = ASValue.split(":")[0]
            if not AS in list_ASescomm:
                list_ASescomm.append(AS)

    communities = " ".join(communities)
    list_ASescomm = " ".join(list_ASescomm)

    return communities,list_ASescomm;

"""
'get_ASesCommASPATH' me devolverá una lista en forma de string en donde se indiquen
aquellos ASes que ponen communities siempre y cuando estos ASes pertenezcan al ASPATH:
"""
def get_ASesCommASPATH(communities, ASes_different):

    list_ASescommASPATH = [];
    communities = communities.split(" ")
    for community in communities:
        AS = community.split(":")[0]
        if AS in ASes_different and not AS in list_ASescommASPATH:
            list_ASescommASPATH.append(AS)

    if len(list_ASescommASPATH) > 0:
        list_ASescommASPATH = ' '.join(list_ASescommASPATH)
    else:
        list_ASescommASPATH = 'No-ASescommASPATH'

    return list_ASescommASPATH;

"""
'get_hopsComm' devolverá una secuencia de strings en donde se vea si se encuentran
communities puestas a distancia '0' (es decir, puestas por el ASMonitor), a distancia
'1', '2','3', etc.
"""
def get_hopsComm(ASes_different,list_ASescomm):

    hop = 0;
    hop_comm = [];
    for AS in ASes_different:
        if AS in list_ASescomm:
            hop_comm.append(str(hop))
        hop = hop + 1;

    if len(hop_comm) > 0:
        hop_comm = " " + " ".join(hop_comm) + " "
    else:
        hop_comm = 'No-CommHops'

    return hop_comm;

"""
'get_iden_ASes_aspath' devolverá aspath público cuando todos los ASes del aspath
son de rango público, aspath privado cuando en el aspath se encuentra algún AS
de rango privado, o si en aspath se encuentra algún AS cuyo valor sea superior
al valor 65535:
"""
def get_iden_ASes_aspath(ASes_different):

    # Identificación de AS:
    AS_reserved = [0,65535]
    AS_public = range(1,64495+1)
    AS_reserved_doc = range(64496,64511+1)
    AS_privates = range(64512,65534+1)

    list_iden = [];
    list_rango = [];
    for AS in ASes_different:
        if int(AS) in AS_reserved:
            iden = 'Reservado_0_65535'
        elif int(AS) in AS_public:
            iden = 'Público'
        elif int(AS) in AS_reserved_doc:
            iden = 'Reservado_doc'
        elif int(AS) in AS_privates:
            iden = 'Privado'
        else:
            iden = 'Unknown'

        if not iden in list_iden:
            list_iden.append(iden)

        if int(AS) < 65535:
            rango = 'AS < 65535'
        elif int(AS) > 65535:
            rango = 'AS > 65535'
        else:
            rango = 'Unknown'

        if not rango in list_rango:
            list_rango.append(rango)

    iden = ' '.join(list_iden)
    rango = ' '.join(list_rango)

    return iden,rango;

"""
'get_iden_ASes_comm' devolverá AS público cuando todos los ASes que ponen communities
son de rango público, AS privado cuando se encuentra algún AS que pone communities
de rango privado, o se encuentra algún AS cuyo valor sea superior al valor 65535:
"""
def get_iden_ASes_comm(communities):

    # Identificación de AS:
    AS_reserved = [0,65535]
    AS_public = range(1,64495+1)
    AS_reserved_doc = range(64496,64511+1)
    AS_privates = range(64512,65534+1)

    communities = communities.split(" ")

    list_iden = [];
    list_rango = [];
    for community in communities:
        try:
            AS = int(community.split(":")[0])
        except ValueError:
            print community;
            print ""
            continue;

        if int(AS) in AS_reserved:
            iden = 'Reservado_0_65535'
        elif int(AS) in AS_public:
            iden = 'Público'
        elif int(AS) in AS_reserved_doc:
            iden = 'Reservado_doc'
        elif int(AS) in AS_privates:
            iden = 'Privado'
        else:
            iden = 'Unknown'

        if not iden in list_iden:
            list_iden.append(iden)

        if int(AS) < 65535:
            rango = 'AS < 65535'
        elif int(AS) > 65535:
            rango = 'AS > 65535'
        else:
            rango = 'Unknown'

        if not rango in list_rango:
            list_rango.append(rango)

    iden = ' '.join(list_iden)
    rango = ' '.join(list_rango)

    return iden,rango;

"""
'get_mapea_ASes' mapeará los ASes que ponen communities y veremos si estos ASes
que ponen communities se encuetran en los ASes que forman el ASPATH:
"""
def get_mapea_ASes(communities, ASes_different):

    communities = communities.split(" ")

    list_mapea_ASes = [];
    for community in communities:
        AS = community.split(":")[0]
        if AS in ASes_different:
            iden = 'Matchean'
        elif not AS in ASes_different:
            iden = 'No matchean'
        else:
            iden = 'Unknown'

        if not iden in list_mapea_ASes:
            list_mapea_ASes.append(iden)

    if len(list_mapea_ASes) == 1:
        mapea_ASes = list_mapea_ASes[0]
    elif len(list_mapea_ASes) == 2:
        if 'Matchean' in list_mapea_ASes and 'No matchean' in list_mapea_ASes:
            mapea_ASes = 'Alguna vez matchean'
        else:
            mapea_ASes = 'Unknown'
    else:
        mapea_ASes = 'Unknown'

    return mapea_ASes;

"""
La función 'info_aspath' devolverá la siguiente información para cada ASPATH distinto
encontrado en el dataframe pasado como entrada a la función:
    - ASPATH
    - Colector donde se anuncia este ASPATH
    - Número de anuncios bajo este ASPATH
    - Número de anuncios con atributos communities
    - Porcentaje de anuncios con atributo communities
    - Tag 'nunca/alguna vez/(casi) siempre' ve communities
    - Tag que indica si en el ASPATH existe Prepending
    - ASPATH sin prepeding (en caso de no tenerlo dejar el ASPATH original)
    - Longitud del ASPATH/ruta
    - Clasificar cada AS del ASPATH: monitor, tránsito u origen
    - Communities distintas anunciadas bajo el ASPATH
    - Lista de ASes que ponen communities bajo el ASPATH
    - Lista de ASes que ponen communities y que están en el ASPATH
    - Saltos en el ASPATH a los cuales el monitor encuentra communities
    - Salto más cercano para el cual veo communities
    - ASPATH con ASes públicos, privados o por encima del AS 65535
    - Communities puestas por ASes públicos, privados o por encima del valor 65535
    - Mapear ASes que ponen communities con los ASes del ASPATH
"""
def info_aspath(df_collector,rrc):

    # Obtenemos la lista de todos aquellos ASPATHs distintos en el colector de entrada:
    # (Agrupamos por ASPATH)
    ASPATHS = list(df_collector.ASPATH.unique())
    df_ASPATHS = df_collector.groupby('ASPATH')

    data_aspath = {};
    for aspath in ASPATHS:
        info_aspath = [];
        # Generamos df con la información para dicho ASPATH:
        df_aspath = df_ASPATHS.get_group(aspath)

        # Colector al que pertenece este ASPATH:
        id_rrc = rrc.split(".")[0]
        info_aspath.append(id_rrc)

        # Número de anuncios bajo este ASPATH:
        count_Announced = len(df_aspath)
        info_aspath.append(count_Announced)

        # Numero de anuncios con communities:
        df_aspath_comm = df_aspath[df_aspath['ASesValuesComm'] != '-']
        count_Announced_Comm = len(df_aspath_comm)
        info_aspath.append(count_Announced_Comm)

        # Porcentaje de anuncios con communities bajo este ASPATH:
        try:
            porcentaje_comm = float(float(count_Announced_Comm)/(float(count_Announced)))
            porcentaje_comm = float(porcentaje_comm)*float(100)
            porcentaje_comm_str = "{0:.3f}".format(porcentaje_comm)
        except ZeroDivisionError:
            porcentaje_comm = 0.0;
            porcentaje_comm_str = "{0:.3f}".format(porcentaje_comm)

        info_aspath.append(porcentaje_comm_str)

        # Etiqueto el resultado obtenido:
        tag = get_tag(porcentaje_comm)
        info_aspath.append(tag)

        # Determinar si se está haciendo ASPATHPrep:
        ASes = aspath.split(" ")
        ASes_total = [];
        ASes_different = [];
        for AS in ASes:
            ASes_total.append(AS)
            if not AS in ASes_different:
                ASes_different.append(AS)

        if len(ASes_different) < len(ASes_total):
            aspath_prep = 'Prepending';
            aspath_diff = " ".join(ASes_different)
        elif len(ASes_different) == len(ASes_total):
            aspath_prep = 'No-Prepeding';
            aspath_diff = aspath;
        else:
            print "Mmmm... prepeding..."
            sys.exit();

        info_aspath.append(aspath_prep)
        info_aspath.append(aspath_diff)

        # ¿Cuanto es la longitud de la ruta (sin considerar Prepending)?
        info_aspath.append(len(ASes_different))

        # Clasificar cada AS del ASPATH: monitor, tránsito u origen
        clasificacion_ASes = get_clasificacion_ASes(ASes_different)
        info_aspath.append(clasificacion_ASes)

        # Communities distintas anunciadas bajo el ASPATH:
        # Lista de ASes que ponen communities:
        if count_Announced_Comm != 0:
            communities,list_ASescomm = get_communities(df_aspath_comm)
            info_aspath.append(communities)
            info_aspath.append(list_ASescomm)
        else:
            info_aspath.append('No-Communities')
            info_aspath.append('No-Communities')

        # Lista de ASes que ponen communities y están en el ASPATH:
        if count_Announced_Comm != 0:
            list_ASescommASPATH = get_ASesCommASPATH(communities, ASes_different)
            info_aspath.append(list_ASescommASPATH)
        else:
            info_aspath.append('No-Communities')

        # De los ASes que forman el ASPATH, ¿cuantos han puesto communities?
        if count_Announced_Comm != 0:
            hops_comm = get_hopsComm(ASes_different,list_ASescomm)
            info_aspath.append(hops_comm)
        else:
            info_aspath.append('No-Communities')

        # ASPATH con ASes públicos, privados o por encima del AS 65535:
        iden_ASes_aspath,rango = get_iden_ASes_aspath(ASes_different)
        info_aspath.append(iden_ASes_aspath)
        info_aspath.append(rango)

        # Communities puestas por ASes públicos, privados o por encima del valor 65535:
        if count_Announced_Comm != 0:
            iden_ASes_comm,rango = get_iden_ASes_comm(communities)
            info_aspath.append(iden_ASes_comm)
            info_aspath.append(rango)
        else:
            info_aspath.append('No-Communities')
            info_aspath.append('No-Communities')

        # Mapear ASes que ponen communities con los ASes del ASPATH:
        if count_Announced_Comm != 0:
            mapea_ASes = get_mapea_ASes(communities, ASes_different)
            info_aspath.append(mapea_ASes)
        else:
            info_aspath.append('No-Communities')

        data_aspath.update({aspath:info_aspath})

    return data_aspath;

# =================================== Main() ===================================
print "Comienza la ejecución: Hora -> ", asctime(localtime());
start_time = time()

# rrcs = ['rrc00.ripe','rrc01.ripe','rrc03.ripe','rrc04.ripe','rrc05.ripe','rrc06.ripe',\
#         'rrc07.ripe','rrc10.ripe','rrc11.ripe','rrc12.ripe','rrc13.ripe','rrc14.ripe',\
#         'rrc15.ripe','rrc16.ripe','rrc18.ripe','rrc19.ripe','rrc20.ripe','rrc21.ripe']

rrcs = ['rrc11.ripe','rrc12.ripe','rrc13.ripe','rrc14.ripe',\
        'rrc15.ripe','rrc16.ripe','rrc18.ripe','rrc19.ripe','rrc20.ripe','rrc21.ripe']

Header = ['RRC_ID','ABW','IPMonitor','ASMonitor','AnnouncedPrefix',\
        'IPType','ASPATH','Neighbor','Communities','Large_Communities',\
        'ASesValuesComm','ASesComm'];

for rrc in rrcs:
    print rrc
    file_read = '/srv/agarcia/TFM-BGP/Jesus/DATA/'+rrc+'.txt'
    df_collector = pd.read_csv(file_read, sep='|',header=None, names=Header, dtype={"Neighbor": object});

    """
    Analizar cada uno de los ASPATHs distintos y sus communities anunciadas bajo el ASPATH
    encontrados en cada uno de los colectores:
    """
    data_aspath = info_aspath(df_collector,rrc)
    df_aspaths = pd.DataFrame.from_dict(data_aspath,orient='index')
    df_aspaths.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_'+rrc+'.txt',\
                sep='|',header=None, index=True)

# Unifico la información obtenida de cada uno de los colectores:
print 'Unir los datos de los colectores en un unico fichero txt:'
rrcs = ['rrc00.ripe','rrc01.ripe','rrc03.ripe','rrc04.ripe','rrc05.ripe','rrc06.ripe',\
        'rrc07.ripe','rrc10.ripe','rrc11.ripe','rrc12.ripe','rrc13.ripe','rrc14.ripe',\
        'rrc15.ripe','rrc16.ripe','rrc18.ripe','rrc19.ripe','rrc20.ripe','rrc21.ripe']

Header_ASPATHs = ['ASPATH_Original','RRC_ID','count_Announced','count_Announced_Comm','Pcount_Announced_Comm',\
        'Tag_count_Announced_Comm','Tag_Prep','ASPATH','long_ruta','Clasi_ASes','Communities',\
        'ASes_Comm','ASesASPATH_Comm','Hops_Comm','iden_ASes_aspath','Range_ASes_aspath',\
        'iden_ASes_comm','Range_ASes_comm','Macheo_ASes_aspath_comm']

df_global = pd.DataFrame([], columns = Header_ASPATHs)
for rrc in rrcs:
    print rrc
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_'+rrc+'.txt'
    df_rrc = pd.read_csv(file_read, sep='|',header=None, names=Header_ASPATHs);

    # Añado la información al df general:
    df_global = df_global.append(df_rrc, sort=False)

# Guardamos el dataframe como txt:
df_global.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_RRCs.txt',\
                    sep='|',header=None, index=None)

print "Termina la ejecución: Hora -> ", asctime(localtime());
elapsed_time = time() - start_time
print("Tiempo de ejecucion: "+ str(elapsed_time))
