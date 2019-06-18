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


""" ============================= FUNCIONES ================================ """
"""
Preguntas a responder:
    - ¿Cuantos ASPATHs se encuentran en el dataframe?
    - ¿Cuantos ASPATHs distintos se encuentran en el dataframe?
    - ¿Cuantos ASPATHs se ven en más de un colector? Porcentaje de ello.
    - ¿Cuantas rutas diferentes se encuentran en el dataframe?
    - Porcentaje de ASPATHs en los que nunca/alguna vez/(casi) siempre se ven communities
    - Porcentaje de ASPATHs cuyos valores de communities machean con los ASes del ASPATH
    - (Analizar las posibles combinaciones de lo anterior)
    - Porcentaje de ASPATHs cuyos valores de communities no machean con los ASes del ASPATH
    - (Analizar las posibles combinaciones de lo anterior)
    - Porcentaje de ASPATHs cuyos valores de communities alguna vez machean con los ASes del ASPATH
    - (Analizar las posibles combinaciones de lo anterior)
"""
def analysis_ASPATHs_rrcs():

    Header_ASPATHs = ['ASPATH_Original','RRC_ID','count_Announced','count_Announced_Comm','Pcount_Announced_Comm',\
            'Tag_count_Announced_Comm','Tag_Prep','ASPATH','long_ruta','Clasi_ASes','Communities',\
            'ASes_Comm','ASesASPATH_Comm','Hops_Comm','iden_ASes_aspath','Range_ASes_aspath',\
            'iden_ASes_comm','Range_ASes_comm','Macheo_ASes_aspath_comm']

    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_RRCs.txt'
    df_aspaths = pd.read_csv(file_read, sep='|',header=None, names=Header_ASPATHs);

    #Columnas dataframe necesarias para este análisis:
    df_aspaths = df_aspaths[['ASPATH_Original','RRC_ID','Tag_count_Announced_Comm','ASPATH',\
                    'iden_ASes_aspath','Range_ASes_aspath','iden_ASes_comm','Range_ASes_comm',\
                    'Macheo_ASes_aspath_comm']]

    print "Cantidad de ASPATHs encontrados en el total de RRCs:"
    print len(df_aspaths)
    print ""
    print "Cantidad de ASPATHs distintos encontrados en el total de RRCs:"
    aspaths_diff = list(df_aspaths.ASPATH_Original.unique())
    print len(aspaths_diff)
    print ""
    print "Cantidad de rutas distintas encontradas en el total de RRCs:"
    rutas_diff = list(df_aspaths.ASPATH.unique())
    print len(rutas_diff)
    print ""

    # Analizar el porcentaje de ASPATHs que se ven en más de un colector:
    df_ASPATHs_diff = df_aspaths.groupby('ASPATH_Original')
    data_aspath = {}
    for aspath in aspaths_diff:
        info = [];
        df = df_ASPATHs_diff.get_group(aspath)
        count_rrcs = list(df.RRC_ID.unique())
        info.append(len(count_rrcs))

        data_aspath.update({aspath:info})

    df_ASPATHs_diff = pd.DataFrame.from_dict(data_aspath,orient='index')
    df_ASPATHs_diff = df_ASPATHs_diff.reset_index();
    df_ASPATHs_diff = df_ASPATHs_diff.rename(columns={'index': 'ASPATH', 0: 'Count_RRCs'})
    df_count_aspaths = df_ASPATHs_diff[df_ASPATHs_diff['Count_RRCs'] > 1]
    print "Cantidad de ASPATHs que se ven en más de un colector:"
    print len(df_count_aspaths)
    print ""

    # Porcentaje de cantidad de ASPATHs que se ven en más de un colector:
    porcentaje = float(len(df_count_aspaths))/float(len(aspaths_diff))
    porcentaje = float(porcentaje)*float(100)
    porcentaje = "{0:.3f}".format(porcentaje)
    print "Porcentaje de ASPATHs que se ven en más de un colector:"
    print porcentaje
    print ""

    # Porcentaje de ASPATHs que nunca/alguna vez/(casi) siempre ven communities:
    tags = list(df_aspaths.Tag_count_Announced_Comm.unique())
    df_tags = df_aspaths.groupby('Tag_count_Announced_Comm')
    data_tag_comm = {};
    for tag in tags:
        info = [];
        df = df_tags.get_group(tag)
        info.append(len(df))

        porcentaje = float(len(df))/float(len(df_aspaths))
        porcentaje = float(porcentaje)*float(100)
        porcentaje = "{0:.3f}".format(porcentaje)
        info.append(porcentaje)

        data_tag_comm.update({tag:info})

    df_result = pd.DataFrame.from_dict(data_tag_comm,orient='index')
    print df_result
    print ""
    df_result.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/Result_1.txt',\
                        sep='|',header=None, index=True)

    # Porcentaje de ASPATHs que mapean sus valores de communities con los ASes del ASPATH:
    # (Filtrar por aquellos ASPATHS que alguna vez/(casi) siempre vean communities)
    df_comm = df_aspaths[df_aspaths['Tag_count_Announced_Comm'] != 'Nunca']
    tags = list(df_comm.Macheo_ASes_aspath_comm.unique())
    df_tags = df_comm.groupby('Macheo_ASes_aspath_comm')
    data_tag_mapeo = {};
    for tag in tags:
        info = [];
        df = df_tags.get_group(tag)
        info.append(len(df))

        porcentaje = float(len(df))/float(len(df_comm))
        porcentaje = float(porcentaje)*float(100)
        porcentaje = "{0:.3f}".format(porcentaje)
        info.append(porcentaje)

        data_tag_mapeo.update({tag:info})

    df_result = pd.DataFrame.from_dict(data_tag_mapeo,orient='index')
    print df_result
    print ""
    df_result.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/Result_2.txt',\
                        sep='|',header=None, index=True)

    # Analizo aquellos ASPATHs-Comm que matchean:
    df_matchean = df_comm[df_comm['Macheo_ASes_aspath_comm'] == 'Matchean']
    print "ASPATHs-Comm que matchean:"
    count_aspaths_machean = len(df_matchean)
    print count_aspaths_machean
    print ""

    print "Combinaciones analizadas que matchean:"
    comb_iden_ASes_aspath = list(df_matchean.iden_ASes_aspath.unique())
    comb_Range_ASes_aspath = list(df_matchean.Range_ASes_aspath.unique())
    comb_iden_ASes_comm = list(df_matchean.iden_ASes_comm.unique())
    comb_Range_ASes_comm = list(df_matchean.Range_ASes_comm.unique())

    data_comb = {};
    comb = 1;
    for iden_aspath in comb_iden_ASes_aspath:
        for rango_aspath in comb_Range_ASes_aspath:
            for iden_comm in comb_iden_ASes_comm:
                for rango_comm in comb_Range_ASes_comm:
                    info = [];
                    info.append(iden_aspath)
                    info.append(rango_aspath)
                    info.append(iden_comm)
                    info.append(rango_comm)

                    data_comb.update({comb:info})
                    comb = comb + 1

    df = pd.DataFrame.from_dict(data_comb,orient='index')
    df = df.reset_index();
    df_combinations = df.rename(columns={'index': 'Comb', 0: 'iden_aspath',1:'rango_aspath',\
                        2:'iden_comm',3:'rango_comm'})
    print df_combinations;

    # Analizo las combinaciones anteriores:
    comb = 1;
    data_mapea = {};
    for combination in range(0,len(df_combinations)):
        info = [];
        df_comb = df_combinations[df_combinations['Comb'] == comb]
        iden_aspath_item = df_comb.iden_aspath.item();
        rango_aspath_item = df_comb.rango_aspath.item();
        iden_comm_item = df_comb.iden_comm.item();
        rango_comm_item = df_comb.rango_comm.item();

        info.append(iden_aspath_item)
        info.append(rango_aspath_item)
        info.append(iden_comm_item)
        info.append(rango_comm_item)

        # Busco cuantos ASPATHs se encuentran bajo cada combinación posible:
        df_result_comb = df_matchean[df_matchean['iden_ASes_aspath'] == iden_aspath_item]
        df_result_comb = df_result_comb[df_result_comb['Range_ASes_aspath'] == rango_aspath_item]
        df_result_comb = df_result_comb[df_result_comb['iden_ASes_comm'] == iden_comm_item]
        df_result_comb = df_result_comb[df_result_comb['Range_ASes_comm'] == rango_comm_item]
        info.append(len(df_result_comb))

        porcentaje = float(len(df_result_comb))/float(count_aspaths_machean)
        porcentaje = float(porcentaje)*float(100)
        porcentaje = "{0:.3f}".format(porcentaje)
        info.append(porcentaje)

        data_mapea.update({comb:info})
        comb = comb + 1;

    df_result = pd.DataFrame.from_dict(data_mapea,orient='index')
    print df_result
    print ""
    df_result.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/Result_3.txt',\
                        sep='|',header=None, index=True)


    # Analizo aquellos ASPATHs-Comm que alguna vez matchean:
    df_algunavez_matchean = df_comm[df_comm['Macheo_ASes_aspath_comm'] == 'Alguna vez matchean']
    print "ASPATHs-Comm que alguna vez matchean:"
    count_aspaths_algunavez_machean = len(df_algunavez_matchean)
    print count_aspaths_algunavez_machean
    print ""

    print "Combinaciones analizadas que alguna vez matchean:"
    comb_iden_ASes_aspath = list(df_algunavez_matchean.iden_ASes_aspath.unique())
    comb_Range_ASes_aspath = list(df_algunavez_matchean.Range_ASes_aspath.unique())
    comb_iden_ASes_comm = list(df_algunavez_matchean.iden_ASes_comm.unique())
    comb_Range_ASes_comm = list(df_algunavez_matchean.Range_ASes_comm.unique())

    data_comb = {};
    comb = 1;
    for iden_aspath in comb_iden_ASes_aspath:
        for rango_aspath in comb_Range_ASes_aspath:
            for iden_comm in comb_iden_ASes_comm:
                for rango_comm in comb_Range_ASes_comm:
                    info = [];
                    info.append(iden_aspath)
                    info.append(rango_aspath)
                    info.append(iden_comm)
                    info.append(rango_comm)

                    data_comb.update({comb:info})
                    comb = comb + 1

    df = pd.DataFrame.from_dict(data_comb,orient='index')
    df = df.reset_index();
    df_combinations = df.rename(columns={'index': 'Comb', 0: 'iden_aspath',1:'rango_aspath',\
                        2:'iden_comm',3:'rango_comm'})
    print df_combinations;

    # Analizo las combinaciones anteriores:
    comb = 1;
    data_mapea = {};
    for combination in range(0,len(df_combinations)):
        info = [];
        df_comb = df_combinations[df_combinations['Comb'] == comb]
        iden_aspath_item = df_comb.iden_aspath.item();
        rango_aspath_item = df_comb.rango_aspath.item();
        iden_comm_item = df_comb.iden_comm.item();
        rango_comm_item = df_comb.rango_comm.item();

        info.append(iden_aspath_item)
        info.append(rango_aspath_item)
        info.append(iden_comm_item)
        info.append(rango_comm_item)

        # Busco cuantos ASPATHs se encuentran bajo cada combinación posible:
        df_result_comb = df_algunavez_matchean[df_algunavez_matchean['iden_ASes_aspath'] == iden_aspath_item]
        df_result_comb = df_result_comb[df_result_comb['Range_ASes_aspath'] == rango_aspath_item]
        df_result_comb = df_result_comb[df_result_comb['iden_ASes_comm'] == iden_comm_item]
        df_result_comb = df_result_comb[df_result_comb['Range_ASes_comm'] == rango_comm_item]
        info.append(len(df_result_comb))

        porcentaje = float(len(df_result_comb))/float(count_aspaths_algunavez_machean)
        porcentaje = float(porcentaje)*float(100)
        porcentaje = "{0:.3f}".format(porcentaje)
        info.append(porcentaje)

        data_mapea.update({comb:info})
        comb = comb + 1;

    df_result = pd.DataFrame.from_dict(data_mapea,orient='index')
    print df_result
    print ""
    df_result.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/Result_4.txt',\
                        sep='|',header=None, index=True)

    # Analizo aquellos ASPATHs-Comm que nunca matchean:
    df_no_matchean = df_comm[df_comm['Macheo_ASes_aspath_comm'] == 'No matchean']
    print "ASPATHs-Comm que no matchean:"
    count_aspaths_no_machean = len(df_no_matchean)
    print count_aspaths_no_machean
    print ""

    print "Combinaciones analizadas que no matchean:"
    comb_iden_ASes_aspath = list(df_no_matchean.iden_ASes_aspath.unique())
    comb_Range_ASes_aspath = list(df_no_matchean.Range_ASes_aspath.unique())
    comb_iden_ASes_comm = list(df_no_matchean.iden_ASes_comm.unique())
    comb_Range_ASes_comm = list(df_no_matchean.Range_ASes_comm.unique())

    data_comb = {};
    comb = 1;
    for iden_aspath in comb_iden_ASes_aspath:
        for rango_aspath in comb_Range_ASes_aspath:
            for iden_comm in comb_iden_ASes_comm:
                for rango_comm in comb_Range_ASes_comm:
                    info = [];
                    info.append(iden_aspath)
                    info.append(rango_aspath)
                    info.append(iden_comm)
                    info.append(rango_comm)

                    data_comb.update({comb:info})
                    comb = comb + 1

    df = pd.DataFrame.from_dict(data_comb,orient='index')
    df = df.reset_index();
    df_combinations = df.rename(columns={'index': 'Comb', 0: 'iden_aspath',1:'rango_aspath',\
                        2:'iden_comm',3:'rango_comm'})
    print df_combinations;

    # Analizo las combinaciones anteriores:
    comb = 1;
    data_mapea = {};
    for combination in range(0,len(df_combinations)):
        info = [];
        df_comb = df_combinations[df_combinations['Comb'] == comb]
        iden_aspath_item = df_comb.iden_aspath.item();
        rango_aspath_item = df_comb.rango_aspath.item();
        iden_comm_item = df_comb.iden_comm.item();
        rango_comm_item = df_comb.rango_comm.item();

        info.append(iden_aspath_item)
        info.append(rango_aspath_item)
        info.append(iden_comm_item)
        info.append(rango_comm_item)

        # Busco cuantos ASPATHs se encuentran bajo cada combinación posible:
        df_result_comb = df_no_matchean[df_no_matchean['iden_ASes_aspath'] == iden_aspath_item]
        df_result_comb = df_result_comb[df_result_comb['Range_ASes_aspath'] == rango_aspath_item]
        df_result_comb = df_result_comb[df_result_comb['iden_ASes_comm'] == iden_comm_item]
        df_result_comb = df_result_comb[df_result_comb['Range_ASes_comm'] == rango_comm_item]
        info.append(len(df_result_comb))

        porcentaje = float(len(df_result_comb))/float(count_aspaths_no_machean)
        porcentaje = float(porcentaje)*float(100)
        porcentaje = "{0:.3f}".format(porcentaje)
        info.append(porcentaje)

        data_mapea.update({comb:info})
        comb = comb + 1;

    df_result = pd.DataFrame.from_dict(data_mapea,orient='index')
    print df_result
    print ""
    df_result.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/Result_5.txt',\
                        sep='|',header=None, index=True)

    return None;

