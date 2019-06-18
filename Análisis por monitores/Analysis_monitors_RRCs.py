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

""" ============================= FUNCIONES ================================ """
"""
La función 'get_tag' me volverá una etiqueta nunca/alguna vez/casi siempre/siempre
dependiendo del valor de porcentaje de entrada en dicha función:
"""
def get_tag(porcentaje):

    if porcentaje == 0.0:
        tag = 'Nunca';
    elif porcentaje == 100.0:
        tag = 'Siempre';
    elif porcentaje >= 90.0 and porcentaje < 100.0:
        tag = 'Casi siempre'
    elif porcentaje > 100.0:
        tag = 'Error! Mayor 100%'
    else:
        tag = 'Alguna vez'

    return tag;

"""
La función 'get_neighbors' me devolverá una lista en forma de string con todos aquellos
vecinos disintos encontrados a un salto del monitor. También devolverá el total de
vecinos distintos encontrados:
"""
def get_neighbors(df):

    neighbors = list(df.Neighbor.unique())
    num_neighbors = len(neighbors)

    neighbors = " ".join(neighbors)

    return neighbors,num_neighbors;

"""
La función 'monitor_comm' nos indica el número de anuncios para los cuales hubo
atributos communities, y que en estos anuncios aparezca el ASMonitor poniendo
algún valor de community propio:
"""
def monitor_comm(monitor,df_IPMonitor_comm):

    count_monitor_comm = 0;

    seq_communities = list(df_IPMonitor_comm.ASesComm)
    for communities in seq_communities:
        ASes_Comm = communities.split(" ")
        if str(monitor) in ASes_Comm:
            count_monitor_comm = count_monitor_comm + 1;

    return count_monitor_comm;

"""
La función 'monitor_neighbors_comm' devolverá el número de anuncios BGP en los cuales
se ven communities puestas por los ASes vecinos del monitor (siguiente salto en el ASPATH).
"""
def monitor_neighbors_comm(monitor, df_IPMonitor_comm):

    # Combinaciones posibles ASMonitor más vecino potencial a poner communities:
    neighbors = list(df_IPMonitor_comm.Neighbor.unique())
    monitor_neighbors = [];
    for neighbor in neighbors:
        monitor_neighbors.append(str(monitor) + ' ' + str(neighbor) + ' ')

    count_neigh_comm = 0;
    for monitor_neighbor in monitor_neighbors:
        df_monitorNeighbor = df_IPMonitor_comm[df_IPMonitor_comm['ASPATH'].str.contains(monitor_neighbor)]
        if not df_monitorNeighbor.empty:
            neighbor = monitor_neighbor.split(" ")[1]
            seq_communities = list(df_monitorNeighbor.ASesComm)
            for communities in seq_communities:
                ASes_Comm = communities.split(" ")
                if neighbor in ASes_Comm:
                    count_neigh_comm = count_neigh_comm + 1;

    return count_neigh_comm;

