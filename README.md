# Jasper-Module-MQTT

Jasper MQTT Module based on ArtBIT's [HAL9000 Raspberry PI Instructable](http://www.instructables.com/id/RaspberryPI-HAL9000/)

When triggered it publishes a simple MQTT event using the following topic:
```
jasper/*device*/*index* 
```
Available devices:
  * device
  * light
  * blinds
  * door
  * temperature

Available locations:
  * bed
  * bath
  * front
  * back
  * side
  * sun
  * office
  * living
  * kitchen
  *dining

Available topic messages:
  * on
  * off
  * up
  * down
  * open
  * close
  * lock
  * unlock
  * status


## Steps to install MQTT Module

* Install the python Mosquitto package:
```
sudo pip install paho-mqtt
```
* run the following commands in order:
```
git clone https://github.com/ArtBIT/jasper-module-mqtt.git
cp jasper-module-mqtt/Mqtt.py <path to jasper/client/modules>
#i.e. cp jasper-module-mqtt/Mqtt.py /usr/local/lib/jasper/client/modules/
```
* Edit `~/.jasper/profile.yml` and add the follwing at the bottom:
```
mqtt:
  hostname: 'your.mqtt.broker.hostname.or.ip'
  port: 1883
  protocol: 'MQTTv31' # Note: this should be either MQTTv31 or MQTTv311, I had problems with Ubuntu broker and MQTTv311
```
* Restart the Pi:
```
sudo reboot
```
## Congrats, JASPER MQTT Module is now installed and ready for use.
Here are some examples:
```
YOU: Bedroom light off
JASPER: *publishes an mqtt event* topic:jasper/light/bed message:off
YOU: Front door lock
JASPER: *publishes an mqtt event* topic:hal9000/door/front message:lock
```

