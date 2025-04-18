import paho.mqtt.client as mqtt
import json
import random
import time

# Create a client instance
client = mqtt.Client()

# Connect to the broker
client.connect("test.mosquitto.org", 1883, 60)

for i in range(100000):
    pattern1 = json.dumps({
        "secret_key": "b22b4615-a250-4b20-a275-a3159ea3c0fc", 
        "flow_rate": round(random.uniform(130.0, 150.0), 5),
        "energy": round(random.uniform(400.0, 500.0), 5),
        "temperature": round(random.uniform(-150.0, -100.0), 5),
        "pressure": round(random.uniform(900.0, 1000.0), 5)
        })

    pattern2 = json.dumps({
        "secret_key": "b22b4615-a250-4b20-a275-a3159ea3c0fc", 
        "flow_rate": round(random.uniform(0.0, 3.0), 5),
        "energy": round(random.uniform(0.0, 20.0), 5),
        "temperature": round(random.uniform(0.0, 30.0), 5),
        "pressure": round(random.uniform(20.0, 50.0), 5)
    })

    pattern3 = json.dumps({
        "secret_key": "b22b4615-a250-4b20-a275-a3159ea3c0fc", 
        "flow_rate": round(random.uniform(-130.0, -150.0), 5),
        "energy": round(random.uniform(-400.0, -500.0), 5),
        "temperature": round(random.uniform(150.0, 100.0), 5),
        "pressure": round(random.uniform(-900.0, -1000.0), 5)
        })

# Publish a message to the topic

    if i % 2 == 0:
        client.publish("hamza/topic", pattern1)
    else:
        # client.publish("hamza/topic", pattern2)
        pass
        
    time.sleep(1)
    # client.publish("hamza/topic", pattern3)
    print("data sent")
    # print("itr",i, "message", message)

client.disconnect()
