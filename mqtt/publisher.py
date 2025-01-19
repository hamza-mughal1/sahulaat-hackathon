import paho.mqtt.client as mqtt
import json
import random
import time

# Create a client instance
client = mqtt.Client()

# Connect to the broker
client.connect("test.mosquitto.org", 1883, 60)

for i in range(10):
    pattern1 = json.dumps({
        "secret_key": "bf11341e-7b6f-463e-bca2-72e43ef5cdcb", 
        "flow_rate": round(random.uniform(130.0, 150.0), 5),
        "energy": round(random.uniform(400.0, 500.0), 5),
        "temperature": round(random.uniform(-150.0, -100.0), 5),
        "pressure": round(random.uniform(900.0, 1000.0), 5)
        })

    pattern2 = json.dumps({
        "secret_key": "bf11341e-7b6f-463e-bca2-72e43ef5cdcb", 
        "flow_rate": round(random.uniform(0.0, 3.0), 5),
        "energy": round(random.uniform(0.0, 20.0), 5),
        "temperature": round(random.uniform(0.0, 30.0), 5),
        "pressure": round(random.uniform(20.0, 50.0), 5)
    })

    pattern3 = json.dumps({
        "secret_key": "81c9a8d6-a4ac-40b8-9af5-5286cd8d161f", 
        "flow_rate": round(random.uniform(-130.0, -150.0), 5),
        "energy": round(random.uniform(-400.0, -500.0), 5),
        "temperature": round(random.uniform(150.0, 100.0), 5),
        "pressure": round(random.uniform(-900.0, -1000.0), 5)
        })

# Publish a message to the topic

    if i % 2 == 0:
        client.publish("hamza/topic", pattern1)
    else:
        client.publish("hamza/topic", pattern2)
        
    time.sleep(1)
    # client.publish("hamza/topic", pattern3)
    print("data sent")
    # print("itr",i, "message", message)

client.disconnect()
