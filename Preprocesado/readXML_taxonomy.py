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
import xml.etree.ElementTree as ET
import collections

""" ============================== FUNCIONES =============================== """

# =================================== Main() ===================================

# xtree = ET.parse("CommunityTaxonomy-DataBase.xml")
# xroot = xtree.getroot()
#
# comm = [];
# generaltype = [];
# subtype = [];
# subsubtype = [];
# characterization = [];
# comment = [];
#
# for node in xroot:
#     for subnode in node:
#         info_comm = [];
#         for subsubnode in subnode:
#             if subsubnode.tag == 'community':
#                 community = subsubnode.text;
#                 comm.append(community)
#             elif subsubnode.tag == 'taxonomy':
#                 dicc = subsubnode.attrib;
#                 generaltype_value = dicc.get('generaltype')
#                 subtype_value = dicc.get('subtype')
#                 subsubtype_value = dicc.get('subsubtype')
#                 characterization_value = dicc.get('characterization')
#                 generaltype.append(generaltype_value)
#                 subtype.append(subtype_value)
#                 subsubtype.append(subsubtype_value)
#                 characterization.append(characterization_value)
#             elif subsubnode.tag == 'comment':
#                 comment_value = subsubnode.text
#                 comment.append(comment_value)
#
# colums_name = ['community','generaltype','subtype','subsubtype','characterization','comment']
# create_dataframe = list(zip(comm,generaltype,subtype,subsubtype,characterization,comment))
# df = pd.DataFrame(create_dataframe, columns=colums_name)
# df.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Results/taxonomy_database.txt',\
#                     sep='|',header=None, index=False)

Header = ['AS_Value','AS','Value','Type_AS','Flag','CAIDA','Range_AS','Type_Value']
typeIP = 'IPv4'
day = '20181201'
file_read = '/srv/agarcia/TFM-BGP/Jesus/Results/AS-Value/'+typeIP+'/ASValue_'+day+'.txt'
df_ASValue = pd.read_csv(file_read, sep='|', header=None, names=Header, index_col=False);

Header = ['community','generaltype','subtype','subsubtype','characterization','comment']
file_read = '/srv/agarcia/TFM-BGP/Jesus/CommunityTaxonomy/taxonomy_database.txt'
df_Taxonomy = pd.read_csv(file_read, sep='|', header=None, names=Header, index_col=False);
df_Taxonomy.drop_duplicates(subset=Header, keep='last',inplace = True)
# df_Taxonomy.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Results/taxonomy_database.txt',\
#                     sep='|',header=None, index=False)

lista = [];
for community in df_Taxonomy.community:
    lista.append(community)

counter_ValuesComm = collections.Counter(lista)
df = pd.DataFrame.from_dict(counter_ValuesComm, orient='index').reset_index()
df = df.rename(columns={'index': 'Community', 0: 'Counter'})
df = df.sort_values(by='Counter', ascending=False)
print df.head(10)
sys.exit();

dicc_macheo = {};
for ASValue in df_ASValue.AS_Value:
    info = [];
    df = df_Taxonomy[df_Taxonomy['community'] == ASValue]
    if not df.empty:
        info.append('Taxonomy_Found')
    else:
        info.append('Taxonomy_NotFound')

    dicc_macheo.update({ASValue:info})

df = pd.DataFrame.from_dict(dicc_macheo,orient='index')
df.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Results/macheo_' + day + '.txt',sep='|',header=None, index=True)

Header = ['AS_Value','Taxonomy']
file_read = '/srv/agarcia/TFM-BGP/Jesus/Results/macheo_' + day + '.txt'
df_Taxonomy_valid = pd.read_csv(file_read, sep='|', header=None, names=Header, index_col=False);

df_found = df_Taxonomy_valid[df_Taxonomy_valid['Taxonomy'] == 'Taxonomy_Found']

columns_name = ['community','generaltype','subtype','subsubtype','characterization','comment']
df_result = pd.DataFrame([],columns = columns_name)
ASValues = list(df_found.AS_Value)
print ASValues;
print len(ASValues)
for ASValue in ASValues:
    df = df_Taxonomy[df_Taxonomy['community'] == ASValue]
    df_result = df_result.append(df, sort=False)

df_result.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Results/macheo_' + day + '.txt',sep='|',header=None, index=False)
