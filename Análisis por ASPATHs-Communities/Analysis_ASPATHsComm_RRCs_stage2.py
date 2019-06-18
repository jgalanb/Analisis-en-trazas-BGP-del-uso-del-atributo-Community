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


def get_rango(ASes):

    ASes = ASes.split(" ")

    list_ASes = [];
    for AS in ASes:
        try:
            if int(AS) <= 65535:
                # ASes 16 bits
                if int(AS) == 0:
                    iden = '01-Reservado_0'
                elif int(AS) >= 1 and int(AS) <= 23455:
                    iden = '02-Público_16b'
                elif int(AS) == 23456:
                    iden = '03-AS_TRANS'
                elif int(AS) >= 23457 and int(AS) <= 64495:
                    iden = '02-Público_16b'
                elif int(AS) >= 64496 and int(AS) <= 64511:
                    iden = '05-Reservado_Doc_16b'
                elif int(AS) >= 64512 and int(AS) <= 65534:
                    iden = '06-Privado_16b'
                elif int(AS) == 65535:
                    iden = '07-Reservado_65535'

            elif int(AS) > 65535:
                # ASes 32 bits
                if int(AS) >= 65536 and int(AS) <= 65551:
                    iden = '08-Reservado_Doc_32b'
                elif int(AS) >= 65552 and int(AS) <= 131071:
                    iden = '09-Reservado_32b'
                elif int(AS) >= 131072 and int(AS) <= 4199999999:
                    iden = '10-Público_32b'
                elif int(AS) >= 4200000000 and int(AS) <= 4294967294:
                    iden = '11-Privado_32b'
                elif int(AS) == 4294967295:
                    iden = '12-Reservado_4294967295'
            else:
                iden = 'Unknown'

            if not iden in list_ASes:
                list_ASes.append(iden)
        except ValueError:
            pass;

    list_ASes.sort();
    list_ASes = ' '.join(list_ASes)

    return list_ASes;

"""
'get_mapea_ASes' mapeará los ASes que ponen communities y veremos si estos ASes
que ponen communities se encuetran en los ASes que forman el ASPATH:
"""
def get_mapea_ASes(ASPATH, ASes_Comm):

    ASes_ASPATH = ASPATH.split(" ")
    ASes_Comm = ASes_Comm.split(" ")

    list_mapea_ASes = [];
    for AS in ASes_Comm:
        if AS in ASes_ASPATH:
            iden = 'Matchean'
        elif not AS in ASes_ASPATH:
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

# =================================== Main() ===================================
print "Comienza la ejecución: Hora -> ", asctime(localtime());
start_time = time()

"""
Se pretende hacer una mejor identificación del rango en el cual se encuentran
aquellos ASes que forman parte del ASPATH frente a aquellos ASes que ponen communities.
Ordenar la etiquetación de los rangos.
Unicamente son considerados aquellos ASPATHs que alguna vez/(casi) siempre ven Communities.
Determinar si coinciden o no los ASes que ponen communities con los ASes del ASPATH.
"""
Header_ASPATHs = ['ASPATH_Original','RRC_ID','count_Announced','count_Announced_Comm','Pcount_Announced_Comm',\
        'Tag_count_Announced_Comm','Tag_Prep','ASPATH','long_ruta','Clasi_ASes','Communities',\
        'ASes_Comm','ASesASPATH_Comm','Hops_Comm','iden_ASes_aspath','Range_ASes_aspath',\
        'iden_ASes_comm','Range_ASes_comm','Macheo_ASes_aspath_comm']

file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_RRCs.txt'
df_aspaths = pd.read_csv(file_read, sep='|',header=None, names=Header_ASPATHs);
df_aspaths = df_aspaths[df_aspaths['Tag_count_Announced_Comm'] != 'Nunca']
print "Cantidad de ASPATHs que alguna vez/(casi) siempre ven communities: ",len(df_aspaths)
df_aspaths = df_aspaths[['ASPATH','Communities','ASes_Comm']]

well_known_comm = ['65535:0','65535:1','65535:2','65535:3','65535:4','65535:5','65535:6',\
                '65535:7','65535:8','65535:666','65535:65281','65535:65282','65535:65283',\
                '65535:65284']

add_Rango_ASes_ASPATH = [];
add_Rango_ASes_Comm = [];
add_coinciden = [];
for index, row in df_aspaths.iterrows():

    ASPATH = row.ASPATH
    Communities = row.Communities
    Communities = Communities.split(" ")
    ASes_Comm = row.ASes_Comm

    iden_ASes = get_rango(ASPATH)
    add_Rango_ASes_ASPATH.append(iden_ASes)

    S1 = set(well_known_comm)
    S2 = set(Communities)
    found = S1.intersection(S2)
    if len(found) != 0:

        list_Comm = [];
        for comm in Communities:
            if not comm in well_known_comm:
                list_Comm.append(comm)

        ASes_Comm = [];
        for comm in list_Comm:
            AS = comm.split(":")[0]
            if not AS in ASes_Comm:
                ASes_Comm.append(AS)

        ASes_Comm = ' '.join(ASes_Comm)

    iden_ASes = get_rango(ASes_Comm)
    add_Rango_ASes_Comm.append(iden_ASes)

    matcheo_ASes = get_mapea_ASes(ASPATH, ASes_Comm)
    add_coinciden.append(matcheo_ASes)

df_aspaths.insert(3,'iden_ASes_ASPATH',add_Rango_ASes_ASPATH)
df_aspaths.insert(4,'iden_ASes_Comm',add_Rango_ASes_Comm)
df_aspaths.insert(5,'Macheo_ASes_aspath_comm',add_coinciden)

df_aspaths.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_Stage2.txt',\
            sep='|',header=None, index=None)

print "Termina la ejecución: Hora -> ", asctime(localtime());
elapsed_time = time() - start_time
print("Tiempo de ejecucion: "+ str(elapsed_time))
