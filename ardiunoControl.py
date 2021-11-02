from pyfirmata import Arduino, SERVO
import time
import math
port = '/dev/cu.usbmodem1301'
# pin = 10
board = Arduino(port)
board.digital[13].mode = SERVO

def rotateServo(pin, angle):
    print(angle)
    board.digital[pin].write(((256*(angle-45))/360))
    time.sleep(0.015)


# rotateServo(13, 180)
# # rotateServo(12, 180)
print("start")
time.sleep(2)
rotateServo(13, 45)
# # rotateServo(12, 240)
time.sleep(2)
rotateServo(13, 90)
# # rotateServo(12, 120)
time.sleep(2)
rotateServo(13, 135)
time.sleep(2)
rotateServo(13, 180)
time.sleep(2)
rotateServo(13, 270)
# # rotateServo(12, 180)
# i= 0
# while True:
#     time.sleep(1.5)
#     rotateServo(13, 90)
#     # rotateServo(12,240)
#     time.sleep(1.5)
#     rotateServo(13, 180)
#     # rotateServo(12, 180)
#     time.sleep(1.5)
#     rotateServo(13, 270)
#     # rotateServo(12, 120)
#     time.sleep(1.5)
#     rotateServo(13, 180)
#     # rotateServo(12, 180)
#     print(i)
#     i+=1
