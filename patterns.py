import board
import neopixel
import random
import math
import threading
import time
import colorsys
import datetime

num_pixels = 100
pixels=neopixel.NeoPixel(board.D21, num_pixels, auto_write=False)

dim = .95
max_brightness = 50

h=0

available_patterns = ["random_chase", "solid_chase", "rainbow_chase", "rainbow_cycle", "fill", "rainbow_fill", "rainbow_scroll", "clock"]

def pattern(p, r, g, b):
    t = threading.current_thread()
    while(getattr(t, "do_run", True)):
        eval(p+"(r, g, b)")
    blank()

def blank():
    pixels.fill((0,0,0))
    pixels.show()

def random_chase(r, g, b):
    for j in range(num_pixels):
        pixels[j] = (random.randint(0, max_brightness), random.randint(0, max_brightness),random.randint(0, max_brightness))
        for i in range(num_pixels):
            pixels[i] = (math.floor(dim * pixels[i][0]),  math.floor(dim * pixels[i][1]), math.floor(dim * pixels[i][2]))
        pixels.show()

def solid_chase(r, g, b):
    for j in range(num_pixels):
        pixels[j] = (r, b, g)
        for i in range(num_pixels):
            pixels[i] = (math.floor(dim * pixels[i][0]),  math.floor(dim * pixels[i][1]), math.floor(dim * pixels[i][2]))
        pixels.show()

def rainbow_chase(r, g, b):
    s = 1.0
    v = max_brightness/255
    # this should probably be changed 
    global h
    rgb = colorsys.hsv_to_rgb(h, s, v)
    for j in range(num_pixels):
        pixels[j] = ((math.floor(rgb[0]*255)), (math.floor(rgb[1]*255)), (math.floor(rgb[2]*255)))
        for i in range(num_pixels):
            pixels[i] = (math.floor(dim * pixels[i][0]),  math.floor(dim * pixels[i][1]), math.floor(dim * pixels[i][2]))
            if h > 1:
                h = 0
            h += .0003
            rgb = colorsys.hsv_to_rgb(h, s, v)
        pixels.show()


def rainbow_cycle(r, g, b):
    s = 1.0
    v = max_brightness/255
    # this should probably be changed
    global h
    if h>1:
        h=0
    h += .0001
    rgb = colorsys.hsv_to_rgb(h, s, v)
    pixels.fill(((math.floor(rgb[0]*255)), (math.floor(rgb[1]*255)), (math.floor(rgb[2]*255))))
    time.sleep(.001)
    pixels.show()

def rainbow_fill(r, g, b):
    s = 1.0
    v = max_brightness/255
    i = 0
    while(i<num_pixels):
        for h in range(0, 255, 2):
            rgb = colorsys.hsv_to_rgb(h/255, s, v)
            pixels[i] = ((math.floor(rgb[0]*255)), (math.floor(rgb[1]*255)), (math.floor(rgb[2]*255)))
            i += 1
            if i >= num_pixels:
                break
    pixels.show()

def rainbow_scroll(r, g, b):
    s = 1.0
    v = max_brightness/255
    h_offset = round(time.time()*25)

    for pixel_ind in range(num_pixels):
        rgb = colorsys.hsv_to_rgb(((h_offset + pixel_ind) % 255)/255, s, v)
        pixels[pixel_ind] = ((math.floor(rgb[0]*255)), (math.floor(rgb[1]*255)), (math.floor(rgb[2]*255)))
    pixels.show()
     
def clock(r, g, b):
    leds_on = math.floor(timedelta_percentage(datetime.datetime.now()) * num_pixels)
    led_blink_index = math.ceil(timedelta_percentage(datetime.datetime.now()) * num_pixels)

    blink_status_on = round(time.time()) % 2 == 1
    
    for pixel_ind in range(leds_on):
        pixels[pixel_ind] = (r,b,g)
    if blink_status_on:
        pixels[led_blink_index-1] = (r,b,g)
    else:
        pixels[led_blink_index-1] = (0,0,0)
    pixels.show()


def fill(r, g, b):
    pixels.fill((r, b, g))
    pixels.show()

def timedelta_percentage(input_datetime):
    d = input_datetime - datetime.datetime.combine(input_datetime.date(), datetime.time())
    return d.total_seconds() / 86400.0


if __name__ == "__main__":
    random_chase(0, 0, 0)
