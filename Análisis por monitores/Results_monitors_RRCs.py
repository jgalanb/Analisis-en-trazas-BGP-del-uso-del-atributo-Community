#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Importación de librerias empleadas en el codigo:
"""
from __future__ import unicode_literals
import sys, re;
from os import *
import pandas as pd
import numpy as np
from time import time,localtime, asctime
import socket
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pylab import *
import collections

""" ============================= FUNCIONES ================================ """
"""
'analysis_IPMonitors':
    - ¿Cuantos IPMonitores distintos se han identificado?
    - ASes monitores con comportamiento distinto en colectores
        (Etiqueta de resultados distintos en ver communities, comm monitores o comm neighbors)
"""
def analysis_IPMonitors():

    Header_monitors = ['IPMonitor','RRC_ID','ASMonitor','Announced','Announced_Comm','PAnnounced_Comm',\
                        'TagAnnounced_Comm','Neighbors','Num_Neighbors','Announced_MonitorComm',\
                        'PAnnounced_MonitorComm','TagAnnounced_MonitorComm','Announced_NeighComm',\
                        'PAnnounced_NeighComm','TagAnnounced_NeighComm']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Monitors_RRCs.txt'
    df_IPMonitors = pd.read_csv(file_read, sep='|',header=None, names=Header_monitors);

    # ASesMonitores = list(df_IPMonitors.ASMonitor.unique())
    # df_ASesMonitores = df_IPMonitors.groupby('ASMonitor')
    #
    # for ASMonitor in ASesMonitores:
    #     df_ASMonitor = df_ASesMonitores.get_group(ASMonitor)
    #     tag_comm = list(df_ASMonitor.TagAnnounced_Comm.unique());
    #     if len(tag_comm) > 1:
    #         print ASMonitor;
    #         print list(df_ASMonitor.IPMonitor.unique());
    #         print list(df_ASMonitor.RRC_ID.unique());
    #         print tag_comm;
    #         print list(df_ASMonitor.TagAnnounced_Comm.unique());
    #         print ""
    #
    # sys.exit();

    # Lista de IPMonitors distintos en el total de colectores:
    IPMonitors = list(df_IPMonitors.IPMonitor.unique())
    print "Número total de IPMonitors: ", len(IPMonitors)

    return None;

"""
'analysis_ASMonitors':
    - ¿Cuantos ASes monitores distintos se encuentran en los colectores?
    - Rango y clasificación CAIDA para estos ASes monitores
    - ¿Cuantos ASes monitores engloban más de un IPMonitor?
    - ¿Qué ASes engloban más de un IPMonitor, y cuantos engloban?
