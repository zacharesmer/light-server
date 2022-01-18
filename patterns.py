import board
import neopixel
import random
import math
import threading
import time
import colorsys

num_pixels = 100
pixels=neopixel.NeoPixel(board.D21, num_pixels, auto_write=False)

dim = .95
max_brightness = 255

h=0

available_patterns = ["random_chase", "solid_chase", "rainbow_chase", "rainbow_cycle", "fill", "rainbow_fill"]

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
    v = 1.0
    # this could be a for loop but it has to be interruptable by the server
    global h
    rgb = colorsys.hsv_to_rgb(h/255, s, v)
    for j in range(num_pixels):
        if h > 255:
            h = 0
        h += 2
        pixels[j] = ((math.floor(rgb[0]*255)), (math.floor(rgb[1]*255)), (math.floor(rgb[2]*255)))
        for i in range(num_pixels):
            pixels[i] = (math.floor(dim * pixels[i][0]),  math.floor(dim * pixels[i][1]), math.floor(dim * pixels[i][2]))
        pixels.show()


def rainbow_cycle(r, g, b):
    s = 1.0
    v = 1.0
    # this could be a for loop but it has to be interruptable by the server
    global h
    if h>255:
        h=0
    h += 1
    rgb = colorsys.hsv_to_rgb(h/255, s, v)
    pixels.fill(((math.floor(rgb[0]*255)), (math.floor(rgb[1]*255)), (math.floor(rgb[2]*255))))
    time.sleep(.05)
    pixels.show()

def rainbow_fill(r, g, b):
    s = 1.0
    v = 1.0
    i = 0
    while(i<num_pixels):
        for h in range(0, 255, 2):
            rgb = colorsys.hsv_to_rgb(h/255, s, v)
            pixels[i] = ((math.floor(rgb[0]*255)), (math.floor(rgb[1]*255)), (math.floor(rgb[2]*255)))
            i += 1
            if i >= num_pixels:
                break
    pixels.show()


def fill(r, g, b):
    pixels.fill((r, b, g))
    pixels.show()

if __name__ == "__main__":
    random_chase(0, 0, 0)
