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
'analysis_ASes_ClasiGeneral':
    - ASes que fueron vistos solo como origen, tránsito, monitor... o combinación
      de ello
    - ASes cuyo valor de AS < 65535, = 65535, > 65535
"""
def analysis_ASes_ClasiGeneral():

    Header = ['AS','ClasiGeneral']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASes_ClasiGeneral.txt'
    df_ClasiGeneral = pd.read_csv(file_read, sep='|',header=None, names = Header);

    # Clasificación de los ASes:
    ASes_diff = list(df_ClasiGeneral.AS.unique())
    df_TypeAS = df_ClasiGeneral.groupby('ClasiGeneral')
    Types_AS = list(df_ClasiGeneral.ClasiGeneral.unique())

    colums_df = ['Type_AS','ASes','Porcentaje']
    df_print = pd.DataFrame([],columns = colums_df)

    for type_AS in Types_AS:
        info_type_AS = [];
        df = df_TypeAS.get_group(type_AS);
        list_ASes = list(df.AS.unique())

        if type_AS == 'Origen/Transito':
            type_AS = 'Origen/Tránsito'
        elif type_AS == 'Transito':
            type_AS = 'Tránsito'
        elif type_AS == 'Monitor/Transito/Origen':
            type_AS = 'Monitor/Tránsito/Origen'

        info_type_AS.append(type_AS)
        info_type_AS.append(len(list_ASes))

        try:
            porcen = float(float(len(list_ASes))/float(len(ASes_diff)))
            porcen = float(porcen)*float(100);
        except ZeroDivisionError:
            porcen = 0.0;
        info_type_AS.append(porcen);

        df_inter = pd.DataFrame([info_type_AS],columns = colums_df)
        df_print = df_print.append(df_inter, sort=False)

    df_print = df_print.sort_values(by='Porcentaje', ascending=False)
    print "Grah01"
    print df_print
    print ""
    id_color = ['navy','navy','navy','navy','navy']
    df_print.plot(kind='bar',x='Type_AS', y= 'Porcentaje', rot=45, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Clasificación ASes colectores', fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah01.png',bbox_inches = "tight");
    plt.close

    # Porcentaje de ASes que superan el valor 65535:
    info = [];
    df = df_ClasiGeneral[df_ClasiGeneral['AS'] <= 65535]
    info.append(len(df))
    df = df_ClasiGeneral[df_ClasiGeneral['AS'] > 65535]
    info.append(len(df))
    print "Grah02"
    print info
    print ""

    labels = ['ASes 16 bits','ASes 32 bits']
    sizes = [info[0],info[1]]
    explode = (0,0.1)
    colors = ['lightblue','tomato']

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=0)
    ax.axis('equal')

    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Porcentaje ASes 16 bits y 32 bits',\
                fontsize=16, fontweight=0, color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah02.png',bbox_inches = "tight");
    plt.close

    return None;

"""
'analysis_CAIDA':
    - CAIDA para ASes que solo fueron vistos como origen
    - CAIDA para ASes que alguna vez he visto como tránsito
