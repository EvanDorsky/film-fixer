#!/bin/bash

function date_fix {
	key_input=""
	for filename in $1/*.jpg; do
		echo $filename
		date
		while :
		do
			read -rsn1 key_input
			case $key_input in
				j)
					echo date goes down
					;;
				k)
					echo date goes up
					;;
				p)
					echo done
					break
					;;
			esac
		done
				
		magick display -resize 400 $filename
	done
}

date_fix $1