import board
import neopixel
import random
import math
import threading

num_pixels = 100
max_brightness = 50
pixels=neopixel.NeoPixel(board.D21, num_pixels, auto_write=False)
dim = .95

def random_chase():
    t = threading.current_thread()
    while(getattr(t, "do_run", True)):
        for j in range(num_pixels):
            pixels[j] = (random.randint(0, max_brightness), random.randint(0, max_brightness),random.randint(0, max_brightness))
            for i in range(num_pixels):
                pixels[i] = (math.floor(dim * pixels[i][0]),  math.floor(dim * pixels[i][1]), math.floor(dim * pixels[i][2]))
            pixels.show()
    pixels.fill((0,0,0))



if __name__ == "__main__":
    random_chase()
