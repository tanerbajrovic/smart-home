# General Imports
from time import sleep, time
from machine import SPI
from micropython import const
from alarm import AlarmState
from buzzer import Buzzer
from colors import WHITE, BLUE, RED, GREEN
from mqtt import *

# Display-related imports
from ili934xnew import ILI9341
from keypad import *
import tt24, tt32

# Device Info
deviceName = "Smart Home"
deviceVersion = "1.0"
adminContact = "user@etf.unsa.ba"

# Inputs/Outputs
alarmState = AlarmState(locked = False)
pirSensor = Pin(28, Pin.IN)
buzzer = Buzzer(13)

# Tracks whether movement detection has been sent 
signalSent = False

# Handler method for IRQ interrupt of PIR sensor.
def motionDetected(t):
    global signalSent
    # print("-> Movement Detected")
    if alarmState.isLocked():  # Intruder alert
        # print("Currently locked")
        buzzer.startBeeping()
        if not signalSent:
            publish("Motion detected")
            signalSent = True        
    else:
        # print("Currently unlocked")
        buzzer.stopBeeping()


pirSensor.irq(motionDetected, Pin.IRQ_RISING)

# Display setup
SCR_WIDTH = const(320)
SCR_HEIGHT = const(240)
SCR_ROT = const(2)
CENTER_Y = int(SCR_WIDTH / 2)
CENTER_X = int(SCR_HEIGHT / 2)
LEFT_MARGIN = 10
TOP_MARGIN = 20

# SPI comms with display
TFT_CLK_PIN = const(18)
TFT_MOSI_PIN = const(19)
TFT_MISO_PIN = const(16)
TFT_CS_PIN = const(17)
TFT_RST_PIN = const(20)
TFT_DC_PIN = const(15)

spi = SPI(
    0,
    baudrate=62500000,
    miso=Pin(TFT_MISO_PIN),
    mosi=Pin(TFT_MOSI_PIN),
    sck=Pin(TFT_CLK_PIN))

display = ILI9341(
    spi,
    cs=Pin(TFT_CS_PIN),
    dc=Pin(TFT_DC_PIN),
    rst=Pin(TFT_RST_PIN),
    w=SCR_WIDTH,
    h=SCR_HEIGHT,
    r=SCR_ROT)

display.erase()
display.set_pos(0, 0)
display.set_font(tt32)
display.set_color(BLUE, WHITE)

fonts = ["tt24", "tt32"]
activeFont = fonts[1]

def displayMessageSlowly(message: str, duration = 0.1) -> None:
    totalLength = 0
    if activeFont == fonts[0]:
        totalLength = tt24.get_width(message)
    else:
        totalLength = tt32.get_width(message)
    startPosition = (SCR_HEIGHT - totalLength) // 2
    display.set_pos(startPosition, display._y)
    for character in message:
        display.write(character)
        sleep(duration)


# ? Refactor this.
def showStartupMessage() -> None:
    display.erase()
    display.set_pos(LEFT_MARGIN, TOP_MARGIN)
    displayMessageSlowly(deviceName)
    display.set_pos(LEFT_MARGIN, TOP_MARGIN + 40)
    displayMessageSlowly(f"V{deviceVersion}")
    display.set_pos(LEFT_MARGIN, TOP_MARGIN + 80)
    displayMessageSlowly("Welcome!")
    sleep(1)


# Waiting screen view
def showWaitScreen() -> None:
    # Setup
    display.erase()
    display.set_font(tt32)
    display.set_pos(LEFT_MARGIN, TOP_MARGIN + 40)
    displayMessageSlowly("Loading...")
    sleep(1)


# Unlocked screen view
def showUnlockedScreen() -> None:
    display.erase()
    display.set_pos(LEFT_MARGIN, TOP_MARGIN)
    display.set_font(tt32)
    display.set_color(GREEN, WHITE)
    displayMessageSlowly("DEACTIVATED")
    display.set_color(BLUE, WHITE)
    display.set_pos(LEFT_MARGIN, TOP_MARGIN + 40)
    display.set_font(tt24)
    if not alarmState.hasCode():
        display.print("Press '*' to add your code")
    else:
        display.print("Press '#' to activate the alarm")


