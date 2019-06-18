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

# https://matplotlib.org/devdocs/tutorials/colors/colors.html

""" ============================= FUNCIONES ================================ """
def get_count(list_count):

    data_hop = {};
    for element in list_count:
        hops = element.split(" ")
        for hop in hops:
            hop_count = hop.split(":")
            list_hop = data_hop.get(hop_count[0])
            if list_hop == None:
                data_hop.update({hop_count[0]:hop_count[1]})
            else:
                count = int(list_hop) + int(hop_count[1])
                data_hop.update({hop_count[0]:count})

    df = pd.DataFrame.from_dict(data_hop,orient='index')
    df = df.reset_index();
    df = df.rename(columns={'index': 'Hop', 0: 'Count'})
    id_hops = [];
    for hop in df.Hop:
        i = hop.split('Hop')[1]
        id_hops.append(i)
    id_hops = map(int, id_hops)
    df.insert(1,'id_hops',id_hops)
    df = df.sort_values(by='id_hops', ascending=True)

    cadena = [];
    for hop in df.Hop:
        df_info_hop = df[df['Hop'] == hop]
        count = df_info_hop.Count.item();
        string = hop + ':' + str(count)
        cadena.append(string)

    cadena = ' '.join(cadena)

    return cadena;

"""
'join_information': Unir la información referente a cada una de las longitudes diferentes
 de rutas que se han identificado para cada colector:
"""
def join_information(df_rutas):

    long_rutas = list(df_rutas.long_ruta.unique())
    df_long_rutas = df_rutas.groupby('long_ruta')

    data_rutas = {};
    for rutas in long_rutas:
        info = [];
        df_long_ruta = df_long_rutas.get_group(rutas)

        count_rutas_total = list(df_long_ruta.count_rutas);
        count_rutas_total = map(int, count_rutas_total)
        info.append(sum(count_rutas_total))

        count_NUNCA_comm_total = list(df_long_ruta.count_NUNCA_comm);
        count_NUNCA_comm_total = map(int, count_NUNCA_comm_total)
        info.append(sum(count_NUNCA_comm_total))

        count_rutas_NoASesASPATH_total = list(df_long_ruta.count_rutas_NoASesASPATH);
        count_rutas_NoASesASPATH_total = map(int, count_rutas_NoASesASPATH_total)
        info.append(sum(count_rutas_NoASesASPATH_total))

        max_hopComm_total = list(df_long_ruta.max_hopComm);
        for n, i in enumerate(max_hopComm_total):
            if i == '-':
                max_hopComm_total[n] = -1
        max_hopComm_total = map(int, max_hopComm_total)
        info.append(max(max_hopComm_total))

        list_count_aspath = list(df_long_ruta.count_aspath)
        for n, i in enumerate(list_count_aspath):
            if i == '-':
                list_count_aspath[n] = 'Hop0:0'
        count_aspath_total = get_count(list_count_aspath)
        info.append(count_aspath_total)

        count_total_total = list(df_long_ruta.count_total);
        for n, i in enumerate(count_total_total):
            if i == '-':
                count_total_total[n] = 0
        count_total_total = map(int, count_total_total)
        info.append(sum(count_total_total))

        data_rutas.update({rutas:info})

    df = pd.DataFrame.from_dict(data_rutas,orient='index')
    df.to_csv(r'/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Rutas/Rutas_RRCs_join.txt',\
                        sep='|',header=None, index=True)

    return None;

