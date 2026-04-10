import asyncio
def sensormock():

    print("reading 1")
    yield 1
    print("reading 2")
    yield 2
    print("reading 3")
    yield 3

gen = sensormock()
# print("hii")
# print(next(gen))
# print(next(gen))
# print("hello")
# print(next(gen))
async def sensordata():
    print("reading 1")
    yield 1
    await asyncio.sleep(3)
    print("reading 2")
    yield 2
    print("reading 3")
    yield 3



async def main():
    async for i in sensordata():
        print(i)
        
# asyncio.run(main())

async def sensor(name,delay):
    print("starting reading")
    for i in range(1,3):
        await asyncio.sleep(delay)
        yield f"{name} reading {i}"
async def consume_sensor(gen):
    async for i in gen:
        print(i)
async def run_sensors():
    gen1 = sensor("sensor1",3)
    gen2 = sensor("sensor2",1)
    await asyncio.gather(
        consume_sensor(gen1),
        consume_sensor(gen2)
    )

    
asyncio.run(run_sensors())
