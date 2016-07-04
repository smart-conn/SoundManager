import paho.mqtt.publish as publish

publish.single("sound_manager/stop_all", "payload", hostname = "127.0.0.1", port = 1883)