"""
'info_monitor' devolverá una serie de parámetros referente a cada uno de los IPMonitors
distintos encontrados en el dataframe pasado como entrada en la función:
"""
def info_monitor(df_rrc,rrc):

    # Obtenemos la lista de todos aquellos IP Monitors en el dataframe de entrada:
    # (Agrupamos por IPMonitor)
    IPMonitors = list(df_rrc.IPMonitor.unique())
    df_IPMonitors = df_rrc.groupby('IPMonitor')

    data_monitors = {}
    for IPMonitor in IPMonitors:
        info_IPMonitor = []

        # Colector al que pertenece este IPMonitor:
        id_rrc = rrc.split(".")[0]
        info_IPMonitor.append(id_rrc)

        # Generamos df con la información para dicho IPMonitor:
        df_IPMonitor = df_IPMonitors.get_group(IPMonitor)

        # Encontramos el AS Monitor para dicha IP Monitor:
        AS_Monitor = list(df_IPMonitor.ASMonitor.unique())
        if len(AS_Monitor) == 1:
            monitor = AS_Monitor[0]
        elif len(AS_Monitor) > 1:
            monitor = 'Multiples_AS_Monitor'
        else:
            monitor = 'Mmmm...'

        info_IPMonitor.append(monitor)

        # Número total de anuncios que realiza:
        count_Announced = len(df_IPMonitor)
        info_IPMonitor.append(count_Announced)

        # Número total de anuncios con communities:
        df_IPMonitor_comm = df_IPMonitor[df_IPMonitor['ASesValuesComm'] != '-']
        count_Announced_Comm = len(df_IPMonitor_comm)
        info_IPMonitor.append(count_Announced_Comm)

        # Porcentaje de anuncios con communities:
        try:
            porcentaje_comm = float(float(count_Announced_Comm)/(float(count_Announced)))
            porcentaje_comm = float(porcentaje_comm)*float(100)
            porcentaje_comm_str = "{0:.3f}".format(porcentaje_comm)
        except ZeroDivisionError:
            porcentaje_comm = 0.0;
            porcentaje_comm_str = "{0:.3f}".format(porcentaje_comm)

        info_IPMonitor.append(porcentaje_comm_str)

        # Etiqueto el resultado obtenido:
        tag = get_tag(porcentaje_comm)
        info_IPMonitor.append(tag)

        # Obtener la lista de vecinos distintos para el monitor:
        neighbors, num_neighbors = get_neighbors(df_IPMonitor)
        info_IPMonitor.append('List neighbors')
        info_IPMonitor.append(num_neighbors)

        # Ocurrencia en las cuales el ASMonitor pone communities:
        count_monitor_comm = monitor_comm(monitor,df_IPMonitor_comm);
        info_IPMonitor.append(count_monitor_comm)

        # Porcentaje de anuncios con communities puestas por el ASMonitor:
        try:
            porcentaje_comm = float(float(count_monitor_comm)/(float(count_Announced_Comm)))
            porcentaje_comm = float(porcentaje_comm)*float(100)
            porcentaje_comm_str = "{0:.3f}".format(porcentaje_comm)
        except ZeroDivisionError:
            porcentaje_comm = 0.0;
            porcentaje_comm_str = "{0:.3f}".format(porcentaje_comm)

        info_IPMonitor.append(porcentaje_comm_str)

        # Etiqueto el resultado obtenido:
        tag = get_tag(porcentaje_comm)
        info_IPMonitor.append(tag)

        # Ocurrencia en las cuales los ASes vecinos ponen communities:
        count_neigh_comm = monitor_neighbors_comm(monitor, df_IPMonitor_comm)
        info_IPMonitor.append(count_neigh_comm)

        # Porcentaje de anuncios con communities puestas por los ASes vecinos:
        try:
            porcentaje_comm = float(float(count_neigh_comm)/(float(count_Announced_Comm)))
            porcentaje_comm = float(porcentaje_comm)*float(100)
            porcentaje_comm_str = "{0:.3f}".format(porcentaje_comm)
        except ZeroDivisionError:
            porcentaje_comm = 0.0;
            porcentaje_comm_str = "{0:.3f}".format(porcentaje_comm)

        info_IPMonitor.append(porcentaje_comm_str)

        # Etiqueto el resultado obtenido:
        tag = get_tag(porcentaje_comm)
        info_IPMonitor.append(tag)

        data_monitors.update({IPMonitor:info_IPMonitor})

    return data_monitors;

"""
La función 'get_communities_monitor' devolverá lista en donde se vean las communities
puestas por el monitor en el caso de que el monitor siempre o casi siempre ponga
communities propias:
"""
def get_communities_monitor(monitor, df):

    list_communities = [];
    seq_communities = list(df.ASesValuesComm)
    for communities in seq_communities:
        ASesValues = communities.split(" ")
        for ASValue in ASesValues:
            AS = ASValue.split(":")[0]
            if str(monitor) == AS and not ASValue in list_communities:
                list_communities.append(ASValue)

    return list_communities;

"""
'get_monitors_ASValues' me devolverá un diccionario en donde se puedan ver los valores
de communities puestos por ASes monitors, y además diferenciar si dicha community es
regular o large:
"""
def get_monitors_ASValues(df_rrc,df_rrc_monitors):

    # Filtramos por aquellos monitores que siempre o casi siempre ven communities:
    tags_study = ['Siempre', 'Casi siempre','Alguna vez']
    for tag in list(df_rrc_monitors.TagAnnounced_Comm.unique()):
        if not tag in tags_study:
            df_rrc_monitors = df_rrc_monitors[df_rrc_monitors['TagAnnounced_Comm'] != tag]

    # Filtramos por aquellos monitores que siempre o casi siempre ponen communities propias:
    for tag in list(df_rrc_monitors.TagAnnounced_MonitorComm.unique()):
        if not tag in tags_study:
            df_rrc_monitors = df_rrc_monitors[df_rrc_monitors['TagAnnounced_MonitorComm'] != tag]

    # Lista de aquellos monitores que serán considerados en este apartado:
    # (Agrupamos por ASMonitor)
    ASes_Monitors = list(df_rrc_monitors.ASMonitor.unique())
    df_ASesMonitors = df_rrc.groupby('ASMonitor')

    list_communities = [];
    for AS_Monitor in ASes_Monitors:

        # Generamos df con la información para dicho ASMonitor:
        df_ASMonitor = df_ASesMonitors.get_group(AS_Monitor)
        df_ASMonitor_comm = df_ASMonitor[df_ASMonitor['ASesValuesComm'] != '-']
        communities = get_communities_monitor(AS_Monitor, df_ASMonitor_comm)
        for comm in communities:
            if not comm in list_communities:
                list_communities.append(comm)

    # Genero dataframe unicamente con los valores communities:
    data_ASValue = {}
    for community in list_communities:
        info = [];

        ASComm = community.split(":")

        # ASMonitor:
        ASMonitor = ASComm[0]
        info.append(ASMonitor)

        # ¿Es community regular o large?
        if len(ASComm) == 2:
            tag = 'Regular'
        elif len(ASComm) == 3:
            tag = 'Large'
        else:
            tag = 'Mmmm...'
        info.append(tag)

        data_ASValue.update({community:info})

    return data_ASValue

