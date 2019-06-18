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
import socket

""" ======= FUNCIONES ======= """
"""
La función 'get_list_files_BGP' nos devolverá la lista de ficheros en función de los
parámetros de entrada que son el ID del RRC y el día (aunque será el mismo para todas
las RRCs consideradas en el proyecto):
"""
def get_list_files_BGP(rrc,day):

    """
    Cargar los ficheros correspondientes al RRC indicado:
    """
    list_files_bview = [];
    list_files_update = [];

    for file in listdir('/srv/agarcia/TFM-BGP/Jesus/DATA/'+rrc):

        if re.match("^updates." + day ,file):
            list_files_update.append(file);
        elif re.match("^bview." + day ,file):
            list_files_bview.append(file);
        else:
            print ('Error name file!');
            sys.exit();

    list_files_bview.sort();
    list_files_update.sort();

    list_files_BGP_day = [];
    list_files_BGP_day = list_files_bview + list_files_update;

    return list_files_BGP_day;

"""
La función 'create_mega_dataframe' generará un dataframe de dimensiones enormes, pero que
me ayudará a reducir el número de bucles a hacer.
Este DataFrame será generado a nivel de día.
"""
def create_mega_dataframe(list_df, Header, Header_drop):

    df_all_files = pd.DataFrame([], columns = Header)

    for df in list_df:
        df_all_files = df_all_files.append(df, sort=False)

    # Eliminamos información que no nos será de utilidad en este análisis:
    df_all_files = df_all_files.drop(columns = Header_drop)

    return df_all_files;

def type_prefix(prefix):

    prefix_split = prefix.split("/")[0]
    try:
        socket.inet_aton(prefix_split)
        IPPrefix = 'IPv4'
    except socket.error:
        IPPrefix = 'IPv6'

    return IPPrefix;

def get_neighbors(aspath, monitor):

    try:
        neighbor = aspath.split(" ")[1]
        if str(monitor) == neighbor:
            neighbor = "Monitor ASPATHPrep"
    except IndexError:
        neighbor = "No-Neighbor"

    return neighbor

def add_moreinfo(df_all_files,rrc):

    add_ID_RRC = [];
    add_IPType = [];
    add_neighbor = [];

    for index, row in df_all_files.iterrows():

        rrc_info = rrc.split(".")[0]
        add_ID_RRC.append(rrc_info)

        ABW = row.ABW;
        if ABW == 'A' or ABW == 'B':
            IPPrefix = type_prefix(row.AnnouncedPrefix)
            add_IPType.append(IPPrefix)

            neighbor = get_neighbors(row.ASPATH, row.ASMonitor)
            add_neighbor.append(neighbor)
        else:
            add_IPType.append('-')
            add_neighbor.append('-')

    df_all_files.insert(0,'RRC_ID',add_ID_RRC)
    df_all_files.insert(4,'IPType',add_IPType)
    df_all_files.insert(5,'Neighbor',add_neighbor)

    df_day = df_all_files[['RRC_ID','ABW','IPMonitor','ASMonitor','AnnouncedPrefix',\
                        'IPType','ASPATH','Neighbor','Communities','Large_Communities']]

    return df_day;

"""
La función 'get_announced_typeIP' nos devolverá un primer df filtrado con aquellos
anuncios de prefijos IPv4, y por tanto, se corresponderá que monitores IPv4.
También en este dataframe solamente aparecerán anuncios (no borrados de prefijos):
"""
def get_announced_typeIP(df_day, typeIP):

    # Eliminamos los anuncios de borrado de prefijos:
    df_day = df_day[df_day['ABW'] != 'W']

    # Eliminamos ASPATHS nulos:
    df_day = df_day[df_day['ASPATH'] != '-']

    # Eliminamos ASPATHs con agregados:
    df_day = df_day[df_day['ASPATH'].str.endswith('}') == False]

    # Agrupo por anuncios de prefijos typeIP:
    df = df_day.groupby('IPType');
    df = df.get_group(typeIP)

    return df;

