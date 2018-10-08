"""
body.py
Raspberry Pi Cue System for RHS Stage & Light Crew
This code is for a "Body" Control Station
NOTE: THIS CODE HAS NOT YET BEEN TESTED, USE AT YOUR OWN RISK!

Created by Brett Bender (JustADev) 2018
"""

from gpiozero import LED, Button
from time import sleep
from subprocess import check_call
import paho.mqtt.client as mqtt

## GPIO Setup
# LEDs
backCurtainLed = LED(17)
midCurtainLed = LED(18)
mainCurtainLed = LED(27)
leftStageLed = LED(22)
rightStageLed = LED(23)

# Buttons
backCurtainBut = Button(5)
midCurtainBut = Button(26)
mainCurtainBut = Button(6)
leftStageBut = Button(13)
rightStageBut = Button(19)
## End GPIO Setup

## Status Variables
# Back Curtain
backCurtainOnline = False
backCurtainGo = False
backCurtainAsking = False
backCurtainReady = False
# Mid Curtain
midCurtainOnline = False
midCurtainGo = False
midCurtainAsking = False
midCurtainReady = False
# Main Curtain
mainCurtainOnline = False
mainCurtainGo = False
mainCurtainAsking = False
mainCurtainReady = False
# Left Stage
leftStageOnline = False
leftStageGo = False
leftStageAsking = False
leftStageReady = False
# Right Stage
rightStageOnline = False
rightStageGo = False
rightStageAsking = False
rightStageReady = False
## End Status Variables

## Ident Variables
backCurtainIdent = "BC"
midCurtainIdent = "CC"
mainCurtainIdent = "MC"
leftStageIdent = "LS"
rightStageIdent = "RS"
## End Ident Variables

## MQTT Setup
legTopic = "QSys/Legs"
bodyTopic = "QSys/Body"
serverIP = "localhost" # Change to IP of MQTT Broker
thisIP = "10.0.0.39" # Change to IP of the spider

## Start MQTT Setup

mqtt_client = mqtt.Client(serverIP, 1883, 60)
# The callback for when the client receives a CONNACK response from the server.
def mqtt_on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(bodyTopic)

def sendMsg(legIdent, msg):
	mqtt_client.publish(legTopic, legIdent+"/"+thisIP+"/"+msg)


# The callback for when a PUBLISH message is received from the server.
# Define pretty much all events in here
def mqtt_on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    pyld = msg.payload.split("/")
    ident = pyld[0]
    action = pyld[2]
    # Back Curtain Actions
    if ident == backCurtainIdent:
        if action == "ONLINE":
            backCurtainOnline = True
        elif action == "READY" and backCurtainAsking:
            sendMsg(backCurtainIdent, "CONFIRMED")
            backCurtainReady = True
            backCurtainLed.on
        elif action == "SHUTDOWN":
            backCurtainOnline = False
            backCurtainGo = False
            backCurtainReady = False
            backCurtainLed.off
    # Mid Curtain Actio s
    elif ident == midCurtainIdent:
        if action == "ONLINE":
            midCurtainOnline = True
        elif action == "READY" and midCurtainAsking:
            sendMsg(midCurtainIdent, "CONFIRMED")
            midCurtainReady = True
            midCurtainLed.on
        elif action == "SHUTDOWN":
            midCurtainOnline = False
            midCurtainGo = False
            midCurtainReady = False
            midCurtainLed.off
    # Main Curtain Actions
    elif ident == mainCurtainIdent:
        if action == "ONLINE":
            mainCurtainOnline = True
        elif action == "READY" and mainCurtainAsking:
            sendMsg(mainCurtainIdent, "CONFIRMED")
            mainCurtainReady = True
            mainCurtainLed.on
        elif action == "SHUTDOWN":
            mainCurtainOnline = False
            mainCurtainGo = False
            mainCurtainReady = False
            mainCurtainLed.off
    # Right Stage Actions
    elif ident == rightStageIdent:
        if action == "ONLINE":
            rightStageOnline = True
        elif action == "READY" and rightStageAsking:
            sendMsg(rightStageIdent, "CONFIRMED")
            rightStageReady = True
            rightStageLed.on
        elif action == "SHUTDOWN":
            rightStageOnline = False
            rightStageGo = False
            rightStageReady = False
            rightStageLed.off
    # Left Stage Actions
    elif ident == leftStageIdent:
        if action == "ONLINE":
            leftStageOnline = True
        elif action == "READY" and leftStageAsking:
            sendMsg(leftStageIdent, "CONFIRMED")
            leftStageReady = True
            leftStageLed.on
        elif action == "SHUTDOWN":
            leftStageOnline = False
            leftStageGo = False
            leftStageReady = False
            leftStageLed.off