"""
La función 'get_communities_neighbors' devolverá lista en donde se vean las communities
puestas por los vecinos del monitor en el caso de que el monitor vea (casi) siempre
communities puestas por sus vecinos:
"""
def get_communities_neighbors(monitor,df_IPMonitor_comm):

    # Combinaciones posibles ASMonitor más vecino potencial a poner communities:
    neighbors = list(df_IPMonitor_comm.Neighbor.unique())
    monitor_neighbors = [];
    for neighbor in neighbors:
        monitor_neighbors.append(str(monitor) + ' ' + str(neighbor) + ' ')

    communities = [];
    for monitor_neighbor in monitor_neighbors:
        df_monitorNeighbor = df_IPMonitor_comm[df_IPMonitor_comm['ASPATH'].str.contains(monitor_neighbor)]
        if not df_monitorNeighbor.empty:
            neighbor = monitor_neighbor.split(" ")[1]
            for seq_communities in list(df_monitorNeighbor.ASesValuesComm):
                ASesValues = seq_communities.split(" ")
                for ASValue in ASesValues:
                    AS = ASValue.split(":")[0]
                    if AS == neighbor and not ASValue in communities:
                        communities.append(ASValue)

    return communities;

"""
'get_neighbors_ASValues' me devolverá un diccionario en donde se puedan ver los valores
de communities puestos por ASes vecinos. Para cada community se indicará si el valor
de community es regular o large:
"""
def get_neighbors_ASValues(df_rrc,df_rrc_monitors):

    # Filtramos por aquellos monitores que siempre o casi siempre ven communities:
    tags_study = ['Siempre', 'Casi siempre','Alguna vez']
    for tag in list(df_rrc_monitors.TagAnnounced_Comm.unique()):
        if not tag in tags_study:
            df_rrc_monitors = df_rrc_monitors[df_rrc_monitors['TagAnnounced_Comm'] != tag]

    # Filtramos por aquellos monitores que siempre o casi siempre ven communities de sus vecinos:
    for tag in list(df_rrc_monitors.TagAnnounced_NeighComm.unique()):
        if not tag in tags_study:
            df_rrc_monitors = df_rrc_monitors[df_rrc_monitors['TagAnnounced_NeighComm'] != tag]

    # Lista de aquellos monitores que serán considerados en este apartado:
    # (Agrupamos por ASMonitor)
    ASes_Monitors = list(df_rrc_monitors.ASMonitor.unique())
    df_ASesMonitors = df_rrc.groupby('ASMonitor')

    list_communities = [];
    for AS_Monitor in ASes_Monitors:

        # Generamos df con la información para dicho ASMonitor:
        df_ASMonitor = df_ASesMonitors.get_group(AS_Monitor)
        df_ASMonitor_comm = df_ASMonitor[df_ASMonitor['ASesValuesComm'] != '-']
        communities = get_communities_neighbors(AS_Monitor,df_ASMonitor_comm)
        for comm in communities:
            if not comm in list_communities:
                list_communities.append(comm)

    # Genero dataframe unicamente con los valores communities:
    data_ASValue = {}
    for community in list_communities:
        info = [];

        ASComm = community.split(":")

        # ASNeighbor:
        ASNeighbor = ASComm[0]
        info.append(ASNeighbor)

        # ¿Es community regular o large?
        if len(ASComm) == 2:
            tag = 'Regular'
        elif len(ASComm) == 3:
            tag = 'Large'
        else:
            tag = 'Mmmm...'
        info.append(tag)

        data_ASValue.update({community:info})

    return data_ASValue

