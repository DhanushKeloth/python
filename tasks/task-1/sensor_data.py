import random 
from datetime import datetime
import asyncio
import stats as cs

statuses=["NORMAL","WARNING","CRITICAL"]
sensor_ids=['T1','T2','T3']
# sensor_base={
#     'T1':70,
#     'T2':75,
#     'T3':80
# }
def get_status():
    # return random.choice(statuses)
    # cal_stats()
    pass

def get_temperature():
    # return round(random.random()*100,2)
    return round(random.uniform(70,110),1)
def get_vibrations():
    return round(random.random(),2)

async def generate_data():
    while True:
        for sensor in sensor_ids:      
            temp = get_temperature()
            vibrations = get_vibrations()
            stat_values = cs.cal_stats(sensor,temp)
            print(stat_values)
            status= stat_values.get("status")
            time = datetime.now().strftime("%H:%M:%S")
            data={
                 "sensor_id":sensor,
                 "temp":temp,
                 "vibrations":vibrations,
                 "status":status,
                 "time":time
            }
            yield data
        await asyncio.sleep(1)
# async def main():
#     async for data in generate_data():
#         print(f"[{data['time']}] temp={data['temp']}F vibration={data['vibrations']}g status={data['status']}")
        
        
# asyncio.run(main())