"""
def analysis_ASMonitors():

    Header_ASesMonitors = ['ASMonitor','IPMonitors','Num_IPMonitors','RRCs','Num_RRCs',\
                            'Tag_Comm','Tag_Comm_Monitor','Tag_Comm_Neigh','Rango','CAIDA']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASMonitors_RRCs.txt'
    df_ASesMonitors = pd.read_csv(file_read, sep='|',header=None, names=Header_ASesMonitors);

    df = df_ASesMonitors[df_ASesMonitors['Num_IPMonitors'] > 1]
    df = df.sort_values(by='Num_IPMonitors', ascending=False)

    print "ASes que engloban más de un IPMonitor:"
    df_show = df[['ASMonitor','Num_IPMonitors']]
    print df_show;
    print ""

    # Rango de los ASes monitores:
    ASes_monitors_diff = list(df_ASesMonitors.ASMonitor.unique())
    df_TypeAS = df_ASesMonitors.groupby('Rango')
    Types_AS = list(df_ASesMonitors.Rango.unique())

    colums_df = ['Type_AS','ASes','%']
    df_print = pd.DataFrame([],columns = colums_df)

    for type_AS in Types_AS:
        info_type_AS = [];
        df = df_TypeAS.get_group(type_AS);
        list_ASes = list(df.ASMonitor.unique())

        info_type_AS.append(type_AS)
        info_type_AS.append(len(list_ASes))

        try:
            porcen = float(float(len(list_ASes))/float(len(ASes_monitors_diff)))
            porcen = float(porcen)*float(100);
        except ZeroDivisionError:
            porcen = 0.0;
        info_type_AS.append(porcen);

        df_inter = pd.DataFrame([info_type_AS],columns = colums_df)
        df_print = df_print.append(df_inter, sort=False)

    df_print = df_print.sort_values(by='%', ascending=False)
    print "Grah02"
    print df_print;
    print ""
    id_color = ['blue','red','darkblue']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Rango de los ASes monitores', fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah02.png',\
            bbox_inches = "tight");
    plt.close

    # Análisis CAIDA de los monitores:
    ASes_monitors_diff = list(df_ASesMonitors.ASMonitor.unique())
    df_TypeAS = df_ASesMonitors.groupby('CAIDA')
    Types_AS = list(df_ASesMonitors.CAIDA.unique())

    colums_df = ['Type_AS','ASes','%']
    df_print = pd.DataFrame([],columns = colums_df)

    for type_AS in Types_AS:
        info_type_AS = [];
        df = df_TypeAS.get_group(type_AS);
        list_ASes = list(df.ASMonitor.unique())

        info_type_AS.append(type_AS)
        info_type_AS.append(len(list_ASes))

        try:
            porcen = float(float(len(list_ASes))/float(len(ASes_monitors_diff)))
            porcen = float(porcen)*float(100);
        except ZeroDivisionError:
            porcen = 0.0;
        info_type_AS.append(porcen);

        df_inter = pd.DataFrame([info_type_AS],columns = colums_df)
        df_print = df_print.append(df_inter, sort=False)

    df_print = df_print.sort_values(by='%', ascending=False)
    print "Grah03"
    print df_print;
    print ""
    id_color = ['darkblue','darkblue','darkblue','red']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Clasificación CAIDA ASes monitores', fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah03.png',\
            bbox_inches = "tight");
    plt.close

    # Representación gráfica de ASes monitores que engloban más de un IPMonitor:

    result = [];
    # ¿Cuantos ASes engloban más de un IPMonitor?
    df = df_ASesMonitors[df_ASesMonitors['Num_IPMonitors'] > 1]
    result.append(len(df))
    # ¿Cuantos ASes engloban un único IPMonitor?
    df = df_ASesMonitors[df_ASesMonitors['Num_IPMonitors'] == 1]
    result.append(len(df))
    print "Grah04"
    print result;
    print ""

    # Representación gráfica:
    labels = ['Engloba más de un IP monitor','Solo engloba a un IP monitor']
    sizes = [result[0],result[1]]
    explode = (0.1,0)
    colors = ['yellowgreen','lightblue']

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors = colors, autopct='%1.1f%%',
            shadow=True, startangle=0)
    ax.axis('equal')

    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic')
    plt.suptitle('Porcentaje de ASes monitores que engloban más de un IP Monitor', fontsize=16, fontweight=0, \
                color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah04.png',\
            bbox_inches = "tight");
    plt.close

    # Porcentaje ocurrencia en la que los ASes monitores ven communities:
    result = len(list(df_ASesMonitors.ASMonitor.unique()))
    print "ASes monitores analizados en grah05: ",result
    result = [];
    df = df_ASesMonitors[df_ASesMonitors['Tag_Comm'] == 'Nunca']
    result.append(len(df))
    df = df_ASesMonitors[df_ASesMonitors['Tag_Comm'] == 'Alguna vez']
    result.append(len(df))
    df = df_ASesMonitors[df_ASesMonitors['Tag_Comm'] == 'Casi siempre']
    result.append(len(df))
    df = df_ASesMonitors[df_ASesMonitors['Tag_Comm'] == 'Siempre']
    result.append(len(df))
    print "Grah05"
    print result;
    print ""

    # Representación gráfica:
    labels = ['Nunca','Alguna vez','Casi siempre','Siempre']
    sizes = [result[0],result[1],result[2],result[3]]
    explode = (0,0,0,0)
    colors = ['tomato','yellowgreen','lightblue','blue']

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=45)
    ax.axis('equal')

    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Porcentaje de ocurrencia en que los ASes monitores ven communities', fontsize=16, fontweight=0, \
                color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah05.png',\
            bbox_inches = "tight");
    plt.close

    # Para los ASes monitores que alguna vez o (casi) siempre ven communities, porcentaje de
    # ocurrencia en la cual estos mismos ASes monitores ponen communities propias:
    df_ASesMonitors = df_ASesMonitors[df_ASesMonitors['Tag_Comm'] != 'Nunca']

    result = len(list(df_ASesMonitors.ASMonitor.unique()))
    print "ASes monitores analizados en grah06/07: ",result
    result = [];
    df = df_ASesMonitors[df_ASesMonitors['Tag_Comm_Monitor'] == 'Nunca']
    result.append(len(df))
    df = df_ASesMonitors[df_ASesMonitors['Tag_Comm_Monitor'] == 'Alguna vez']
    result.append(len(df))
    df = df_ASesMonitors[df_ASesMonitors['Tag_Comm_Monitor'] == 'Casi siempre']
    result.append(len(df))
    df = df_ASesMonitors[df_ASesMonitors['Tag_Comm_Monitor'] == 'Siempre']
    result.append(len(df))
    print "Grah06"
    print result;
    print ""

    # Representación gráfica:
    labels = ['Nunca','Alguna vez','Casi siempre','Siempre']
    sizes = [result[0],result[1],result[2],result[3]]
    explode = (0,0,0,0)
    colors = ['tomato','yellowgreen','lightblue','blue']

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax.axis('equal')

    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('ASes monitores que alguna vez/(casi) siempre ven communities, en qué porcentaje ponen communities propias',\
                fontsize=16, fontweight=0, color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah06.png',\
            bbox_inches = "tight");
    plt.close

    # Para los ASes monitores que alguna vez o (casi) siempre ven communities, en qué porcentaje
    # de ocurrencia, ven communities de sus vecinos:
    result = [];
    df = df_ASesMonitors[df_ASesMonitors['Tag_Comm_Neigh'] == 'Nunca']
    result.append(len(df))
    df = df_ASesMonitors[df_ASesMonitors['Tag_Comm_Neigh'] == 'Alguna vez']
    result.append(len(df))
    df = df_ASesMonitors[df_ASesMonitors['Tag_Comm_Neigh'] == 'Casi siempre']
    result.append(len(df))
    df = df_ASesMonitors[df_ASesMonitors['Tag_Comm_Neigh'] == 'Siempre']
    result.append(len(df))
    print "Grah07"
    print result;
    print ""

    # Representación gráfica:
    labels = ['Nunca','Alguna vez','Casi siempre','Siempre']
    sizes = [result[0],result[1],result[2],result[3]]
    explode = (0,0,0,0)
    colors = ['tomato','yellowgreen','lightblue','blue']

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=0)
    ax.axis('equal')

    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('ASes monitores que alguna vez/(casi) siempre ven communities, en qué porcentaje ven communities de sus vecinos',\
                fontsize=16, fontweight=0, color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah07.png',\
            bbox_inches = "tight");
    plt.close

    return None;

"""
'analysis_CommunitiesASMonitors':
    - Número total de ASes monitores
    - Communities distintas identificadas
    - Del total de communities, ¿cuantas son regular o large?
    - ASes que emplean communities regular, large o ambas
    - De los ASes que son large, cuantos ASes son mayores a 65535
    - Análisis de las regular communities:
        - Database 'On BGP Communities' y RFC4384
