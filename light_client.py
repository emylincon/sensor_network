import RPi.GPIO as GPIO
import os
from pyfiglet import Figlet
import sys
import time
from termcolor import colored, cprint

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)


def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.15)


os.system('clear')
print('>> starting...')
delay_print("<======================================================")

os.system('clear')
custom_fig = Figlet(font='graffiti')
cprint(custom_fig.renderText('welcome to LSBU'), 'yellow')
cprint("/*****************************************************\\", 'yellow')
cprint("*                                                     *", 'yellow')
cprint("*      Enter Off Or On to Control the Led Light       *", 'red')
cprint("*                                                     *", 'yellow')
cprint("\*****************************************************/\n", 'yellow')

while True:
    try:
        text = input(">> ").lower()
        if text == 'on':
            GPIO.output(17, True)
        elif text == 'off':
            GPIO.output(17, False)
        elif (text == 'stop') or (text == 'exit'):
            break
        else:
            print("invalid input \n You Typed: ", text)
    except KeyboardInterrupt:
        print("\nProgramme Terminated\n")
        break