"""
def analysis_CAIDA():

    Header = ['AS','ClasiGeneral','CAIDA']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASes_CAIDA.txt'
    df_ClasiCAIDA = pd.read_csv(file_read, sep='|',header=None, names=Header);

    df_Origen = df_ClasiCAIDA[df_ClasiCAIDA['ClasiGeneral'] == 'Origen']
    df_Transito = df_ClasiCAIDA[df_ClasiCAIDA['ClasiGeneral'].str.contains('Transito')]

    # Análisis CAIDA ASes solo vistos como origen:
    ASes_diff = list(df_Origen.AS.unique())
    df_TypeAS = df_Origen.groupby('CAIDA')
    Types_AS = list(df_Origen.CAIDA.unique())

    colums_df = ['Type_AS','ASes','Porcentaje']
    df_print = pd.DataFrame([],columns = colums_df)

    for type_AS in Types_AS:
        info_type_AS = [];
        df = df_TypeAS.get_group(type_AS);
        list_ASes = list(df.AS.unique())

        info_type_AS.append(type_AS)
        info_type_AS.append(len(list_ASes))

        try:
            porcen = float(float(len(list_ASes))/float(len(ASes_diff)))
            porcen = float(porcen)*float(100);
        except ZeroDivisionError:
            porcen = 0.0;
        info_type_AS.append(porcen);

        df_inter = pd.DataFrame([info_type_AS],columns = colums_df)
        df_print = df_print.append(df_inter, sort=False)

    df_print = df_print.sort_values(by='Porcentaje', ascending=False)
    print "Grah03"
    print df_print
    print ""
    id_color = ['darkblue','darkblue','darkblue','red']
    df_print.plot(kind='bar',x='Type_AS', y= 'Porcentaje', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Clasificación CAIDA ASes solo vistos como origen', fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah03.png',bbox_inches = "tight");
    plt.close

    # Análisis CAIDA ASes vistos alguna vez como tránsito:
    ASes_diff = list(df_Transito.AS.unique())
    df_TypeAS = df_Transito.groupby('CAIDA')
    Types_AS = list(df_Transito.CAIDA.unique())

    colums_df = ['Type_AS','ASes','Porcentaje']
    df_print = pd.DataFrame([],columns = colums_df)

    for type_AS in Types_AS:
        info_type_AS = [];
        df = df_TypeAS.get_group(type_AS);
        list_ASes = list(df.AS.unique())

        info_type_AS.append(type_AS)
        info_type_AS.append(len(list_ASes))

        try:
            porcen = float(float(len(list_ASes))/float(len(ASes_diff)))
            porcen = float(porcen)*float(100);
        except ZeroDivisionError:
            porcen = 0.0;
        info_type_AS.append(porcen);

        df_inter = pd.DataFrame([info_type_AS],columns = colums_df)
        df_print = df_print.append(df_inter, sort=False)

    df_print = df_print.sort_values(by='Porcentaje', ascending=False)
    print "Grah04"
    print df_print
    print ""
    id_color = ['darkblue','darkblue','darkblue','red']
    df_print.plot(kind='bar',x='Type_AS', y= 'Porcentaje', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Clasificación CAIDA ASes vistos alguna vez como tránsito', fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah04.png',bbox_inches = "tight");
    plt.close

    return None;

"""
'analysis_RangoASes':
    - Rango para ASes que solo fueron vistos como origen
    - Rango para ASes que alguna vez he visto como tránsito
