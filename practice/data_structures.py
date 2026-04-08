#lists
nums=[1,2,3,4]
nums.append(5) #adds ele at end
nums.pop(0) #remove at index 0
nums.insert(0,100)
print(nums)
print(nums[::-1]) #reverse
print(nums[1:3]) #slicing
# for i in range(len(nums)):
#     print(nums[i])

#list comprehension
squares = [num**2 for num in range(1,5)]
print(squares)
#tuples
tup=("dog","cat","mouse")
#unpacking
dog,cat,mouse=tup
print(dog)
print(cat)
print(mouse)

#sets
#no duplicates
numbers =set([1,2,2,4])
print(numbers)

#used for set operations
set1={1,2,3,4}
set1.add(1)
print(set1)
set2={3,4,5,6}
print(set1.union(set2))
print(set1.intersection(set2))
print(set1.difference(set2))

#dictionaries
#key value pair
person={
    "name":"dhanush",
    "age":20,
    "address":{
        "city":"chennai",
        "state":"tamilnadu"
    }
}
print(person["address"]["city"])
print(person.keys()) #gets keys
# print(person.clear())
print(person.values())
print(person.get("number","not found"))


#strings
sample_string = "dhanush"
sample_para ="dhanush is a good boy"
print(f"my name is {sample_string}")
print(sample_string[2:4])
print(sample_string.capitalize())
print(sample_string.lower())
print(sample_string.upper())
print(sample_string.replace("u","a"))
words = sample_para.split(" ")
print(words)
print(len(words))
# sample_string[0]="b" error because string is immutable
print(sample_string)
print(sample_string.find("u"))#return index