from flask import Flask, render_template
import threading
import lights
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("home.html", available_patterns=light_driver.available_patterns)

@app.route("/start")
def pick_pattern():
    return ":)"

@app.route("/start/<p>/", defaults={"r":50, "g":50, "b":50})
@app.route("/start/<p>/<int:r>+<int:g>+<int:b>")
def start_pattern(p, r, g, b):
    # if lights are not stopped, stop them
    if not light_driver.stop.is_set():
        stop_pattern()
    # check if pattern is valid
    if p not in light_driver.available_patterns:
        return("not today >:)")
    # Verify that the old pattern has actually stopped
    # If it has, run the new pattern in a thread
    if light_driver.thread is None:
        light_driver.start_pattern(p, g, r, b)
        return(f"Started {escape(p)}")
    return("old pattern not stopped successfully")

@app.route("/stop")
def stop_pattern():
    light_driver.blank()
    try:
        light_driver.stop.set()
        # join the thread to wait for it to finish
        light_driver.thread.join()
        # now there's no more thread so update the variable to point to None
        light_driver.thread = None
        # turn off all the lights
        light_driver.blank()
        return("Stopped!")
    except Exception as e:
        # There might be an exception if there is no thread active
        print(e)
        light_driver.blank()
        return("Nothing to stop.")

@app.route("/brightness/<int:brightness>")
def set_brightness(brightness):
    if (brightness < 256 and brightness >=0):
        light_driver.max_brightness = brightness
        light_driver.brightness_mult = brightness/255
    return "Brightness adjusted"

if __name__ == "__main__":
    light_driver = lights.Lights(num_pixels=100, max_brightness=255)
    app.run(host="0.0.0.0", port=5000, debug=True)