"""
def analysis_RangoASes():

    Header = ['AS','ClasiGeneral','Rango']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASesRango_RRCs.txt'
    df_ASesRango = pd.read_csv(file_read, sep='|',header=None, names = Header);

    # ASes que solo haya visto como origen:
    df_ASesOrigen = df_ASesRango[df_ASesRango['ClasiGeneral'] == 'Origen']

    ASes_diff = list(df_ASesOrigen.AS.unique())
    df_TypeAS = df_ASesOrigen.groupby('Rango')
    Types_AS = list(df_ASesOrigen.Rango.unique())

    colums_df = ['Type_AS','ASes','Porcentaje']
    df_print = pd.DataFrame([],columns = colums_df)

    for type_AS in Types_AS:
        info_type_AS = [];
        df = df_TypeAS.get_group(type_AS);
        list_ASes = list(df.AS.unique())

        info_type_AS.append(type_AS)
        info_type_AS.append(len(list_ASes))

        try:
            porcen = float(float(len(list_ASes))/float(len(ASes_diff)))
            porcen = float(porcen)*float(100);
        except ZeroDivisionError:
            porcen = 0.0;
        info_type_AS.append(porcen);

        df_inter = pd.DataFrame([info_type_AS],columns = colums_df)
        df_print = df_print.append(df_inter, sort=False)

    df_print = df_print.sort_values(by='Porcentaje', ascending=False)
    print 'grah05'
    print df_print
    print ""
    id_color = ['blue','red','darkblue','yellow','blue']
    df_print.plot(kind='bar',x='Type_AS', y= 'Porcentaje', rot=45, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Rango de los ASes vistos solo como origen', fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah05.png',bbox_inches = "tight");
    plt.close

    # ASes que alguna vez haya visto como tránsito
    df_ASesOrigen = df_ASesRango[df_ASesRango['ClasiGeneral'].str.contains('Transito')]

    ASes_diff = list(df_ASesOrigen.AS.unique())
    df_TypeAS = df_ASesOrigen.groupby('Rango')
    Types_AS = list(df_ASesOrigen.Rango.unique())

    colums_df = ['Type_AS','ASes','Porcentaje']
    df_print = pd.DataFrame([],columns = colums_df)

    for type_AS in Types_AS:
        info_type_AS = [];
        df = df_TypeAS.get_group(type_AS);
        list_ASes = list(df.AS.unique())

        info_type_AS.append(type_AS)
        info_type_AS.append(len(list_ASes))

        try:
            porcen = float(float(len(list_ASes))/float(len(ASes_diff)))
            porcen = float(porcen)*float(100);
        except ZeroDivisionError:
            porcen = 0.0;
        info_type_AS.append(porcen);

        df_inter = pd.DataFrame([info_type_AS],columns = colums_df)
        df_print = df_print.append(df_inter, sort=False)

    df_print = df_print.sort_values(by='Porcentaje', ascending=False)
    print 'grah06'
    print df_print
    print ""
    id_color = ['blue','red','darkblue','yellow','blue']
    df_print.plot(kind='bar',x='Type_AS', y= 'Porcentaje', rot=45, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Rango de los ASes vistos alguna vez como tránsito', fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah06.png',bbox_inches = "tight");
    plt.close

    return None;

"""
'analysis_ASes':
    - Porcentaje de ASes que nunca/alguna vez/(casi) siempre ponen communities propias
"""
def analysis_ASes():

    Header = ['AS','ClasiGeneral','count_aspaths','count_aspaths_comm','porcentaje_comm',\
                'tag_comm','ValuesComm']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Info_ASes_RRCs.txt'
    df_ASes = pd.read_csv(file_read, sep='|',header=None, names = Header);

    ASes_diff = list(df_ASes.AS.unique())
    df_TypeAS = df_ASes.groupby('tag_comm')
    Types_AS = list(df_ASes.tag_comm.unique())

    colums_df = ['Type_AS','ASes','Porcentaje']
    df_print = pd.DataFrame([],columns = colums_df)

    for type_AS in Types_AS:
        info_type_AS = [];
        df = df_TypeAS.get_group(type_AS);
        list_ASes = list(df.AS.unique())

        info_type_AS.append(type_AS)
        info_type_AS.append(len(list_ASes))

        try:
            porcen = float(float(len(list_ASes))/float(len(ASes_diff)))
            porcen = float(porcen)*float(100);
        except ZeroDivisionError:
            porcen = 0.0;
        info_type_AS.append(porcen);

        df_inter = pd.DataFrame([info_type_AS],columns = colums_df)
        df_print = df_print.append(df_inter, sort=False)

    df_print = df_print.sort_values(by='Porcentaje', ascending=False)
    print "Grah07"
    print df_print
    print ""
    id_color = ['red','green','lightblue','blue']
    df_print.plot(kind='bar',x='Type_AS', y= 'Porcentaje', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Porcentaje de ocurrencia en que los ASes ponen communities propias', fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah07.png',bbox_inches = "tight");
    plt.close

    return None;

"""
'analysis_CommASes':
    -
