#!/bin/bash

localfolder=./downloads/complete
folderid=0B6VJgbksxQNSdHdfQXlRYWZqU00

cd $localfolder
for i in ./*
do
    if [ "$i" != "./*" ]
    then
        flock -n "$i" -c "drive upload -f \"$i\" -p $folderid && rm -rf \"$i\"" &
    fi
done
