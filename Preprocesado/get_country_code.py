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

# Fuente: https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv

Header = ['Region','CC','CC_binary']
file_read = '/srv/agarcia/TFM-BGP/Jesus/RFCs/Country_Code.txt'
df_CC = pd.read_csv(file_read, sep='|',header=None, names=Header);
df_CC = df_CC.fillna({'Region':'NA'})

df_CC = list(df_CC.Region.unique())

print df_CC;
sys.exit();

file_read = '/srv/agarcia/TFM-BGP/Jesus/RFCs/CC.csv'
df = pd.read_csv(file_read)
df = df.rename(columns={'country-code': 'country_code', 'sub-region':'sub_region'})
df = df.fillna({'country_code':'-'})
df = df.fillna({'region':'Antarctica'})
df = df.fillna({'sub_region':'-'})

Header_drop = ['alpha-2','alpha-3','iso_3166-2','intermediate-region','region-code',\
                'sub-region-code','intermediate-region-code']
df = df.drop(columns = Header_drop)

region_iden = ['AF','OC','AS','AQ','EU','LAC','NA']

Header = ['Region','CC','CC_binary']
df_CC = pd.DataFrame([], columns = Header)
for region in region_iden:

    if region == 'AF':
        region_found = 'Africa'
        df_region = df[df['region'] == region_found]
    elif region == 'OC':
        region_found = 'Oceania'
        df_region = df[df['region'] == region_found]
    elif region == 'AS':
        region_found = 'Asia'
        df_region = df[df['region'] == region_found]
    elif region == 'AQ':
        region_found = 'Antarctica'
        df_region = df[df['region'] == region_found]
    elif region == 'EU':
        region_found = 'Europe'
        df_region = df[df['region'] == region_found]
    elif region == 'LAC':
        region_found = 'Latin America and the Caribbean'
        df_region = df[df['sub_region'] == region_found]
    elif region == 'NA':
        region_found = 'Northern America'
        df_region = df[df['sub_region'] == region_found]
    else:
        print "Mmm..."
        sys.exit();

    country_codes = list(df_region.country_code)
    for code in country_codes:
        code = int(code)
        code_binary = np.binary_repr(code, width=10)

        info = [];
        info.append(region)
        info.append(code)
        info.append(code_binary)

        df_inter = pd.DataFrame([info],columns = Header)
        df_CC = df_CC.append(df_inter, sort=False)

print df_CC

df_CC.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/RFCs/Country_Code.txt',\
                sep='|',header=None, index=None)
