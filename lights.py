import board
import neopixel
import random
import math
import threading
import time
import colorsys
import datetime

import pdb

class Lights:
    '''
    A class to hold patterns of lights and a NeoPixel instance. 
    Also has a threading Event to manage the lights
    '''
    def __init__(self, num_pixels, max_brightness):
        self.num_pixels = num_pixels
        self.max_brightness = max_brightness
        self.brightness_mult = max_brightness/255

        # defaults to False, waits to become True
        self.stop = threading.Event()
        # the lights should initially be stopped until someone starts a pattern
        self.stop.set()
        # this will hold the thread the lights are currently running in
        self.thread = None

        self.pixels=neopixel.NeoPixel(board.D21, num_pixels, auto_write=False, pixel_order="BGR")
        self.available_patterns = ["random_chase", "solid_chase", "rainbow_chase", "rainbow_cycle", "fill", "rainbow_fill", "rainbow_scroll", "clock"]

        # multiplier for fade out
        self.dim_amount = .95
        self.hue = 0.0

    def start_pattern(self, p, r, g, b):
        self.stop.clear()
        self.thread = threading.Thread(target=self.pattern, args=[p, r, g, b])
        self.thread.start()

    def pattern(self, p, r, g, b):
        while(not self.stop.is_set()):
            # run the pattern p
            getattr(self, p)(r, g, b)
        self.blank()

    def fill(self, r, g, b):
        self.pixels.fill((r, g, b))
        self.pixels.show()

    def blank(self):
        self.pixels.fill((0,0,0))
        self.pixels.show()

    def dim_one(self, i):
        self.pixels[i] = (math.floor(self.dim_amount * self.pixels[i][0]), math.floor(self.dim_amount * self.pixels[i][1]), math.floor(self.dim_amount * self.pixels[i][2]))

    def dim_all(self):
        for i in range(self.num_pixels):
            self.dim_one(i)

    def random_chase(self, r, g, b):
        for j in range(self.num_pixels):
            self.pixels[j] = (random.randint(0, self.max_brightness), random.randint(0, self.max_brightness),random.randint(0, self.max_brightness))
            self.dim_all()
            self.pixels.show()

    def solid_chase(self, r, g, b):
        for j in range(self.num_pixels):
            self.pixels[j] = (r, g, b)
            self.dim_all()
            self.pixels.show()

    def rainbow_chase(self, r, g, b):
        sat = 1.0
        val = self.brightness_mult
        rgb = colorsys.hsv_to_rgb(self.hue, sat, val)
        for j in range(self.num_pixels):
            self.pixels[j] = ((math.floor(rgb[0]*255)), (math.floor(rgb[1]*255)), (math.floor(rgb[2]*255)))
            for i in range(self.num_pixels):
                self.dim_one(i)
                if self.hue > 1:
                    self.hue = 0
                self.hue += .0003
                rgb = colorsys.hsv_to_rgb(self.hue, sat, val)
            self.pixels.show()

    def rainbow_cycle(self, r, g, b):
        sat = 1.0
        val = self.brightness_mult
        if self.hue > 1:
            self.hue =0
        self.hue += .0001
        rgb = colorsys.hsv_to_rgb(self.hue, sat, val)
        self.pixels.fill(((math.floor(rgb[0]*255)), (math.floor(rgb[1]*255)), (math.floor(rgb[2]*255))))
        time.sleep(.001)
        self.pixels.show()

    def rainbow_fill(self, r, g, b):
        sat = 1.0
        val = self.brightness_mult
        i = 0
        while(i<self.num_pixels):
            for h in range(0, 255, 2):
                rgb = colorsys.hsv_to_rgb(h/255, sat, val)
                self.pixels[i] = ((math.floor(rgb[0]*255)), (math.floor(rgb[1]*255)), (math.floor(rgb[2]*255)))
                i += 1
                if i >= self.num_pixels:
                    break
        self.pixels.show()

    def rainbow_scroll(self, r, g, b):
        sat = 1.0
        val = self.brightness_mult
        h_offset = round(time.time()*25)

        for pixel_ind in range(self.num_pixels):
            rgb = colorsys.hsv_to_rgb(((h_offset + pixel_ind) % 255)/255, sat, val)
            self.pixels[pixel_ind] = ((math.floor(rgb[0]*255)), (math.floor(rgb[1]*255)), (math.floor(rgb[2]*255)))
        self.pixels.show()
         
    def clock(self, r, g, b):
        leds_on = math.floor(self.timedelta_percentage(datetime.datetime.now()) * self.num_pixels)
        led_blink_index = math.ceil(self.timedelta_percentage(datetime.datetime.now()) * self.num_pixels)

        blink_status_on = round(time.time()) % 2 == 1
        
        for pixel_ind in range(leds_on):
            self.pixels[pixel_ind] = (r,g,b)
        if blink_status_on:
            self.pixels[led_blink_index-1] = (r,g,b)
        else:
            self.pixels[led_blink_index-1] = (0,0,0)
        self.pixels.show()

    def timedelta_percentage(self, input_datetime):
        d = input_datetime - datetime.datetime.combine(input_datetime.date(), datetime.time())
        return d.total_seconds() / 86400.0


if __name__ == "__main__":
    patterns = Lights(100, 255)