"""
'get_rango_ASMonitor' determinará si el ASMonitor es de rango público o privado,
o si por ejemplo el AS está fuera del rango de 65535:
https://www.iana.org/assignments/as-numbers/as-numbers.xhtml(Internet)
"""
def get_rango_ASMonitor(ASMonitor):

    if int(ASMonitor) <= 65535:
        # ASes 16 bits
        if int(ASMonitor) == 0:
            iden = 'Reservado_0'
        elif int(ASMonitor) >= 1 and int(ASMonitor) <= 23455:
            iden = 'Público_16b'
        elif int(ASMonitor) == 23456:
            iden = 'AS_TRANS'
        elif int(ASMonitor) >= 23457 and int(ASMonitor) <= 64495:
            iden = 'Público_16b'
        elif int(ASMonitor) >= 64496 and int(ASMonitor) <= 64511:
            iden = 'Reservado_Doc_16b'
        elif int(ASMonitor) >= 64512 and int(ASMonitor) <= 65534:
            iden = 'Privado_16b'
        elif int(ASMonitor) == 65535:
            iden = 'Reservado_65535'

    elif int(ASMonitor) > 65535:
        # ASes 32 bits
        if int(ASMonitor) >= 65536 and int(ASMonitor) <= 65551:
            iden = 'Reservado_Doc_32b'
        elif int(ASMonitor) >= 65552 and int(ASMonitor) <= 131071:
            iden = 'Reservado_32b'
        elif int(ASMonitor) >= 131072 and int(ASMonitor) <= 4199999999:
            iden = 'Público_32b'
        elif int(ASMonitor) >= 4200000000 and int(ASMonitor) <= 4294967294:
            iden = 'Privado_32b'
        elif int(ASMonitor) == 4294967295:
            iden = 'Reservado_4294967295'
    else:
        iden = 'Unknown'

    return iden;

"""
'get_CAIDA' devolverá si lo encuentra la clasificación CAIDA para el ASMonitor:
"""
def get_CAIDA(ASMonitor):

    # Análisis CAIDA (tipo de AS):
    # types: Content|Enterpise|Transit/Access
    Header_CAIDA = ['AS','source','type']
    df_CAIDA = pd.read_csv('/srv/agarcia/TFM-BGP/Jesus/CAIDA/df_CAIDAResult.txt', sep='|',  \
                        header=None, names=Header_CAIDA);

    # Clasificación CAIDA para el AS:
    df = df_CAIDA[df_CAIDA['AS'] == int(ASMonitor)]
    if df.empty:
        type_ASMonitor = 'Unknown'
    else:
        type_ASMonitor = df.type.item()

    return type_ASMonitor;

# =================================== Stages() ==================================
"""
Generar dataframe con la información referente a cada uno de los IPMonitors proveedores
(es decir, que anuncien al menos 30.000 prefijos distintos durante un periodo de tiempo,
que será de un día en nuestro caso).
Para cada monitor obtendremos una serie de parámetros para descubrir su comportamiento:
"""
def stage1():
    print "Comienza la ejecución: Hora -> ", asctime(localtime());
    start_time = time()

    rrcs = ['rrc00.ripe','rrc01.ripe','rrc03.ripe','rrc04.ripe','rrc05.ripe','rrc06.ripe',\
            'rrc07.ripe','rrc10.ripe','rrc11.ripe','rrc12.ripe','rrc13.ripe','rrc14.ripe',\
            'rrc15.ripe','rrc16.ripe','rrc18.ripe','rrc19.ripe','rrc20.ripe','rrc21.ripe']

    Header = ['RRC_ID','ABW','IPMonitor','ASMonitor','AnnouncedPrefix',\
            'IPType','ASPATH','Neighbor','Communities','Large_Communities',\
            'ASesValuesComm','ASesComm'];

    for rrc in rrcs:
        print rrc + " Hora -> ", asctime(localtime());
        file_read = '/srv/agarcia/TFM-BGP/Jesus/DATA/'+rrc+'.txt'
        df_rrc = pd.read_csv(file_read, sep='|',header=None, names=Header, dtype={"Neighbor": object});

        data_monitors = info_monitor(df_rrc,rrc)
        df_monitors = pd.DataFrame.from_dict(data_monitors,orient='index')
        df_monitors.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Monitors_'+rrc+'.txt',\
                    sep='|',header=None, index=True)

    # Unifico la información obtenida de cada uno de los colectores:
    Header_monitors = ['IPMonitor','RRC_ID','ASMonitor','Announced','Announced_Comm','PAnnounced_Comm',\
                        'TagAnnounced_Comm','Neighbors','Num_Neighbors','Announced_MonitorComm',\
                        'PAnnounced_MonitorComm','TagAnnounced_MonitorComm','Announced_NeighComm',\
                        'PAnnounced_NeighComm','TagAnnounced_NeighComm']

    df_collectors = pd.DataFrame([], columns = Header_monitors)
    for rrc in rrcs:
        file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Monitors_'+rrc+'.txt'
        df_rrc = pd.read_csv(file_read, sep='|',header=None, names=Header_monitors);

        # Añado la información al df general:
        df_collectors = df_collectors.append(df_rrc, sort=False)

    # Guardamos el dataframe como txt:
    df_collectors.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Monitors_RRCs.txt',\
                        sep='|',header=None, index=None)

    print "Termina la ejecución: Hora -> ", asctime(localtime());
    elapsed_time = time() - start_time
    print("Tiempo de ejecucion: "+ str(elapsed_time))

    return None;