"""
'analysis_aspaths_comm':
    - ASPATHs-Comm coinciden
    - ASPATHs-Comm alguna vez coinciden
    - ASPATHs-Comm no coinciden
"""
def analysis_aspaths_comm():

    Header = ['ID_Comb','iden_aspath_item','rango_aspath_item','iden_comm_item','rango_comm_item',\
                'count_aspaths','porcentaje']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/Result_3.txt'
    df_analysis = pd.read_csv(file_read, sep='|',header=None, names=Header);
    df_analysis = df_analysis[df_analysis['count_aspaths'] > 0]

    idenASPATH_item = 'Unknown'
    idenCOMM_item = 'Unknown'

    idenASPATH_item = idenASPATH_item.split("|")
    idenCOMM_item = idenCOMM_item.split("|")

    df_found0 = df_analysis['iden_aspath_item'] == idenASPATH_item[0]
    # df_found1 = df_analysis['iden_aspath_item'] == idenASPATH_item[1]
    # df_found2 = df_analysis['iden_aspath_item'] == idenASPATH_item[2]
    # df_found3 = df_analysis['iden_aspath_item'] == idenASPATH_item[3]
    df_ASPATH = df_analysis[df_found0]
    # df_ASPATH = df_analysis[df_found0 | df_found1]

    df_found0 = df_ASPATH['iden_comm_item'] == idenCOMM_item[0]
    # df_found1 = df_ASPATH['iden_comm_item'] == idenCOMM_item[1]
    # df_found2 = df_ASPATH['iden_comm_item'] == idenCOMM_item[2]
    # df_found3 = df_ASPATH['iden_comm_item'] == idenCOMM_item[3]
    # df_found4 = df_ASPATH['iden_comm_item'] == idenCOMM_item[4]
    # df_found5 = df_ASPATH['iden_comm_item'] == idenCOMM_item[5]
    df_Comm = df_ASPATH[df_found0]
    # df_Comm = df_ASPATH[df_found0 | df_found1]
    # df_Comm = df_ASPATH[df_found0 | df_found1 | df_found2 | df_found3 | df_found4 | df_found5]

    print df_Comm
    count_aspaths = list(df_Comm.count_aspaths)
    count_aspaths = map(int, count_aspaths)
    count_aspaths = sum(count_aspaths)
    print ""
    print count_aspaths;
    print ""

    return None;

