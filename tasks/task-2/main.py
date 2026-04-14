import redis
import pickle
import time
import uuid
import os
import random
from multiprocessing import Process

# Connect to Redis
# Ensure your Redis server is running (redis-cli ping -> PONG)
r = redis.Redis(host='localhost', port=6379, db=0)

def generate_thumbnail(image_id, size=(256, 256)):
    time.sleep(1)  # Simulate work
    return f"/thumbs/{image_id}_{size[0]}x{size[1]}.jpg"

def send_email(to, template):
    # Simulate a 60% chance of failure to test retries
    if random.random() < 0.6:
        raise ConnectionError("SMTP Server Timeout")
    time.sleep(1)
    return "email_sent"

def enqueue(func, *args, **kwargs):
    task_id = str(uuid.uuid4())[:6] # Short unique ID
    
    task_envelope = {
        "id": task_id,
        "func": func,
        "args": args,
        "kwargs": kwargs,
        "retries": 0,
        "max_retries": 3,
        "start_time": time.time()
    }
    
    # Push to 'default' queue and set initial status
    r.rpush("default_queue", pickle.dumps(task_envelope))
    r.set(f"result:{task_id}", pickle.dumps({"status": "PENDING", "func": func.__name__, "retries": 0}))
    
    print(f" [PRODUCER] Queued Task {task_id}: {func.__name__}")
    return task_id
def worker_loop(worker_name):
    print(f" [{worker_name}] started and polling...")
    while True:
        # BLPOP blocks until a task is available
        _, data = r.blpop("default_queue")
        task = pickle.loads(data)
        tid = task['id']
        
        print(f" [{worker_name}] Picked up task {tid} ({task['func'].__name__})")
        
        try:
            # Execute the task
            result_val = task['func'](*task['args'], **task['kwargs'])
            duration = round(time.time() - task['start_time'], 2)
            
            # Store Success in Result Backend
            r.set(f"result:{tid}", pickle.dumps({
                "status": "SUCCESS", 
                "func": task['func'].__name__,
                "retries": task['retries'], 
                "duration": f"{duration}s",
                "result": result_val
            }))
            print(f" [{worker_name}] Task {tid} COMPLETED")

        except Exception as e:
            # Retry Logic
            if task['retries'] < task['max_retries']:
                task['retries'] += 1
                # Exponential Backoff: 2, 4, 8 seconds
                wait_time = 2 ** task['retries']
                
                print(f" [{worker_name}] Task {tid} FAILED ({e}) - retry {task['retries']}/{task['max_retries']} in {wait_time}s")
                
                # Update status in backend and sleep before re-queueing
                r.set(f"result:{tid}", pickle.dumps({"status": "RETRYING", "func": task['func'].__name__, "retries": task['retries']}))
                time.sleep(wait_time)
                r.rpush("default_queue", pickle.dumps(task))
            else:
                # Permanent failure -> Dead Letter Queue
                print(f" [{worker_name}] Task {tid} PERMANENTLY FAILED. Moving to DLQ.")
                r.rpush("dead_letter_queue", pickle.dumps(task))
                r.set(f"result:{tid}", pickle.dumps({"status": "DEAD_LETTER", "func": task['func'].__name__, "retries": task['retries'], "duration": "-"}))

def print_dashboard():
    print("\n" + "="*60)
    print(f"{'Task ID':<10} | {'Func':<10} | {'Status':<12} | {'Retries':<8} | {'Duration'}")
    print("-" * 60)
    
    # Scan for all result keys
    for key in r.scan_iter("result:*"):
        raw_data = r.get(key)
        if raw_data:
            data = pickle.loads(raw_data)
            task_id = key.decode().split(":")[1]
            status = data.get("status", "N/A")
            func = data.get("func", "N/A")
            retries = data.get("retries", 0)
            duration = data.get("duration", "-")
            print(f"{task_id:<10} | {func[:10]:<10} | {status:<12} | {retries:<8} | {duration}")
    print("="*60 + "\n")


if __name__ == "__main__":
    # 1. Clear previous Redis data (Optional, for clean demo)
    r.flushdb()

    # 2. Start 3 Worker Processes
    workers = []
    for i in range(1, 4):
        p = Process(target=worker_loop, args=(f"Worker-{i}",))
        p.start()
        workers.append(p)

    # 3. Producer creates tasks
    time.sleep(1) # Give workers time to start
    enqueue(generate_thumbnail, image_id=4521, size=(256, 256))
    enqueue(send_email, to="bob@co.com", template="welcome")
    enqueue(send_email, to="alice@co.com", template="receipt") # Adding one more for fun
    
    # 4. Wait for processing, then show Dashboard
    print("\n... Waiting for workers to process tasks ...\n")
    time.sleep(15) # Wait enough time for retries to happen
    print_dashboard()

    # Kill workers so the script ends
    for p in workers:
        p.terminate()