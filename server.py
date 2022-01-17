from flask import Flask
import threading
import lights
from markupsafe import escape

app = Flask(__name__)

run_lights = None

@app.route("/")
def hello_world():
    return("<p>Hello, world!</p>")

@app.route("/start")
def pick_pattern():
    # TODO generate a list of available patterns with links to start them
    return

@app.route("/start/<p>")
def start_pattern(p):
    # there's probably an enormous security problem here
    pattern = getattr(lights, p)
    global run_lights 
    # stop the current pattern
    if run_lights is not None:
        stop_pattern()
    run_lights = threading.Thread(target=pattern)
    run_lights.start()
    return(f"<p>Started {escape(p)}</p>")

@app.route("/stop")
def stop_pattern():
    try:
        global run_lights
        run_lights.do_run = False
        run_lights.join()
        run_lights = None
        return("Stopped!")
    except Exception as e:
        print(e)
        return("Nothing to stop.")