def analysis_aspaths_comm_stage2():

    Header = ['iden_aspath_item','iden_comm_item','count_aspaths']
    file = 'ASPATHs_Comm_no_matchean.csv'
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/'+file
    df_analysis = pd.read_csv(file_read, sep=',',header=None, names=Header);

    total_aspaths = list(df_analysis.count_aspaths)
    total_aspaths = map(int, total_aspaths)
    total_aspaths = sum(total_aspaths)
    print total_aspaths;
    df_analysis = df_analysis.sort_values(by='count_aspaths', ascending=False)

    count_aspaths = list(df_analysis.count_aspaths)

    porcentaje = [];
    ID_Comb = [];
    id_comb = 0
    for count in count_aspaths:
        try:
            porcentaje_comm = float(float(count)/(float(total_aspaths)))
            porcentaje_comm = float(porcentaje_comm)*float(100)
            porcentaje_comm_str = "{0:.3f}".format(porcentaje_comm)
        except ZeroDivisionError:
            porcentaje_comm = 0.0;
            porcentaje_comm_str = "{0:.3f}".format(porcentaje_comm)

        id_comb = id_comb + 1
        ID_Comb.append(id_comb)
        porcentaje.append(porcentaje_comm_str)
    df_analysis.insert(0,'ID_Comb',ID_Comb)
    df_analysis.insert(3,'Porcentaje',porcentaje)

    df_analysis.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/'+file,\
                sep=',',header=None, index=None)

    return None;

