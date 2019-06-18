#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Importación de librerias empleadas en el codigo:
"""
import sys, re;
from os import *
import pandas as pd
import numpy as np

def create_mega_dataframe(list_df, Header_CAIDA):

    df_all_files = pd.DataFrame([], columns = Header_CAIDA)

    for df in list_df:
        df_all_files = df_all_files.append(df, sort=True)

    df_all_files.sort_values('AS')
    df_all_files.drop_duplicates(subset=['AS'], keep='last',inplace = True)

    return df_all_files;

# =================================== Main() ===================================

list_files_CAIDA = ['20150801.as2types.txt', '20181101.as2types.txt', '20181201.as2types.txt',\
                    '20190101.as2types.txt','20190201.as2types.txt'];

Header_CAIDA = ['AS','source','type']

list_df = [];

for file in list_files_CAIDA:
    df = pd.read_csv('/srv/agarcia/TFM-BGP/Jesus/CAIDA/' + file, sep='|',  \
                        header=None, names=Header_CAIDA);
    list_df.append(df)

df_all_files = create_mega_dataframe(list_df, Header_CAIDA)

df_all_files.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/CAIDA/df_CAIDAResult.txt',sep='|',header=None, index=None)
