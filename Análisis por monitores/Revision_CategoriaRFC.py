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
'analysis_categoryRFC':
    - Filtrar por aquellos ASPATHs que alguna vez/(casi) siempre ven communities
    - Filtrar por aquellos ASPATHs que alguna vez (o) coinciden los ASes comm con los ASes ASPATH
    - Busco ASPATHs con coincidencia de communities ASes que sean 'Categoria RFC'
"""
def analysis_categoryRFC():

    Header_ASPATHs = ['ASPATH_Original','RRC_ID','count_Announced','count_Announced_Comm','Pcount_Announced_Comm',\
            'Tag_count_Announced_Comm','Tag_Prep','ASPATH','long_ruta','Clasi_ASes','Communities',\
            'ASes_Comm','ASesASPATH_Comm','Hops_Comm','iden_ASes_aspath','Range_ASes_aspath',\
            'iden_ASes_comm','Range_ASes_comm','Macheo_ASes_aspath_comm']

    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_RRCs.txt'
    df_aspaths = pd.read_csv(file_read, sep='|',header=None, names=Header_ASPATHs);
    df_aspaths = df_aspaths[df_aspaths['Tag_count_Announced_Comm'] != 'Nunca']
    df_aspaths = df_aspaths[df_aspaths['Macheo_ASes_aspath_comm'] != 'No matchean']

    # Valores de communities que se deben buscar:
    Header = ['Community','AS','Type','Taxonomy','RFC','RFC_Sign']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASValuesMonitors_RRCs_RC.txt'
    df_Communities = pd.read_csv(file_read, sep='|',header=None, names=Header);
    df_Communities = df_Communities.fillna({'RFC_Sign':'NA'})
    df_Communities = df_Communities[df_Communities['RFC'] == 'Category_RFC4384']

    search = list(df_Communities.Community.unique())
    print search
    print len(search)
    print ""

    add_ASPATH_Original = [];
    add_Communities = [];
    for index, row in df_aspaths.iterrows():

        ASPATH_str = row.ASPATH_Original
        ASPATH_split = ASPATH_str.split(" ")
        Communities_str = row.Communities
        Comm_split = Communities_str.split(" ")

        for ASValue in Comm_split:
            if ASValue in search:
                add_ASPATH_Original.append(ASPATH_str)
                add_Communities.append(Communities_str)

    list_ASPATHs_Comm = list(zip(add_ASPATH_Original, add_Communities))
    df = pd.DataFrame(list_ASPATHs_Comm, columns = ['ASPATH', 'Communities'])
    print "Stage1:"
    print len(df)
    print ""
    df.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASesMonitors_CategoryRFC_stage1.txt',\
                sep='|',header=None, index=True)

    return None;

"""
'analysis_categoryRFC_stage2':
    - Eliminar tuplas duplicadas
    - Coincidencias bajo una misma tupla ASPATHs-Comm
"""
def analysis_categoryRFC_stage2():

    Header = ['ASPATH','Communities']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASesMonitors_CategoryRFC_stage1.txt'
    df_aspaths = pd.read_csv(file_read, sep='|',header=None, names=Header);
    df_aspaths.drop_duplicates(subset=Header, keep='last',inplace = True)

    # Valores de communities que se deben buscar:
    Header = ['Community','AS','Type','Taxonomy','RFC','RFC_Sign']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASValuesMonitors_RRCs_RC.txt'
    df_Communities = pd.read_csv(file_read, sep='|',header=None, names=Header);
    df_Communities = df_Communities.fillna({'RFC_Sign':'NA'})
    df_Communities = df_Communities[df_Communities['RFC'] == 'Category_RFC4384']

    search = list(df_Communities.Community.unique())

    add_count = [];
    for index, row in df_aspaths.iterrows():

        Comm_str = row.Communities;
        Comm_split = Comm_str.split(" ")

        count = 0;
        for ASValue in Comm_split:
            if ASValue in search:
                count = count + 1;

        add_count.append(count)

    df_aspaths.insert(2,'count',add_count)
    print "Stage2:"
    print len(df_aspaths)
    print ""
    df_aspaths.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASesMonitors_CategoryRFC_stage2.txt',\
                sep='|',header=None, index=True)

    return None;

"""
'analysis_categoryRFC_stage3':
    - Buscar ASPATHs-Comm con más de una coincidencia
    - Nueva columna con esas coincidencias
    - ASes distitos con dichas coincidencias