"""
def analysis_CommunitiesASMonitors():

    Header_Comm_Monitors = ['Community','AS','Type']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASValuesMonitors_RRCs.txt'
    df_CommunitiesMonitors = pd.read_csv(file_read, sep='|',header=None, names=Header_Comm_Monitors);

    result = [];
    df = df_CommunitiesMonitors[df_CommunitiesMonitors['Type'] == 'Regular']
    result.append(len(df))
    df = df_CommunitiesMonitors[df_CommunitiesMonitors['Type'] == 'Large']
    result.append(len(df))
    print "Grah08"
    print result;
    print ""

    # Representación gráfica:
    labels = ['Regular Communities','Large Communities']
    sizes = [result[0],result[1]]
    explode = (0.1,0)
    colors = ['azure','lightblue']

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors = colors, autopct='%1.1f%%',
            shadow=True, startangle=0)
    ax.axis('equal')

    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic')
    plt.suptitle('Porcentaje del tipo de communities puestas por los ASes monitores', fontsize=16, fontweight=0, \
                color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah08.png',\
            bbox_inches = "tight");
    plt.close

    # Analizar si los ASes monitores emplean regular communities, large communities o ambos:
    ASes_monitores = list(df_CommunitiesMonitors.AS.unique())

    data_AS = {};
    for AS in ASes_monitores:
        info = [];
        df = df_CommunitiesMonitors[df_CommunitiesMonitors['AS'] == int(AS)]
        tag = list(df.Type.unique())
        if len(tag) == 1:
            info.append(tag[0])
        elif len(tag) == 2:
            info.append('Ambas')
        else:
            print "Mmmm"
            sys.exit();

        data_AS.update({AS:info})

    df_tagComm = pd.DataFrame.from_dict(data_AS,orient='index')
    df_tagComm = df_tagComm.reset_index();
    df_tagComm = df_tagComm.rename(columns={'index': 'AS', 0: 'Tag'})

    df_show = df_tagComm[df_tagComm['Tag'] == 'Ambas']
    print df_show;
    print ""

    Header_Comm_Monitors = ['Community','AS','Type','Taxonomy','RFC','RFC_Sign']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASValuesMonitors_RRCs_RC.txt'
    df_CommunitiesMonitors = pd.read_csv(file_read, sep='|',header=None, names=Header_Comm_Monitors);
    df_CommunitiesMonitors = df_CommunitiesMonitors.fillna({'RFC_Sign':'NA'})

    result = [];
    # Pares AS:Comm que no machaan con el database:
    df = df_CommunitiesMonitors[df_CommunitiesMonitors['Taxonomy'] == 'Taxonomy_NotFound']
    result.append(len(df))
    # Pares AS:Comm que machean con el database:
    df = df_CommunitiesMonitors[df_CommunitiesMonitors['Taxonomy'] == 'Taxonomy_Found']
    result.append(len(df))
    print "Grah10"
    print result
    print ""

    # Representación gráfica:
    labels = ['AS:Comm no encontrados','AS:Comm encontrados']
    sizes = [result[0],result[1]]
    explode = (0,0.1)
    colors = ['coral','lightblue']

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels,colors = colors,  autopct='%1.1f%%',
            shadow=True, startangle=0)
    ax.axis('equal')

    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle("Porcentaje pares ASMonitor:Comm encontrados en el database 'On BGP Communities'", fontsize=16, fontweight=0, \
                color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah10.png',\
            bbox_inches = "tight");
    plt.close

    # Dataframe con la taxonomía seguida en el articulo 'On BGP Communities':
    Header = ['community','generaltype','subtype','subsubtype','characterization','comment']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/RFCs/taxonomy_database.txt'
    df_Taxonomy = pd.read_csv(file_read, sep='|', header=None, names=Header, index_col=False);
    df_Taxonomy.drop_duplicates(subset=Header, keep='last',inplace = True)
    df_Taxonomy.drop(['comment'],axis = 1)
    df_Taxonomy.drop_duplicates(subset=['community'],keep='last',inplace = True)

    # Analizo los pares AS:Comm que sí han macheado:
    df_Found = df_CommunitiesMonitors[df_CommunitiesMonitors['Taxonomy'] == 'Taxonomy_Found']
    columns_name = ['community','generaltype','subtype','subsubtype','characterization','comment']
    df_taxonomyMonitors = pd.DataFrame([],columns = columns_name)
    for Community in df_Found.Community:
        df = df_Taxonomy[df_Taxonomy['community'] == Community]
        df_taxonomyMonitors = df_taxonomyMonitors.append(df, sort=False)

    communities_diff = list(df_taxonomyMonitors.community.unique())
    df_TypeAS = df_taxonomyMonitors.groupby('generaltype')
    Types_AS = list(df_taxonomyMonitors.generaltype.unique())

    colums_df = ['Type_AS','ASes','%']
    df_print = pd.DataFrame([],columns = colums_df)

    for type_AS in Types_AS:
        info_type_AS = [];
        df = df_TypeAS.get_group(type_AS);
        list_communities = list(df.community.unique())

        info_type_AS.append(type_AS)
        info_type_AS.append(len(list_communities))

        try:
            porcen = float(float(len(list_communities))/float(len(communities_diff)))
            porcen = float(porcen)*float(100);
        except ZeroDivisionError:
            porcen = 0.0;
        info_type_AS.append(porcen);

        df_inter = pd.DataFrame([info_type_AS],columns = colums_df)
        df_print = df_print.append(df_inter, sort=False)

    df_print = df_print.sort_values(by='%', ascending=False)
    print "Grah11"
    print df_print
    print ""
    id_color = ['darkgreen','darkblue']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle("Clasificación taxonomía pares ASMonitor:Comm", fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 70)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah11.png',\
            bbox_inches = "tight");
    plt.close

    # Clasificación inbound para los AS:Comm encontrados:
    df_inbound = df_taxonomyMonitors[df_taxonomyMonitors['generaltype'] == 'inbound']

    communities_diff = list(df_inbound.community.unique())
    df_TypeAS = df_inbound.groupby('subtype')
    Types_AS = list(df_inbound.subtype.unique())

    colums_df = ['Type_AS','ASes','%']
    df_print = pd.DataFrame([],columns = colums_df)

    for type_AS in Types_AS:
        info_type_AS = [];
        df = df_TypeAS.get_group(type_AS);
        list_communities = list(df.community.unique())

        info_type_AS.append(type_AS)
        info_type_AS.append(len(list_communities))

        try:
            porcen = float(float(len(list_communities))/float(len(communities_diff)))
            porcen = float(porcen)*float(100);
        except ZeroDivisionError:
            porcen = 0.0;
        info_type_AS.append(porcen);

        df_inter = pd.DataFrame([info_type_AS],columns = colums_df)
        df_print = df_print.append(df_inter, sort=False)

    df_print = df_print.sort_values(by='%', ascending=False)
    print "Grah12"
    print df_print
    print ""
    id_color = ['darkgreen','darkgreen']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle("Clasificación taxonomía 'inbound' pares ASMonitor:Comm", fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah12.png',\
            bbox_inches = "tight");
    plt.close

    # Clasificación outbound para los AS:Comm encontrados:
    df_outbound = df_taxonomyMonitors[df_taxonomyMonitors['generaltype'] == 'outbound']

    communities_diff = list(df_outbound.community.unique())
    df_TypeAS = df_outbound.groupby('subsubtype')
    Types_AS = list(df_outbound.subsubtype.unique())

    colums_df = ['Type_AS','ASes','%']
    df_print = pd.DataFrame([],columns = colums_df)

    for type_AS in Types_AS:
        info_type_AS = [];
        df = df_TypeAS.get_group(type_AS);
        list_communities = list(df.community.unique())

        info_type_AS.append(type_AS)
        info_type_AS.append(len(list_communities))

        try:
            porcen = float(float(len(list_communities))/float(len(communities_diff)))
            porcen = float(porcen)*float(100);
        except ZeroDivisionError:
            porcen = 0.0;
        info_type_AS.append(porcen);

        df_inter = pd.DataFrame([info_type_AS],columns = colums_df)
        df_print = df_print.append(df_inter, sort=False)

    df_print = df_print.sort_values(by='%', ascending=False)
    print "Grah13"
    print df_print
    print ""
    id_color = ['darkblue','darkblue','darkblue']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle("Clasificación taxonomía 'outbound' pares ASMonitor:Comm", fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 60)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah13.png',\
            bbox_inches = "tight");
    plt.close

    # Análisis RFC:
    #   - ¿Cuantos pares AS:Comm se encuentran en la RFC?

    result = [];
    df = df_CommunitiesMonitors[df_CommunitiesMonitors['RFC'] == 'Unknown']
    result.append(len(df))
    df = df_CommunitiesMonitors[df_CommunitiesMonitors['RFC'] == 'Category_RFC4384']
    result.append(len(df))
    df = df_CommunitiesMonitors[df_CommunitiesMonitors['RFC'] == 'Region Identifier']
    result.append(len(df))
    print "Grah18"
    print result
    print ""

    # Representación gráfica:
    labels = ['AS:Comm desconocida','AS:Comm Categoria RFC','AS:Comm Identificador de región']
    sizes = [result[0],result[1],result[2]]
    explode = (0,0,0)
    colors = ['tomato','blue','lightblue']

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels,colors = colors,  autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax.axis('equal')

    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle("Porcentaje pares ASMonitor:Comm que coinciden con 'RFC4384'", fontsize=16, fontweight=0, \
                color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah18.png',\
            bbox_inches = "tight");
    plt.close

    # Para aquellos pares que han matchado con la categoria RFC:
    df_CategoryRFC = df_CommunitiesMonitors[df_CommunitiesMonitors['RFC'] == 'Category_RFC4384']

    communities_diff = list(df_CategoryRFC.Community.unique())
    df_TypeAS = df_CategoryRFC.groupby('RFC_Sign')
    Types_AS = list(df_CategoryRFC.RFC_Sign.unique())

    colums_df = ['Type_AS','ASes','%']
    df_print = pd.DataFrame([],columns = colums_df)

    for type_AS in Types_AS:
        info_type_AS = [];
        df = df_TypeAS.get_group(type_AS);
        list_communities = list(df.Community.unique())

        info_type_AS.append(type_AS)
        info_type_AS.append(len(list_communities))

        try:
            porcen = float(float(len(list_communities))/float(len(communities_diff)))
            porcen = float(porcen)*float(100);
        except ZeroDivisionError:
            porcen = 0.0;
        info_type_AS.append(porcen);

        df_inter = pd.DataFrame([info_type_AS],columns = colums_df)
        df_print = df_print.append(df_inter, sort=False)

    df_print = df_print.sort_values(by='%', ascending=False)
    print "Grah19"
    print df_print;
    print ""
    id_color = ['blue','blue','blue','blue','blue','blue','blue']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=90, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Categoria RFC pares ASMonitor:Comm', fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel('Categoria')
    plt.ylabel('%')
    plt.ylim(0, 35)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah19.png',\
            bbox_inches = "tight");
    plt.close

    # Para aquellos pares que han matcheado con el identificador de región:
    df_RegionRFC = df_CommunitiesMonitors[df_CommunitiesMonitors['RFC'] == 'Region Identifier']

    communities_diff = list(df_RegionRFC.Community.unique())
    df_TypeAS = df_RegionRFC.groupby('RFC_Sign')
    Types_AS = list(df_RegionRFC.RFC_Sign.unique())

    colums_df = ['Type_AS','ASes','%']
    df_print = pd.DataFrame([],columns = colums_df)

    for type_AS in Types_AS:
        info_type_AS = [];
        df = df_TypeAS.get_group(type_AS);
        list_communities = list(df.Community.unique())

        info_type_AS.append(type_AS)
        info_type_AS.append(len(list_communities))

        try:
            porcen = float(float(len(list_communities))/float(len(communities_diff)))
            porcen = float(porcen)*float(100);
        except ZeroDivisionError:
            porcen = 0.0;
        info_type_AS.append(porcen);

        df_inter = pd.DataFrame([info_type_AS],columns = colums_df)
        df_print = df_print.append(df_inter, sort=False)

    df_print = df_print.sort_values(by='%', ascending=False)
    print "Grah20"
    print df_print;
    print ""
    id_color = ['blue','blue','blue','blue','blue','blue','blue']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Identificador de región pares ASMonitor:Comm', fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel('Categoria')
    plt.ylabel('%')
    plt.ylim(0, 35)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah20.png',\
            bbox_inches = "tight");
    plt.close

    return None;

"""
'analysis_CommunitiesASNeighbors':
    - Número total de ASes vecinos
    - Communities distintas identificadas
    - Del total de communities, ¿cuantas son regular o large?
    - ASes que emplean communities regular, large o ambas
    - De los ASes que son large, cuantos ASes son mayores a 65535
    - Análisis de las regular communities:
        - Database 'On BGP Communities' y RFC4384
