from fastapi import WebSocket, FastAPI,WebSocketDisconnect
from collections import defaultdict
import json

app = FastAPI()
connections=[]

rooms = defaultdict(list)
user_info = {} #name, room
user_to_ws = {} #name->websocket

async def broadcasr_users(room):
    user_list = []
    for ws in rooms[room]:
        user_list.append(user_info[ws]['name'])
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
            print("connected to server")
            if res["type"]=="join":
                name = res["name"]
                room = res["room"]
                user_info[websocket]={"name":name,"room":room}
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
                
                # print(user)
            
    except WebSocketDisconnect:
        user = user_info.get(websocket)
        if user:
            room = user["room"]
            name = user["name"]

            if websocket in rooms[room]:
                rooms[room].remove(websocket)
            del user_info[websocket]
            print(f"{user['name']} left {room}")
            
            await broadcasr_users(room)
        # connections.remove(websocket)
        # print("client disconnected")
    finally:
        await websocket.close()