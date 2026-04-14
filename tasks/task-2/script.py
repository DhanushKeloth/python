import pickle
import time

def simulate_task(image_id):
    print("process image with ",image_id)
    time.sleep(3)
    print("image success ",image_id)


def simulate_email(email_id):
    print("sending email to ",email_id)
    time.sleep(3)
    print("email sento to ",email_id)


def worker_loop(data):
    print("worker waiting for the tasks")
    task = pickle.loads(data) #converts the bytes to a dictionary
    task['func'](*task['args'])

task_data={
  'func':simulate_task,
  'args':(1,)  
}
task_bytes = pickle.dumps(task_data)
email_task ={
    'func':simulate_email,
    'args':("dhanushkeloth@gmail.com",)
}

email_bytes = pickle.dumps(email_task) #converts the dictionary to bytes

worker_loop(task_bytes)
worker_loop(email_bytes)


# recieved_task = pickle.loads(task_bytes)

#here * is used to unpack the tuple and passed as arguments to the function
# recieved_task['func'](*recieved_task['args']) 

