import numpy as np
from mqtt.db_connection import add_notification

def cosine_similarity(vec1, vec2):
  vec1 = np.array(vec1)*5
  vec2 = np.array(vec2)*5

  dot_product = np.dot(vec1, vec2)
  norm_vec1 = np.linalg.norm(vec1)
  norm_vec2 = np.linalg.norm(vec2)

  cosine_similarity = dot_product / (norm_vec1 * norm_vec2)

  return cosine_similarity

"""{'secret_key': '81c9a8d6-a8ac-40b8-9af5-5286cd8d161f', 'flow_rate': 10.0, 'energy': 5.0, 'pressure': 9.0, 'temperature': 3.0}
{'id': 1, 'sensor_id': 1, 'flow_rate': 4.0, 'energy': 4.0, 'pressure': 4.0, 'temperature': 4.0, 'created_at': datetime.datetime(2025, 1, 18, 17, 58, 6, 688643)}
{'id': 3, 'sensor_id': 1, 'flow_rate': 4.0, 'energy': 4.0, 'pressure': 4.0, 'temperature': 4.0, 'created_at': datetime.datetime(2025, 1, 18, 20, 49, 24, 832511)}
{'id': 2, 'sensor_id': 2, 'flow_rate': 4.0, 'energy': 4.0, 'pressure': 4.0, 'temperature': 4.0, 'created_at': datetime.datetime(2025, 1, 18, 17, 58, 35, 211917)}"""

async def pattern_matching(data, patterns, user_id, record_id, sensor_id):
    if not patterns:
        await add_notification(user_id, record_id, sensor_id)
        return
    similarities = {}
    data = data.model_dump()
    data = [
        data["flow_rate"],
        data["energy"],
        data["pressure"],
        data["temperature"]
    ]
    
    for pattern in patterns:
        pattern_data = [
            pattern["flow_rate"],
            pattern["energy"],
            pattern["pressure"],
            pattern["temperature"]
        ]
        similarity = cosine_similarity(data, pattern_data)
        similarities[(pattern["name"],pattern["id"])] = float(similarity)
        
    
    matched = max(similarities.items(), key=lambda item: item[1])
    
    
    if matched[1] < 0.85:
        await add_notification(user_id, sensor_id, record_id)
        return
    
    return matched