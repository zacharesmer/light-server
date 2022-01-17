import board
import neopixel
import random
import math
import threading

num_pixels = 100
max_brightness = 50
pixels=neopixel.NeoPixel(board.D21, num_pixels, auto_write=False)
dim = .95

def pattern(p, r, g, b):
    t = threading.current_thread()
    while(getattr(t, "do_run", True)):
        eval(p+"(r, g, b)")
    pixels.fill((0,0,0))
    pixels.show()

def random_chase(r, g, b):
    for j in range(num_pixels):
        pixels[j] = (random.randint(0, max_brightness), random.randint(0, max_brightness),random.randint(0, max_brightness))
        for i in range(num_pixels):
            pixels[i] = (math.floor(dim * pixels[i][0]),  math.floor(dim * pixels[i][1]), math.floor(dim * pixels[i][2]))
        pixels.show()

def fill(r, g, b):
    pixels.fill((r, b, g))
    pixels.show()

if __name__ == "__main__":
    random_chase()
