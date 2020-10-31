#!/bin/bash
 
# check network availability 
while true
do
  TIMEOUT=5
  SITE_TO_CHECK="172.30.17.37"
  RET_CODE=`curl -I -s --connect-timeout $TIMEOUT $SITE_TO_CHECK -w %{http_code} | tail -n1`
  if [ "x$RET_CODE" = "x200" ]; then
  echo "Network OK, will send mail..."
  break
  else
  echo "Network not ready, wait..."
  sleep 1s
  fi
done

python3 /home/pi/Desktop/main.py 2xxxxx xxxxx