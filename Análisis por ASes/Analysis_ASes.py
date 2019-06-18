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
'get_ClasiASes_RRCs': Obtener un dataframe de los distintos ASes encontrados en
el total de los colectores, pero además conociendo el comportamiento que han tenido
dichos ASes en los colectores, es decir... si fue visto como Monitor,Origen o Tránsito:
"""
def get_ClasiASes_RRCs():

    Header_ASPATHs = ['ASPATH_Original','RRC_ID','count_Announced','count_Announced_Comm','Pcount_Announced_Comm',\
            'Tag_count_Announced_Comm','Tag_Prep','ASPATH','long_ruta','Clasi_ASes','Communities',\
            'ASes_Comm','ASesASPATH_Comm','Hops_Comm','iden_ASes_aspath','Range_ASes_aspath',\
            'iden_ASes_comm','Range_ASes_comm','Macheo_ASes_aspath_comm']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_RRCs.txt'
    df_RRCs = pd.read_csv(file_read, sep='|',header=None, names=Header_ASPATHs);
    df_RRCs = df_RRCs[['Clasi_ASes']]

    # Clasificaciones únicas encontradas en el total de ASPATHs:
    Clasificaciones_ASes = list(df_RRCs.Clasi_ASes.unique())

    list_ClasiASes = [];
    for clasiASes_ASPATH in Clasificaciones_ASes:
        clasi_ASes = clasiASes_ASPATH.split(" ")[1:-1]
        for item in clasi_ASes:
            if not item in list_ClasiASes:
                list_ClasiASes.append(item)

    # Para cada AS-Clasificación encontrada en el total de los colectores, separo
    # la información y genero dataframe resultante:

    data_ClasiASes = {};
    for item in list_ClasiASes:
        info = [];

        AS = item.split("-")[0]
        Clasi = item.split("-")[1]

        info.append(AS)
        info.append(Clasi)

        data_ClasiASes.update({item:info})

    df_ClasiASes = pd.DataFrame.from_dict(data_ClasiASes,orient='index')
    df_ClasiASes.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Clasi_ASes_RRCs.txt',\
                sep='|',header=None, index=True)

    return df_ClasiASes;

"""
'get_ASes_ClasiGeneral': Obtener un dataframe de los distintos ASes encontrados en
el total de los colectores, además de conocer las formas en las cuales dicho AS
fue visto en los colectores, es decir... si fue visto solo como origen, origen y monitor,
transito y origen, etc:
"""
def get_ASes_ClasiGeneral():

    Header_ClasiASes = ['AS_Clasi','AS','Clasi']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Clasi_ASes_RRCs.txt'
    df_ClasiASes = pd.read_csv(file_read, sep='|',header=None, names=Header_ClasiASes);

    # Lista con todos los ASes diferentes vistos en los colectores:
    # (Agrupar información por AS)
    ASes = list(df_ClasiASes.AS.unique())
    df_ASes = df_ClasiASes.groupby('AS')

    data_AS = {};
    for AS in ASes:
        info = [];

        df_AS = df_ASes.get_group(AS)

        # Formas en las que fue visto dicho AS:
        clasi = list(df_AS.Clasi.unique())
        if len(clasi) == 1:
            tag = clasi[0]
        else:
            tag = '/'.join(clasi)

        info.append(tag)

        data_AS.update({AS:info})

    df_ASes = pd.DataFrame.from_dict(data_AS,orient='index')
    df_ASes.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASes_ClasiGeneral.txt',\
                sep='|',header=None, index=True)

    return None;

"""
'info_ASes':
    - ASPATHs en los que se ve dicho AS-Clasi
    - ASPATHs en los que dicho AS-Clasi pone algún valor de community
    - Communities que anuncia dicho AS
