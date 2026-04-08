try:
    print(10/0)
except ZeroDivisionError:
    print("cannot divide by zero")
finally:
    print("this will always execute")

#raise exception 

    
age=int(input("enter age: "))
if age<0:
    raise Exception("age can't be negative")
else:
    print("valid age")

