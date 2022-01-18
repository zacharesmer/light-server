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
sudo python3 server.py
```

Access the web interface on the local network at 
```
<raspberrypi hostname>:5000
```

## Other notes

Add more patterns or change the number of LEDs in patterns.py. Any pattern function must have an entry in the `available_patterns` whitelist, which will also generate a button for it. Each pattern is run in a new thread, and when the stop button is pressed, the server updates a flag that is checked in a while loop surrounding the pattern function. Because of this, long-running pattern functions will not stop correctly, so try to keep the repeating unit short.

## Plans
- Make the server something more legit and hardened than a flask development server
- Redesign things so patterns aren't using global variables
- Connect some Google smart home actions to control the lights