"""
'Stage_1b': Analizar la información del monitor desde el punto de vista del AS monitor,
en lugar de hacerlo con respecto al IPMonitor.
Un ASMonitor puede englobar más de un IPMonitor.
"""
def stage_1b():

    Header_monitors = ['IPMonitor','RRC_ID','ASMonitor','Announced','Announced_Comm','PAnnounced_Comm',\
                        'TagAnnounced_Comm','Neighbors','Num_Neighbors','Announced_MonitorComm',\
                        'PAnnounced_MonitorComm','TagAnnounced_MonitorComm','Announced_NeighComm',\
                        'PAnnounced_NeighComm','TagAnnounced_NeighComm']

    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Monitors_RRCs.txt'
    df_monitors = pd.read_csv(file_read, sep='|',header=None, names=Header_monitors);

    # Lista de ASes distintos:
    # (Agrupo por AS monitor)
    ASMonitors = list(df_monitors.ASMonitor.unique())
    df_ASMonitors = df_monitors.groupby('ASMonitor')

    data_ASMonitor = {};
    for ASMonitor in ASMonitors:
        info = [];

        # Información referente al AS monitor:
        df_ASMonitor = df_ASMonitors.get_group(ASMonitor)

        # IPMonitors distintos que engloba el ASMonitor:
        IPMonitors = list(df_ASMonitor.IPMonitor.unique())
        IPMonitors_str = ' '.join(IPMonitors)
        info.append(IPMonitors_str)
        info.append(len(IPMonitors))

        # Colectores distintos que engloba el ASMonitor:
        RRCs = list(df_ASMonitor.RRC_ID.unique())
        RRCs_str = ' '.join(RRCs)
        info.append(RRCs_str)
        info.append(len(RRCs))

        # Tags visto communities distintos que ven cada AS:
        # ¿Comportamiento diferente en cada colector?
        tags_comm = list(df_ASMonitor.TagAnnounced_Comm.unique())
        if len(tags_comm) > 1:
            porcentaje_comm = list(df_ASMonitor.PAnnounced_Comm)
            porcentaje_comm = map(float, porcentaje_comm)
            result = sum(porcentaje_comm)/len(porcentaje_comm)
            tag = get_tag(result)
            info.append(tag)
        elif len(tags_comm) == 1:
            tag = tags_comm[0]
            info.append(tag)

        # Tag visto communities puestas por el ASMonitor:
        tags_comm_monitor = list(df_ASMonitor.TagAnnounced_MonitorComm.unique())
        if len(tags_comm_monitor) > 1:
            porcentaje_comm = list(df_ASMonitor.PAnnounced_MonitorComm)
            porcentaje_comm = map(float, porcentaje_comm)
            result = sum(porcentaje_comm)/len(porcentaje_comm)
            tag = get_tag(result)
            info.append(tag)
        elif len(tags_comm_monitor) == 1:
            tag = tags_comm_monitor[0]
            info.append(tag)

        # Tag visto communities puestas por los vecinos del monitor:
        tags_comm_neigh = list(df_ASMonitor.TagAnnounced_NeighComm.unique())
        if len(tags_comm_neigh) > 1:
            porcentaje_comm = list(df_ASMonitor.PAnnounced_NeighComm)
            porcentaje_comm = map(float, porcentaje_comm)
            result = sum(porcentaje_comm)/len(porcentaje_comm)
            tag = get_tag(result)
            info.append(tag)
        elif len(tags_comm_neigh) == 1:
            tag = tags_comm_neigh[0]
            info.append(tag)

        # Rango del ASMonitor:
        iden = get_rango_ASMonitor(ASMonitor)
        info.append(iden)

        # Análisis CAIDA:
        caida = get_CAIDA(ASMonitor);
        info.append(caida)

        data_ASMonitor.update({ASMonitor:info})

    df_ASMonitors = pd.DataFrame.from_dict(data_ASMonitor,orient='index')
    # Guardamos el dataframe como txt:
    df_ASMonitors.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASMonitors_RRCs.txt',\
                        sep='|',header=None, index=True)

    return None;

