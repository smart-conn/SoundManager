import paho.mqtt.publish as publish

publish.single("sound_manager/resume", "payload", hostname = "127.0.0.1", port = 1883)