import json 

async def publish_data(websocket, payload):
  response= json.dumps(payload)
  await websocket.send(response)
  print("response sent:", response)
