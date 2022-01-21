from flask import Flask, render_template
import threading
import lights
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("home.html", available_patterns=lights.available_patterns)

@app.route("/start")
def pick_pattern():
    return ":)"

@app.route("/start/<p>/", defaults={"r":50, "g":50, "b":50})
@app.route("/start/<p>/<int:r>+<int:g>+<int:b>")
def start_pattern(p, r, g, b):
    # if lights are not stopped, stop them
    if not lights.stop.is_set():
        stop_pattern()
    # check if pattern is valid
    if p not in lights.available_patterns:
        return("not today >:)")
    # Verify that the old pattern has actually stopped
    # If it has, run the new pattern in a thread
    if lights.thread is None:
        lights.thread = threading.Thread(target=lights.pattern, args=[p, r, g, b])
        lights.thread.start()
        lights.stop.clear()
        return(f"Started {escape(p)}")
    return("old pattern not stopped successfully")

@app.route("/stop")
def stop_pattern():
    lights.blank()
    try:
        lights.stop.set()
        # join the thread to wait for it to finish
        lights.thread.join()
        # now there's no more thread so update the variable to point to None
        lights.thread = None
        # turn off all the lights
        lights.blank()
        return("Stopped!")
    except Exception as e:
        # There might be an exception if there is no thread active
        print(e)
        lights.blank()
        return("Nothing to stop.")

@app.route("/brightness/<int:brightness>")
def set_brightness(brightness):
    if (brightness < 256 and brightness >=0):
        lights.max_brightness = brightness

if __name__ == "__main__":
    lights = lights.Lights(num_pixels=100, max_brightness=255)
    app.run(host="0.0.0.0", port=5000, debug=True)
