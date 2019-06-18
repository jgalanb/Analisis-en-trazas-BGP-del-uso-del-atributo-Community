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
'analysis_ASes_Reserved':
    - Número de ASPATHs en los que se ven valores de ASes reservados
    - ASPATHs donde se vea el AS 0
    - ASPATHs donde se sea el AS 65535
    - Para aquellos ASPATHs con ASes 0, cuantos ASPATHs hay con al menos un AS > 65535
    - Para aquellos ASPATHs con ASes 65535, cuantos ASPATHs hay con al menos un AS > 65535
    - ASes que no coinciden y su ocurrencia de aparecer en los ASPATHs
    - Esos ASes, ¿alguna vez habian formado parte de un ASPATH?
"""
def analysis_ASes_Reserved():

    Header_ASPATHs = ['ASPATH_Original','RRC_ID','count_Announced','count_Announced_Comm','Pcount_Announced_Comm',\
            'Tag_count_Announced_Comm','Tag_Prep','ASPATH','long_ruta','Clasi_ASes','Communities',\
            'ASes_Comm','ASesASPATH_Comm','Hops_Comm','iden_ASes_aspath','Range_ASes_aspath',\
            'iden_ASes_comm','Range_ASes_comm','Macheo_ASes_aspath_comm']

    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_RRCs.txt'
    df_aspaths = pd.read_csv(file_read, sep='|',header=None, names=Header_ASPATHs);
    df_aspaths = df_aspaths[df_aspaths['Macheo_ASes_aspath_comm'] == 'Alguna vez matchean']
    print "ASPATHs-Comm que alguna vez coinciden: ", len(df_aspaths)

    df_reserved = df_aspaths[df_aspaths['iden_ASes_comm'].str.contains('Reservado_0_65535')]
    print "ASPATHs con valores de ASes reservados: ",len(df_reserved)

    ASPATHs_0 = []
    ASPATHs_65535 = [];
    ASes_no_coinciden = [];
    for index, row in df_reserved.iterrows():

        ASPATH_item = row.ASPATH;
        ASPATH_split = ASPATH_item.split(" ")
        ASes_Comm_item = row.ASes_Comm;
        ASes_Comm_split = ASes_Comm_item.split(" ")

        for AS in ASes_Comm_split:
            if not AS in ASPATH_split:
                ASes_no_coinciden.append(AS)

        for AS in ASes_Comm_split:
            if int(AS) == 0 and not ASPATH_item in ASPATHs_0:
                ASPATHs_0.append(ASPATH_item)
            elif int(AS) == 65535 and not ASPATH_item in ASPATHs_65535:
                ASPATHs_65535.append(ASPATH_item)

    print "Rutas distintas donde veo el valor de AS0 reservado: ", len(ASPATHs_0)
    print "Rutas distintas donde veo el valor de AS65535 reservado: ", len(ASPATHs_65535)

    count_0 = [];
    for aspath in ASPATHs_0:
        ASes = aspath.split(" ")
        for AS in ASes:
            if int(AS) > 65535 and not aspath in count_0:
                count_0.append(aspath)

    count_65535 =[];
    for aspath in ASPATHs_65535:
        ASes = aspath.split(" ")
        for AS in ASes:
            if int(AS) > 65535 and not aspath in count_65535:
                count_65535.append(aspath)

    print "Rutas distintas con al menos un AS > 65535 donde se ven comm AS0: ",len(count_0)
    print "Rutas distintas con al menos un AS > 65535 donde se ven comm AS65535: ",len(count_65535)

    counter_ASesComm = collections.Counter(ASes_no_coinciden)
    df_ASesComm = pd.DataFrame.from_dict(counter_ASesComm, orient='index').reset_index()
    df_ASesComm.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASes_Comm_algunavez_coinciden.txt',\
                sep='|',header=None, index=False)

    Header = ['AS','Count']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASes_Comm_algunavez_coinciden.txt'
    df_ASesComm = pd.read_csv(file_read, sep='|',header=None, names=Header);
    df_ASesComm = df_ASesComm.sort_values(by='Count',ascending=False)
    print df_ASesComm;

    Header_ClasiGeneral = ['AS','ClasiGeneral']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASes_ClasiGeneral.txt'
    df_ClasiGeneral =  pd.read_csv(file_read, sep='|',header=None, names = Header_ClasiGeneral);

    add_idenAS = [];
    add_typeAS = [];
    for index, row in df_ASesComm.iterrows():

        AS = row.AS

        df = df_ClasiGeneral[df_ClasiGeneral['AS'] == int(AS)]
        if df.empty:
            found_AS = 'Not_Found'
            type_AS = 'Not_Found'
        else:
            found_AS = 'Found'
            type_AS = df.ClasiGeneral.item();

        add_idenAS.append(found_AS)
        add_typeAS.append(type_AS)

    df_ASesComm.insert(2,'idenAS',add_idenAS)
    df_ASesComm.insert(3,'typeAS',add_typeAS)
    df_ASesComm.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASes_Comm_algunavez_coinciden.txt',\
                sep='|',header=None, index=False)

    return None;

# =================================== Main() ===================================
print "Comienza la ejecución: Hora -> ", asctime(localtime());
start_time = time()

"""
Análisis ASPATHs-Comm que alguna vez coinciden:
    - Análisis de los ASPATHs en donde aparecen ASes reseravdos: 0 ó 65535
"""
analysis_ASes_Reserved();


print "Termina la ejecución: Hora -> ", asctime(localtime());
elapsed_time = time() - start_time
print("Tiempo de ejecucion: "+ str(elapsed_time))