"""
def analysis_categoryRFC_stage3():

    Header = ['ASPATH','Communities','count']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASesMonitors_CategoryRFC_stage2.txt'
    df_aspaths = pd.read_csv(file_read, sep='|',header=None, names=Header);
    df_aspaths.drop_duplicates(subset=Header, keep='last',inplace = True)
    df_aspaths = df_aspaths[df_aspaths['count'] > 1]

    # Valores de communities que se deben buscar:
    Header = ['Community','AS','Type','Taxonomy','RFC','RFC_Sign']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASValuesMonitors_RRCs_RC.txt'
    df_Communities = pd.read_csv(file_read, sep='|',header=None, names=Header);
    df_Communities = df_Communities.fillna({'RFC_Sign':'NA'})
    df_Communities = df_Communities[df_Communities['RFC'] == 'Category_RFC4384']

    search = list(df_Communities.Community.unique())

    add_ASComm = [];
    add_AS = [];
    count_ASes = [];
    for index, row in df_aspaths.iterrows():

        Comm_str = row.Communities;
        Comm_split = Comm_str.split(" ")

        list_ASComm = [];
        list_AS = [];
        count = 0
        for ASValue in Comm_split:
            AS = ASValue.split(":")[0]
            if ASValue in search and not ASValue in list_ASComm:
                list_ASComm.append(ASValue)

                if not AS in list_AS:
                    list_AS.append(AS)
                    count = count + 1;

        list_ASComm = ' '.join(list_ASComm)
        list_ASComm = ' ' + list_ASComm + ' '
        add_ASComm.append(list_ASComm)

        list_AS = ' '.join(list_AS)
        add_AS.append(list_AS)
        count_ASes.append(count)

    # Añadir la nueva columna generada:
    df_aspaths.insert(3,'AS_Comm',add_ASComm)
    df_aspaths.insert(4,'ASes',add_AS)
    df_aspaths.insert(5,'Count_ASes',count_ASes)
    print "Stage3:"
    print len(df_aspaths)
    print ""
    df_aspaths.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASesMonitors_CategoryRFC_stage3.txt',\
                sep='|',header=None, index=False)

    return None;

"""
'analysis_categoryRFC_stage4':
    - Comprobación de coincidencias
"""
def analysis_categoryRFC_stage4():

    Header = ['ASPATH','Communities','count','AS_Comm','ASes','count_ASes']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASesMonitors_CategoryRFC_stage3.txt'
    df_aspaths = pd.read_csv(file_read, sep='|',header=None, names=Header);

    df_aspaths = df_aspaths[df_aspaths['count_ASes'] == 1]

    print "ASPATHs con ASesValues Categoria RFC que se ponen para el mismo ASPATHs:"
    print len(df_aspaths)
    print ""

    ValuesComm = [];
    for index, row in df_aspaths.iterrows():

        ASComm_str = row.AS_Comm
        ASComm_split = ASComm_str.split(" ")[1:-1]

        list_valueComm = [];
        for ASValue in ASComm_split:
            Value = ASValue.split(":")[1]
            if not Value in list_valueComm:
                list_valueComm.append(Value)

        list_valueComm = ' '.join(list_valueComm)
        ValuesComm.append(list_valueComm)

    df_aspaths.insert(6,'ValuesComm',ValuesComm)
    df_aspaths.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASesMonitors_CategoryRFC_stage4.txt',\
                sep='|',header=None, index=False)


    return None;

"""
'analysis_categoryRFC_stage5':
    - Compruebo combinaciones que más coinciden
"""
def analysis_categoryRFC_stage5():

    Header = ['ASPATH','Communities','count','AS_Comm','ASes','count_ASes','ValuesComm']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Monitors/ASesMonitors_CategoryRFC_stage4.txt'
    df_aspaths = pd.read_csv(file_read, sep='|',header=None, names=Header);

    print df_aspaths;
    print ""

    # Análisis valores communities que coinciden bajo un mismo ASPATH
    ASPATHs_total = list(df_aspaths.ASPATH)
    df_TypeComm = df_aspaths.groupby('ValuesComm')
    Types_Comm = list(df_aspaths.ValuesComm.unique())

    colums_df = ['Type_Comm','ASPATHs','%']
    df_print = pd.DataFrame([],columns = colums_df)

    for type_comm in Types_Comm:
        info_type_comm = [];
        df = df_TypeComm.get_group(type_comm);
        list_ASPATHs = list(df.ASPATH)

        info_type_comm.append(type_comm)
        info_type_comm.append(len(list_ASPATHs))

        try:
            porcen = float(float(len(list_ASPATHs))/float(len(ASPATHs_total)))
            porcen = float(porcen)*float(100);
        except ZeroDivisionError:
            porcen = 0.0;
        info_type_comm.append(porcen);

        df_inter = pd.DataFrame([info_type_comm],columns = colums_df)
        df_print = df_print.append(df_inter, sort=False)

    df_print = df_print.sort_values(by='%', ascending=False)
    print ""
    print df_print;
    print ""

    return None;

# =================================== Main() ===================================
print "Comienza la ejecución: Hora -> ", asctime(localtime());
start_time = time()

analysis_categoryRFC();
analysis_categoryRFC_stage2();
analysis_categoryRFC_stage3();
analysis_categoryRFC_stage4();
analysis_categoryRFC_stage5();

print "Termina la ejecución: Hora -> ", asctime(localtime());
elapsed_time = time() - start_time
print("Tiempo de ejecucion: "+ str(elapsed_time))
