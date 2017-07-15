PIDFILE=/home/pi/ViviFutbolPI/ScriptLocks/camera.pid

if [ -f $PIDFILE ]
then
  PID=$(cat $PIDFILE)
  ps -p $PID > /dev/null 2>&1
  if [ $? -eq 0 ]
  then
    python /home/pi/ViviFutbolPI/ScriptExecutors/executorError.py "openCamera.sh exits because process is already running"
    exit 1
  else
    # Process not found, assume not running
    echo $$ > $PIDFILE
    if [ $? -ne 0 ]
    then
        python /home/pi/ViviFutbolPI/ScriptExecutors/executorError.py "openCamera.sh exits because it couldnt create PID file case 1"
      exit 1
    fi
  fi
else
  echo $$ > $PIDFILE
  if [ $? -ne 0 ]
  then
    python /home/pi/ViviFutbolPI/ScriptExecutors/executorError.py "openCamera.sh exits because it couldnt create PID file case 2"
    exit 1
  fi
fi

python /home/pi/ViviFutbolPI/ScriptExecutors/executorError.py "openCamera.sh executed correctly"
sleep 5m
rm $PIDFILE