"""
def analysis_CommASes():

    Header = ['Community','AS','Type']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASValueComm_RRCs.txt'
    df_Comm = pd.read_csv(file_read, sep='|',header=None, names = Header);

    result = [];
    df = df_Comm[df_Comm['Type'] == 'Regular']
    result.append(len(df))
    df = df_Comm[df_Comm['Type'] == 'Large']
    result.append(len(df))
    print "Grah08"
    print result;
    print ""

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
    plt.suptitle('Porcentaje del tipo de communities puestas por los ASes', fontsize=16, fontweight=0, \
                color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah08.png',\
            bbox_inches = "tight");
    plt.close

    # Analizar si los ASes emplean regular communities, large communities o ambos:
    ASes = list(df_Comm.AS.unique())

    data_AS = {};
    for AS in ASes:
        info = [];
        df = df_Comm[df_Comm['AS'] == int(AS)]
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
    print "ASes que emplean tanto LC como RC:"
    print df_show;
    print ""

    # Analizo Regular Communities:
    #   - 'On BGP communities' Database
    #   - RFC 4384

    Header = ['Community','AS','Type','Taxonomy','RFC','RFC_Sign']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASValueComm_RRCs_RC.txt'
    df_Comm = pd.read_csv(file_read, sep='|',header=None, names=Header);
    df_Comm = df_Comm.fillna({'RFC_Sign':'NA'})

    result = [];
    # Pares AS:Comm que no machaan con el database:
    df = df_Comm[df_Comm['Taxonomy'] == 'Taxonomy_NotFound']
    result.append(len(df))
    # Pares AS:Comm que machean con el database:
    df = df_Comm[df_Comm['Taxonomy'] == 'Taxonomy_Found']
    result.append(len(df))
    print "Grah09"
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
    plt.suptitle("Porcentaje pares AS:Comm encontrados en el database 'On BGP Communities'", fontsize=16, fontweight=0, \
                color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah09.png',\
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
    df_Found = df_Comm[df_Comm['Taxonomy'] == 'Taxonomy_Found']
    columns_name = ['community','generaltype','subtype','subsubtype','characterization','comment']
    df_taxonomyComm = pd.DataFrame([],columns = columns_name)
    for Community in df_Found.Community:
        df = df_Taxonomy[df_Taxonomy['community'] == Community]
        df_taxonomyComm = df_taxonomyComm.append(df, sort=False)

    communities_diff = list(df_taxonomyComm.community.unique())
    df_TypeAS = df_taxonomyComm.groupby('generaltype')
    Types_AS = list(df_taxonomyComm.generaltype.unique())

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
    print "Grah10"
    print df_print
    print ""
    id_color = ['darkgreen','darkblue']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle("Clasificación taxonomía pares AS:Comm", fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 60)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah10.png',\
            bbox_inches = "tight");
    plt.close

    # Clasificación inbound para los AS:Comm encontrados:
    df_inbound = df_taxonomyComm[df_taxonomyComm['generaltype'] == 'inbound']

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
    print "Grah11"
    print df_print
    print ""
    id_color = ['darkgreen','darkgreen']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle("Clasificación taxonomía 'inbound' pares AS:Comm", fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah11.png',\
            bbox_inches = "tight");
    plt.close

    # Clasificación outbound para los AS:Comm encontrados:
    df_outbound = df_taxonomyComm[df_taxonomyComm['generaltype'] == 'outbound']

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
    print "Grah12"
    print df_print
    print ""
    id_color = ['darkblue','darkblue','darkblue']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle("Clasificación taxonomía 'outbound' pares AS:Comm", fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 60)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah12.png',\
            bbox_inches = "tight");
    plt.close

    # Análisis RFC:
    #   - ¿Cuantos pares AS:Comm se encuentran en la RFC?

    result = [];
    df = df_Comm[df_Comm['RFC'] == 'Unknown']
    result.append(len(df))
    df = df_Comm[df_Comm['RFC'] == 'Category_RFC4384']
    result.append(len(df))
    df = df_Comm[df_Comm['RFC'] == 'Region Identifier']
    result.append(len(df))
    print "Grah13"
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
    plt.suptitle("Porcentaje pares AS:Comm que coinciden con 'RFC4384'", fontsize=16, fontweight=0, \
                color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah13.png',\
            bbox_inches = "tight");
    plt.close

    # Para aquellos pares que han matchado con la categoria RFC:
    df_CategoryRFC = df_Comm[df_Comm['RFC'] == 'Category_RFC4384']

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
    print "Grah14"
    print df_print;
    print ""
    id_color = ['blue','blue','blue','blue','blue','blue','blue']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=90, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Categoria RFC pares AS:Comm', fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel('Categoria')
    plt.ylabel('%')
    plt.ylim(0, 40)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah14.png',\
            bbox_inches = "tight");
    plt.close

    # Para aquellos pares que han matcheado con el identificador de región:
    df_RegionRFC = df_Comm[df_Comm['RFC'] == 'Region Identifier']

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
    print "Grah15"
    print df_print;
    print ""
    id_color = ['blue','blue','blue','blue','blue','blue','blue']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Identificador de región pares AS:Comm', fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel('Categoria')
    plt.ylabel('%')
    plt.ylim(0, 40)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah15.png',\
            bbox_inches = "tight");
    plt.close

    return None;

"""
'analysis_CommASesOrigen':
    -
