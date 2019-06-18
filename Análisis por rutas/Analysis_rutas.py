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
'get_max_hop' devolverá a qué distancia máximo espero ver communities puestas por
los ASes que forman parte de la ruta, en función de la longitud de la ruta:
"""
def get_max_hop(df_aspath_comm):

    max_hop = []
    for ruta in df_aspath_comm.ASPATH_Original:
        df = df_aspath_comm[df_aspath_comm['ASPATH_Original'] == ruta]
        hops = df.Hops_Comm.item()
        hops = hops.split(" ")
        hops = hops[1:-1]
        for hop in hops:
            max_hop.append(hop)

    max_hop.sort(key=int)
    max_hop = max_hop[-1];

    return max_hop;

"""
'get_hops' devolverá un string en donde se indique las rutas donde se ven communities
puestas por ASes a distancia 0, a distancia 1,etc:
"""
def get_hops(max_hop, df_aspath_comm):

    count_aspath = [];
    count = 0;
    for hop in range(0,int(max_hop)+1):
        string = "Hop"+str(hop)+":"
        hop = ' ' + str(hop) + ' '

        df = df_aspath_comm[df_aspath_comm['Hops_Comm'].str.contains(hop)]
        count_diff_rutas = len(list(df.ASPATH.unique()))
        count = count + count_diff_rutas
        string = string+str(count_diff_rutas)
        count_aspath.append(string)

    count_aspath = " ".join(count_aspath)

    return count_aspath,count;

"""
'info_rutas' devolverá un diccionario con la siguiente información a partir de las
distintas longitudes de ruta sin considerar Prepending (en caso de que hubiera):
    - Longitud ruta
    - Número de rutas distintas con dicha longitud
    - Número de rutas distintas que NUNCA ven communities
    - Número de rutas que ven communities puestas por ASes que no son del aspath
    - A qué distancia máxima espero ver communities
    - Rutas con communities a un salto, dos saltos, tres saltos, etc.
    - Count de todas esas rutas (dará mayor que el total de rutas distintas)
"""
def info_rutas(df_aspaths):

    # Agrupo los distintos aspaths en función de su longitud:
    # ¿Cuantas longitudes distintas hay?
    long_aspaths = list(df_aspaths.long_ruta.unique())
    df_longaspaths = df_aspaths.groupby('long_ruta')

    data_rutas = {};
    for longitud in long_aspaths:
        info = [];
        # Generamos df con la información para dicha longitud:
        df_longaspath = df_longaspaths.get_group(longitud)

        # RRC de estudio:
        rrc_id = list(df_longaspath.RRC_ID.unique())
        if len(rrc_id) == 1:
            info.append(rrc_id[0])
        else:
            info.append('Multiples_RRCs')

        # Número de rutas distintas con dicha longitud:
        count_rutas = len(list(df_longaspath.ASPATH.unique()))
        info.append(count_rutas)

        # Número de rutas distintas que NUNCA ven communities:
        df_NUNCA_comm = df_longaspath[df_longaspath['Tag_count_Announced_Comm'] == 'Nunca']
        count_NUNCA_comm = len(list(df_NUNCA_comm.ASPATH.unique()))
        info.append(count_NUNCA_comm)

        # Número de rutas que ven communities puestas por ASes que no son del aspath:
        df_comm = df_longaspath[df_longaspath['Hops_Comm'] != 'No-Communities']
        df_ASes = df_comm[df_comm['Hops_Comm'] == 'No-CommHops']
        count_rutas = len(list(df_ASes.ASPATH.unique()))
        info.append(count_rutas)

        # Para esta longitud de ruta, ¿en cuantos saltos espero ver communities?
        df_aspath_comm = df_comm[df_comm['Hops_Comm'] != 'No-CommHops']
        if not df_aspath_comm.empty:
            max_hopComm = get_max_hop(df_aspath_comm)
            info.append(max_hopComm)
        else:
            info.append('-')

        # Rutas con communities a un salto, dos saltos, tres saltos, etc.:
        if not df_aspath_comm.empty:
            count_aspath,count_total = get_hops(max_hopComm,df_aspath_comm)
            info.append(count_aspath)
            info.append(count_total)
        else:
            info.append('-')
            info.append('-')

        data_rutas.update({longitud:info})

    return data_rutas;

# =================================== Main() ===================================
print "Comienza la ejecución: Hora -> ", asctime(localtime());
start_time = time()

"""
Analizo las rutas de cada colector y después uno resultados. Sé que hay ASPATHs que
se ven en más de un colector, y que pueden tener atributos de estudio diferentes, por ejemplo:
Para un ASPATH concreto, que bajo un colector siempre vea communities y para otro colector
nunca vea communities.
Esto no importa, dado que a pesar de ser ASPATHs iguales vistos en varios colectores,
estas rutas se dirigen a IP monitores distintos, por tanto, asumo que son rutas distintas.

