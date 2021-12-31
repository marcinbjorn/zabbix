#!/bin/bash
output="{\"data\":["
var=0
for file in /root/gpstracker/zabbix/*; do
  if [ $var != 0 ]
  then
    output+=","
  fi
  output+="{\"{#V_NAME}\":\"$(basename -- $file)\"}"
  var=1
  done
output+="]}"
echo "$output"
