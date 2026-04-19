from fastapi import WebSocket, FastAPI,WebSocketDisconnect
from collections import defaultdict
import json

app = FastAPI()
connections=[]

rooms = defaultdict(list)
user_info = {} #websocket->name, room
user_to_ws = {} #name->websocket

async def broadcasr_users(room):
    user_list = []
    for ws in rooms[room]:
        user_list.append({
            "name": user_info[ws]["name"],
            "status": "online"   # always online
        })
    payload = {
        "type":"users",
        "users":user_list
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

                await broadcasr_users(room)

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
            room = user["room"]
            name = user["name"]
            user_info[websocket]["status"]="offline"
            if websocket in rooms[room]:
                rooms[room].remove(websocket)
            if name in user_to_ws:
                del user_to_ws[name]
            del user_info[websocket]
            print(f"{user['name']} left {room}")
            
            await broadcasr_users(room)
        # connections.remove(websocket)
        # print("client disconnected")
    finally:
        await websocket.close()