Otra consideración es emplear las 'rutas', no el ASPATH, tiene más sentido emplear
el ASPATH sin considerar Prepending == 'ruta'
"""
rrcs = ['rrc00.ripe','rrc01.ripe','rrc03.ripe','rrc04.ripe','rrc05.ripe','rrc06.ripe',\
        'rrc07.ripe','rrc10.ripe','rrc11.ripe','rrc12.ripe','rrc13.ripe','rrc14.ripe',\
        'rrc15.ripe','rrc16.ripe','rrc18.ripe','rrc19.ripe','rrc20.ripe','rrc21.ripe']

Header_ASPATHs = ['ASPATH_Original','RRC_ID','count_Announced','count_Announced_Comm','Pcount_Announced_Comm',\
        'Tag_count_Announced_Comm','Tag_Prep','ASPATH','long_ruta','Clasi_ASes','Communities',\
        'ASes_Comm','ASesASPATH_Comm','Hops_Comm','iden_ASes_aspath','Range_ASes_aspath',\
        'iden_ASes_comm','Range_ASes_comm','Macheo_ASes_aspath_comm']

for rrc in rrcs:
    print rrc;
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_'+rrc+'.txt'
    df_aspaths = pd.read_csv(file_read, sep='|',header=None, names=Header_ASPATHs);

    # Quedarme con las columnas necesarias para este análisis:
    df_aspaths = df_aspaths[['ASPATH_Original','RRC_ID','Tag_count_Announced_Comm',\
                        'ASPATH','long_ruta','Hops_Comm']]

    # Analizamos las rutas según su longitud de ASPATH (sin considerar Prepending si lo hubiera):
    data_rutas = info_rutas(df_aspaths)
    df_rutas = pd.DataFrame.from_dict(data_rutas,orient='index')
    df_rutas.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Rutas/Rutas_'+rrc+'.txt',\
                sep='|',header=None, index=True)

# Unifico la información obtenida de cada uno de los colectores:
print 'Unir los datos de los colectores en un unico fichero txt:'
Header_rutas = ['long_ruta','RRC_ID','count_rutas','count_NUNCA_comm','count_rutas_NoASesASPATH',\
                'max_hopComm','count_aspath','count_total']

df_global = pd.DataFrame([], columns = Header_rutas)
for rrc in rrcs:
    print rrc
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Rutas/Rutas_'+rrc+'.txt'
    df_rrc = pd.read_csv(file_read, sep='|',header=None, names=Header_rutas);

    # Añado la información al df general:
    df_global = df_global.append(df_rrc, sort=False)

# Guardamos el dataframe como txt:
df_global.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Rutas/Rutas_RRCs.txt',\
                    sep='|',header=None, index=None)

print "Termina la ejecución: Hora -> ", asctime(localtime());
elapsed_time = time() - start_time
print("Tiempo de ejecucion: "+ str(elapsed_time))
