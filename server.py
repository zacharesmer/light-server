from flask import Flask
import threading
import patterns
from markupsafe import escape

app = Flask(__name__)

run_lights = None

@app.route("/")
def hello_world():
    return("<p>Hello, world!</p>")

@app.route("/start")
def pick_pattern():
    # TODO generate a list of available patterns with links to start them
    return "Under construction"

@app.route("/start/<p>/", defaults={"r":0, "g":0, "b":0})
@app.route("/start/<p>/<int:r>+<int:g>+<int:b>")
def start_pattern(p, r, g, b):
    global run_lights 
    # stop the current pattern if it exists
    if run_lights is not None:
        stop_pattern()
    # run the pattern in a thread
    run_lights = threading.Thread(target=patterns.pattern, args=[p, r, g, b])
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
