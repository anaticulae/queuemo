#!/usr/bin/bash

: "${WORKER:=1}"
: "${JOBS:=1}"
: "${RUNTIME:=10}"

: "${DEV_SERVER_PORT:=8080}"
: "${DEV_SERVER_URL:=0.0.0.0}"

pip list

echo "download docu007..."
export HOVERPOWER_PACKAGES=docu
powerdownload && powerdecrypt
echo "download docu007 downloaded"

echo "viewo start..."
viewo --debug --port=${DEV_SERVER_PORT} --host=${DEV_SERVER_URL} &
PID1=$!
sleep 10
echo "viewo started..."
echo "queuemo start..."
queuemo --jobs=${JOBS} --runtime=${RUNTIME} -VV &
PID2=$!
echo "queuemo started..."
echo "docu007 push..."
pusher --port=${DEV_SERVER_PORT} --host=${DEV_SERVER_URL} -vvv docu007 &
PID3=$!
echo "docu007 pushed..."

wait $PID2
STATUS2=$?

wait $PID3
STATUS3=$?

# Check results
if [ $STATUS2 -eq 0 ] && [ $STATUS3 -eq 0 ]; then
    echo "Both applications completed successfully."
else
    echo "App2 exit code: $STATUS2"
    echo "App3 exit code: $STATUS3"
    exit 1
fi
