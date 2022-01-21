# Light-server
This is a work-in-progress python server to run on a raspberry pi and control the connected LEDs. 

## Instructions for use:

(Optional) Use a virtual environment
```
python -m venv env
. env/bin/activate
```

Install the requirements 
```
pip install -r requirements.txt
```

Run the server 
```
nohup sudo python3 server.py &
```
Alternatively, there is a helper script `server.sh` that activates the virtual environment, runs the server, and starts an ngrok tunnel. It can also be called with stop to stop the server and ngrok.
```
bash server.sh start
```

Access the web interface on the local network at 
```
<raspberrypi hostname>:5000
```

## Other notes

Add more patterns in lights.py. Any pattern function must have an entry in the `available_patterns` whitelist, which will also generate a button for it. Each pattern is run in a new thread, and when the stop button is pressed, the server updates an event that is checked in a while loop surrounding the pattern function. Because of this, long-running pattern functions will not stop correctly, so try to keep the repeating unit short.

## Plans
- Make brightness slider work with all the patterns
- Make the server something more legit and hardened than a flask development server
- Connect some Google smart home actions to control the lights
