import paho.mqtt.publish as publish
import os, json

publish.single("sound_manager/play", json.dumps({"soundId":"222","file":os.path.abspath("test.mp3")}), hostname = "127.0.0.1", port = 1883)