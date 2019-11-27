#!/bin/bash



fichier="file.txt"

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
				if [ -s $fichier ]; then 
				
				line=$(head -n 1 $fichier)
				date=$( awk 'NR==1' $fichier| awk '{print $1}' ) ;
				day=$(awk 'NR==1' $fichier | awk '{print $1}' | cut -c1-2 ) ;
				month=$(awk 'NR==1' $fichier| awk '{print $1}'  | cut -c4-5 ) ;
				an=$(awk 'NR==1' $fichier | awk '{print $1}'  | cut -c7- ) ;
				heure=$(awk 'NR==1' $fichier | awk '{print $2}') ;
				heureH=$(awk 'NR==1' $fichier | awk '{print $2}'  | cut -c1-2) ;
				heureM=$(awk 'NR==1' $fichier | awk '{print $2}' | cut -c4-5) ;
				heureS=$(awk 'NR==1' $fichier | awk '{print $2}'  | cut -c7-8) ;
				lat=$(awk 'NR==1' $fichier | awk -F ":" '{print $3}' ) ;
				idCommande=$(awk 'NR==1' $fichier | awk -F ":" '{print $2}' | cut -c3) ;
				idUser=$( awk 'NR==1' $fichier | awk -F ":" '{print $2}' | cut -c2) ;
				long=$(awk 'NR==1' $fichier |awk -F ":" '{print $2}'  | cut -c4-) ;
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
						mv  /home/drogon/"$day$month$an_$heureH$heureM$heureS"".txt" /home/drogon/TrafficJam/Pedestrian
		
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
					mv  /home/drogon/"$day$month$an_$heureH$heureM$heureS"".txt" /home/drogon/TrafficJam/Car
					
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
					mv  /home/drogon/"$day$month$an_$heureH$heureM$heureS"".txt" /home/drogon/TrafficJam/Bollard
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
					mv  /home/drogon/"$nameUser$day$month$an_$heureH$heureM$heureS"".txt" /home/drogon/TrafficJam/Others
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
					mv  /home/drogon/"$nameUser$day$month$an_$heureH$heureM$heureS"".txt" /home/drogon/TrafficJam/EmergencyVehicle
		
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
					mv  /home/drogon/"$day$month$an_$heureH$heureM$heureS"".txt" /home/drogon/Accident/Pedestrian
			elif [ $idCommande -eq 0 ] && [ $idUser -eq 2 ]
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
					mv  /home/drogon/"$day$month$an_$heureH$heureM$heureS"".txt" /home/drogon/Accident/Bollard
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
					mv  /home/drogon/"$day$month$an_$heureH$heureM$heureS"".txt" /home/drogon/Accident/Car
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
				mv  /home/drogon/"$day$month$an_$heureH$heureM$heureS"".txt" /home/drogon/Accident/Others
	
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
				mv  /home/drogon/"$day$month$an_$heureH$heureM$heureS"".txt" /home/drogon/Accident/EmergencyVehicle

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
				mv  /home/drogon/"$day$month$an_$heureH$heureM$heureS"".txt" /home/drogon/Localisation/EmergencyVehicle
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
				mv  /home/drogon/"$day$month$an_$heureH$heureM$heureS"".txt" /home/drogon/Localisation/Pedestrian

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
				mv  /home/drogon/"$day$month$an_$heureH$heureM$heureS"".txt" /home/drogon/Localisation/Car
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
				mv  /home/drogon/"$day$month$an_$heureH$heureM$heureS"".txt" /home/drogon/Localisation/Bollard
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
				mv  /home/drogon/"$day$month$an_$heureH$heureM$heureS"".txt" /home/drogon/Localisation/Others
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
				mv  /home/drogon/"$day$month$an_$heureH$heureM$heureS"".txt" /home/drogon/Others/Car
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
				mv  /home/drogon/"$day$month$an_$heureH$heureM$heureS"".txt" /home/drogon/Others/Bollard
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
				mv  /home/drogon/"$day$month$an_$heureH$heureM$heureS"".txt" /home/drogon/Others/EmergencyVehicle
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
				mv  /home/drogon/"$day$month$an_$heureH$heureM$heureS"".txt" /home/drogon/Others/Others
				fi
		 
		sed -i '1d' $fichier
		sed -i '/^[[:space:]]*$/d' $fichier
		
			echo "End of the frame decoding :    $line" 	
		fi
		done	
	