"""
Stage2: Para los casos en los cuales el AS Monitor alguna vez/(casi) siempre ve valores de
communities en sus anuncios, y además alguna vez/(casi) siempre el AS monitor pone valores
de communities propios, identificar dichos pares AS:Comm y diferenciar si son
communities regulares o large communities:
"""
def stage2():
    print "Comienza la ejecución Stage 2: Hora -> ", asctime(localtime());
    start_time = time()

    rrcs = ['rrc00.ripe','rrc01.ripe','rrc03.ripe','rrc04.ripe','rrc05.ripe','rrc06.ripe',\
            'rrc07.ripe','rrc10.ripe','rrc11.ripe','rrc12.ripe','rrc13.ripe','rrc14.ripe',\
            'rrc15.ripe','rrc16.ripe','rrc18.ripe','rrc19.ripe','rrc20.ripe','rrc21.ripe']

    Header = ['RRC_ID','ABW','IPMonitor','ASMonitor','AnnouncedPrefix',\
            'IPType','ASPATH','Neighbor','Communities','Large_Communities',\
            'ASesValuesComm','ASesComm'];

    Header_monitors = ['IPMonitor','RRC_ID','ASMonitor','Announced','Announced_Comm','PAnnounced_Comm',\
                        'TagAnnounced_Comm','Neighbors','Num_Neighbors','Announced_MonitorComm',\
                        'PAnnounced_MonitorComm','TagAnnounced_MonitorComm','Announced_NeighComm',\
                        'PAnnounced_NeighComm','TagAnnounced_NeighComm']

    for rrc in rrcs:
        print rrc
        file_read = '/srv/agarcia/TFM-BGP/Jesus/DATA/'+rrc+'.txt'
        df_rrc = pd.read_csv(file_read, sep='|',header=None, names=Header, dtype={"Neighbor": object});

        file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Monitors_'+rrc+'.txt'
        df_rrc_monitors = pd.read_csv(file_read, sep='|',header=None, names=Header_monitors);

        data_ASValue = get_monitors_ASValues(df_rrc,df_rrc_monitors);
        df_monitors_ASValues = pd.DataFrame.from_dict(data_ASValue,orient='index')
        df_monitors_ASValues.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASValuesMonitors_'+rrc+'.txt',\
                    sep='|',header=None, index=True)

    # Unifico la información obtenida de cada uno de los colectores:
    Header_Comm_Monitors = ['Community','AS','Type']
    df_global = pd.DataFrame([], columns = Header_Comm_Monitors)
    for rrc in rrcs:
        file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASValuesMonitors_'+rrc+'.txt'
        df_rrc = pd.read_csv(file_read, sep='|',header=None, names=Header_Comm_Monitors);

        # Añado la información al df general:
        df_global = df_global.append(df_rrc, sort=False)

    # Guardamos el dataframe como txt:
    # (Eliminamos communities duplicadas)
    df_global.drop_duplicates(subset=Header_Comm_Monitors, keep='last',inplace = True)
    df_global.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASValuesMonitors_RRCs.txt',\
                        sep='|',header=None, index=None)

    print "Termina la ejecución: Hora -> ", asctime(localtime());
    elapsed_time = time() - start_time
    print("Tiempo de ejecucion: "+ str(elapsed_time))

    return None;

