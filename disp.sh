#!/bin/bash

function date_fix {
	key_input=""
	date_format="%Y-%m-%d %H:%m"
	date_format_date="%Y-%m-%d"
	current_date=$(date "+$date_format")
	for filename in $1/*.jpg; do
		echo $filename
		while :
		do
			read -rsn1 key_input
			case $key_input in
				j)
					current_date=$(date -jv -1d -f "$date_format" "$current_date" "+$date_format")
					echo $current_date
					;;
				k)
					current_date=$(date -jv +1d -f "$date_format" "$current_date" "+$date_format")
					echo $current_date
					;;
				g)
					echo done
					break
					;;
			esac
		done
				
		magick display -resize 400 $filename
	done
}

date_fix $1