"""
def analysis_CommASesOrigen():

    Header = ['Community','AS','Type']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASOrigenValueComm_RRCs.txt'
    df_Comm = pd.read_csv(file_read, sep='|',header=None, names = Header);

    result = [];
    df = df_Comm[df_Comm['Type'] == 'Regular']
    result.append(len(df))
    df = df_Comm[df_Comm['Type'] == 'Large']
    result.append(len(df))
    print "Grah16"
    print result;
    print ""

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
    plt.suptitle('Porcentaje del tipo de communities puestas por los ASes solo vistos como origen',\
                fontsize=16, fontweight=0,color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah16.png',\
            bbox_inches = "tight");
    plt.close

    # Analizar si los ASes emplean regular communities, large communities o ambos:
    ASes = list(df_Comm.AS.unique())

    data_AS = {};
    for AS in ASes:
        info = [];
        df = df_Comm[df_Comm['AS'] == int(AS)]
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
    print "ASes solo vistos como origen que emplean tanto LC como RC:"
    print df_show;
    print ""

    # Analizo Regular Communities:
    #   - 'On BGP communities' Database
    #   - RFC 4384

    Header = ['Community','AS','Type','Taxonomy','RFC','RFC_Sign']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASOrigenValueComm_RRCs_RC.txt'
    df_Comm = pd.read_csv(file_read, sep='|',header=None, names=Header);
    df_Comm = df_Comm.fillna({'RFC_Sign':'NA'})

    result = [];
    # Pares AS:Comm que no machaan con el database:
    df = df_Comm[df_Comm['Taxonomy'] == 'Taxonomy_NotFound']
    result.append(len(df))
    # Pares AS:Comm que machean con el database:
    df = df_Comm[df_Comm['Taxonomy'] == 'Taxonomy_Found']
    result.append(len(df))
    print "Grah17"
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
    plt.suptitle("Porcentaje pares ASOrigen:Comm encontrados en el database 'On BGP Communities'", fontsize=16, fontweight=0, \
                color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah17.png',\
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
    df_Found = df_Comm[df_Comm['Taxonomy'] == 'Taxonomy_Found']
    columns_name = ['community','generaltype','subtype','subsubtype','characterization','comment']
    df_taxonomyComm = pd.DataFrame([],columns = columns_name)
    for Community in df_Found.Community:
        df = df_Taxonomy[df_Taxonomy['community'] == Community]
        df_taxonomyComm = df_taxonomyComm.append(df, sort=False)

    communities_diff = list(df_taxonomyComm.community.unique())
    df_TypeAS = df_taxonomyComm.groupby('generaltype')
    Types_AS = list(df_taxonomyComm.generaltype.unique())

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
    print "Grah18"
    print df_print
    print ""
    id_color = ['darkgreen','darkblue']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle("Clasificacion taxonomía pares ASOrigen:Comm", fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah18.png',\
            bbox_inches = "tight");
    plt.close

    # Clasificación inbound para los AS:Comm encontrados:
    df_inbound = df_taxonomyComm[df_taxonomyComm['generaltype'] == 'inbound']

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
    print "Grah19"
    print df_print
    print ""
    id_color = ['darkgreen','darkgreen']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle("Clasificacion taxonomía 'inbound' pares ASOrigen:Comm", fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah19.png',\
            bbox_inches = "tight");
    plt.close

    # Clasificación outbound para los AS:Comm encontrados:
    df_outbound = df_taxonomyComm[df_taxonomyComm['generaltype'] == 'outbound']

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
    print "Grah20"
    print df_print
    print ""
    id_color = ['darkblue','darkblue','darkblue']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle("Clasificacion taxonomía 'outbound' pares ASOrigen:Comm", fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah20.png',\
            bbox_inches = "tight");
    plt.close

    # Análisis RFC:
    #   - ¿Cuantos pares AS:Comm se encuentran en la RFC?

    result = [];
    df = df_Comm[df_Comm['RFC'] == 'Unknown']
    result.append(len(df))
    df = df_Comm[df_Comm['RFC'] == 'Category_RFC4384']
    result.append(len(df))
    df = df_Comm[df_Comm['RFC'] == 'Region Identifier']
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
    plt.suptitle("Porcentaje pares ASOrigen:Comm que coinciden con 'RFC4384'", fontsize=16, fontweight=0, \
                color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah21.png',\
            bbox_inches = "tight");
    plt.close

    # Para aquellos pares que han matchado con la categoria RFC:
    df_CategoryRFC = df_Comm[df_Comm['RFC'] == 'Category_RFC4384']

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
    plt.suptitle('Categoria RFC pares ASOrigen:Comm', fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel('Categoria')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah22.png',\
            bbox_inches = "tight");
    plt.close

    # Para aquellos pares que han matcheado con el identificador de región:
    df_RegionRFC = df_Comm[df_Comm['RFC'] == 'Region Identifier']

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
    plt.suptitle('Identificador de región pares ASOrigen:Comm', fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel('Categoria')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah23.png',\
            bbox_inches = "tight");
    plt.close

    return None;

"""
'analysis_CommASesTransito':
    -
