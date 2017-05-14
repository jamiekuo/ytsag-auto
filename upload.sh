#!/bin/bash

localfolder=./downloads/complete
folderid=0B6VJgbksxQNSaW9aTTNVNnczTkk

cd $localfolder
for i in ./*
do
    if [ "$i" != "./*" ]
    then
        flock -n "$i" -c "drive upload -f \"$i\" -p $folderid && rm -rf \"$i\"" &
    fi
done
