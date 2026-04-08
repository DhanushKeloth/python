#functions
def sayHello():
    print("hello world")
sayHello()

def add(a,b=10):
    return a+b
print(add(2,3))
print(add(2)) #uses default value
print(add(b=2,a=5)) #uses named arguments

#lambda functions
count = lambda x: x+1
print(count(2))

def master_func(name, *args, status="Active", **kwargs):
    print(f"Name: {name}")
    print(f"Args: {args}")
    print(f"Status: {status}")
    print(f"Kwargs: {kwargs}")

# Calling the function
master_func("Dhanush", 1, 2, 3, location="Chennai", role="Dev")

def sumall(*args):
    return sum(args)
print(sumall(1,2,3,4,5))

numbers=[1,2,3,4,5]
doubled = list(map(lambda x:x*2, numbers))
print(doubled)

even = list(filter(lambda x:x%2==0,numbers))
print(even)
names=["dhanush", "admin", "guest", "dev_user"]

filtered = list(filter(lambda name:len(name)>5,names))
print(filtered)