"""
def analysis_CommASesTransito():

    Header = ['Community','AS','Type']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASTransitoValueComm_RRCs.txt'
    df_Comm = pd.read_csv(file_read, sep='|',header=None, names = Header);

    result = [];
    df = df_Comm[df_Comm['Type'] == 'Regular']
    result.append(len(df))
    df = df_Comm[df_Comm['Type'] == 'Large']
    result.append(len(df))
    print "Grah24"
    print result;
    print ""

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
    plt.suptitle('Porcentaje del tipo de communities puestas por los ASes vistos alguna vez como tránsito',\
                fontsize=16, fontweight=0,color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah24.png',\
            bbox_inches = "tight");
    plt.close

    # Analizar si los ASes emplean regular communities, large communities o ambos:
    ASes = list(df_Comm.AS.unique())

    data_AS = {};
    for AS in ASes:
        info = [];
        df = df_Comm[df_Comm['AS'] == int(AS)]
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
    print "ASes alguna vez vistos como tránsito que emplean tanto LC como RC:"
    print df_show;
    print ""

    # Analizo Regular Communities:
    #   - 'On BGP communities' Database
    #   - RFC 4384

    Header = ['Community','AS','Type','Taxonomy','RFC','RFC_Sign']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASTransitoValueComm_RRCs_RC.txt'
    df_Comm = pd.read_csv(file_read, sep='|',header=None, names=Header);
    df_Comm = df_Comm.fillna({'RFC_Sign':'NA'})

    result = [];
    # Pares AS:Comm que no machaan con el database:
    df = df_Comm[df_Comm['Taxonomy'] == 'Taxonomy_NotFound']
    result.append(len(df))
    # Pares AS:Comm que machean con el database:
    df = df_Comm[df_Comm['Taxonomy'] == 'Taxonomy_Found']
    result.append(len(df))
    print "Grah25"
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
    plt.suptitle("Porcentaje pares ASTránsito:Comm encontrados en el database 'On BGP Communities'", fontsize=16, fontweight=0, \
                color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah25.png',\
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
    df_Found = df_Comm[df_Comm['Taxonomy'] == 'Taxonomy_Found']
    columns_name = ['community','generaltype','subtype','subsubtype','characterization','comment']
    df_taxonomyComm = pd.DataFrame([],columns = columns_name)
    for Community in df_Found.Community:
        df = df_Taxonomy[df_Taxonomy['community'] == Community]
        df_taxonomyComm = df_taxonomyComm.append(df, sort=False)

    communities_diff = list(df_taxonomyComm.community.unique())
    df_TypeAS = df_taxonomyComm.groupby('generaltype')
    Types_AS = list(df_taxonomyComm.generaltype.unique())

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
    print "Grah26"
    print df_print
    print ""
    id_color = ['darkgreen','darkblue']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle("Clasificacion taxonomía pares ASTránsito:Comm", fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah26.png',\
            bbox_inches = "tight");
    plt.close

    # Clasificación inbound para los AS:Comm encontrados:
    df_inbound = df_taxonomyComm[df_taxonomyComm['generaltype'] == 'inbound']

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
    print "Grah27"
    print df_print
    print ""
    id_color = ['darkgreen','darkgreen']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle("Clasificacion taxonomía 'inbound' pares ASTránsito:Comm", fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah27.png',\
            bbox_inches = "tight");
    plt.close

    # Clasificación outbound para los AS:Comm encontrados:
    df_outbound = df_taxonomyComm[df_taxonomyComm['generaltype'] == 'outbound']

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
    print "Grah28"
    print df_print
    print ""
    id_color = ['darkblue','darkblue','darkblue']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle("Clasificacion taxonomía 'outbound' pares ASTránsito:Comm", fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel(' ')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah28.png',\
            bbox_inches = "tight");
    plt.close

    # Análisis RFC:
    #   - ¿Cuantos pares AS:Comm se encuentran en la RFC?

    result = [];
    df = df_Comm[df_Comm['RFC'] == 'Unknown']
    result.append(len(df))
    df = df_Comm[df_Comm['RFC'] == 'Category_RFC4384']
    result.append(len(df))
    df = df_Comm[df_Comm['RFC'] == 'Region Identifier']
    result.append(len(df))
    print "Grah29"
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
    plt.suptitle("Porcentaje pares ASTránsito:Comm que coinciden con 'RFC4384'", fontsize=16, fontweight=0, \
                color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah29.png',\
            bbox_inches = "tight");
    plt.close

    # Para aquellos pares que han matchado con la categoria RFC:
    df_CategoryRFC = df_Comm[df_Comm['RFC'] == 'Category_RFC4384']

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
    print "Grah30"
    print df_print;
    print ""
    id_color = ['blue','blue','blue','blue','blue','blue','blue']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=90, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Categoria RFC pares ASTránsito:Comm', fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel('Categoria')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah30.png',\
            bbox_inches = "tight");
    plt.close

    # Para aquellos pares que han matcheado con el identificador de región:
    df_RegionRFC = df_Comm[df_Comm['RFC'] == 'Region Identifier']

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
    print "Grah31"
    print df_print;
    print ""
    id_color = ['blue','blue','blue','blue','blue','blue','blue']
    df_print.plot(kind='bar',x='Type_AS', y= '%', rot=0, fontsize=10,\
                align='center',color=id_color, edgecolor='none',legend=False);
    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Identificador de región pares ASTránsito:Comm', fontsize=16, fontweight=0, \
                color='black', style='italic')
    plt.xlabel('Categoria')
    plt.ylabel('%')
    plt.ylim(0, 100)
    plt.grid();

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Graficas/grah31.png',\
            bbox_inches = "tight");
    plt.close

    return None;

# =================================== Main() ===================================
print "Comienza la ejecución: Hora -> ", asctime(localtime());
start_time = time()

# analysis_ASes_ClasiGeneral();
# analysis_CAIDA();
# analysis_RangoASes();
analysis_ASes();
analysis_CommASes();
# analysis_CommASesOrigen();
# analysis_CommASesTransito();


print "Termina la ejecución: Hora -> ", asctime(localtime());
elapsed_time = time() - start_time
print("Tiempo de ejecucion: "+ str(elapsed_time))
