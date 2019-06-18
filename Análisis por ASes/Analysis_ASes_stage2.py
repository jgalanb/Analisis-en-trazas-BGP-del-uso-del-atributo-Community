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
La función 'get_tag' me volverá una etiqueta nunca/alguna vez/casi siempre/siempre
dependiendo del valor de porcentaje de entrada en dicha función:
"""
def get_tag(porcentaje):

    if porcentaje == 0.0:
        tag = 'Nunca';
    elif porcentaje == 100.0:
        tag = 'Siempre';
    elif porcentaje >= 90.0:
        tag = 'Casi siempre'
    else:
        tag = 'Alguna vez'

    return tag;

"""
'completar_info' devolverá  un diccionario con aquellos ASes que fueron
encontrados, y los siguientes valores:
    - AS-Clasificación
    - AS
    - Clasificación en dicho colector
    - Clasificación general (¿cómo ha sido visto en todos los colectores?)
    - Número de ASPATHs en los que se ve dicho AS
    - Número de ASPATHs en los que se ve que dicho AS pone algún valor de community
    - Porcentaje de ocurrencia
    - Tag (nunca/alguna vez/(casi) siempre)
    - Valores de communities que anuncia el AS
"""
def completar_info():

    Header_ClasiGeneral = ['AS','ClasiGeneral']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASes_ClasiGeneral.txt'
    df_ClasiGeneral =  pd.read_csv(file_read, sep='|',header=None, names = Header_ClasiGeneral);

    Header = ['AS_Clasi','count_aspaths','count_aspaths_comm','ValuesComm']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Info_ASesClasi.txt'
    df_ASesClasi = pd.read_csv(file_read, sep='|',header=None, names = Header);

    ASesClasi = list(df_ASesClasi.AS_Clasi)

    data_ASClasi = {};
    for ASClasi in ASesClasi:
        info = [];

        # Identificación del AS, clasifición RRC y clasficación general:
        AS = ASClasi.split("-")[0]
        info.append(AS)
        Clasi_RRC = ASClasi.split("-")[1]
        info.append(Clasi_RRC)
        df = df_ClasiGeneral[df_ClasiGeneral['AS'] == int(AS)]
        Clasi_General = df.ClasiGeneral.item();
        info.append(Clasi_General)

        # Número de ASPATHs en los que se ve dicho AS:
        df_ASClasi = df_ASesClasi[df_ASesClasi['AS_Clasi'] == ASClasi]
        count_aspaths = df_ASClasi.count_aspaths.item();
        info.append(count_aspaths)

        # Número de ASPATHs en los que se ve que dicho AS pone algún valor de community:
        count_aspaths_comm = df_ASClasi.count_aspaths_comm.item();
        info.append(count_aspaths_comm)

        # Porcentaje de ocurrencia:
        try:
            porcentaje_comm = float(float(count_aspaths_comm)/(float(count_aspaths)))
            porcentaje_comm = float(porcentaje_comm)*float(100)
            porcentaje_comm_str = "{0:.3f}".format(porcentaje_comm)
        except ZeroDivisionError:
            porcentaje_comm = 0.0;
            porcentaje_comm_str = "{0:.3f}".format(porcentaje_comm)

        info.append(porcentaje_comm_str)

        # Etiqueto el resultado obtenido:
        tag_comm = get_tag(porcentaje_comm)
        info.append(tag_comm)

        # Valores de communities que anuncia el AS:
        if tag_comm != 'Nunca':
            communities = df_ASClasi.ValuesComm.item();
            valuesComm = communities.split(" ")[1:]
            communities_unique = [];
            for value in valuesComm:
                if not value in communities_unique and value != 'X':
                    communities_unique.append(value)
            ValuesComm = ' '.join(communities_unique)
            info.append(ValuesComm)
        else:
            info.append('Nunca-Communities')

        data_ASClasi.update({ASClasi:info})

    df_ASClasi = pd.DataFrame.from_dict(data_ASClasi,orient='index')
    df_ASClasi.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Info_ASesClasi_RRCs.txt',\
                sep='|',header=None, index=True)

    return None;

"""
'analysis_ASes': Analizar los ASes que se han encontrado en el total de colectores:
"""
def analysis_ASes():

    Header_ASesClasi = ['AS_Clasi','AS','ClasiRRC','ClasiGeneral','count_aspaths','count_aspaths_comm',\
                    'porcentaje_comm','tag_comm','ValuesComm']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Info_ASesClasi_RRCs.txt'
    df_ASes = pd.read_csv(file_read, sep='|',header=None, names = Header_ASesClasi);

    # Agrupar información por AS:
    # (Puede tener distinta información dependiendo de la clasificación hecha)
    ASes = list(df_ASes.AS.unique())
    df_ASes = df_ASes.groupby('AS')

    data_AS = {};
    for AS in ASes:
        info = [];
        df_AS = df_ASes.get_group(AS)

        # Clasificación general del AS:
        ClasiGeneral_AS = list(df_AS.ClasiGeneral.unique());
        if len(ClasiGeneral_AS) == 1:
            info.append(ClasiGeneral_AS[0])
        else:
            print "Problemaaaa!"
            sys.exit();

        # Número de ASPATHs en los que aparece el AS:
        count_aspaths_info = list(df_AS.count_aspaths)
        count_aspaths_info = map(int, count_aspaths_info)
        count_aspaths_info = sum(count_aspaths_info)
        info.append(count_aspaths_info)

        # Número de ASPATHs en los que el AS pone algún valor de community:
        count_aspaths_comm_info = list(df_AS.count_aspaths_comm)
        count_aspaths_comm_info = map(int, count_aspaths_comm_info)
        count_aspaths_comm_info = sum(count_aspaths_comm_info)
        info.append(count_aspaths_comm_info)

        # Porcentaje de ocurrencia:
        try:
            porcentaje_comm = float(float(count_aspaths_comm_info)/(float(count_aspaths_info)))
            porcentaje_comm = float(porcentaje_comm)*float(100)
            porcentaje_comm_str = "{0:.3f}".format(porcentaje_comm)
        except ZeroDivisionError:
            porcentaje_comm = 0.0;
            porcentaje_comm_str = "{0:.3f}".format(porcentaje_comm)

        info.append(porcentaje_comm_str)

        # Etiqueto el resultado obtenido:
        tag_comm = get_tag(porcentaje_comm)
        info.append(tag_comm)

        # Valores de communities:
        seq_communities = list(df_AS.ValuesComm.unique())
        if len(seq_communities) == 1:
            info.append(seq_communities[0])
        else:
            communities_ASes = [];
            for seq_community in seq_communities:
                communities = seq_community.split(" ")
                for comm in communities:
                    if not comm in communities_ASes and comm != 'Nunca-Communities':
                        communities_ASes.append(comm)

            communities_ASes_str = ' '.join(communities_ASes)
            info.append(communities_ASes_str)

        data_AS.update({AS:info})

    df_AS = pd.DataFrame.from_dict(data_AS,orient='index')
    df_AS.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Info_ASes_RRCs.txt',\
                sep='|',header=None, index=True)

    return None;

"""
'analysis_ASComm': Se analizan los pares AS:Comm distintos que se han encontrado.
Da igual que el AS se comporte como monitor,tránsito u origen, se analizan todos.
"""
def analysis_ASComm():

    Header = ['AS','ClasiGeneral','count_aspaths','count_aspaths_comm','porcentaje_comm',\
                'tag_comm','ValuesComm']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Info_ASes_RRCs.txt'
    df_ASes = pd.read_csv(file_read, sep='|',header=None, names = Header);

    # Tags communities de estudio:
    tags_study = ['Siempre', 'Casi siempre','Alguna vez']
    for tag in list(df_ASes.tag_comm.unique()):
        if not tag in tags_study:
            df_ASes = df_ASes[df_ASes['tag_comm'] != tag]

    # Lista de ASes resultante:
    ASes = list(df_ASes.AS)

    ASesComm = [];
    for AS in ASes:
        df_AS = df_ASes[df_ASes['AS'] == int(AS)]
        valuesComm = df_AS.ValuesComm.item();

        values = valuesComm.split(" ")
        for value in values:
            if not value in ASesComm:
                ASesComm.append(value)

    data_ASValue = {};
    for community in ASesComm:
        info = [];

        comm = community.split(":")

        # ASMonitor:
        ASMonitor = comm[0]
        info.append(ASMonitor)

        # ¿Es community regular o large?
        if len(comm) == 2:
            tag = 'Regular'
        elif len(comm) == 3:
            tag = 'Large'
        else:
            tag = 'Mmmm...'
        info.append(tag)

        data_ASValue.update({community:info})

    df_ASValue = pd.DataFrame.from_dict(data_ASValue,orient='index')

    df_ASValue.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASValueComm_RRCs.txt',\
                sep='|',header=None, index=True)

    return None;

def analysis_ASOrigenComm():

    Header = ['AS','ClasiGeneral','count_aspaths','count_aspaths_comm','porcentaje_comm',\
                'tag_comm','ValuesComm']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Info_ASes_RRCs.txt'
    df_ASes = pd.read_csv(file_read, sep='|',header=None, names = Header);

    # Filtramos por aquellos ASes que solo se han visto como origen:
    df_ASes = df_ASes[df_ASes['ClasiGeneral'] == 'Origen']

    # Tags communities de estudio:
    tags_study = ['Siempre', 'Casi siempre','Alguna vez']
    for tag in list(df_ASes.tag_comm.unique()):
        if not tag in tags_study:
            df_ASes = df_ASes[df_ASes['tag_comm'] != tag]

    # Lista de ASes resultante:
    ASes = list(df_ASes.AS)

    ASesComm = [];
    for AS in ASes:
        df_AS = df_ASes[df_ASes['AS'] == int(AS)]
        valuesComm = df_AS.ValuesComm.item();

        values = valuesComm.split(" ")
        for value in values:
            if not value in ASesComm:
                ASesComm.append(value)

    data_ASValue = {};
    for community in ASesComm:
        info = [];

        comm = community.split(":")

        # ASMonitor:
        ASMonitor = comm[0]
        info.append(ASMonitor)

        # ¿Es community regular o large?
        if len(comm) == 2:
            tag = 'Regular'
        elif len(comm) == 3:
            tag = 'Large'
        else:
            tag = 'Mmmm...'
        info.append(tag)

        data_ASValue.update({community:info})

    df_ASValue = pd.DataFrame.from_dict(data_ASValue,orient='index')
    df_ASValue.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASOrigenValueComm_RRCs.txt',\
                sep='|',header=None, index=True)

    return None;

def analysis_ASTransitoComm():

    Header = ['AS','ClasiGeneral','count_aspaths','count_aspaths_comm','porcentaje_comm',\
                'tag_comm','ValuesComm']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/Info_ASes_RRCs.txt'
    df_ASes = pd.read_csv(file_read, sep='|',header=None, names = Header);

    # Filtramos por aquellos ASes que alguna vez se hayan visto como tránsito:
    df_ASes = df_ASes[df_ASes['ClasiGeneral'].str.contains('Transito')]

    # Tags communities de estudio:
    tags_study = ['Siempre', 'Casi siempre','Alguna vez']
    for tag in list(df_ASes.tag_comm.unique()):
        if not tag in tags_study:
            df_ASes = df_ASes[df_ASes['tag_comm'] != tag]

    # Lista de ASes resultante:
    ASes = list(df_ASes.AS)

    ASesComm = [];
    for AS in ASes:
        df_AS = df_ASes[df_ASes['AS'] == int(AS)]
        valuesComm = df_AS.ValuesComm.item();

        values = valuesComm.split(" ")
        for value in values:
            if not value in ASesComm:
                ASesComm.append(value)

    data_ASValue = {};
    for community in ASesComm:
        info = [];

        comm = community.split(":")

        # ASMonitor:
        ASMonitor = comm[0]
        info.append(ASMonitor)

        # ¿Es community regular o large?
        if len(comm) == 2:
            tag = 'Regular'
        elif len(comm) == 3:
            tag = 'Large'
        else:
            tag = 'Mmmm...'
        info.append(tag)

        data_ASValue.update({community:info})

    df_ASValue = pd.DataFrame.from_dict(data_ASValue,orient='index')
    df_ASValue.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASTransitoValueComm_RRCs.txt',\
                sep='|',header=None, index=True)

    return None;

def analysis_rango_ASes():

    Header_ClasiGeneral = ['AS','ClasiGeneral']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASes_ClasiGeneral.txt'
    df_ClasiGeneral =  pd.read_csv(file_read, sep='|',header=None, names = Header_ClasiGeneral);

    ASes = list(df_ClasiGeneral.AS.unique())

    data_AS = {};
    for AS in ASes:
        info = [];
        df_AS = df_ClasiGeneral[df_ClasiGeneral['AS'] == int(AS)]
        Clasi_general = df_AS.ClasiGeneral.item()
        info.append(Clasi_general)

        if int(AS) <= 65535:
            # ASes 16 bits
            if int(AS) == 0:
                iden = 'Reservado_0'
            elif int(AS) >= 1 and int(AS) <= 23455:
                iden = 'Público_16b'
            elif int(AS) == 23456:
                iden = 'AS_TRANS'
            elif int(AS) >= 23457 and int(AS) <= 64495:
                iden = 'Público_16b'
            elif int(AS) >= 64496 and int(AS) <= 64511:
                iden = 'Reservado_Doc_16b'
            elif int(AS) >= 64512 and int(AS) <= 65534:
                iden = 'Privado_16b'
            elif int(AS) == 65535:
                iden = 'Reservado_65535'

        elif int(AS) > 65535:
            # ASes 32 bits
            if int(AS) >= 65536 and int(AS) <= 65551:
                iden = 'Reservado_Doc_32b'
            elif int(AS) >= 65552 and int(AS) <= 131071:
                iden = 'Reservado_32b'
            elif int(AS) >= 131072 and int(AS) <= 4199999999:
                iden = 'Público_32b'
            elif int(AS) >= 4200000000 and int(AS) <= 4294967294:
                iden = 'Privado_32b'
            elif int(AS) == 4294967295:
                iden = 'Reservado_4294967295'
        else:
            iden = 'Unknown'

        info.append(iden)
        data_AS.update({AS:info})

    df_AS = pd.DataFrame.from_dict(data_AS,orient='index')
    df_AS.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASesRango_RRCs.txt',\
                sep='|',header=None, index=True)

    return None;

def anaysis_CAIDA_ASes():

    # Análisis CAIDA (tipo de AS):
    # types: Content|Enterpise|Transit/Access
    Header_CAIDA = ['AS','source','type']
    df_CAIDA = pd.read_csv('/srv/agarcia/TFM-BGP/Jesus/CAIDA/df_CAIDAResult.txt', sep='|',  \
                        header=None, names=Header_CAIDA);

    Header = ['AS','ClasiGeneral']
    file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASes_ClasiGeneral.txt'
    df_ClasiGeneral = pd.read_csv(file_read, sep='|',header=None, names=Header);

    ASes = list(df_ClasiGeneral.AS.unique())
    df_ASes = df_ClasiGeneral.groupby('AS')

    data_ASes = {};
    for AS in ASes:
        info = [];
        df_AS = df_ASes.get_group(AS)
        Clasi_General = df_AS.ClasiGeneral.item()
        info.append(Clasi_General)

        # Clasificación CAIDA para el AS:
        df = df_CAIDA[df_CAIDA['AS'] == int(AS)]
        if df.empty:
            type_AS = 'Unknown'
        else:
            type_AS = df.type.item()

        info.append(type_AS)
        data_ASes.update({AS:info})

    df = pd.DataFrame.from_dict(data_ASes,orient='index')
    df.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASes_CAIDA.txt',\
                sep='|',header=None, index=True)

    return None;

"""
'analisis_RegularComm':
    -
