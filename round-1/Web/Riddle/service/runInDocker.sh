if [ $# -eq 0 ]
  then
    IP="127.0.0.1" 
else
    IP=$1
fi

docker build -t riddle .
docker run -d --user nobody -i -p $IP:5069:5069 -w /home riddle sh ./run.sh 