"""
'plot_results': Representación de los resultados para cada longitud de ruta:
Obtendremos la información respecto al número de rutas totales que existen en cada
apartado.
"""
def plot_results(df_rutas):

    long_rutas = list(df_rutas.long_ruta.unique())
    df_long_rutas = df_rutas.groupby('long_ruta')

    for long_ruta in long_rutas:
        data_ruta = {};
        data_ruta_distance = {};
        df_info = df_long_rutas.get_group(long_ruta)

        # Total de rutas que existen:
        count_rutas_info = df_info.count_rutas.item()
        info = [];
        info.append(int(count_rutas_info))
        info.append(1)
        info.append('navy')
        data_ruta.update({'Total rutas':info})

        # Total de rutas que NUNCA ven communities:
        count_NUNCA_comm_info = df_info.count_NUNCA_comm.item()
        info = [];
        info.append(int(count_NUNCA_comm_info))
        info.append(2)
        info.append('red')
        data_ruta.update({'Rutas nunca ven comm':info})

        # Rutas que ven communities pero no son puestas por ASes que forman la ruta:
        count_rutas_NoASesASPATH_info = df_info.count_rutas_NoASesASPATH.item()
        info = [];
        info.append(int(count_rutas_NoASesASPATH_info))
        info.append(3)
        info.append('orange')
        data_ruta.update({'No comm ASes ASPATH':info})

        # Rutas que son analizadas:
        info = [];
        count_analysis = count_rutas_info - count_NUNCA_comm_info - count_rutas_NoASesASPATH_info
        info.append(int(count_analysis))
        info.append(4)
        info.append('green')
        data_ruta.update({'Rutas analizadas':info})

        # Rutas con communities a distancia cero, distancia uno, dos, etc:
        count = 1
        count_aspath_info = df_info.count_aspath.item()
        count_aspath_info = count_aspath_info.split(" ")
        for element in count_aspath_info:
            hop_count = element.split(":")
            info = [];
            info.append(int(hop_count[1]))
            info.append(count)
            info.append('blue')
            hop = 'Distancia ' + hop_count[0].split("Hop")[1]
            data_ruta_distance.update({hop:info})

            count = count + 1

        # Representación count rutas:
        df = pd.DataFrame.from_dict(data_ruta,orient='index')
        df = df.reset_index();
        df = df.rename(columns={'index': 'info', 0: 'Count', 1:'Orden', 2:'Color'})
        df_print = df.sort_values(by='Orden', ascending=True)

        id_color = list(df_print.Color)
        df_print.plot(kind='bar',x='info', y= 'Count', rot=90, fontsize=10,align='center',color=id_color, edgecolor='none',legend=False);
        plt.title(" ", fontsize=16, fontweight=0, \
                    color='black', loc='center', style='italic' )
        plt.suptitle('Rutas de longitud '+str(long_ruta), fontsize=16, fontweight=0, \
                    color='black', style='italic')
        plt.xlabel(' ')
        plt.ylabel('Número de rutas')
        plt.grid();

        savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Rutas/Graficas/grah_ruta'+str(long_ruta)+'.png',bbox_inches = "tight");
        plt.close

        # Representación count rutas:
        df = pd.DataFrame.from_dict(data_ruta_distance,orient='index')
        df = df.reset_index();
        df = df.rename(columns={'index': 'info', 0: 'Count', 1:'Orden', 2:'Color'})
        df_print = df.sort_values(by='Orden', ascending=True)

        id_color = list(df_print.Color)
        df_print.plot(kind='bar',x='info', y= 'Count', rot=90, fontsize=10,align='center',color=id_color, edgecolor='none',legend=False);
        plt.title(" ", fontsize=16, fontweight=0, \
                    color='black', loc='center', style='italic' )
        plt.suptitle('Distancia communities para rutas de longitud '+str(long_ruta), fontsize=16, fontweight=0, \
                    color='black', style='italic')
        plt.xlabel(' ')
        plt.ylabel('Número de rutas')
        plt.grid();

        savefig('/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Rutas/Graficas/grah_distance_ruta'+str(long_ruta)+'.png',bbox_inches = "tight");
        plt.close

    return None;

# =================================== Main() ===================================
print "Comienza la ejecución: Hora -> ", asctime(localtime());
start_time = time()

# Header_rutas = ['long_ruta','RRC_ID','count_rutas','count_NUNCA_comm','count_rutas_NoASesASPATH',\
#                 'max_hopComm','count_aspath','count_total']
#
# file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Rutas/Rutas_RRCs.txt';
# df_rutas = pd.read_csv(file_read, sep='|',header=None, names=Header_rutas);
#
# join_information(df_rutas)

Header_rutas = ['long_ruta','count_rutas','count_NUNCA_comm','count_rutas_NoASesASPATH',\
                'max_hopComm','count_aspath','count_total']
file_read = '/srv/agarcia/TFM-BGP/Jesus/Analysis/Results/Rutas/Rutas_RRCs_join.txt'
df_rutas = pd.read_csv(file_read, sep='|',header=None, names=Header_rutas);

plot_results(df_rutas)

print "Termina la ejecución: Hora -> ", asctime(localtime());
elapsed_time = time() - start_time
print("Tiempo de ejecucion: "+ str(elapsed_time))