"""
def analisis_RegularComm():

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

    Header = ['Community','AS','Type'];
    file_read = file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASTransitoValueComm_RRCs.txt'
    df_Comm = pd.read_csv(file_read, sep='|',header=None, names=Header);
    df_Comm = df_Comm[df_Comm['Type'] == 'Regular']

    info_taxonomy = [];
    info_RFC = [];
    info_RFCSign = [];
    for index, row in df_Comm.iterrows():

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

    df_Comm.insert(3,'Taxonomy',info_taxonomy)
    df_Comm.insert(4,'RFC',info_RFC)
    df_Comm.insert(5,'RFC_Sign',info_RFCSign)

    df_Comm = df_Comm[['Community','AS','Type','Taxonomy','RFC','RFC_Sign']]

    df_Comm.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASes/ASTransitoValueComm_RRCs_RC.txt',\
                    sep='|',header=None, index=None)

    return None;

# =================================== Main() ===================================
print "Comienza la ejecución: Hora -> ", asctime(localtime());
start_time = time()

"""
'completar_info': Completar información referente a cada combinación AS Clasificación
identificada (69973):
"""
# completar_info()

"""
'analysis_ASes': Nos interesa la información desde el punto de vista de los ASes, y
no de las combinaciones ASEs-Clasi que hemos obtenido antes:
"""
# analysis_ASes();

"""
'analysis_ASComm': Se analizarán los pares AS:Comm distintos encontrados para aquellos
ASes que alguna vez/(casi) siempre ponen communities.
(Se consideran todos los ASes con independencia de la clasificación que tengan)
También se analizarán los ASes que solamente hayan sido vistos como origen, y finalmente
los ASes que alguna vez han sido vistos como tránsito:
"""
# analysis_ASComm();
# analysis_ASOrigenComm();
# analysis_ASTransitoComm();

"""
Análisis de los rangos de los ASes:
"""
analysis_rango_ASes();

"""
Análisis CAIDA de los ASEs:
"""
# anaysis_CAIDA_ASes();

"""
Análisis de las communities regulares en los ASes, ASes origen y ASes tránsito:
"""
# analisis_RegularComm();

print "Termina la ejecución: Hora -> ", asctime(localtime());
elapsed_time = time() - start_time
print("Tiempo de ejecucion: "+ str(elapsed_time))