# Locked screen view
def showLockedScreen() -> None:
    display.erase()
    display.set_pos(LEFT_MARGIN, TOP_MARGIN)
    display.set_font(tt32)
    display.set_color(RED, WHITE)
    displayMessageSlowly("ACTIVATED")
    display.set_color(BLUE, WHITE)
    display.set_font(tt24)
    display.set_pos(LEFT_MARGIN, TOP_MARGIN + 40)
    display.print("Enter your code to  deactivate your alarm")


# Bricked screen view
def showBrickedScreen() -> None:
    display.erase()
    display.set_pos(LEFT_MARGIN, TOP_MARGIN)
    display.set_font(tt24)
    display.set_color(RED, WHITE)
    display.print("Your alarm has been bricked")
    display.set_pos(LEFT_MARGIN, TOP_MARGIN + 80)
    display.print(f"Contact your admin for a reset password at {adminContact}")
    while True:
        buzzer.startScreaming()
        sleep(0.5)
        buzzer.startBeeping()
        sleep(0.5)


# Remaining code attempts
attemptsLeft = 3

def beginCountdown(duration: int) -> None:
    display.erase()
    display.set_pos(LEFT_MARGIN, TOP_MARGIN)
    display.set_font(tt32)
    displayMessageSlowly("STAND BY")
    display.set_font(tt24)
    display.set_pos(LEFT_MARGIN, TOP_MARGIN + 40)
    display.print("Activating in:")
    remainingTime = duration
    while remainingTime:
        display.set_pos(LEFT_MARGIN, TOP_MARGIN + 80)
        display.print(f"{remainingTime}s")
        remainingTime -= 1
        sleep(1)


# Logic for code verification and alarm deactivation
def inputSecretCode() -> str:
    global pin_digits, attemptsLeft
    # display.erase()
    display.set_font(tt32)
    display.set_pos(LEFT_MARGIN, display._y + 40)
    pin_digits = []
    while len(pin_digits) < 4:
        mqtt_conn.check_msg()
        key = Keypad4x4Read(col_list, row_list)
        if key != None:
            if key.isdigit():
                display.write("*")
                pin_digits.append(int(key))
    stringCode = ""
    for digit in pin_digits:
        stringCode = stringCode + str(digit)
    display.set_font(tt24)
    return stringCode             
    

# Logic for adding a new code
def setNewCode() -> None:
    display.erase()
    display.set_pos(LEFT_MARGIN, TOP_MARGIN)
    display.print("Enter your new code")
    newCode = inputSecretCode()
    
    display.erase()
    display.set_pos(LEFT_MARGIN, TOP_MARGIN)
    display.print("Confirm your new code")
    confirmCode = inputSecretCode()
    
    if newCode == confirmCode:
        alarmState.setCode(newCode)
        display.erase()
        display.set_pos(LEFT_MARGIN, TOP_MARGIN)
        display.print("Code changed successfully!")
        sleep(1.25)
        showUnlockedScreen()
    else:
        display.erase()
        display.set_pos(LEFT_MARGIN, TOP_MARGIN)
        display.print("Codes DO NOT match!")
        display.set_pos(LEFT_MARGIN, TOP_MARGIN + 80)
        displayMessageSlowly("Alarm not active")
        sleep(1)
        showUnlockedScreen()


# Alarm logic when locked (turned on).
def alarmLockedLogic() -> None:
    global attemptsLeft, signalSent
    print("--- Locked Logic ---")
    secretCode = inputSecretCode()
    unlockedSuccessfully = alarmState.unlock(secretCode)
    
    if unlockedSuccessfully:
        buzzer.stopBeeping()
        signalSent = False
        showUnlockedScreen()
        attemptsLeft = 3
    else:
        publish("Incorrect password entered")
        attemptsLeft -= 1
        if attemptsLeft == 0:
            showBrickedScreen()
        display.erase()
        display.set_pos(LEFT_MARGIN, TOP_MARGIN + 40)
        display.print(f"Incorrect password. You have {attemptsLeft} attempt(s) left.")


# Alarm logic when unlocked (turned off).
def alarmUnlockedLogic() -> None:
    # print("--- Unlocked Logic ---")
    key = Keypad4x4Read(col_list, row_list)
    if key == "#":
        beginCountdown(10)
        alarmState.lock()
        showLockedScreen()
    elif key == "*":
        setNewCode()
        

showStartupMessage()
showWaitScreen()
showUnlockedScreen()


while True:
    if alarmState.isLocked():
        alarmLockedLogic()
    else:
        alarmUnlockedLogic()
    sleep(0.05)
    mqtt_conn.check_msg()
