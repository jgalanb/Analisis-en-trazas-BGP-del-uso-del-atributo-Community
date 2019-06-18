#!/bin/sh

for i in $(ls /srv/agarcia/TFM-BGP/DATA);do
	echo "$i"
	cd /srv/agarcia/TFM-BGP/Jesus/DATA
	mkdir "$i"
	cd /srv/agarcia/TFM-BGP/Jesus/bgpdump
	for j in $(ls /srv/agarcia/TFM-BGP/DATA/"$i");do
		./bgpdump -m -l /srv/agarcia/TFM-BGP/DATA/"$i"/"$j" -O /srv/agarcia/TFM-BGP/Jesus/DATA/"$i"/"$j".txt
		echo "$j"
	done;
done;

echo Completed