"""
La función 'get_announced_requiered' devolverá el dataframe con todos los anuncios
realizados por monitores según el tipo de IP que hayamos definido, y que además
sean proveedores, es decir, que durante el día anuncien al menos 30.000 prefijos distintos:
"""
def get_announced_requiered(df_typeIP, prefix_requiered):

    data_monitors = {};

    # Obtenemos la lista de todos aquellos IP Monitors en el día:
    # (Agrupamos por IPMonitor)
    df_day = df_typeIP;
    IPMonitors = list(df_day.IPMonitor.unique());
    df_IPMonitors = df_day.groupby('IPMonitor')

    for IPMonitor in IPMonitors:
        info = [];

        # Generamos df con la información para dicho IPMonitor:
        df_IPMonitor = df_IPMonitors.get_group(IPMonitor);

        # Número de prefijos distintos que anuncia:
        prefixes = len(list(df_IPMonitor.AnnouncedPrefix.unique()));
        info.append(prefixes)

        data_monitors.update({IPMonitor:info})

    df = pd.DataFrame.from_dict(data_monitors,orient='index')
    df = df.reset_index()
    df = df.rename(columns={'index': 'IPMonitor', 0:'Num_Prefixes'})
    df = df.sort_values(by='Num_Prefixes', ascending=False)

    # Nos quedamos solamente con aquellos monitores que anuncien al menos 30.000 prefijos:
    df = df[df['Num_Prefixes'] >= prefix_requiered]

    # Lista de monitores válidos:
    list_monitors = list(df.IPMonitor.unique());

    for IPMonitor in list(df_typeIP.IPMonitor.unique()):
        if not IPMonitor in list_monitors:
            df_typeIP = df_typeIP[df_typeIP['IPMonitor'] != IPMonitor]

    return df_typeIP;

# =================================== Main() ===================================
print "Comienza la ejecución: Hora -> ", asctime(localtime());
start_time = time()

# """
# Generar para cada RRC (colector) su TXT independiente con toda la información referente
# al día elegido para la realización del análisis:
# """
# print "Generar dataframe por cada RRC uniendo los ficheros:"
# rrcs = ['rrc00.ripe','rrc01.ripe','rrc03.ripe','rrc04.ripe','rrc05.ripe','rrc06.ripe',\
#         'rrc07.ripe','rrc10.ripe','rrc11.ripe','rrc12.ripe','rrc13.ripe','rrc14.ripe',\
#         'rrc15.ripe','rrc16.ripe','rrc18.ripe','rrc19.ripe','rrc20.ripe','rrc21.ripe']
# day = '20180110'
#
# for rrc in rrcs:
#     print rrc;
#     list_files_BGP = get_list_files_BGP(rrc,day);
#
#     Header = ['Tipo', 'Tiempo','ABW','IPMonitor','ASMonitor','AnnouncedPrefix','ASPATH',\
#             'ORIGIN','NEXTHOP','NumASPATH','ASPATHORIGEN','Communities', 'Large_Communities',\
#             '-4','-5','-6']
#
#     Header_drop = ['Tipo', 'Tiempo','ORIGIN','NEXTHOP','NumASPATH',\
#                     'ASPATHORIGEN','-4','-5','-6']
#
#     list_df = [];
#
#     for file in list_files_BGP:
#         df = pd.read_csv('/srv/agarcia/TFM-BGP/Jesus/DATA/'+rrc+'/' + file, sep='|',  \
#                             header=None, names=Header,index_col=False);
#         df = df.fillna({'ASPATH':'-'})
#         df = df.fillna({'Communities':'-'})
#         df = df.fillna({'Large_Communities':'-'})
#
#         list_df.append(df)
#
#     df_all_files = create_mega_dataframe(list_df, Header, Header_drop)
#     df_day = add_moreinfo(df_all_files,rrc);
#     df_day.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/DATA/General/'+rrc+'_'+day+'.txt',sep='|',header=None, index=False)
#
# """
# Crear dataframe con toda la información referente en cada RRC. En cada colector, filtraremos
# quitando aquellos anuncios 'W', ASPATHs nulos y agregados, que sean unicamente anuncios
# de prefijos IPv4 proviniente de monitores proveedores (es decir, que anuncien al menos
# 30.000 prefijos distintos durante ese día de análisis):
# """
# print "Generar dataframe de cada RRC filtrando por parametros deseados:"
# rrcs = ['rrc00.ripe','rrc01.ripe','rrc03.ripe','rrc04.ripe','rrc05.ripe','rrc06.ripe',\
#         'rrc07.ripe','rrc10.ripe','rrc11.ripe','rrc12.ripe','rrc13.ripe','rrc14.ripe',\
#         'rrc15.ripe','rrc16.ripe','rrc18.ripe','rrc19.ripe','rrc20.ripe','rrc21.ripe']
# day = '20180110'
# typeIP = 'IPv4'
# prefix_requiered = 30000;
#
# Header = ['RRC_ID','ABW','IPMonitor','ASMonitor','AnnouncedPrefix',\
#         'IPType','ASPATH','Neighbor','Communities','Large_Communities']
#
# for rrc in rrcs:
#     print rrc;
#     file_read = '/srv/agarcia/TFM-BGP/Jesus/DATA/General/'+rrc+'_'+day+'.txt'
#     df_rrc = pd.read_csv(file_read, sep='|',header=None, names=Header, dtype={"Neighbor": object});
#
#     df_typeIP = get_announced_typeIP(df_rrc, typeIP)
#     df_requiered = get_announced_requiered(df_typeIP, prefix_requiered)
#     df_requiered.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/DATA/General_filtered/'+rrc+'_filtered.txt',\
#                         sep='|',header=None, index=None)

