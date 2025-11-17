import time
import numpy as np
from mss import mss
from mqtt_control import send_color_rgb

FPS = 6  # how many times per second to sample screen

def main():
    with mss() as sct:
        monitor = sct.monitors[1]  # main screen

        while True:
            img = np.array(sct.grab(monitor))[:, :, :3]  # RGB
            h, w, _ = img.shape

            # optional: center crop to avoid taskbar/edges
            crop = img[h//10: h-h//10, w//10: w-w//10]

            avg = crop.mean(axis=(0, 1))
            r, g, b = map(int, avg)

            send_color_rgb(r, g, b)
            print(f"Published RGB({r}, {g}, {b})")

            time.sleep(1 / FPS)

if __name__ == "__main__":
    main()