mqtt_client.on_connect = mqtt_on_connect
mqtt_client.on_message = mqtt_on_message

mqtt_client.connect()

## End MQTT Setup

## Button Logic Start
def backCurtain_buttonPress():
    if backCurtainReady or backCurtainAsking:
        sendMsg(backCurtainIdent, "GO")
        backCurtainLed.on
        backCurtainReady = False
        backCurtainGo = True
        backCurtainAsking = False
    elif backCurtainGo:
        sendMsg(backCurtainIdent, "NONE")
        backCurtainLed.off
        backCurtainReady = False
        backCurtainGo = False
        backCurtainAsking = False
    else:
        sendMsg(backCurtainIdent, "ASKING")
        backCurtainAsking = True
        backCurtainLed.blink(0.5,0.5)

def midCurtain_buttonPress():
    if midCurtainReady or midCurtainAsking:
        sendMsg(midCurtainIdent, "GO")
        midCurtainLed.on
        midCurtainReady = False
        midCurtainGo = True
        midCurtainAsking = False
    elif midCurtainGo:
        sendMsg(midCurtainIdent, "NONE")
        midCurtainLed.off
        midCurtainReady = False
        midCurtainGo = False
        midCurtainAsking = False
    else:
        sendMsg(midCurtainIdent, "ASKING")
        midCurtainAsking = True
        midCurtainLed.blink(0.5,0.5)
    
def mainCurtain_buttonPress():
    if mainCurtainReady or mainCurtainAsking:
        sendMsg(mainCurtainIdent, "GO")
        mainCurtainLed.on
        mainCurtainReady = False
        mainCurtainGo = True
        mainCurtainAsking = False
    elif mainCurtainGo:
        sendMsg(mainCurtainIdent, "NONE")
        mainCurtainLed.off
        mainCurtainReady = False
        mainCurtainGo = False
        mainCurtainAsking = False
    else:
        sendMsg(mainCurtainIdent, "ASKING")
        mainCurtainAsking = True
        mainCurtainLed.blink(0.5,0.5)

def leftStage_buttonPress():
    if leftStageReady or leftStageAsking:
        sendMsg(leftStageIdent, "GO")
        leftStageLed.on
        leftStageReady = False
        leftStageGo = True
        leftStageAsking = False
    elif leftStageGo:
        sendMsg(leftStageIdent, "NONE")
        leftStageLed.off
        leftStageReady = False
        leftStageGo = False
        leftStageAsking = False
    else:
        sendMsg(leftStageIdent, "ASKING")
        leftStageAsking = True
        leftStageLed.blink(0.5,0.5)

def rightStage_buttonPress():
    if rightStageReady or rightStageAsking:
        sendMsg(rightStageIdent, "GO")
        rightStageLed.on
        rightStageReady = False
        rightStageGo = True
        rightStageAsking = False
    elif rightStageGo:
        sendMsg(rightStageIdent, "NONE")
        rightStageLed.off
        rightStageReady = False
        rightStageGo = False
        rightStageAsking = False
    else:
        sendMsg(rightStageIdent, "ASKING")
        rightStageAsking = True
        rightStageLed.blink(0.5,0.5)


mainCurtainBut.when_pressed = mainCurtain_buttonPress()
midCurtainBut.when_pressed = midCurtain_buttonPress()
backCurtainBut.when_pressed = backCurtain_buttonPress()
leftStageBut.when_pressed = leftStage_buttonPress()
rightStageBut.when_pressed = rightStage_buttonPress()

print("Body Online")
mqtt_client.loop_forever