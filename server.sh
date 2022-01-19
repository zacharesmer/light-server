usage="Usage: $0 <start> or $0 <stop>"
if [ "$#" -ne 1 ];
then
  echo "$usage"
fi
if [ "$1" == "start" ];
then
  . env/bin/activate;
  nohup sudo python3 server.py &
  echo "$!" > pid.txt
  nohup ngrok http --region=us --hostname=zachslights.ngrok.io 5000 & 
  echo "$!" >> pid.txt
elif [ "$1" == "stop" ];
then
  while read pid; do
    kill "$pid"
  done <pid.txt
  rm pid.txt
else
  echo "$usage";
fi
