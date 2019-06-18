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

Header_ASPATHs = ['ASPATH','Communities','ASes_Comm','iden_ASes_ASPATH','iden_ASes_Comm','Macheo_ASes_aspath_comm']
file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_Stage2.txt'
df_aspaths = pd.read_csv(file_read, sep='|',header=None, names=Header_ASPATHs);

df_analysis = df_aspaths[df_aspaths['Macheo_ASes_aspath_comm'] == 'No matchean']
count_total_ASPATHs = len(df_analysis)
print "ASPATHs considerados: ",len(df_analysis)

list_iden_ASes_ASPATH = list(df_analysis.iden_ASes_ASPATH.unique())
list_iden_ASes_Comm = list(df_analysis.iden_ASes_Comm.unique())

comb = 1;
data_comb = {};
for ASes_ASPATH in list_iden_ASes_ASPATH:
    for ASes_Comm in list_iden_ASes_Comm:
        info = [];
        df_stage1 = df_analysis[df_analysis['iden_ASes_ASPATH'] == ASes_ASPATH]
        df_stage2 = df_stage1[df_stage1['iden_ASes_Comm'] == ASes_Comm]

        count_aspaths = len(df_stage2)

        percentage = float(count_aspaths)/float(count_total_ASPATHs)
        percentage = float(percentage)*float(100)

        info.append(ASes_ASPATH)
        info.append(ASes_Comm)
        info.append(count_aspaths)
        info.append(percentage)
        data_comb.update({comb:info})
        comb = comb + 1

df_result = pd.DataFrame.from_dict(data_comb,orient='index')
df_result.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_stage2_no_matchean.txt',\
            sep='|',header=None, index=True)

Header = ['ID_Comb','iden_ASes_ASPATH','iden_ASes_Comm','count_aspaths','percentage']
file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_stage2_no_matchean.txt'
df_result = pd.read_csv(file_read, sep='|',header=None, names=Header);

df_result = df_result[df_result['count_aspaths'] != 0]
df_result = df_result.sort_values(by='count_aspaths', ascending=False)
df_result = df_result.drop(['ID_Comb'], axis=1)
ID_Comb = range(1,len(df_result) + 1)
df_result.insert(0,'ID_Comb',ID_Comb)
df_result.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/ASPATH-Comm/ASPATHs_stage2_no_matchean.txt',\
            sep='|',header=None, index=None)
