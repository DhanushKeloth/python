print("hello world")

# variables
a = 10
b = 20
print(a + b)

num = int(input("enter a number: "))
print(num)
print(type(num))
# int str float complex bool
isvalid = True
print(type(isvalid))
n = bool(0)
print(n)

# operators
#arithmetic
print("arithmetic")
print(5 + 4)
print(2**3) #power
print("floor division",type(6//3)) # floor division display int
print(type(10/3)) # division give float value
print(10 % 3)

#comparision
print("comparision")
print(5>3)
print(5<3)
print(5==3) 
print(5!=3)

#logical operators
print("logical operators")
print(5>3 and 6>4)
print(5>3 or 6>4)
print(not True)

#membership operators check whether a sequence is present in an object
print("a" in "apple") #true
print("a" not in "apple") #false

#identity (is ,is not) check whether two variables point to same object
print("identity")
x = 5
y = 5
print(x is y) #true checks for memory location 
print(x is not y) #false
#for int works only from -5 to 256 and returns true


# control flow
#if
print("control flow\n")
if(5>3):
    print("5 is greater than 3")
elif(5==3):
    print("5 is equal to 3")
else:
    print("5 is not greater than 3")
age =20
status = "adult" if age>18 else "kid"
print(status)

#while
print("while")
i = 1
while(i<=10):
    print(i)
    i+=1
for i in range(1,11,2):#step size as last arg
    if i==5:
        break
    print(i)

