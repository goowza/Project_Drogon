
#!/bin/bash

FIFO=`pwd`/fifo1
rm fifo1
[ -p "$FIFO" ] ||mkfifo "$FIFO"
folderEvent=("Accident" "TrafficJam" "Localisation" "Others")
folderUser=("Pedestrian" "Car" "EmergencyVehicle" "Bollard" "Others")
for i in ${folderEvent[@]}
do
	if [ ! -d "$i" ] ; then
	mkdir $i
	fi
	for j in ${folderUser[@]}
	do
	if [ ! -d "$i/$j" ] ; then
	mkdir  $i/$j
	fi
	done
done
	oldIFS=$IFS
	IFS=$'\n'
			while [ 1 ]
			do
				#if [ -s $fichier ]; then 
				if read  line <$FIFO ; then
				if [ ! $line == " " ] 
				then
				#line=$(head -n 1 $fichier)
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
				#echo "IDcommande " $idCommande
				idUser=$(echo "$line"| awk -F ":" '{print $2}' | cut -c2) ;
				long=$(echo "$line" | awk -F ":" '{print $2}'  | cut -c4-) ;
				echo "Decoding of the following frame :    $line"
	 			if [ ${idCommande} -eq 1 ] &&  [ ${idUser} -eq 1 ]
				then
						nameUser="Pedestrian"
						nameCommande='TrafficJam'
						touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
						mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/TrafficJam/Pedestrian
		
				elif [ $idCommande -eq 1 ] && [ $idUser -eq 0 ]
				then
					nameUser="Car"
					nameCommande='TrafficJam'
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
					mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/TrafficJam/Car
					
			   elif [ $idCommande -eq 1 ] && [ $idUser -eq 2]
			  then
					
					nameUser="Bollard"
					nameCommande='TrafficJam'
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
					mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/TrafficJam/Bollard
			elif [ $idCommande -eq 1 ] && [ $idUser = "z"];
			then
				# embouitellage others
			
					nameUser="Others"
					nameCommande='TrafficJam'
					touch "$nameUser$day$month$an_$heureH$heureM$heureS"".txt"
					echo  "--------------------------------">"$nameUser$day$month$an_$heureH$heureM$heureS"".txt"
					echo "Trame received : $line" >> "$nameUser$day$month$an_$heureH$heureM$heureS"".txt"
					echo "User ( $nameUser ) signalized a $nameCommande at $heure - $date" >>"$nameUser$day$month$an_$heureH$heureM$heureS"".txt"
					echo "Latitude : $lat   Longitude  : $long" >>"$nameUser$day$month$an_$heureH$heureM$heureS"".txt"
					echo "--------------------------------">> "$nameUser$day$month$an_$heureH$heureM$heureS"".txt"
					mv  `pwd`/"$nameUser$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/TrafficJam/Others
			elif [ $idCommande -eq 1 ] && [ $idUser -eq 3];
			then
				# embouitellage others
			
					nameUser="EmergencyVehicle"
					nameCommande='TrafficJam'
					touch "$nameUser$day$month$an_$heureH$heureM$heureS"".txt"
					echo  "--------------------------------">"$nameUser$day$month$an_$heureH$heureM$heureS"".txt"
					echo "Trame received : $line" >> "$nameUser$day$month$an_$heureH$heureM$heureS"".txt"
					echo "User ( $nameUser ) signalized a $nameCommande at $heure - $date" >>"$nameUser$day$month$an_$heureH$heureM$heureS"".txt"
					echo "Latitude : $lat   Longitude  : $long" >>"$nameUser$day$month$an_$heureH$heureM$heureS"".txt"
					echo "--------------------------------">> "$nameUser$day$month$an_$heureH$heureM$heureS"".txt"
					mv  `pwd`/"$nameUser$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/TrafficJam/EmergencyVehicle
		
			elif [ $idCommande -eq 0 ] && [ $idUser -eq 1 ]
			then
			
					nameUser="Pedestrian"
					nameCommande='Accident'
						touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
					mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Accident/Pedestrian
			elif [ $idCommande -eq 0 ] && [ $idUser -eq 2 ]
			then
				
					nameUser="Bollard"
					nameCommande='Accident'
						touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
					mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Accident/Bollard
			elif [ $idCommande -eq 0 ]  && [ $idUser -eq 0 ]	
			then
				
		
					nameUser="Car"
					nameCommande='Accident'
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
					mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Accident/Car
			elif [ $idCommande -eq 0  ] && [ $idUser = "z"] ;
			then
		
				nameUser="Others"
				nameCommande='Accident'
				touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Accident/Others
	
			elif [ $idCommande -eq 0  ] && [ $idUser -eq 3] ;
			then
		
				nameUser="EmergencyVehicle"
				nameCommande='Accident'
				touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Accident/EmergencyVehicle

			elif [ $idCommande -eq 2  ] && [ $idUser -eq 3] ;
			then
		
				nameUser="EmergencyVehicle"
				nameCommande='Localisation'
				touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Localisation/EmergencyVehicle
			elif [ $idCommande -eq 2 ] && [ $idUser -eq 1] ;
			then
		
				nameUser="Pedestrian"
				nameCommande='Localisation'
				touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Localisation/Pedestrian

			elif [ $idCommande -eq 2 ] && [ $idUser -eq 0] ;
			then
		
				nameUser="Car"
				nameCommande='Localisation'
				touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Localisation/Car
			elif [ $idCommande -eq 2 ] && [ $idUser -eq 2] ;
			then
		
				nameUser="Bollard"
				nameCommande='Localisation'
				touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Localisation/Bollard
			elif [ $idCommande -eq 2 ] && [ $idUser = "z"] ;
			then
		
				nameUser="Others"
				nameCommande='Localisation'
				touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Localisation/Others
			elif [ $idCommande = "z"  ] && [ $idUser -eq 1 ];
			then
			
				nameUser="Pedestrian"
				nameCommande='Others'
				touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  /home/tp-ada-insa/"$day$month$an_$heureH$heureM$heureS"".txt" /home/tp-ada-insa/Others/Pedestrian
			elif [ $idCommande = "z" ] && [ $idUser -eq 0 ]	;
			then
			 	
				nameUser="Car"
				nameCommande='Others'
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Others/Car
			elif [ $idCommande = "z" ] && [ $idUser -eq 2 ];
			then
				nameUser="Bollard"
				nameCommande='Others'
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Others/Bollard
			elif [ $idCommande = "z" ] && [ $idUser -eq 3 ];
			then
				nameUser="EmergencyVehicle"
				nameCommande='Others'
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Others/EmergencyVehicle
			else
			
				nameUser="Others"
				nameCommande='Others'
					touch "$day$month$an_$heureH$heureM$heureS"".txt";
						echo  "-------------------------------------------------------------------------------">"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Trame received : $line" >> "$day$month$an_$heureH$heureM$heureS"".txt";
						echo "From:  $nameUser " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Event :  $nameCommande at $heure on $date " >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "Latitude : $lat   Longitude  : $long" >>"$day$month$an_$heureH$heureM$heureS"".txt";
						echo "-----------------------------------------------------------------------------">> "$day$month$an_$heureH$heureM$heureS"".txt";
				mv  `pwd`/"$day$month$an_$heureH$heureM$heureS"".txt" `pwd`/Others/Others
				fi
		 
		#sed -i '1d' $fichier
		#sed -i '/^[[:space:]]*$/d' $fichier
		
			echo "End of the frame decoding :    $line" 	
		fi
               fi 
		done	
	