"""
'grah_results':
    - Grah01: Porcentaje de ASPATHs que se ven en más de un colector
    - Grah02: Porcentaje de ASPATHs que nunca/alguna vez/(casi) siempre ven communities
    - Grah03: Porcentaje de ASPATHs que sus communities matchean, alguna vez matchean o no matchean
    - Grah04: Porcentaje de ASPATHs matchean, combinaciones posibles
    - Grah05: Porcentaje de ASPATHs alguna vez matchean, combinaciones posibles
    - Grah06: Porcentaje de ASPATHs no matchean, combinaciones posibles
"""
def grah_results():

    labels = ['Único colector','Más de un colector']
    sizes = [14177021,1727936]
    explode = (0,0.1)
    colors = ['lightblue','yellowgreen']

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors = colors, autopct='%1.1f%%',
            shadow=True, startangle=0)
    ax.axis('equal')

    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic')
    plt.suptitle('Porcentaje de ASPATHs distintos vistos en más de un colector', fontsize=16, fontweight=0, \
                color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/Graficas/grah01.png',bbox_inches = "tight");
    plt.close

    Header = ['Tag_Comm','Count_ASPATHs','Porcentaje']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/Result_1.txt'
    df_aspaths = pd.read_csv(file_read, sep='|',header=None, names=Header);

    info = [];
    df = df_aspaths[df_aspaths['Tag_Comm'] == 'Nunca']
    porcentaje = df.Porcentaje.item();
    info.append(porcentaje)
    df = df_aspaths[df_aspaths['Tag_Comm'] == 'Alguna vez']
    porcentaje = df.Porcentaje.item();
    info.append(porcentaje)
    df = df_aspaths[df_aspaths['Tag_Comm'] == 'Casi siempre']
    porcentaje = df.Porcentaje.item();
    info.append(porcentaje)
    df = df_aspaths[df_aspaths['Tag_Comm'] == 'Siempre']
    porcentaje = df.Porcentaje.item();
    info.append(porcentaje)

    # Representación gráfica:
    labels = ['Nunca','Alguna vez/Casi siempre','Siempre']
    sizes = [info[0],0,info[3]]
    explode = (0.1,0,0)
    colors = ['tomato','yellowgreen','blue']

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax.axis('equal')

    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Porcentaje de ocurrencia en que los ASPATHs ven communities', fontsize=16, fontweight=0, \
                color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/Graficas/grah02.png',bbox_inches = "tight");
    plt.close

    Header_ASPATHs = ['ASPATH','Communities','ASes_Comm','iden_ASes_ASPATH','iden_ASes_Comm','Macheo_ASes_aspath_comm']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_Stage2.txt'
    df_aspaths = pd.read_csv(file_read, sep='|',header=None, names=Header_ASPATHs);

    info = [];
    df = df_aspaths[df_aspaths['Macheo_ASes_aspath_comm'] == 'No matchean']
    info.append(len(df))
    df = df_aspaths[df_aspaths['Macheo_ASes_aspath_comm'] == 'Alguna vez matchean']
    info.append(len(df))
    df = df_aspaths[df_aspaths['Macheo_ASes_aspath_comm'] == 'Matchean']
    info.append(len(df))
    print 'Grah03:'
    print info

    # Representación gráfica:
    labels = ['No coinciden','Alguna vez coinciden', 'Coinciden']
    sizes = [info[0],info[1],info[2]]
    explode = (0,0,0)
    colors = ['red','coral','lightblue']

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=0)
    ax.axis('equal')

    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Porcentaje de ASPATHs cuyos ASes communities anunciados coinciden con los ASes del ASPATH', \
                fontsize=16, fontweight=0, color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/Graficas/grah03.png',bbox_inches = "tight");
    plt.close

    Header = ['ID_Comb','iden_ASes_ASPATH','iden_ASes_Comm','Count_ASPATHs','percentage']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_stage2_matchean.txt'
    df_comb = pd.read_csv(file_read, sep='|',header=None, names=Header);

    info = [];
    df = df_comb[df_comb['ID_Comb'] == 1]
    count_aspaths = df.Count_ASPATHs.item();
    info.append(count_aspaths)
    df = df_comb[df_comb['ID_Comb'] == 2]
    count_aspaths = df.Count_ASPATHs.item();
    info.append(count_aspaths)

    info_sum = [];
    for i in range(3,len(df_comb)+1):
        df = df_comb[df_comb['ID_Comb'] == i]
        count_aspaths = df.Count_ASPATHs.item();
        info_sum.append(count_aspaths)

    sum_aspaths = sum(info_sum)
    info.append(sum_aspaths)

    # Representación gráfica:
    labels = ['Combinación 1','Combinación 2','Combinaciones 3-23']
    sizes = [info[0],info[1],info[2]]
    explode = (0,0,0)
    colors = ['blue','lightblue','yellowgreen']

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=45)
    ax.axis('equal')

    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Combinaciones ASPATHs-Comm que coinciden',\
                fontsize=16, fontweight=0, color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/Graficas/grah04.png',\
            bbox_inches = "tight");
    plt.close

    Header = ['ID_Comb','iden_ASes_ASPATH','iden_ASes_Comm','Count_ASPATHs','percentage']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_stage2_algunavez_matchean.txt'
    df_comb = pd.read_csv(file_read, sep='|',header=None, names=Header);

    info = [];
    df = df_comb[df_comb['ID_Comb'] == 1]
    count_aspaths = df.Count_ASPATHs.item();
    info.append(count_aspaths)
    df = df_comb[df_comb['ID_Comb'] == 2]
    count_aspaths = df.Count_ASPATHs.item();
    info.append(count_aspaths)
    df = df_comb[df_comb['ID_Comb'] == 3]
    count_aspaths = df.Count_ASPATHs.item();
    info.append(count_aspaths)
    df = df_comb[df_comb['ID_Comb'] == 4]
    count_aspaths = df.Count_ASPATHs.item();
    info.append(count_aspaths)
    df = df_comb[df_comb['ID_Comb'] == 5]
    count_aspaths = df.Count_ASPATHs.item();
    info.append(count_aspaths)

    info_sum = [];
    for i in range(6,len(df_comb)+1):
        df = df_comb[df_comb['ID_Comb'] == i]
        count_aspaths = df.Count_ASPATHs.item();
        info_sum.append(count_aspaths)

    sum_aspaths = sum(info_sum)
    info.append(sum_aspaths)

    # Representación gráfica:
    labels = ['Combinación 1','Combinación 2','Combinación 3','Combinación 4','Combinación 5',\
                'Combinaciones 6-88']
    sizes = [info[0],info[1],info[2],info[3],info[4],info[5]]
    explode = (0,0,0,0,0,0)
    colors = ['blue','lightblue','navy','azure','cyan','orangered']
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=45)
    ax.axis('equal')

    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Combinaciones ASPATHs-Comm que alguna vez coinciden',\
                fontsize=16, fontweight=0, color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/Graficas/grah05.png',\
            bbox_inches = "tight");
    plt.close

    Header = ['ID_Comb','iden_ASes_ASPATH','iden_ASes_Comm','Count_ASPATHs','percentage']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_stage2_no_matchean.txt'
    df_comb = pd.read_csv(file_read, sep='|',header=None, names=Header);

    info = [];
    df = df_comb[df_comb['ID_Comb'] == 1]
    count_aspaths = df.Count_ASPATHs.item();
    info.append(count_aspaths)
    df = df_comb[df_comb['ID_Comb'] == 2]
    count_aspaths = df.Count_ASPATHs.item();
    info.append(count_aspaths)
    df = df_comb[df_comb['ID_Comb'] == 3]
    count_aspaths = df.Count_ASPATHs.item();
    info.append(count_aspaths)
    df = df_comb[df_comb['ID_Comb'] == 4]
    count_aspaths = df.Count_ASPATHs.item();
    info.append(count_aspaths)
    df = df_comb[df_comb['ID_Comb'] == 5]
    count_aspaths = df.Count_ASPATHs.item();
    info.append(count_aspaths)

    info_sum = [];
    for i in range(6,len(df_comb)+1):
        df = df_comb[df_comb['ID_Comb'] == i]
        count_aspaths = df.Count_ASPATHs.item();
        info_sum.append(count_aspaths)

    sum_aspaths = sum(info_sum)
    info.append(sum_aspaths)

    # Representación gráfica:
    labels = ['Combinación 1','Combinación 2','Combinación 3','Combinación 4','Combinación 5',\
                'Combinaciones 6-89']
    sizes = [info[0],info[1],info[2],info[3],info[4],info[5]]
    explode = (0,0,0,0,0,0)
    colors = ['blue','lightblue','navy','azure','cyan','orangered']

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=45)
    ax.axis('equal')

    plt.title(" ", fontsize=16, fontweight=0, \
                color='black', loc='center', style='italic' )
    plt.suptitle('Combinaciones ASPATHs-Comm que no coinciden',\
                fontsize=16, fontweight=0, color='black', style='italic')

    savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/Graficas/grah06.png',\
            bbox_inches = "tight");
    plt.close

    return None;