"""
Stage3: Para los casos en los cuales el AS Monitor (casi) siempre ve valores de
communities en sus anuncios, y además (casi) siempre el AS monitor ve communities
de sus ASes vecinos, identificar dichas communities y si son regulares o larges:
"""
def stage3():
    print "Comienza la ejecución Stage 3: Hora -> ", asctime(localtime());
    start_time = time()

    rrcs = ['rrc00.ripe','rrc01.ripe','rrc03.ripe','rrc04.ripe','rrc05.ripe','rrc06.ripe',\
            'rrc07.ripe','rrc10.ripe','rrc11.ripe','rrc12.ripe','rrc13.ripe','rrc14.ripe',\
            'rrc15.ripe','rrc16.ripe','rrc18.ripe','rrc19.ripe','rrc20.ripe','rrc21.ripe']

    Header = ['RRC_ID','ABW','IPMonitor','ASMonitor','AnnouncedPrefix',\
            'IPType','ASPATH','Neighbor','Communities','Large_Communities',\
            'ASesValuesComm','ASesComm'];

    Header_monitors = ['IPMonitor','RRC_ID','ASMonitor','Announced','Announced_Comm','PAnnounced_Comm',\
                        'TagAnnounced_Comm','Neighbors','Num_Neighbors','Announced_MonitorComm',\
                        'PAnnounced_MonitorComm','TagAnnounced_MonitorComm','Announced_NeighComm',\
                        'PAnnounced_NeighComm','TagAnnounced_NeighComm']

    for rrc in rrcs:
        print rrc
        file_read = '/srv/agarcia/TFM-BGP/Jesus/DATA/'+rrc+'.txt'
        df_rrc = pd.read_csv(file_read, sep='|',header=None, names=Header, dtype={"Neighbor": object});

        file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Monitors_'+rrc+'.txt'
        df_rrc_monitors = pd.read_csv(file_read, sep='|',header=None, names=Header_monitors);

        data_ASValue = get_neighbors_ASValues(df_rrc,df_rrc_monitors)
        df_neighbors_ASValues = pd.DataFrame.from_dict(data_ASValue,orient='index')
        df_neighbors_ASValues.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASValuesNeighbors_'+rrc+'.txt',\
                    sep='|',header=None, index=True)

    # Unifico la información obtenida de cada uno de los colectores:
    Header_Comm_Neigh = ['Community','AS','Type']
    df_global = pd.DataFrame([], columns = Header_Comm_Neigh)
    for rrc in rrcs:
        file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASValuesNeighbors_'+rrc+'.txt'
        df_rrc = pd.read_csv(file_read, sep='|',header=None, names=Header_Comm_Neigh);

        # Añado la información al df general:
        df_global = df_global.append(df_rrc, sort=False)

    # Guardamos el dataframe como txt:
    # (Eliminamos communities duplicadas)
    df_global.drop_duplicates(subset=Header_Comm_Neigh, keep='last',inplace = True)
    df_global.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASValuesNeighbors_RRCs.txt',\
                        sep='|',header=None, index=None)

    print "Termina la ejecución: Hora -> ", asctime(localtime());
    elapsed_time = time() - start_time
    print("Tiempo de ejecucion: "+ str(elapsed_time))

    return None;

