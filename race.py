import RPi.GPIO as GPIO
import time
from buzzerMusic import BuzzerMusic as Music
from ledScreen import LedScreen

ledScreen = LedScreen()

ledPinArray1 = [26, 19, 13, 6]
ledPinArray2 = [18, 23, 24, 25]
global ledPin1
global ledPin2

buzzerPin = 12
btn1 = 21
btn2 = 20

Music = Music(buzzerPin)

btn1_status = False
btn2_status = False

game_status = False

player1 = ""
player2 = ""

def setup():
    global ledPin1
    global ledPin2

    GPIO.setwarnings(False)

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(ledPinArray1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ledPinArray2, GPIO.OUT, initial=GPIO.LOW)

    GPIO.setup(buzzerPin, GPIO.OUT, initial=GPIO.HIGH)

    GPIO.setup(btn1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    ledPin1 = [GPIO.PWM(ledPinArray1[x], 100)for x in range(4)]
    ledPin2 = [GPIO.PWM(ledPinArray2[x], 100)for x in range(4)]

    for x in range(4):
        ledPin1[x].start(100)
        ledPin2[x].start(100)

    GPIO.add_event_detect(btn1, GPIO.FALLING, callback=btn1Push)
    GPIO.add_event_detect(btn2, GPIO.FALLING, callback=btn2Push)

def startMessage():
    global player1
    global player2
    ledScreen.lcd_string("Insert a name", ledScreen.LCD_LINE_1)
    ledScreen.lcd_string("for player 1", ledScreen.LCD_LINE_2)
    player1 = input("Player1= ")
    ledScreen.lcd_string("Player 1 is ", ledScreen.LCD_LINE_1)
    ledScreen.lcd_string(player1, ledScreen.LCD_LINE_2)

    ledScreen.lcd_string("Insert a name", ledScreen.LCD_LINE_1)
    ledScreen.lcd_string("for player 2", ledScreen.LCD_LINE_2)
    player2 = input("Player2= ")
    ledScreen.lcd_string("Player 2 is ", ledScreen.LCD_LINE_1)
    ledScreen.lcd_string(player2, ledScreen.LCD_LINE_2)

    ledScreen.lcd_string("Ready to play...", ledScreen.LCD_LINE_1)
    ledScreen.lcd_string("", ledScreen.LCD_LINE_2)


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
    global player1score
    global player2score

    game_status = False
    ledScreen.lcd_string("The winner is...", ledScreen.LCD_LINE_1)
    ledScreen.lcd_string("..." + winner, ledScreen.LCD_LINE_2)
    Music.starWars(buzzerPin)
    ledScreen.lcd_string("***Score***:", ledScreen.LCD_LINE_1)
    ledScreen.lcd_string("...", ledScreen.LCD_LINE_2)
    time.sleep(2)
    ledScreen.lcd_string(player1 + ":  " + str(player1score), ledScreen.LCD_LINE_1)
    ledScreen.lcd_string(player2 + ":  " + str(player2score), ledScreen.LCD_LINE_2)
    for i in range(4):
        ledPin1[i].ChangeDutyCycle(100)
        ledPin2[i].ChangeDutyCycle(100)
    menu()


def incrementLight(btn):
    global LI_btn1
    global LI_btn2
    global ledOn1
    global ledOn2
    global player1
    global player2
    global player1score
    global player2score

    if btn == btn1:
        if LI_btn1 != 0:
            LI_btn1 = LI_btn1 - 10
        else:
            LI_btn1 = 100
            
        if LI_btn1 == 100:
            ledOn1 = ledOn1+1
        if ledOn1 < 4:
            ledPin1[ledOn1].ChangeDutyCycle(LI_btn1)
        else:
            player1score = player1score+1
            winner(player1)
    elif btn == btn2:
        if LI_btn2 != 0:
            LI_btn2 = LI_btn2 - 10
        else:
            LI_btn2 = 100
        if LI_btn2 == 100:
            ledOn2 = ledOn2+1
        if ledOn2 < 4:
            ledPin2[ledOn2].ChangeDutyCycle(LI_btn2)
        else:
            player2score = player2score+1
            winner(player2)
    else:
        print("Error: Not button")

def trafficLight():
    global game_status
    for j in range(4):
        ledPin1[j].ChangeDutyCycle(0)
        ledPin2[j].ChangeDutyCycle(0)
        GPIO.output(buzzerPin, GPIO.LOW)
        time.sleep(0.3)
        GPIO.output(buzzerPin, GPIO.HIGH)
        time.sleep(0.5)
    for j in range(4):
        ledPin1[j].ChangeDutyCycle(100)
        ledPin2[j].ChangeDutyCycle(100)
    GPIO.output(buzzerPin, GPIO.LOW)
    time.sleep(1)
    GPIO.output(buzzerPin, GPIO.HIGH)
    game_status = True

def menu():
    global LI_btn1
    global LI_btn2
    global ledOn1
    global ledOn2
    global player1score
    global player2score
    LI_btn1 = 0
    LI_btn2 = 0
    ledOn1 = -1
    ledOn2 = -1
    try:
        choice = int(input("Choose an option:\n 1)Play new game\n 2)Repeat game\n 3)Exit game\n"))
        if choice == 1:
            player1score = 0
            player2score = 0
            startMessage()
            trafficLight()
        elif choice == 2:
            GPIO.output(buzzerPin, GPIO.HIGH)
            for i in range(4):
                ledPin1[i].ChangeDutyCycle(100)
                ledPin2[i].ChangeDutyCycle(100)
            print("Get ready to play again")
            ledScreen.lcd_string("You chose to...", ledScreen.LCD_LINE_1)
            ledScreen.lcd_string("...play again", ledScreen.LCD_LINE_2)
            trafficLight()
        elif choice == 3:
            print("Thank you for playing our game")
            ledScreen.lcd_string("Game over", ledScreen.LCD_LINE_1)
            ledScreen.lcd_string("Bye bye", ledScreen.LCD_LINE_2)
            time.sleep(10)
        else:
            print("Enter only 1 or 2 or 3")
            menu()
    except ValueError:
        print("Enter only numbers")
        menu()

def destroy():
    # Release resource
    GPIO.output(buzzerPin, GPIO.HIGH)
    for i in range(4):
        ledPin1[i].ChangeDutyCycle(100)
        ledPin2[i].ChangeDutyCycle(100)
    GPIO.cleanup()
    pass

try:
    ledScreen.lcd_init()
    setup()
    menu()
except KeyboardInterrupt:
    destroy()
finally:
    ledScreen.lcd_byte(0x01, ledScreen.LCD_CMD)