from machine import PWM, Pin
import time

class Buzzer:
    
    # Values
    LOW = 0
    MID = 32000
    HIGH = 64000
    
    # Constructor
    def __init__(self, pin_number: int):
        self.instance = PWM(Pin(pin_number, Pin.OUT))
        self.setFrequency(400)
        self.setDuty(self.LOW)
        
    # Setting duty cycle
    # ! Might modify this
    def setDuty(self, duty_cycle: int) -> None:
        self.instance.duty_u16(duty_cycle)
        
    # Setting frequency 
    def setFrequency(self, frequency: int) -> None:
        self.instance.freq(frequency)
    
    def stopBeeping(self) -> None:
        self.setDuty(self.LOW)
    
    def startBeeping(self) -> None:
        self.setDuty(self.MID)
        
    def startScreaming(self) -> None:
        self.setDuty(self.HIGH)

    