"""
'stage4': Análisis de las communities regulares, tanto en los ASes monitores como
en los ASes vecinos a los monitores.
Generar df unicamente con las communities regulares.
"""
def stage4():
    print "Comienza la ejecución Stage 4: Hora -> ", asctime(localtime());
    start_time = time()

    def get_tagRFC(community):

        value_comm = int(community.split(":")[1])
        if value_comm == 0:
            tag_rfc = 'Category_RFC4384'
            tag_rfc_sign = 'Reserved_0'
        elif value_comm == 1:
            tag_rfc = 'Category_RFC4384'
            tag_rfc_sign = 'Customer Routes'
        elif value_comm == 2:
            tag_rfc = 'Category_RFC4384'
            tag_rfc_sign = 'Peer Routes'
        elif value_comm == 3:
            tag_rfc = 'Category_RFC4384'
            tag_rfc_sign = 'Internal Routes'
        elif value_comm == 4:
            tag_rfc = 'Category_RFC4384'
            tag_rfc_sign = 'Internal More Specific Routes'
        elif value_comm == 5:
            tag_rfc = 'Category_RFC4384'
            tag_rfc_sign = 'Special Purpose Routes'
        elif value_comm == 6:
            tag_rfc = 'Category_RFC4384'
            tag_rfc_sign = 'Upstream Routes'
        else:
            tag_rfc = 'Unknown'
            tag_rfc_sign = 'Unknown'

        # Si no ha macheado con ninguna de las anteriores, miro si es identificador de región:
        if tag_rfc == 'Unknown':
            community_binary = np.binary_repr(value_comm, width=16)
            comm = community_binary[:5]

            if comm == '00001':
                tag_rfc = 'Region Identifier'
                tag_rfc_sign = 'AF'
            elif comm == '00010':
                tag_rfc = 'Region Identifier'
                tag_rfc_sign = 'OC'
            elif comm == '00011':
                tag_rfc = 'Region Identifier'
                tag_rfc_sign = 'AS'
            elif comm == '00100':
                tag_rfc = 'Region Identifier'
                tag_rfc_sign = 'AQ'
            elif comm == '00101':
                tag_rfc = 'Region Identifier'
                tag_rfc_sign = 'EU'
            elif comm == '00110':
                tag_rfc = 'Region Identifier'
                tag_rfc_sign = 'LAC'
            elif comm == '00111':
                tag_rfc = 'Region Identifier'
                tag_rfc_sign = 'NA'
            else:
                tag_rfc = 'Unknown'
                tag_rfc_sign = 'Unknown'

        return tag_rfc, tag_rfc_sign;

    # Dataframe con la taxonomía seguida en el articulo 'On BGP Communities':
    Header = ['community','generaltype','subtype','subsubtype','characterization','comment']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/RFCs/taxonomy_database.txt'
    df_Taxonomy = pd.read_csv(file_read, sep='|', header=None, names=Header, index_col=False);
    df_Taxonomy.drop_duplicates(subset=Header, keep='last',inplace = True)
    df_Taxonomy.drop(['comment'],axis = 1)
    df_Taxonomy.drop_duplicates(subset=['community'],keep='last',inplace = True)

    Header_Comm_Monitors = ['Community','AS','Type'];
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASValuesMonitors_RRCs.txt'
    df_Comm_Monitores = pd.read_csv(file_read, sep='|',header=None, names=Header_Comm_Monitors);
    df_Comm_Monitores = df_Comm_Monitores[df_Comm_Monitores['Type'] == 'Regular']

    info_taxonomy = [];
    info_RFC = [];
    info_RFCSign = [];
    for index, row in df_Comm_Monitores.iterrows():

        community = row.Community

        df = df_Taxonomy[df_Taxonomy['community'] == community]
        if not df.empty:
            tag = 'Taxonomy_Found'
        else:
            tag = 'Taxonomy_NotFound'

        info_taxonomy.append(tag)

        tag_rfc, tag_rfc_sign = get_tagRFC(community)

        info_RFC.append(tag_rfc)
        info_RFCSign.append(tag_rfc_sign)

    df_Comm_Monitores.insert(3,'Taxonomy',info_taxonomy)
    df_Comm_Monitores.insert(4,'RFC',info_RFC)
    df_Comm_Monitores.insert(5,'RFC_Sign',info_RFCSign)

    df_Comm_Monitores = df_Comm_Monitores[['Community','AS','Type','Taxonomy','RFC','RFC_Sign']]

    df_Comm_Monitores.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASValuesMonitors_RRCs_RC.txt',\
                    sep='|',header=None, index=None)

    # Header_Comm_Neigh = ['Community','AS','Type'];
    # file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASValuesNeighbors_RRCs.txt'
    # df_Comm_Neigh = pd.read_csv(file_read, sep='|',header=None, names=Header_Comm_Monitors);
    # df_Comm_Neigh = df_Comm_Neigh[df_Comm_Neigh['Type'] == 'Regular']
    #
    # info_taxonomy = [];
    # info_RFC = [];
    # info_RFCSign = [];
    # for index, row in df_Comm_Neigh.iterrows():
    #
    #     community = row.Community
    #
    #     df = df_Taxonomy[df_Taxonomy['community'] == community]
    #     if not df.empty:
    #         tag = 'Taxonomy_Found'
    #     else:
    #         tag = 'Taxonomy_NotFound'
    #
    #     info_taxonomy.append(tag)
    #
    #     tag_rfc, tag_rfc_sign = get_tagRFC(community)
    #
    #     info_RFC.append(tag_rfc)
    #     info_RFCSign.append(tag_rfc_sign)
    #
    # df_Comm_Neigh.insert(3,'Taxonomy',info_taxonomy)
    # df_Comm_Neigh.insert(4,'RFC',info_RFC)
    # df_Comm_Neigh.insert(5,'RFC_Sign',info_RFCSign)
    #
    # df_Comm_Neigh = df_Comm_Neigh[['Community','AS','Type','Taxonomy','RFC','RFC_Sign']]
    #
    # df_Comm_Neigh.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASValuesNeighbors_RRCs_RC.txt',\
    #                 sep='|',header=None, index=None)

    print "Termina la ejecución: Hora -> ", asctime(localtime());
    elapsed_time = time() - start_time
    print("Tiempo de ejecucion: "+ str(elapsed_time))

    return None;

# =================================== Main() ===================================
# print "Stage 1:"
# stage1()
print "Stage 1b:"
stage_1b()
# print "Stage 2:"
# stage2()
# print "Stage 3:"
# stage3()
# print "Stage 4:"
# stage4();