"""
def analysis_CommunitiesASNeighbors():

    Header_Comm_Neigh = ['Community','AS','Type']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASValuesNeighbors_RRCs.txt'
    df_CommunitiesNeigh = pd.read_csv(file_read, sep='|',header=None, names=Header_Comm_Neigh);

    result = [];
    # ¿Cuantos ASes engloban más de un IPMonitor?
    df = df_CommunitiesNeigh[df_CommunitiesNeigh['Type'] == 'Regular']
    result.append(len(df))
    # ¿Cuantos ASes engloban un único IPMonitor?
    df = df_CommunitiesNeigh[df_CommunitiesNeigh['Type'] == 'Large']
    result.append(len(df))
    print "Grah09"
    print result;
    print ""

    # Representación gráfica:
    labels = ['Regular Communities','Large Communities']
    sizes = [result[0],result[1]]
    explode = (0.1,0)
    colors = ['azure','lightblue']

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors = colors, autopct='%1.1f%%',
            shadow=True, startangle=0)
    ax.axis('equal')

    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic')
    plt.suptitle('Porcentaje del tipo de communities puestas por los ASes vecinos', fontsize=16, fontweight=0, \
                color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah09.png',\
            bbox_inches = "tight");
    plt.close

    # Analizar si los ASes vecinos emplean regular communities, large communities o ambos:
    ASes_neighbors = list(df_CommunitiesNeigh.AS.unique())

    data_AS = {};
    for AS in ASes_neighbors:
        info = [];
        df = df_CommunitiesNeigh[df_CommunitiesNeigh['AS'] == int(AS)]
        tag = list(df.Type.unique())
        if len(tag) == 1:
            info.append(tag[0])
        elif len(tag) == 2:
            info.append('Ambas')
        else:
            print "Mmmm"
            sys.exit();

        data_AS.update({AS:info})

    df_tagComm = pd.DataFrame.from_dict(data_AS,orient='index')
    df_tagComm = df_tagComm.reset_index();
    df_tagComm = df_tagComm.rename(columns={'index': 'AS', 0: 'Tag'})

    df_show = df_tagComm[df_tagComm['Tag'] == 'Ambas']

    Header_Comm_Neigh = ['Community','AS','Type','Taxonomy','RFC','RFC_Sign']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASValuesNeighbors_RRCs_RC.txt'
    df_Comm_Neigh = pd.read_csv(file_read, sep='|',header=None, names=Header_Comm_Neigh);
    df_Comm_Neigh = df_Comm_Neigh.fillna({'RFC_Sign':'NA'})

    result = [];
    # Pares AS:Comm que no machaan con el database:
    df = df_Comm_Neigh[df_Comm_Neigh['Taxonomy'] == 'Taxonomy_NotFound']
    result.append(len(df))
    # Pares AS:Comm que machean con el database:
    df = df_Comm_Neigh[df_Comm_Neigh['Taxonomy'] == 'Taxonomy_Found']
    result.append(len(df))
    print "Grah14"
    print result
    print ""

    # Representación gráfica:
    labels = ['AS:Comm no encontrados','AS:Comm encontrados']
    sizes = [result[0],result[1]]
    explode = (0,0.1)
    colors = ['coral','lightblue']

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels,colors = colors,  autopct='%1.1f%%',
            shadow=True, startangle=0)
    ax.axis('equal')

    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle("Porcentaje pares ASVecino:Comm encontrados en el database 'On BGP Communities'", fontsize=16, fontweight=0, \
                color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah14.png',\
            bbox_inches = "tight");
    plt.close

    # Dataframe con la taxonomía seguida en el articulo 'On BGP Communities':
    Header = ['community','generaltype','subtype','subsubtype','characterization','comment']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/RFCs/taxonomy_database.txt'
    df_Taxonomy = pd.read_csv(file_read, sep='|', header=None, names=Header, index_col=False);
    df_Taxonomy.drop_duplicates(subset=Header, keep='last',inplace = True)
    df_Taxonomy.drop(['comment'],axis = 1)
    df_Taxonomy.drop_duplicates(subset=['community'],keep='last',inplace = True)

    # Analizo los pares AS:Comm que sí han macheado:
    df_Found = df_Comm_Neigh[df_Comm_Neigh['Taxonomy'] == 'Taxonomy_Found']
    columns_name = ['community','generaltype','subtype','subsubtype','characterization','comment']
    df_taxonomyNeigh = pd.DataFrame([],columns = columns_name)
    for community in df_Found.Community:
        df = df_Taxonomy[df_Taxonomy['community'] == community]
        df_taxonomyNeigh = df_taxonomyNeigh.append(df, sort=False)

    communities_diff = list(df_taxonomyNeigh.community.unique())
    df_TypeAS = df_taxonomyNeigh.groupby('generaltype')
    Types_AS = list(df_taxonomyNeigh.generaltype.unique())

    colums_df = ['Type_AS','ASes','%']
    df_print = pd.DataFrame([],columns = colums_df)

    for type_AS in Types_AS:
        info_type_AS = [];
        df = df_TypeAS.get_group(type_AS);
        list_communities = list(df.community.unique())

        info_type_AS.append(type_AS)
        info_type_AS.append(len(list_communities))

        try:
            porcen = float(float(len(list_communities))/float(len(communities_diff)))
            porcen = float(porcen)*float(100);
        except ZeroDivisionError:
            porcen = 0.0;
        info_type_AS.append(porcen);

        df_inter = pd.DataFrame([info_type_AS],columns = colums_df)
        df_print = df_print.append(df_inter, sort=False)

    df_print = df_print.sort_values(by='%', ascending=False)
    print "Grah15"
    print df_print
    print ""
    id_color = ['darkgreen','darkblue']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle("Clasificacion taxonomía pares ASVecino:Comm", fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah15.png',\
            bbox_inches = "tight");
    plt.close

    # Clasificación inbound para los AS:Comm encontrados:
    df_inbound = df_taxonomyNeigh[df_taxonomyNeigh['generaltype'] == 'inbound']

    communities_diff = list(df_inbound.community.unique())
    df_TypeAS = df_inbound.groupby('subtype')
    Types_AS = list(df_inbound.subtype.unique())

    colums_df = ['Type_AS','ASes','%']
    df_print = pd.DataFrame([],columns = colums_df)

    for type_AS in Types_AS:
        info_type_AS = [];
        df = df_TypeAS.get_group(type_AS);
        list_communities = list(df.community.unique())

        info_type_AS.append(type_AS)
        info_type_AS.append(len(list_communities))

        try:
            porcen = float(float(len(list_communities))/float(len(communities_diff)))
            porcen = float(porcen)*float(100);
        except ZeroDivisionError:
            porcen = 0.0;
        info_type_AS.append(porcen);

        df_inter = pd.DataFrame([info_type_AS],columns = colums_df)
        df_print = df_print.append(df_inter, sort=False)

    df_print = df_print.sort_values(by='%', ascending=False)
    print "Grah16"
    print df_print
    print ""
    id_color = ['darkgreen','darkgreen']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle("Clasificacion taxonomía 'inbound' pares ASVecino:Comm", fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah16.png',\
            bbox_inches = "tight");
    plt.close

    # Clasificación outbound para los AS:Comm encontrados:
    df_outbound = df_taxonomyNeigh[df_taxonomyNeigh['generaltype'] == 'outbound']

    communities_diff = list(df_outbound.community.unique())
    df_TypeAS = df_outbound.groupby('subsubtype')
    Types_AS = list(df_outbound.subsubtype.unique())

    colums_df = ['Type_AS','ASes','%']
    df_print = pd.DataFrame([],columns = colums_df)

    for type_AS in Types_AS:
        info_type_AS = [];
        df = df_TypeAS.get_group(type_AS);
        list_communities = list(df.community.unique())

        info_type_AS.append(type_AS)
        info_type_AS.append(len(list_communities))

        try:
            porcen = float(float(len(list_communities))/float(len(communities_diff)))
            porcen = float(porcen)*float(100);
        except ZeroDivisionError:
            porcen = 0.0;
        info_type_AS.append(porcen);

        df_inter = pd.DataFrame([info_type_AS],columns = colums_df)
        df_print = df_print.append(df_inter, sort=False)

    df_print = df_print.sort_values(by='%', ascending=False)
    print "Grah17"
    print df_print
    print ""
    id_color = ['darkblue','darkblue','darkblue']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle("Clasificacion taxonomía 'outbound' pares ASVecino:Comm", fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah17.png',\
            bbox_inches = "tight");
    plt.close

    # Análisis RFC:
    #   - ¿Cuantos pares AS:Comm se encuentran en la RFC?

    result = [];
    df = df_Comm_Neigh[df_Comm_Neigh['RFC'] == 'Unknown']
    result.append(len(df))
    df = df_Comm_Neigh[df_Comm_Neigh['RFC'] == 'Category_RFC4384']
    result.append(len(df))
    df = df_Comm_Neigh[df_Comm_Neigh['RFC'] == 'Region Identifier']
    result.append(len(df))
    print "Grah21"
    print result
    print ""

    # Representación gráfica:
    labels = ['AS:Comm desconocida','AS:Comm Categoria RFC','AS:Comm Identificador de región']
    sizes = [result[0],result[1],result[2]]
    explode = (0,0,0)
    colors = ['tomato','blue','lightblue']

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels,colors = colors,  autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax.axis('equal')

    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle("Porcentaje pares ASVecino:Comm que coinciden con 'RFC4384'", fontsize=16, fontweight=0, \
                color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah21.png',\
            bbox_inches = "tight");
    plt.close

    # Para aquellos pares que han matchado con la categoria RFC:
    df_CategoryRFC = df_Comm_Neigh[df_Comm_Neigh['RFC'] == 'Category_RFC4384']

    communities_diff = list(df_CategoryRFC.Community.unique())
    df_TypeAS = df_CategoryRFC.groupby('RFC_Sign')
    Types_AS = list(df_CategoryRFC.RFC_Sign.unique())

    colums_df = ['Type_AS','ASes','%']
    df_print = pd.DataFrame([],columns = colums_df)

    for type_AS in Types_AS:
        info_type_AS = [];
        df = df_TypeAS.get_group(type_AS);
        list_communities = list(df.Community.unique())

        info_type_AS.append(type_AS)
        info_type_AS.append(len(list_communities))

        try:
            porcen = float(float(len(list_communities))/float(len(communities_diff)))
            porcen = float(porcen)*float(100);
        except ZeroDivisionError:
            porcen = 0.0;
        info_type_AS.append(porcen);

        df_inter = pd.DataFrame([info_type_AS],columns = colums_df)
        df_print = df_print.append(df_inter, sort=False)

    df_print = df_print.sort_values(by='%', ascending=False)
    print "Grah22"
    print df_print;
    print ""
    id_color = ['blue','blue','blue','blue','blue','blue','blue']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=90, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Categoria RFC pares ASVecino:Comm', fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel('Categoria')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah22.png',\
            bbox_inches = "tight");
    plt.close

    # Para aquellos pares que han matcheado con el identificador de región:
    df_RegionRFC = df_Comm_Neigh[df_Comm_Neigh['RFC'] == 'Region Identifier']

    communities_diff = list(df_RegionRFC.Community.unique())
    df_TypeAS = df_RegionRFC.groupby('RFC_Sign')
    Types_AS = list(df_RegionRFC.RFC_Sign.unique())

    colums_df = ['Type_AS','ASes','%']
    df_print = pd.DataFrame([],columns = colums_df)

    for type_AS in Types_AS:
        info_type_AS = [];
        df = df_TypeAS.get_group(type_AS);
        list_communities = list(df.Community.unique())

        info_type_AS.append(type_AS)
        info_type_AS.append(len(list_communities))

        try:
            porcen = float(float(len(list_communities))/float(len(communities_diff)))
            porcen = float(porcen)*float(100);
        except ZeroDivisionError:
            porcen = 0.0;
        info_type_AS.append(porcen);

        df_inter = pd.DataFrame([info_type_AS],columns = colums_df)
        df_print = df_print.append(df_inter, sort=False)

    df_print = df_print.sort_values(by='%', ascending=False)
    print "Grah23"
    print df_print;
    print ""
    id_color = ['blue','blue','blue','blue','blue','blue','blue']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Identificador de región pares ASVecino:Comm', fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel('Categoria')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/Graficas/grah23.png',\
            bbox_inches = "tight");
    plt.close

    return None;

"""
'analysis_RegionIden':
    - ASes monitores
    - ASes vecinos
