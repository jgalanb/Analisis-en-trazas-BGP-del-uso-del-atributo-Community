#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Para ejecutar este archivo:
nohup ./ParaDescargar_v2.py > /srv/agarcia/TFM-BGP/DATA_Generation/output.out &
"""

from urllib.request import urlopen
from os import listdir,mkdir;
import re
import wget

def obtener_ficheros_dia(rrc,date):
    try:
        url = 'http://data.ris.ripe.net/' + rrc + '/' + date;

        website = urlopen(url)
        html = website.read()
        html = html.decode("utf-8")
        files = re.findall('href="(bview.20180110.*.gz)"', html)
        files2 = re.findall('href="(updates.20180110.*.gz)"', html)
        files.reverse()
        files2.reverse()
        files.extend(files2)

    except:
        files = -1
    return [files,url]


date = '2018.01'

for rrc_num in range(0,24):

    if rrc_num != 22:

        if rrc_num < 10:

            rrc = 'rrc0' + str(rrc_num)

        else:

            rrc = 'rrc'+str(rrc_num)

        source = rrc+'.ripe'


        [files,url] = obtener_ficheros_dia(rrc,date)

        if files != -1:

            mkdir("/srv/agarcia/TFM-BGP/DATA/" + source);

            output_directory = "/srv/agarcia/TFM-BGP/DATA/" + source;

            for file_sub in files:
                filename = wget.download(url + "/" + file_sub, out=output_directory)

print ('Download Completed!');
