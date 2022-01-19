from flask import Flask, render_template
import threading
import patterns
from markupsafe import escape

app = Flask(__name__)

run_lights = None

@app.route("/")
def hello_world():
    return(render_template("home.html", available_patterns=patterns.available_patterns))

@app.route("/start")
def pick_pattern():
    return ":)"

@app.route("/start/<p>/", defaults={"r":50, "g":50, "b":50})
@app.route("/start/<p>/<int:r>+<int:g>+<int:b>")
def start_pattern(p, r, g, b):
    global run_lights 
    # stop the current pattern if it exists
    # TODO: the old pattern is not always stopping before the new pattern
    if run_lights is not None:
        stop_pattern()
    # check if pattern is valid
    if p not in patterns.available_patterns:
        return("not today >:)")
    # Verify that the old pattern has actually stopped
    # If it has, run the new pattern in a thread
    if run_lights is None:
        run_lights = threading.Thread(target=patterns.pattern, args=[p, r, g, b])
        run_lights.start()
        return(f"Started {escape(p)}")
    return("something bad has happened")

@app.route("/stop")
def stop_pattern():
    patterns.blank()
    try:
        global run_lights
        run_lights.do_run = False
        run_lights.join()
        run_lights = None
        patterns.blank()
        return("Stopped!")
    except Exception as e:
        print(e)
        patterns.blank()
        return("Nothing to stop.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