"""
'analysis_well_Known_communities':
    - Filtrar aquellos ASPATHs en donde vea communities bien conocidas por la comunidad
    - Búsqueda en el atributo 'Community' del AS65535
    - Reconocer esos AS65535:Community
    - Reconocer que solo existe el AS 65535
    - Búsqueda de los valores Well-Known
"""
def analysis_well_Known_communities():

    Header_ASPATHs = ['ASPATH_Original','RRC_ID','count_Announced','count_Announced_Comm','Pcount_Announced_Comm',\
            'Tag_count_Announced_Comm','Tag_Prep','ASPATH','long_ruta','Clasi_ASes','Communities',\
            'ASes_Comm','ASesASPATH_Comm','Hops_Comm','iden_ASes_aspath','Range_ASes_aspath',\
            'iden_ASes_comm','Range_ASes_comm','Macheo_ASes_aspath_comm']

    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_RRCs.txt'
    df_aspaths = pd.read_csv(file_read, sep='|',header=None, names=Header_ASPATHs);
    df_aspaths = df_aspaths[df_aspaths['Tag_count_Announced_Comm'] != 'Nunca']

    search = '65535:' # Patrón de búsqueda
    df_65535 = df_aspaths[df_aspaths['Communities'].str.contains(search)]
    df_65535.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_65535.txt',\
                sep='|',header=None, index=False)

    return None;

