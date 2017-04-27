#!/bin/bash

localfold=/home/jamie/ytsag/downloads/complete
folderid=0B6VJgbksxQNSNHRJSmRtS0ZWMXM

cd $localfold
for i in ./*
do
    if [ "$i" != "*" ]
    then
        flock -n "$i" -c "drive upload -f \"$i\" -p $folderid && rm -rf \"$i\"" &
    fi
done

