# -*- coding: utf-8-*-
# vim: set expandtab:ts=4:sw=4:ft=python
import re

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

PLACES = ["BED", "LIVING", "KITCHEN", "DINING",
          "OFFICE", "SUN", "BATH", "FRONT", 
          "BACK", "SIDE", "HOME"]
DEVICES = ["DEVICE", "LIGHT", "BLINDS", "DOOR", "TEMPERATURE"]
PAYLOADS = ["ON", "OFF", "OF", "OPEN", "CLOSE", "STATUS", 
            "LOCK", "UNLOCK", "UP", "DOWN"]
DESCRIPTORS = ["WESLEY"]

WORDS = ["MOSQUITTO", "ROOM"] + DEVICES + PLACES + PAYLOADS + DESCRIPTORS
PRIORITY = 4


def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text, by sending a
        mosquitto publish event
        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    words = text.split(' ')
    x = 0
    if words[0] in DESCRIPTORS:
        x += 1
    if words[0 + x] not in PLACES:
        return mic.say(words[0]+" not found in the list of locations")
    if words[1 + x] == "ROOM":
        x += 1
    if words[1 + x] not in DEVICES:
        return mic.say(words[1 + x]+" is not found in the list of valid devices")
    if words[2 + x] not in PAYLOADS:
        return mic.say(words[2 + x]+" is not found in the list of valid payloads")
    if words[0 + x] == "ROOM":
        topic = '/'.join(['jasper']+words[1 + x] + words[0 + x - 1] + words[2 + x])
        payload = words[2 + x]
    else:
        topic = '/'.join(['jasper']+words[1 + x] + words[0 + x] + words[2 + x])
        payload = words[2 + x]
    if payload == 'OF':
        payload = 'OFF'
    if 'protocol' in profile['mqtt'] and profile['mqtt']['protocol'] == 'MQTTv311':
        protocol = mqtt.MQTTv311
    else:
        protocol = mqtt.MQTTv31
    publish.single(topic.lower(), payload=payload.lower(), client_id='hal9000',
                   hostname=profile['mqtt']['hostname'], port=profile['mqtt']['port'],
                   protocol=protocol)


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.
        Arguments:
        text -- user-input, typically transcribed speech
    """

    regex = "(" + "|".join(DEVICES) + ") (" + "|".join(PLACES) + ") (" + "|".join(PAYLOADS) + ") (" + "|".join(DESCRIPTORS) + ")"
    return bool(re.search(regex, text, re.IGNORECASE))