"""
En cada fichero generado, por cada uno de los colectores analizados, generar una
última columna en donde se indiquen los ASes que ponen communities (en caso de que
haya communities), juntando la información con los ASes que ponen large communities:
"""
rrcs = ['rrc00.ripe','rrc01.ripe','rrc03.ripe','rrc04.ripe','rrc05.ripe','rrc06.ripe',\
        'rrc07.ripe','rrc10.ripe','rrc11.ripe','rrc12.ripe','rrc13.ripe','rrc14.ripe',\
        'rrc15.ripe','rrc16.ripe','rrc18.ripe','rrc19.ripe','rrc20.ripe','rrc21.ripe']

Header = ['RRC_ID','ABW','IPMonitor','ASMonitor','AnnouncedPrefix',\
        'IPType','ASPATH','Neighbor','Communities','Large_Communities']

for rrc in rrcs:
    print rrc;
    file_read = '/srv/agarcia/TFM-BGP/Jesus/DATA/General_filtered/'+rrc+'_filtered.txt'
    df_rrc = pd.read_csv(file_read, sep='|',header=None, names=Header, dtype={"Neighbor": object});

    add_ASesValuesComm = [];
    add_ASesComm = [];
    for index, row in df_rrc.iterrows():

        communities = row.Communities;
        large_communities = row.Large_Communities;

        if communities != '-' and large_communities != '-':
            sum_communities = communities + ' ' + large_communities
        elif communities != '-' and large_communities == '-':
            sum_communities = communities
        elif communities == '-' and large_communities != '-':
            sum_communities = large_communities
        elif communities == '-'and large_communities == '-':
            sum_communities = '-'
        else:
            print "Ha pasado algo raro!"
            print communities
            print large_communities
            sys.exit();

        add_ASesValuesComm.append(sum_communities)

        sum_communities = sum_communities.split(" ")

        info = [];
        for ASValue in sum_communities:
            AS = ASValue.split(":")[0]
            if not AS in info:
                info.append(AS)

        info = ' '.join(info)
        add_ASesComm.append(info)

    df_rrc.insert(10,'ASesValuesComm',add_ASesValuesComm)
    df_rrc.insert(11,'ASesComm',add_ASesComm)

    df_rrc = df_rrc[['RRC_ID','ABW','IPMonitor','ASMonitor','AnnouncedPrefix',\
                    'IPType','ASPATH','Neighbor','Communities','Large_Communities',\
                    'ASesValuesComm','ASesComm']]

    df_rrc.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/DATA/'+rrc+'.txt',sep='|',header=None, index=None)

print "Termina la ejecución: Hora -> ", asctime(localtime());
elapsed_time = time() - start_time
print("Tiempo de ejecucion: "+ str(elapsed_time))