def analysis_well_Known_communities_stage2():

    Header_ASPATHs = ['ASPATH_Original','RRC_ID','count_Announced','count_Announced_Comm','Pcount_Announced_Comm',\
            'Tag_count_Announced_Comm','Tag_Prep','ASPATH','long_ruta','Clasi_ASes','Communities',\
            'ASes_Comm','ASesASPATH_Comm','Hops_Comm','iden_ASes_aspath','Range_ASes_aspath',\
            'iden_ASes_comm','Range_ASes_comm','Macheo_ASes_aspath_comm']

    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_65535.txt'
    df_aspaths = pd.read_csv(file_read, sep='|',header=None, names=Header_ASPATHs);
    df_aspaths = df_aspaths[df_aspaths['Tag_count_Announced_Comm'] != 'Nunca']
    df_aspaths = df_aspaths[['ASPATH_Original','Communities']]

    add_ASComm = [];
    add_AS65535 = [];
    for index, row in df_aspaths.iterrows():

        Comm_str = row.Communities;
        Comm_split = Comm_str.split(" ")

        AS65535_Comm = [];
        AS65535 = [];
        for ASValue in Comm_split:
            AS = ASValue.split(":")[0]
            if int(AS) == 65535 and not ASValue in AS65535_Comm:
                AS65535_Comm.append(ASValue)
            if int(AS) == 65535 and not AS in AS65535:
                AS65535.append(AS)

        AS65535_Comm = ' '.join(AS65535_Comm)
        AS65535_Comm = ' ' + AS65535_Comm + ' '
        add_ASComm.append(AS65535_Comm)

        AS65535 = ' '.join(AS65535)
        add_AS65535.append(AS65535)

    # Añadir la nueva columna generada:
    df_aspaths.insert(2,'AS65535_Comm',add_ASComm)
    df_aspaths.insert(3,'AS65535',add_AS65535)
    df_aspaths.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_65535.txt',\
                sep='|',header=None, index=False)

    return None;

