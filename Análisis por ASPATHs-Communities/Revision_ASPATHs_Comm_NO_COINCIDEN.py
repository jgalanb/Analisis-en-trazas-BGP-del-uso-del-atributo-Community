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

def stage1():
    Header_ASPATHs = ['ASPATH','Communities','ASes_Comm','iden_ASes_ASPATH','iden_ASes_Comm','Macheo_ASes_aspath_comm']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_Stage2.txt'
    df_aspaths = pd.read_csv(file_read, sep='|',header=None, names=Header_ASPATHs);
    df_aspaths = df_aspaths[df_aspaths['Macheo_ASes_aspath_comm'] == 'No matchean']
    print "ASPATHs considerados: ",len(df_aspaths)
    print ""

    ASes_Comm = list(df_aspaths.ASes_Comm)

    print "Total de ASes vistos que no coinciden: "
    list_ASes = [];
    list_ASes_unique = [];
    for ASes in ASes_Comm:
        ASes = ASes.split(" ")
        for AS in ASes:
            list_ASes.append(AS)
            if not AS in list_ASes_unique:
                list_ASes_unique.append(AS)

    counter_ASesComm = collections.Counter(list_ASes)
    df_ASesComm = pd.DataFrame.from_dict(counter_ASesComm, orient='index').reset_index()
    df_ASesComm.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASes_Comm_no_coinciden.txt',\
                sep='|',header=None, index=False)

    Header = ['AS','Count']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASes_Comm_no_coinciden.txt'
    df_ASesComm = pd.read_csv(file_read, sep='|',header=None, names=Header);
    df_ASesComm = df_ASesComm.sort_values(by='Count',ascending=False)
    print df_ASesComm;

    print "Total de ASes distintos que no coinciden: ", len(list_ASes_unique)
    print ""

    print "Determinar la cantidad de ASes que fueron vistos alguna vez formando parte de un ASPATH: "
    Header_ClasiGeneral = ['AS','ClasiGeneral']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASes_ClasiGeneral.txt'
    df_ClasiGeneral =  pd.read_csv(file_read, sep='|',header=None, names = Header_ClasiGeneral);

    ASes_search = list(df_ASesComm.AS.unique())

    data_AS = {}
    for AS in ASes_search:
        info = [];

        df = df_ASesComm[df_ASesComm['AS'] == AS]
        count = df.Count.item();
        info.append(count)

        df = df_ClasiGeneral[df_ClasiGeneral['AS'] == AS]
        if not df.empty:
            info.append('Yes')
        else:
            info.append('No')

        data_AS.update({AS:info})

    df_ASClasi = pd.DataFrame.from_dict(data_AS,orient='index')
    df_ASClasi.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASes_Comm_no_coinciden.txt',\
                sep='|',header=None, index=True)

    return None;

def stage2():
    Header = ['ID_Comb','iden_ASes_ASPATH','iden_ASes_Comm','Count_ASPATHs','percentage']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_stage2_no_matchean.txt'
    df_comb = pd.read_csv(file_read, sep='|',header=None, names=Header);

    search = '08-Reservado_Doc_32b|09-Reservado_32b|10-Público_32b|11-Privado_32b|12-Reservado_4294967295'
    df = df_comb[df_comb['iden_ASes_Comm'].str.contains(search)]
    print df

    df_reserved0 = df_comb[df_comb['iden_ASes_Comm'].str.contains('07-Reservado_65535')]
    print df_reserved0
    print ""

    count_aspaths = list(df_reserved0.Count_ASPATHs)
    count_aspaths = map(int, count_aspaths)
    count_aspaths = sum(count_aspaths)
    print count_aspaths;
    print ""

    df_32b = df_comb[df_comb['iden_ASes_ASPATH'].str.contains('32b')]
    print df_32b

    count_aspaths = list(df_32b.Count_ASPATHs)
    count_aspaths = map(int, count_aspaths)
    count_aspaths = sum(count_aspaths)
    print count_aspaths;

    return None;

