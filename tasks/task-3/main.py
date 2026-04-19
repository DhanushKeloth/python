from fastapi import WebSocket, FastAPI,WebSocketDisconnect
from collections import defaultdict
import json
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

app = FastAPI()
connections=[]

rooms = defaultdict(list)
user_info = {} #websocket->name, room
user_to_ws = {} #name->websocket

def get_users(room):
    users = r.smembers(f"users:{room}")
    result = []

    for name in users:
        status = r.hget(f"user:{name}", "status") or "offline"
        result.append({
            "name": name,
            "status": status
        })

    return result
async def broadcast_users(room):
    user_list = get_users(room)

    payload = {
        "type": "users",
        "users": user_list
    }

    for ws in rooms[room]:
        await ws.send_text(json.dumps(payload))
@app.websocket("/ws")
async def websocket_connection(websocket:WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text() #recieve data from the client
            res = json.loads(data);
            # print("connected to server")
            if res["type"]=="join":
                name = res["name"]
                room = res["room"]
                user_info[websocket]={"name":name,"room":room,"status":"online"}
                rooms[room].append(websocket)
                user_to_ws[name]=websocket

                r.sadd(f"users:{room}", name)
                r.hset(f"user:{name}", mapping={
                    "room": room,
                    "status": "online"
                })

                await broadcast_users(room)

                print(f"{name} joined room {room}")
                # print(rooms)
            elif res["type"]=="message":
                user = user_info[websocket]
                room = user['room']
                response = {
                    "type":"message",
                    "name":user['name'],
                    "message":res["message"]
                }
                print(f"{user['name']} sent message",res)
                for users in rooms[room]:
                    data = json.dumps(response)
                    await users.send_text(data) #here users are the client websockets connected 
            elif res["type"]=="dm":
                sender = user_info.get(websocket)
                if not sender:
                    continue

                reciever_name = res["to"]
                reciever_ws = user_to_ws.get(reciever_name)
                
                dm_payload={
                    "type":"dm",
                    "from":sender["name"],
                    "message":res["message"]
                }
                if reciever_ws:
                    await reciever_ws.send_text(json.dumps(dm_payload))
                #send to the sender also 
                await websocket.send_text(json.dumps(dm_payload))
                # print(user)
            elif res["type"]=="typing":
                user = user_info.get(websocket)
                if not user:
                    continue
                room = user["room"]
                payload = {
                    "type": "typing",
                    "name": user["name"],
                    "status": res["status"]
                }
                for conn in rooms[room]:
                    if conn != websocket:
                        await conn.send_text(json.dumps(payload))
                pass
            

    except WebSocketDisconnect:
        user = user_info.get(websocket)

        if user:
            name = user["name"]
            room = user["room"]

            # ✅ Redis updates
            r.hset(f"user:{name}", "status", "offline")
            # r.srem(f"users:{room}", name)   # ⭐ IMPORTANT FIX

            # ✅ Memory cleanup
            if websocket in rooms[room]:
                rooms[room].remove(websocket)

            if name in user_to_ws:
                del user_to_ws[name]

            del user_info[websocket]

            print(f"{name} left {room}")

            await broadcast_users(room)
            # connections.remove(websocket)
        # print("client disconnected")
    