"""
def analysis_RegionIden():

    Header_Comm_Monitors = ['Community','AS','Type','Taxonomy','RFC','RFC_Sign']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASValuesMonitors_RRCs_RC.txt'
    df_CommunitiesMonitors = pd.read_csv(file_read, sep='|',header=None, names=Header_Comm_Monitors);
    df_CommunitiesMonitors = df_CommunitiesMonitors.fillna({'RFC_Sign':'NA'})

    Header = ['Region','CC','CC_binary']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/RFCs/Country_Code.txt'
    df_CC = pd.read_csv(file_read, sep='|',header=None, names=Header,dtype={"CC_binary": str});
    df_CC = df_CC.fillna({'Region':'NA'})

    region_iden = ['AF','OC','AS','AQ','EU','LAC','NA']

    data_region = {};
    list_ASesValues_matchean = [];
    for region in region_iden:
        info = [];

        # ¿Cuantas country codes se han idenficado en la región?
        df_CC_region = df_CC[df_CC['Region'] == region]
        info.append(len(df_CC_region))

        list_CC = list(df_CC_region.CC_binary)

        # Pares AS:Comm distintos identificados en la región:
        df_ASValues = df_CommunitiesMonitors[df_CommunitiesMonitors['RFC_Sign'] == region]
        info.append(len(df_ASValues))

        ASesValues = list(df_ASValues.Community)

        # Para cada ASValue, determinar si los siguientes bits son todo ceros, están
        # en la lista de CC, o son desconocidos
        all_zeros = 0
        matchea_CC = 0
        unknown = 0
        for ASValue in ASesValues:
            Value_Comm = int(ASValue.split(':')[1])
            community_binary = np.binary_repr(Value_Comm, width=16)
            community_binary = community_binary[6:]

            if community_binary == '0000000000':
                all_zeros = all_zeros + 1
            elif community_binary in list_CC:
                matchea_CC = matchea_CC + 1
                list_ASesValues_matchean.append(ASValue)
            else:
                unknown = unknown + 1

        info.append(all_zeros)
        info.append(matchea_CC)
        info.append(unknown)

        data_region.update({region:info})

    df_region_result = pd.DataFrame.from_dict(data_region,orient='index')
    print df_region_result;
    # df_region_result.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASValuesNeighbors_RRCs_RC_Region.txt',\
    #             sep='|',header=None, index=True)

    # Analizo si los valores de communities que coinciden son del mismo AS:
    list_ASes = [];
    for ASValue in list_ASesValues_matchean:
        AS = ASValue.split(":")[0]
        list_ASes.append(AS)

    counter_ASesComm = collections.Counter(list_ASes)
    df = pd.DataFrame.from_dict(counter_ASesComm, orient='index').reset_index()
    df = df.rename(columns={'index': 'AS', 0: 'Tag'})
    df = df.sort_values(by='Tag', ascending=False)

    print df;

    df_show = df_CommunitiesMonitors[df_CommunitiesMonitors['RFC'] == 'Region Identifier']
    df_show = df_show[df_show['AS'] == int(12956)]

    print df_show;

    return None;

# =================================== Main() ===================================
print "Comienza la ejecución: Hora -> ", asctime(localtime());
start_time = time()

"""
'analysis_IPMonitors': Estudio y análisis de los IPMonitores:
"""
analysis_IPMonitors()

"""
'analysis_ASMonitors': Estudio y análisis de los ASes monitores:
"""
analysis_ASMonitors()

"""
'analysis_CommunitiesASMonitors': Estudio y análisis de las distintas communities
anunciadas en el caso de que los ASes monitores casi siempre/siempre vean communities,
además de determinar que casi siempre/siempre estos ASes monitores ponen communities propias:
"""
analysis_CommunitiesASMonitors();

"""
'analysis_CommunitiesASNeighbors':Estudio y análisis de las distintas communities
anunciadas en el caso de que los ASes monitores casi siempre/siempre vean communities,
además de determinar que casi siempre/siempre ven communities de sus vecinos:
"""
# analysis_CommunitiesASNeighbors();

"""
'analysis_RegionIden': Comprobar para los casos de AF, AS, EU y NA que los CC
coinciden con los vistos:
"""
# analysis_RegionIden();

print "Termina la ejecución: Hora -> ", asctime(localtime());
elapsed_time = time() - start_time
print("Tiempo de ejecucion: "+ str(elapsed_time))
