import RPi.GPIO as GPIO
import time
from buzzerMusic import BuzzerMusic as Music



ledPin1 = [26,19,13,6]
ledPin2 = [18,23,24,25]

buzzerPin = 12
btn1 = 21
btn2 = 20

Music = Music(buzzerPin)

btn1_status = False
btn2_status = False

game_status = False

LI_btn1 = 0
LI_btn2 = 0

i = -1
j = -1

def setup():
    global leds1
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    #set all LedPin's mode to output,and initial level to HIGH(3.3V)
    GPIO.setup(ledPin1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ledPin2,GPIO.OUT,initial=GPIO.LOW)

    GPIO.setup(buzzerPin, GPIO.OUT, initial=GPIO.HIGH)

    GPIO.setup(btn1,GPIO.IN,pull_up_down = GPIO.PUD_UP)
    GPIO.setup(btn2,GPIO.IN,pull_up_down = GPIO.PUD_UP)
    
    
    for x in range(4):
        ledPin1[x] = GPIO.PWM(ledPin1[x],100)
        ledPin2[x] = GPIO.PWM(ledPin2[x],100)
        ledPin1[x].start(100)
        ledPin2[x].start(100)

    GPIO.add_event_detect(btn1,GPIO.FALLING, callback = btn1Push)
    GPIO.add_event_detect(btn2,GPIO.FALLING, callback = btn2Push)


def btn1Push(ev=None):
    global game_status
    if game_status:
        incrementLight(btn1)

def btn2Push(ev=None):
    global game_status
    if game_status:
        incrementLight(btn2)

def winner(winner):
    global game_status
    game_status = False
    print("The winner is " + winner)
    Music.starWars(buzzerPin)
    
def incrementLight(btn):
    global LI_btn1
    global LI_btn2
    global i
    global j
    if btn == btn1:
        if LI_btn1 != 0:
            LI_btn1 = LI_btn1 - 10
        else:
            LI_btn1 = 100
        if LI_btn1 == 100:
            i = i+1
        if i < 4:
            ledPin1[i].ChangeDutyCycle(LI_btn1)
        else:
            winner("Player 1")
    elif btn == btn2:
        if LI_btn2 != 0:
            LI_btn2 = LI_btn2 - 10
        else:
            LI_btn2 = 100
        if LI_btn2 == 100:
            j = j+1
        if j < 4:
            ledPin2[j].ChangeDutyCycle(LI_btn2)
        else:
            winner("Player 2")
    else:
        print("Error: Not button")

def trafficLight():
    global game_status
    for j in range(4):
        ledPin1[j].ChangeDutyCycle(0)
        ledPin2[j].ChangeDutyCycle(0)
        #GPIO.output(buzzerPin, GPIO.LOW)
        time.sleep(0.3)
        GPIO.output(buzzerPin,GPIO.HIGH)
        time.sleep(0.5)
    for j in range(4):
        ledPin1[j].ChangeDutyCycle(100)
        ledPin2[j].ChangeDutyCycle(100)
    #GPIO.output(buzzerPin,GPIO.LOW)
    time.sleep(1)
    GPIO.output(buzzerPin,GPIO.HIGH)
    game_status = True

def destroy():
    # Release resource
    GPIO.output(buzzerPin, GPIO.HIGH)
    for i in range(4):
        ledPin1[i].ChangeDutyCycle(100)
        ledPin2[i].ChangeDutyCycle(100)
    GPIO.cleanup()
    pass

setup()
try:
    trafficLight()
except KeyboardInterrupt:
    destroy()
