#!/bin/bash

TARGET_FOLDER="cmaj-csv-measures"

cd $TARGET_FOLDER

for filename in *;
do
	echo "$filename"
	FILE_STRING=${filename##c*e}
	echo "$FILE_STRING"
	csvmidi "$filename" "./new-midis/cmajmidi-m$FILE_STRING.mid"
done
