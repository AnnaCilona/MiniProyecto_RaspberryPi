import RPi.GPIO as GPIO
import time

ledPin1 = [26,19,13,6]
ledPin2 = [18,23,24,25]

buzzerPin = 12
btn1 = 21
btn2 = 20

btn1_status = False
btn2_status = False

game_status = False

def setup():
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    #set all LedPin's mode to output,and initial level to HIGH(3.3V)
    GPIO.setup(ledPin1,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(ledPin2,GPIO.OUT,initial=GPIO.HIGH)

    GPIO.setup(buzzerPin, GPIO.OUT, initial=GPIO.HIGH)

    GPIO.setup(btn1,GPIO.IN,pull_up_down = GPIO.PUD_UP)
    GPIO.setup(btn2,GPIO.IN,pull_up_down = GPIO.PUD_UP)

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

def incrementLight(btn):
    if btn == btn1:
        print("BTN1")
    elif btn == btn2:
        print("BTN2")
    else:
        print("Error: Not button")

def trafficLight():
    global game_status
    for i in range(4):
        GPIO.output(ledPin1[i],GPIO.LOW)
        GPIO.output(ledPin2[i],GPIO.LOW)
        GPIO.output(buzzerPin, GPIO.LOW)
        time.sleep(0.3)
        GPIO.output(buzzerPin,GPIO.HIGH)
        time.sleep(0.5)
    for i in range(4):
        GPIO.output(ledPin1[i],GPIO.HIGH)
        GPIO.output(ledPin2[i],GPIO.HIGH)
    GPIO.output(buzzerPin,GPIO.LOW)
    time.sleep(1)
    GPIO.output(buzzerPin,GPIO.HIGH)
    game_status = True

def destroy():
    # Release resource
    GPIO.output(buzzerPin, GPIO.HIGH)
    GPIO.output(ledPin1,GPIO.HIGH)
    GPIO.output(ledPin2,GPIO.HIGH)
    GPIO.cleanup()
    pass

setup()
try:
    trafficLight()
except KeyboardInterrupt:
    destroy()