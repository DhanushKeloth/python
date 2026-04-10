from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

clients = []

@app.get("/")
def get():
    with open("index.html") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            # broadcast message to all clients
            for client in clients:
                
                await client.send_text(data)

    except WebSocketDisconnect:
        clients.remove(websocket)