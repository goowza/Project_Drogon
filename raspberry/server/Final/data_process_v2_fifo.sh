#!/bin/bash


FIFO=`pwd`/fifo1
FIFO2=`pwd`/fifo2
if [  -d "fifo1" ] ; then
rm fifo1
fi
if [  -d "fifo2" ] ; then
rm fifo2
fi
[ -p "$FIFO" ] ||mkfifo "$FIFO"
[ -p "$FIFO2" ] ||mkfifo "$FIFO2"

folderRelevant=("Pertinent" "noPertinent")
folderEvent=("Accident" "TrafficJam" "Location" "Others")
folderUser=("Pedestrian" "Car" "EmergencyVehicle" "Bollard" "Others")
for h in ${folderRelevant[@]}
do
if [ ! -d "$h" ] ; then
	mkdir $h
	fi
for i in ${folderEvent[@]}
do     
	if [ ! -d "$h/$i" ] ; then
	mkdir $h/$i
	fi
	for j in ${folderUser[@]}
	do
	if [ ! -d "$h/$i/$j" ] ; then
	mkdir  $h/$i/$j
	fi
	done
done
done
	oldIFS=$IFS
	IFS=$'\n'
			while [ 1 ]
			do
			folderEventBis=("Accident" "TrafficJam" )
