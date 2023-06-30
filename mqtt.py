import time, ujson, network
from machine import Pin,PWM
from umqtt.robust import MQTTClient
from buzzer import *

buzzer = Buzzer(13)
klijentid = "tense"

# Uspostavljanje WiFI konekcije
nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect('Ugradbeni', 'USlaboratorija220')
#nic.connect('Bajrovic', 'Bajrovic01')

while not nic.isconnected():
    print("Čekam konekciju ...")
    time.sleep(5)

print("WLAN konekcija uspostavljena")
ipaddr=nic.ifconfig()[0]

print("Mrežne postavke:")
print(nic.ifconfig())

# Funkcija koja se izvršava na prijem MQTT poruke
def sub(topic,msg):
    global buzzer
    print('Tema: '+str(topic))
    print('Poruka: '+str(msg))
    if topic==b'ushome/alarmCommands':
        if (msg ==b'Stop beeping'):
            buzzer.stopBeeping()
        else:
            print(msg)
    else :
        print(topic)
    

def publish(string):
    mqtt_conn.publish("ushome/alarmNotifications",string)

# Uspostavljanje konekcije sa MQTT brokerom
mqtt_conn = MQTTClient(client_id=klijentid, server='broker.hivemq.com',user='',password='',port=1883)
mqtt_conn.set_callback(sub)
mqtt_conn.connect()
mqtt_conn.subscribe(b"ushome/#")

print("Konekcija sa MQTT brokerom uspostavljena")


    