def stage3():
    Header_ASPATHs = ['ASPATH','Communities','ASes_Comm','iden_ASes_ASPATH','iden_ASes_Comm','Macheo_ASes_aspath_comm']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_Stage2.txt'
    df_aspaths = pd.read_csv(file_read, sep='|',header=None, names=Header_ASPATHs);
    df_aspaths = df_aspaths[df_aspaths['Macheo_ASes_aspath_comm'] == 'No matchean']
    df_aspaths = df_aspaths[df_aspaths['iden_ASes_ASPATH'] == '02-Público_16b 10-Público_32b']
    df_aspaths = df_aspaths[df_aspaths['iden_ASes_Comm'] == '02-Público_16b']

    Header_ClasiGeneral = ['AS','ClasiGeneral']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASes_ClasiGeneral.txt'
    df_ClasiGeneral =  pd.read_csv(file_read, sep='|',header=None, names = Header_ClasiGeneral);

    list_ASes_Comm = [];
    for ASes in list(df_aspaths.ASes_Comm.unique()):
        ASes = ASes.split(" ")
        for AS in ASes:
            if not AS in list_ASes_Comm:
                list_ASes_Comm.append(AS)

    print len(list_ASes_Comm)
    print ""

    list_ASes_32b = [];
    for ASes in list(df_aspaths.ASPATH.unique()):
        ASes = ASes.split(" ")
        for AS in ASes:
            if int(AS) > 65535 and not AS in list_ASes_32b:
                list_ASes_32b.append(AS)

    print len(list_ASes_32b)
    print ""

    list_ASes_16b = [];
    for AS in list_ASes_32b:
        AS = AS[:5]
        if not AS in list_ASes_16b:
            list_ASes_16b.append(AS)

    print len(list_ASes_16b)
    print ""

    print "Quedandome solo con los primeros cinco digitos del AS 32b:"
    count = 0;
    count_ASPATH = 0;
    for AS in list_ASes_16b:
        if AS in list_ASes_Comm:
            count = count + 1

            df = df_ClasiGeneral[df_ClasiGeneral['AS'] == AS]
            if not df.empty:
                count_ASPATH = count_ASPATH + 1

    print count;
    print count_ASPATH
    print ""

    print "Pasando el número a 32b y luego me quedo con los primeros 16 bits:"
    list_ASes_16b = [];
    for AS in list_ASes_32b:
        number = np.binary_repr(int(AS), width=32)
        number = number[:16]
        number = int(number, 2)
        if not number in list_ASes_16b:
            list_ASes_16b.append(number)

    print len(list_ASes_16b)
    print ""

    count = 0;
    for AS in list_ASes_16b:
        if AS in list_ASes_Comm:
            count = count + 1;

    print count;
    print ""

    print "Pasando el número a 32b y luego me quedo con los ultimos 16 bits:"
    list_ASes_16b = [];
    for AS in list_ASes_32b:
        number = np.binary_repr(int(AS), width=32)
        number = number[16:]
        number = int(number, 2)
        if not number in list_ASes_16b:
            list_ASes_16b.append(number)

    print len(list_ASes_16b)
    print ""

    count = 0;
    for AS in list_ASes_16b:
        if AS in list_ASes_Comm:
            count = count + 1;

    print count;
    print ""

    return None;

# =================================== Main() ===================================
print "Comienza la ejecución: Hora -> ", asctime(localtime());
start_time = time()

Header_rutas = ['long_ruta','count_rutas','count_NUNCA_comm','count_rutas_NoASesASPATH',\
                'max_hopComm','count_aspath','count_total']
file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Rutas/Rutas_RRCs_join.txt'
df_rutas = pd.read_csv(file_read, sep='|',header=None, names=Header_rutas);
df_rutas = df_rutas[['long_ruta','count_rutas','count_NUNCA_comm','count_rutas_NoASesASPATH','max_hopComm']]

add_count_analysis = [];
add_percentage = [];
for long_ruta in list(df_rutas.long_ruta):
    df = df_rutas[df_rutas['long_ruta'] == long_ruta]
    count_rutas_item = df.count_rutas.item();
    count_NUNCA_comm_item = df.count_NUNCA_comm.item();
    count_rutas_NoASesASPATH_item = df.count_rutas_NoASesASPATH.item();

    count_analysis = int(count_rutas_item) - int(count_NUNCA_comm_item) - int(count_rutas_NoASesASPATH_item)
    add_count_analysis.append(count_analysis)

    percentage = float(count_analysis)/float(count_rutas_item)
    percentage = percentage*float(100)
    add_percentage.append(percentage)

df_rutas.insert(4,'rutas_analysis',add_count_analysis)
df_rutas.insert(5,'percentage_analysis',add_percentage)

print df_rutas;
