import RPi.GPIO as GPIO
import time
from buzzerMusic import BuzzerMusic as Music
import smbus


ledPin1 = [26,19,13,6]
ledPin2 = [18,23,24,25]

buzzerPin = 12
btn1 = 21
btn2 = 20

Music = Music(buzzerPin)

exitGame=False
btn1_status = False
btn2_status = False

game_status = False

LI_btn1 = 0
LI_btn2 = 0

i = -1
j = -1

player1=""
player2=""

#LCD
# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address, if any error, change this address to 0x27
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)
  #end of LCD setup

def lcd_string(message,line):
  # Send string to display
  message = message.ljust(LCD_WIDTH," ")
  lcd_byte(line, LCD_CMD)
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def startMessage():
    global player1
    global player2
    lcd_string("Insert a name",LCD_LINE_1)
    lcd_string("for player 1",LCD_LINE_2)
    player1=input("Player1= ")
    lcd_string("Player 1 is ",LCD_LINE_1)
    lcd_string(player1,LCD_LINE_2)

    lcd_string("Insert a name",LCD_LINE_1)
    lcd_string("for player 2",LCD_LINE_2)
    player2=input("Player2= ")
    lcd_string("Player 2 is ",LCD_LINE_1)
    lcd_string(player2,LCD_LINE_2)
    lcd_string("",LCD_LINE_1)
    lcd_string("",LCD_LINE_2)

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
    global exitGame
    game_status = False
    lcd_string("The winner is...",LCD_LINE_1)
    lcd_string("..." + winner,LCD_LINE_2)
    Music.starWars(buzzerPin)
    lcd_string("Play again?",LCD_LINE_1)
    lcd_string("Y/N",LCD_LINE_2)
    try:
        continue=input("Enter Y to play again, or N to exit the game")
    except:
        continue=input("Enter only Y or N")
    
    if continue =="Y" or "y":
        exitGame=False
    elseif continue =="N" or "n":
        exitGame=True
        lcd_string("Game over",LCD_LINE_1)
        lcd_string("Bye bye",LCD_LINE_2)
        print("Thank you for playing our game")
    
    
    
def incrementLight(btn):
    global LI_btn1
    global LI_btn2
    global i
    global j
    global player1
    global player2
    global winner

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
            winner(player1)
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
        GPIO.output(buzzerPin,GPIO.HIGH)
        time.sleep(0.5)
    for j in range(4):
        ledPin1[j].ChangeDutyCycle(100)
        ledPin2[j].ChangeDutyCycle(100)
    GPIO.output(buzzerPin,GPIO.LOW)
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


lcd_init()
setup()
try:
    while not exitGame:
        startMessage()
        trafficLight()
except KeyboardInterrupt:
    destroy()
finally:
    lcd_byte(0x01, LCD_CMD)