"""
def info_ASes(df_ASes,df_ClasiASes):

    ASesClasi = list(df_ClasiASes.AS_Clasi)

    data_ASClasi = {};
    for ASClasi in ASesClasi:
        info = [];

        # Número de ASPATHs en los que se ve dicho AS:
        info.append(0)

        # Número de ASPATHs en los que se ve que dicho AS pone algún valor de community:
        info.append(0)

        # Valores de communities puestos por el AS:
        info.append('X')

        data_ASClasi.update({ASClasi:info})

    # Recorremos el df_ASes en busca de la información:
    for index, row in df_ASes.iterrows():

        ASes_Clasi = row.Clasi_ASes
        ASes_Clasi = ASes_Clasi.split(" ")[1:-1]
        ASesASPATH = row.ASesASPATH_Comm
        ASesASPATH = ASesASPATH.split(" ")
        AS_Comm = row.Communities
        AS_Comm = AS_Comm.split(" ")

        for ASClasi in ASes_Clasi:
            info_ASClasi = data_ASClasi.get(ASClasi)
            info_ASClasi[0] = int(info_ASClasi[0]) + 1

            AS = ASClasi.split('-')[0]
            if AS in ASesASPATH:
                info_ASClasi[1] = int(info_ASClasi[1]) + 1

                # Buscar valor de community:
                for community in AS_Comm:
                    ASValue = community.split(":")
                    if AS == ASValue[0]:
                        info_ASClasi[2] = info_ASClasi[2] + ' ' + str(community)

            data_ASClasi.update({ASClasi:info_ASClasi})

    return data_ASClasi;

# =================================== Main() ===================================
print "Comienza la ejecución: Hora -> ", asctime(localtime());
start_time = time()

"""
'get_ClasiASes_RRCs': Obtener un dataframe de los distintos ASes encontrados en
el total de los colectores, pero además conociendo el comportamiento que han tenido
dichos ASes en los colectores, es decir... si fue visto como Monitor,Origen o Tránsito:
"""
get_ClasiASes_RRCs();

"""
'get_ASes_ClasiGeneral': Obtener un dataframe de los distintos ASes encontrados en
el total de los colectores, además de conocer las formas en las cuales dicho AS
fue visto en los colectores, es decir... si fue visto solo como origen, origen y monitor,
transito y origen, etc:
"""
get_ASes_ClasiGeneral();

"""
Analizar las combinaciones ASes-Clasificación que se han identificado en el total
de los colectores, partiendo de la información de los ASPATHs:
"""

Header_ClasiAS = ['AS_Clasi','AS','Clasi'];
file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Clasi_ASes_RRCs.txt'
df_ClasiASes =  pd.read_csv(file_read, sep='|',header=None, names = Header_ClasiAS);

Header_ASPATHs = ['ASPATH_Original','RRC_ID','count_Announced','count_Announced_Comm','Pcount_Announced_Comm',\
        'Tag_count_Announced_Comm','Tag_Prep','ASPATH','long_ruta','Clasi_ASes','Communities',\
        'ASes_Comm','ASesASPATH_Comm','Hops_Comm','iden_ASes_aspath','Range_ASes_aspath',\
        'iden_ASes_comm','Range_ASes_comm','Macheo_ASes_aspath_comm']

file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_RRCs.txt'
df_aspaths = pd.read_csv(file_read, sep='|',header=None, names = Header_ASPATHs);
# Quedarse con las columnas necesarias para este análisis:
df_ASes = df_aspaths[['ASPATH_Original','Clasi_ASes','Communities','ASesASPATH_Comm']]

data_ASClasi = info_ASes(df_ASes,df_ClasiASes)
df_ASClasi = pd.DataFrame.from_dict(data_ASClasi,orient='index')
df_ASClasi.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Info_ASesClasi.txt',\
            sep='|',header=None, index=True)

print "Termina la ejecución: Hora -> ", asctime(localtime());
elapsed_time = time() - start_time
print("Tiempo de ejecucion: "+ str(elapsed_time))
