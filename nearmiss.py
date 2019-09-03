# This file derived from the openmv example file for video recording
# and is repurposed to connect to and record ultrasonic distance sensor readings
# 
# Note: You will need an SD card to run this demo.
#
# Once you've finished recording a Mjpeg file you can use VLC to play it. 
# If you are on Ubuntu then
# the built-in video player will work too.
#
# Hardware used
# OpenMV H7
# US-100 (Y401) ultrasonic distance sensor
#
# Physical wiring
# Put the US-100 in serial mode by enabling the jumper
# H7 VIN -----> US-100 VCC (pin 1)
# H7 GND -----> US-100 GND (pin 4)
# H7 P4  -----> US-100 Trig/Tx (pin 2)
# H7 P5  -----> US-100 Echo/Rx (pin 3)
#
# Proof of concept code - not optimised
import sensor, image, time, mjpeg, pyb
from pyb import UART
uart = UART(3, 9600, timeout_char=1000)
uart.init(9600, bits=8, parity=None, stop=1, timeout_char=1000)
pyb.delay(500);

RED_LED_PIN = 1
BLUE_LED_PIN = 3

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QVGA) # or sensor.QQVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
clock = time.clock() # Tracks FPS.

pyb.LED(RED_LED_PIN).on()
sensor.skip_frames(time = 2000) # Give the user time to get ready.

pyb.LED(RED_LED_PIN).off()
pyb.LED(BLUE_LED_PIN).on()

m = mjpeg.Mjpeg("yourvideo.mjpeg")

units = "cm"
intdistance = 0
lastclosepass = 200
currentpass = 200


print("You're on camera!")


def get_distance():
    command = b"\x55"
    ch = uart.write(command)
    ch = uart.read(2)
    #print(ch)
    MSByteDist = ch[0]
    LSByteDist = ch[1]
    mmDist  = round((MSByteDist * 256 + LSByteDist)/10)
    #print(round(mmDist/10))
    return mmDist



#while(True):
for i in range(240):


    oor = False
    distance = get_distance()
    strdistance = str(distance)
    clock.tick()

    img = sensor.snapshot()

    img.draw_rectangle(0, 0, 60, 40, color = (0, 0, 0), thickness = 0, fill = True)


    if oor == False:
        # Character and string rotation can be done at 0, 90, 180, 270, and etc. degrees.
        img.draw_string(1, 1, strdistance, color = (255, 255, 255), scale = 2, mono_space = False,
                        char_rotation = 0, char_hmirror = False, char_vflip = False,
                        string_rotation = 0, string_hmirror = False, string_vflip = False)

        img.draw_string(37, 1, units, color = (255, 255, 255), scale = 2, mono_space = False,
                    char_rotation = 0, char_hmirror = False, char_vflip = False,
                    string_rotation = 0, string_hmirror = False, string_vflip = False)


    m.add_frame(img)
    #print(clock.fps())


m.close(clock.fps())
pyb.LED(BLUE_LED_PIN).off()
print("Done! Reset the camera to see the saved recording.")

