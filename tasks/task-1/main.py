from fastapi import FastAPI,WebSocket,WebSocketDisconnect
import sensor_data as sd
import stats as cs
import asyncio
app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        async for data in sd.generate_data():
            temperature = data['temp']
            sensor_id = data['sensor_id']
            # print(sensor_id)
            result = cs.cal_stats(sensor_id,temperature)
            if result:
                data.update(result)
            await websocket.send_json(data)
            # print(result)
    except WebSocketDisconnect:
        print("client disconnected")
    finally:    
        await websocket.close()
    
