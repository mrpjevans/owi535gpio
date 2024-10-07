from time import sleep

import keyboard
from gpiozero import Motor

grip = Motor(27, 17, enable=22)
wrist = Motor(15, 18, enable=14)
elbow = Motor(3, 4, enable=2)
shoulder = Motor(20, 21, enable=16)
base = Motor(19, 13, enable=26)

def tick():
    pass


def getchar():
   #Returns a single character from standard input
   import tty, termios, sys
   fd = sys.stdin.fileno()
   old_settings = termios.tcgetattr(fd)
   try:
      tty.setcbreak(sys.stdin.fileno())
      ch = sys.stdin.read(1)
   finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
   return ch

while True:
    ch = getchar()

    match(ch):
        case "a":
            print("A")

    if ch.strip() == '':
        print('bye!')
        break

    sleep(0.1)