def analysis_well_Known_communities_stage3():

    Header = ['ASPATH_Original','Communities','AS65535_Comm','AS65535']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_65535.txt'
    df_aspaths = pd.read_csv(file_read, sep='|',header=None, names=Header);

    search = ' 65535:2 '
    df = df_aspaths[df_aspaths['AS65535_Comm'].str.contains(search)]

    print df;
    print len(df)

    return None;

# =================================== Main() ===================================
print "Comienza la ejecución: Hora -> ", asctime(localtime());
start_time = time()

"""
Analizo los ASPATHs:
"""
# analysis_ASPATHs_rrcs()

"""
Analizar los ASPATHs en los casos que los ASes que pongan communities matchean con
los ASes que forman parte del ASPATH, que alguna vez matchean, o que no matcheen
esos ASes de communities con los ASes del ASPATH:
"""
# analysis_aspaths_comm();
# analysis_aspaths_comm_stage2();

"""
'grah_results': Representación gráfica de los resultados obtenidos en el análisis
ASPATHs-Comm
"""
grah_results()

"""
'analysis_well_Known_communities': Esta función me devolverá aquellos ASPATHs en los
cuales se estén viendo communities bien conocidas por la comunidad:
"""
# analysis_well_Known_communities();
# analysis_well_Known_communities_stage2();
# analysis_well_Known_communities_stage3();

print "Termina la ejecución: Hora -> ", asctime(localtime());
elapsed_time = time() - start_time
print("Tiempo de ejecucion: "+ str(elapsed_time))
