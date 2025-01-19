import asyncpg
from utilities.settings import setting

async def sensor_data(data):
    # Connect to PostgreSQL
    conn = await asyncpg.connect(user=setting.db_username, 
                                 password=setting.db_password, 
                                 database=setting.db_name, 
                                 host=setting.db_host, 
                                 port=setting.db_port)

    # Check if the sensor exists using a raw SQL query
    sensor_query = "SELECT * FROM sensors WHERE secret_key = $1"
    sensor = await conn.fetch(sensor_query, data.secret_key)
    
    if not sensor:
        await conn.close()  # Close the connection when done
        return {"message": "Invalid sensor key"}

    sensor_id = sensor[0]['id']  # Extract the sensor_id from the first result

    # Prepare the data to be inserted
    insert_query = """
        INSERT INTO sensors_data (sensor_id, flow_rate, energy, pressure, temperature)
        VALUES ($1, $2, $3, $4, $5)
    """

    # Insert the data into the `sensors_data` table
    try:
        await conn.execute(insert_query, sensor_id, data.flow_rate, data.energy, data.pressure, data.temperature)
        # Retrieve the id of the inserted record
        inserted_id_query = "SELECT currval(pg_get_serial_sequence('sensors_data', 'id'))"
        inserted_id = await conn.fetchval(inserted_id_query)
        
        await conn.close()  # Close the connection
        
        return {"message": "Data added successfully", "id": inserted_id, "user_id": sensor[0]["user_id"]}
    except Exception as e:
        await conn.close()  # Close the connection in case of an error
        print( {"message": f"Failed to add data: {str(e)}"})
        
async def get_all_patterns(data):
    conn = await asyncpg.connect(user=setting.db_username, 
                                 password=setting.db_password, 
                                 database=setting.db_name, 
                                 host=setting.db_host, 
                                 port=setting.db_port)

    # Check if the sensor exists using a raw SQL query
    sensor_query = "SELECT * FROM sensors WHERE secret_key = $1"
    sensor = await conn.fetch(sensor_query, data.secret_key)
    
    if not sensor:
        await conn.close()  # Close the connection when done
        return 0
    
    sensor_id = sensor[0]['id']  # Extract the sensor_id from the first result

    # Query patterns using the sensor_id
    patterns_query = "SELECT * FROM patterns WHERE sensor_id = $1"
    patterns = await conn.fetch(patterns_query, sensor_id)
    
    patterns_list = []
    for pattern in patterns:
        sensor_data_query = "SELECT * FROM sensors_data WHERE id = $1"
        sensor_data = await conn.fetch(sensor_data_query, pattern["record_id"])
        sensor_data_dict = {key: value for key, value in sensor_data[0].items()}
        sensor_data_dict["name"] = pattern["name"]
        sensor_data_dict["id"] = pattern["id"]
        patterns_list.append(sensor_data_dict)

    await conn.close()  # Close the connection when done

    return patterns_list, sensor_id

async def update_state(record_id, sensor_id, pattern_id, confident):
    conn = await asyncpg.connect(user=setting.db_username, 
                                 password=setting.db_password, 
                                 database=setting.db_name, 
                                 host=setting.db_host, 
                                 port=setting.db_port)
    
    state_query = "SELECT * FROM states WHERE sensor_id = $1"
    state = await conn.fetch(state_query, sensor_id)
    
    if not state:
        # Insert a new state if it doesn't exist
        insert_state_query = "INSERT INTO states (record_id, pattern_id, sensor_id, confident) VALUES ($1, $2, $3, $4)"
        await conn.execute(insert_state_query, record_id, pattern_id, sensor_id ,confident)
    else:
        # Update the existing state
        update_query = "UPDATE states SET record_id = $1, pattern_id = $2, confident = $3 WHERE sensor_id = $4"
        await conn.execute(update_query, record_id, pattern_id, confident, sensor_id)
    
    await conn.close()  # Close the connection when done
    return {"message": "State updated successfully"}

async def add_notification(user_id, record_id, sensor_id):
    conn = await asyncpg.connect(user=setting.db_username, 
                                 password=setting.db_password, 
                                 database=setting.db_name, 
                                 host=setting.db_host, 
                                 port=setting.db_port)
    
    insert_query = "INSERT INTO notifications (user_id, sensor_id, record_id) VALUES ($1, $2, $3)"
    await conn.execute(insert_query, user_id, record_id, sensor_id)
    
    await conn.close()  # Close the connection when done
    return {"message": "Notification added successfully"}