#!/bin/bash
output="{\"data\":["
var=0
for file in /var/efw/uplinks/*; do
        if [ $var != 0 ]
        then
        output+=","
        fi
        file2=$file/settings
        name=$(awk '/^NAME/{print substr($0,6)}' $file2)
        interface=$(awk '/^RED_DEV/{print substr($0,9)}' $file2)
        output+="{\"{#INT_NAME}\":\"$name\",\"{#INTERFACE}\":\"$interface\"}"
        var=+1
done
output+="]}"
echo "$output"
