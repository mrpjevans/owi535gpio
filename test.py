from time import sleep

from gpiozero import Motor

grip = Motor(27, 17, enable=22)
grip.stop()
wrist = Motor(15, 18, enable=14)
wrist.stop()
elbow = Motor(3, 4, enable=2)
elbow.stop()
shoulder = Motor(20, 21, enable=16)
shoulder.stop()
base = Motor(19, 13, enable=26)
base.stop()

selected = base
speed = 6

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
        case "1":
            selected.stop()
            selected = base
            print("Base motor selected")
        case "2":
            selected.stop()
            selected = grip
            print("Grip motor selected")
        case "3":
            selected.stop()
            selected = wrist
            print("Wrist motor selected")
        case "4":
            selected.stop()
            selected = elbow
            print("Elbow motor selected")
        case "5":
            selected.stop()
            selected = shoulder
            print("Shoulder motor selected")
        case "w":
            if speed < 10:
                speed += 2
            print("Speed is ", speed)
        case "s":
            if speed > 0:
                speed -= 2
            print("Speed is ", speed)
        case "a":
            selected.backward(speed / 10)
            print("Backwards")
        case "d":
            selected.forward(speed / 10)
            print("Forwards")
        case "f":
            selected.stop()
            print("Stop")
            