for k in ${folderEventBis[@]}
do 
for i in $(ls `pwd`/noPertinent/$k/Pedestrian); do
		if [ -f `pwd`/noPertinent/$k/Pedestrian/$i ]; then
		line=$( sed -n "2 p"  `pwd`/noPertinent/$k/Pedestrian/$i)
		day=$(echo "$line" | awk '{print $1}' | cut -c1-2 ) ;
		date=$( echo "$line" | awk '{print $1}' ) ;
			month=$(echo "$line" | awk '{print $1}'  | cut -c4-5 ) ;
			an=$(echo "$line"| awk '{print $1}'  | cut -c7- ) ;
			heureH=$(echo "$line" | awk '{print $2}'  | cut -c1-2) ;
			heureM=$(echo "$line" | awk '{print $2}' | cut -c4-5) ;
			heureS=$(echo "$line" | awk '{print $2}'  | cut -c7-8) ;
			lat=$(echo "$line"| awk -F ":" '{print $3}' ) ;
			long=$(echo "$line" | awk -F ":" '{print $2}'  | cut -c4-) ;
			ipAdr=$(echo "$line" | awk -F ":" '{print $4}') ;
			sec_file=$(date -d "$an-$month-$day $heureH:$heureM:$heureS" +%s)
			fi
    for j in $(ls `pwd`/noPertinent/$k/Pedestrian); do
				if [ -f `pwd`/noPertinent/$k/Pedestrian/$j ] ; then
				line=$( sed -n "2 p"  `pwd`/noPertinent/$k/Pedestrian/$j)
				
				day2=$( echo "$line" | awk '{print $1}' | cut -c1-2 ) ;
				month2=$(echo "$line" | awk '{print $1}'  | cut -c4-5 ) ;
				an2=$(echo "$line"| awk '{print $1}'  | cut -c7- ) ;
				heureH2=$(echo "$line" | awk '{print $2}'  | cut -c1-2) ;
				heureM2=$(echo "$line" | awk '{print $2}' | cut -c4-5) ;
				heureS2=$(echo "$line" | awk '{print $2}'  | cut -c7-8) ;
				lat2=$(echo "$line"| awk -F ":" '{print $3}' ) ;
				long2=$(echo "$line" | awk -F ":" '{print $2}'  | cut -c4-) ;
				ipAdr2=$(echo "$line" | awk -F ":" '{print $4}') ;
				sec_file2=$(date -d "$an2-$month2-$day2 $heureH2:$heureM2:$heureS2" +%s)
				fi
    for h in $(ls `pwd`/noPertinent/$k/Pedestrian); do
				if [ -f `pwd`/noPertinent/$k/Pedestrian/$h ] ; then
				line=$( sed -n "2 p"  `pwd`/noPertinent/$k/Pedestrian/$h)
					day3=$( echo "$line" | awk '{print $1}' | cut -c1-2 ) ;
					month3=$(echo "$line" | awk '{print $1}'  | cut -c4-5 ) ;
					an3=$(echo "$line"| awk '{print $1}'  | cut -c7- ) ;
					heureH3=$(echo "$line" | awk '{print $2}'  | cut -c1-2) ;
					heureM3=$(echo "$line" | awk '{print $2}' | cut -c4-5) ;
					heureS3=$(echo "$line" | awk '{print $2}'  | cut -c7-8) ;
					lat3=$(echo "$line"| awk -F ":" '{print $3}' ) ;
					long3=$(echo "$line" | awk -F ":" '{print $2}'  | cut -c4-) ;
					ipAdr3=$(echo "$line" | awk -F ":" '{print $4}') ;
					sec_file3=$(date -d "$an3-$month3-$day3 $heureH3:$heureM3:$heureS3" +%s)
					diff=$(( ($sec_file2 - $sec_file) / 60)) #min
					diff2=$(( ($sec_file3 - $sec_file) / 60)) #min
					diffabs=${diff#-}
					diffabs2=${diff2#-}
					#dist1=$(./dist $lat $long $lat2 $long2)
					#echo $dist1 "dist"
					#dist2=$(./dist $lat $long $lat3 $long3)
					#echo $dist2 "dist2"
					#seuil=1000.0
					#&& [ $(echo "$dist1 < $seuil" |bc -l) ] && [ $(echo "$dist2 < $seuil" |bc -l) ] 
        if ([ ! "$j" = "$i" ]) && ([ ! "$h" = "$i" ]) && ([ ! "$h" = "$j" ]) &&  ([ -f `pwd`/noPertinent/$k/Pedestrian/$j ]) &&  ([ -f `pwd`/noPertinent/$k/Pedestrian/$h ]) &&  ([ -f `pwd`/noPertinent/$k/Pedestrian/$i ]); then
	if ([ $day -eq $day2 ] && [ $day -eq $day3 ]) &&  ([ $month -eq $month2 ] && [ $month -eq $month3 ]) &&  ([ $an -eq $an2 ] && [ $an -eq $an3 ]) &&  ([ $diffabs -le 10 ] && [ $diffabs2 -le 10 ]) && ([ ! "$ipAdr2" = "$ipAdr" ]  && [ ! "$ipAdr3" = "$ipAdr" ] && [ ! "$ipAdr3" = "$ipAdr2" ])  ; then
			echo  "-------------------------------------------------------------------------------"
						line=$( sed -n "2 p"  `pwd`/noPertinent/$k/Pedestrian/$i)
						echo "Relevant Information notified" 
						echo "Trame received : $line" 
						echo "Event :  $k  on $date   " 
						echo " Location => (Latitude : $lat  ; Longitude  : $long )" 
						echo "-----------------------------------------------------------------------------"
						
						#line=$( sed -n "2 p"  `pwd`/noPertinent/$k/Pedestrian/$i)
						echo  "Relevant-Event :  $k  on $date at Location => (Latitude : $lat  ; Longitude  : $long )  "  >$FIFO2



		mv   `pwd`/noPertinent/$k/Pedestrian/$i `pwd`/Pertinent/$k/Pedestrian
		rm `pwd`/noPertinent/$k/Pedestrian/$h
		rm `pwd`/noPertinent/$k/Pedestrian/$j
    						
					fi
	
        fi
fi
    done
done
done
done

				if read  line <$FIFO ; then 
				if [ ! $line == " " ] 
				then
				date=$( echo "$line" | awk '{print $1}' ) ;
				day=$( echo "$line" | awk '{print $1}' | cut -c1-2 ) ;
				month=$(echo "$line" | awk '{print $1}'  | cut -c4-5 ) ;
				an=$(echo "$line"| awk '{print $1}'  | cut -c7- ) ;
				heure=$(echo "$line" | awk '{print $2}') ;
				heureH=$(echo "$line" | awk '{print $2}'  | cut -c1-2) ;
				heureM=$(echo "$line" | awk '{print $2}' | cut -c4-5) ;
				heureS=$(echo "$line" | awk '{print $2}'  | cut -c7-8) ;
				lat=$(echo "$line"| awk -F ":" '{print $3}' ) ;
				idCommande=$(echo "$line" | awk -F ":" '{print $2}' | cut -c3) ;
				idUser=$(echo "$line"| awk -F ":" '{print $2}' | cut -c2) ;
				long=$(echo "$line" | awk -F ":" '{print $2}'  | cut -c4-) ;
				ipAdr=$(echo "$line" | awk -F ":" '{print $4}') ;
				echo  $ipAdr
				echo "Decoding of the following frame :    $line"
	 			if [ ${idCommande} -eq 1 ] &&  [ ${idUser} -eq 1 ]
				then
						
						nameUser="Pedestrian"
						nameCommande='TrafficJam'
						echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
						mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/noPertinent/TrafficJam/Pedestrian
				
				elif [ ${idCommande} -eq 1 ] &&  [ ${idUser} -eq 0 ] 
				then
					nameUser="Car"
					nameCommande='TrafficJam'
					echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";		echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
					mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Pertinent/TrafficJam/Car
					
			  elif [ ${idCommande} -eq 1 ] &&  [ ${idUser} -eq 2 ] 
			  then
					
					nameUser="Bollard"
					nameCommande='TrafficJam'
					echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";  
						echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
					mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Pertinent/TrafficJam/Bollard
			elif [ ${idCommande} -eq 1 ] &&  [ "$idUser" = "z" ] 
			then
				# embouitellage others
			
					nameUser="Others"
					nameCommande='TrafficJam'
					echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
					mv  `pwd`/"$nameUser$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/noPertinent/TrafficJam/Others
			elif [ ${idCommande} -eq 1 ] &&  [ ${idUser} -eq 3 ] 
			then
			
					nameUser="EmergencyVehicle"
					nameCommande='TrafficJam'
					echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
					mv  `pwd`/"$nameUser$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Pertinent/TrafficJam/EmergencyVehicle
		
			elif [ ${idCommande} -eq 0 ] &&  [ ${idUser} -eq 1 ] 
			then
			
					nameUser="Pedestrian"
					nameCommande='Accident'
					echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
					mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/noPertinent/Accident/Pedestrian

			elif [ ${idCommande} -eq 0 ] &&  [ ${idUser} -eq 2 ] 
			then
				
					nameUser="Bollard"
					nameCommande='Accident'
					echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
					mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Pertinent/Accident/Bollard
			elif [ ${idCommande} -eq 0 ] &&  [ ${idUser} -eq 0 ] 
			then
				
		
					nameUser="Car"
					nameCommande='Accident'
					echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
					mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Pertinent/Accident/Car
			elif [ ${idCommande} -eq 0 ] &&  [ "${idUser}" = "z" ] 
			then
		
				nameUser="Others"
				nameCommande='Accident'
				echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/noPertinent/Accident/Others
	
			elif [ ${idCommande} -eq 0 ] &&  [ ${idUser} -eq 3 ] 
			then
		
				nameUser="EmergencyVehicle"
				nameCommande='Accident'
				echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Pertinent/Accident/EmergencyVehicle

			elif [ ${idCommande} -eq 2 ] &&  [ ${idUser} -eq 3 ] 
			then
		
				nameUser="EmergencyVehicle"
				nameCommande='Location'
				echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Pertinent/Location/EmergencyVehicle
			elif [ ${idCommande} -eq 2 ] &&  [ ${idUser} -eq 1 ] 
			then
		
				nameUser="Pedestrian"
				nameCommande='Location'
				echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/noPertinent/Location/Pedestrian

			elif [ ${idCommande} -eq 2 ] &&  [ ${idUser} -eq 0 ] 
			then
		
				nameUser="Car"
				nameCommande='Location'
				echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Pertinent/Location/Car
			elif [ ${idCommande} -eq 2 ] &&  [ ${idUser} -eq 2 ] 
			then
		
				nameUser="Bollard"
				nameCommande='Location'
				echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Pertinent/Location/Bollard
			elif [ ${idCommande} -eq 2 ] &&  [ "${idUser}" = "z" ] 
			then
		
				nameUser="Others"
				nameCommande='Location'
				echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/noPertinent/Location/Others
			elif [ "${idCommande}" = "z" ] &&  [ ${idUser} -eq 1 ] 
			then
			
				nameUser="Pedestrian"
				nameCommande='Others'
				echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/noPertinent/Others/Pedestrian
			elif [ "${idCommande}" = "z" ] &&  [ ${idUser} -eq 0 ] 
			then
			 	
				nameUser="Car"
				nameCommande='Others'
				echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
				
				echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/noPertinent/Others/Car
			elif [ "${idCommande}" = "z" ] &&  [ ${idUser} -eq 2 ] 
			then
				nameUser="Bollard"
				nameCommande='Others'
				echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/noPertinent/Others/Bollard
			elif [ "${idCommande}" = "z" ] &&  [ ${idUser} -eq 3 ] 
			then
				nameUser="EmergencyVehicle"
				nameCommande='Others'
				echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Others/EmergencyVehicle

			else
			
				nameUser="Others"
				nameCommande='Others'
				echo " $nameCommande notified by $nameUser (@IP :$ipAdr)"
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo " $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser (@IP :$ipAdr)" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/noPertinent/Others/Others
				fi
		 
		
			echo "End of the frame decoding :    $line" 
			echo "-------------------------------------------------"	
		fi
		
	fi

		
done	
	

