#!/bin/bash

function date_fix {
	key_input=""
	last_disp_job=""
	date_format="%Y:%m:%d %H:%m"
	current_date=$(date "+$date_format")
	echo "$current_date"
	for filename in "$1/"*.jpg; do
		echo $filename
		magick display -resize 600 "$filename" &
		last_disp_job=$!
		while :
		do
			read -rsn1 key_input
			case $key_input in
				j)
					current_date=$(date -jv +1d -f "$date_format" "$current_date" "+$date_format")
					echo $current_date
					;;
				k)
					current_date=$(date -jv -1d -f "$date_format" "$current_date" "+$date_format")
					echo $current_date
					;;
				i)
					current_date=$(date -jv -1M -f "$date_format" "$current_date" "+$date_format")
					echo $current_date
					;;
				o)
					current_date=$(date -jv +1M -f "$date_format" "$current_date" "+$date_format")
					echo $current_date
					;;
				g)
					exiftool -AllDates="$current_date" "$filename"
					kill $last_disp_job
					break
					;;
			esac
		done
	done
	rm -rf "$1/"*_original
}

date_fix "$1"