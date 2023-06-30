from machine import Pin,PWM
from time import sleep

pirSensor = Pin(26, Pin.IN)
buzzer = PWM(Pin(18, Pin.OUT))
buzzer.freq(500)

# Buzzer starts beeping
def startBeeping() -> None:
    global buzzer
    buzzer.duty_u16(6400)

# Buzzer stops beeping
def stopBeeping() -> None:
    global buzzer
    buzzer.duty_u16(00)
    
while True:
    startBeeping()
    sleep(1)
    print("ja")