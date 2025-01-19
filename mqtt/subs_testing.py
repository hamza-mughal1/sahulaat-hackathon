# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import json
import aiomqtt
from schemas.pydantic_schemas.sensor_pydantic_schema import IncomingData
from mqtt.db_connection import sensor_data, get_all_patterns, update_state
from mqtt.pattern_recognition import pattern_matching

async def process_message(message):
        # Process the received message (e.g., store in database)
        # print(f"Processing message: {message.payload.decode()}")
        
        data = json.loads(message.payload.decode())
        try:
            IncomingData(**data)
        except:
            print("Invalid data")
            return
        
        output = await sensor_data(IncomingData(**data))
        if output["message"] == "Data added successfully":
            patterns, sensor_id = await get_all_patterns(IncomingData(**data))
            pattern_data = await pattern_matching(IncomingData(**data), patterns, output["user_id"], output["id"], sensor_id)
            if pattern_data:
                await update_state(output["id"], sensor_id, pattern_data[0][1], pattern_data[1])
        

async def main():
    # Create an MQTT client
    async with aiomqtt.Client(hostname="test.mosquitto.org", port=1883) as client:
        # Connect to the MQTT broker
        await client.subscribe("test.mosquitto.org") 

        # Subscribe to a topic
        await client.subscribe("hamza/topic")

        # Receive and process messages asynchronously
        async for message in client.messages:
            await process_message(message)

async def run_mqtt_consumer():
    while True:
        await asyncio.sleep(1)
        try:
            await main()
        except Exception as e:
            print(f"Error occurred: {e}")
            raise e

if __name__ == "__main__":
    asyncio.run(run_mqtt_consumer())