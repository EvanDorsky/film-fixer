#!/usr/bin/python
import sys, os
import tty, termios
import subprocess
from multiprocessing import Process
import arrow

date_format="YYYY:MM:DD HH:mm:ss"

def display_process(img_path):
    return subprocess.Popen(["magick", "display", "-resize", "600", img_path])

def date_image_process(img_path, dt):
    return subprocess.Popen(["exiftool", "-AllDates="+dt.format(date_format), img_path])

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def reverse_order(path):
    for _, dirname, filenames in os.walk(path):
        filenames = [f for f in filenames if ".jpg" in f]
        i = len(filenames)
        j = 0
        for filename in sorted(filenames):
            new_filename = "01-00000%02d.jpg" % (i-j)
            os.rename(os.path.join(path, filename), os.path.join(path, new_filename))

            j+=1

def date_fix(path):
    key_input = ""

    current_time = arrow.now()

    for _, dirname, filenames in os.walk(path):
        filenames = [f for f in filenames if ".jpg" in f]
        for filename in sorted(filenames):
            img_path = os.path.join(path, filename)

            print img_path

            disp_worker = display_process(img_path)

            while True:
                current_time = current_time.replace(minutes=+1) # increment by a minute each time
                print current_time.format(date_format)
                key_input = getch()

                if key_input == "j":
                    current_time = current_time.replace(days=+1)
                elif key_input == "k":
                    current_time = current_time.replace(days=-1)

                elif key_input == "i":
                    current_time = current_time.replace(hours=+1)
                elif key_input == "o":
                    current_time = current_time.replace(hours=-1)

                elif key_input == "n":
                    current_time = current_time.replace(minutes=+1)
                elif key_input == "m":
                    current_time = current_time.replace(minutes=-1)

                elif key_input == "g":
                    print "Stamping %s with date: %s" % (img_path, current_time.format(date_format))
                    date_image_process(img_path, current_time)
                    disp_worker.terminate()
                    break

    subprocess.Popen(["rm", "-rf", os.path.join(path, "*_original")])

if __name__ == '__main__':
    path = sys.argv[1]
    date_fix(path)
    # reverse_order(path)