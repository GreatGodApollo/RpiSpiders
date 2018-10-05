"""
leg.py
Raspberry Pi Cue System for RHS Stage & Light Crew
This code is for a "Leg" outstation
NOTE: THIS CODE HAS NOT YET BEEN TESTED, USE AT YOUR OWN RISK!

Created by Brett Bender (JustADev) 2018
"""

from gpiozero import LED, Button
from time import sleep
from subprocess import check_call
import paho.mqtt.client as mqtt


## Start Leg Setup
legnum = 1 # For future plans
legident = "MC" # Two Letter Identity for the leg
isready = False
isasking = False
isgo = False
## End Leg Setup

## Start MQTT Pre-Setup
legTopic = "QSys/Legs"
bodyTopic = "QSys/Body"
serverIP = "10.0.0.39" # Change to IP of MQTT Broker
thisIP = "10.0.0.40" # Change to IP of the spider
## End MQTT Pre-Setup

## Start GPIO Setup
# LEDs
greenLed = LED(17)
yellowLed = LED(27)
redLed = LED(22)

# Buttons
readyButton = Button(10)
shutDownButton = Button(10, 4)
## End GPIO Setup

## Start MQTT Setup
# The callback for when the client receives a CONNACK response from the server.
def mqtt_on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(legTopic)

# The callback for when a PUBLISH message is received from the server.
# Define pretty much all events in here
def mqtt_on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    pyld = msg.payload.split("/")
    action = pyld[1]
    if pyld[0] == legident:
    	if action == "GO":
    		greenLed.on
    		isgo = True
    	elif action == "NONE":
    		greenLed.off
    		yellowLed.off
    		redLed.off
    		isgo = False
    		isasking = False
    		isready = False
    	elif action == "ASKING":
    		yellowLed.blink(0.5,0.5)
    		isasking = True
    	elif action == "CONFIRMED":
    		yellowLed.on
    		isasking = False
    		isready = True

mqtt_client = mqtt.Client(serverIP, 1883, 60)
mqtt_client.on_connect = mqtt_on_connect
mqtt_client.on_message = mqtt_on_message

mqtt_client.connect()

mqtt_client.publish(bodyTopic, legident+"/"+thisIP+"/BOOTING")

def sendMsg(msg):
	mqtt_client.publish(bodyTopic, legident+"/"+thisIP+"/"+msg)
## End MQTT Setup

## Extra GPIO Setup
def button_press():
	if isasking:
		sendMsg("READY")
	else:
		redLed.blink(0.5,0.5,1)

def shutdown_button_hold():
	if isgo or isasking or isready:
		redLed.blink(0.5,0.5,1)
	else:
		sendMsg("SHUTDOWN")
		check_call(['sudo', 'poweroff'])


readyButton.when_pressed = button_press
shutDownButton.when_held = shutdown_button_hold

## Setup Complete
# Start Notification (3 blinks of all 3 LEDs)
i = 0
while i < 3:
	greenLed.on
	yellowLed.on
	redLed.on
	sleep(1)
	greenLed.off
	yellowLed.off
	redLed.off
	sleep
	i+=1
	
sendMsg("ONLINE")
print("Leg Ready")
mqtt_client.loop_forever
