#!/usr/bin/python

import pyscreenshot as ImageGrab

from datetime import datetime
import time


def take_screenshot():
    print("take_screenshot")
    image_name = f"screenshot-{str(datetime.now())}"
    print("name: " + image_name)
    start_time = time.time()
    screenshot = ImageGrab.grab()
    print("cdjwoiejoqwi")
    end_time = time.time()
    print(end_time - start_time)

    filepath = f"./screenshots/{image_name}"

    screenshot.save(filepath)

    return filepath

take_screenshot()

