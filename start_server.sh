. env/bin/activate;
nohup sudo python3 server.py &
nohup ngrok http --region=us --hostname=zachslights.ngrok.io 5000 & 
