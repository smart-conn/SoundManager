import subprocess, time, os, json, uuid
from processCtrl import *
from sox import *
import paho.mqtt.client as mqtt

TOPIC_PREFIX = "sound_manager"

def onMessage(client, userdata, msg):
  # print(msg.topic + " " + str(msg.payload))
  try:
    get_msg = json.loads(msg.payload)
    print get_msg
    id = get_msg.get("soundId")
    file = get_msg.get("file")
  except:
    id = str(uuid.uuid4())
  if(msg.topic == TOPIC_PREFIX + "/break"):
    play.immePlay(file, id)
  elif(msg.topic == TOPIC_PREFIX + "/play"):
    play.push(file, id)
  elif(msg.topic == TOPIC_PREFIX + "/pause"):
    play.pause()
  elif(msg.topic == TOPIC_PREFIX + "/resume"):
    play.resume()
  elif(msg.topic == TOPIC_PREFIX + "/stop_all"):
    play.stopAndClear()
  elif(msg.topic == TOPIC_PREFIX + "/stop_all_break"):
    play.immePlayAndClear(file, id)
  else:
    print "ERROR: Nothing is matched."

def onConnect(client, userdata, flags, rc):
  print("MQTT Connected with result code " + str(rc))
  play.clearPlayList()
  play.clearCurr()
  processCtrl.kill()

client = mqtt.Client()
client.on_message = onMessage
client.on_connect = onConnect
client.connect("localhost",  port = 1883)
client.subscribe(TOPIC_PREFIX + "/play")
client.subscribe(TOPIC_PREFIX + "/break")
client.subscribe(TOPIC_PREFIX + "/pause")
client.subscribe(TOPIC_PREFIX + "/resume")
client.subscribe(TOPIC_PREFIX + "/stop_all")
client.subscribe(TOPIC_PREFIX + "/stop_all_break")
client.loop_forever()
