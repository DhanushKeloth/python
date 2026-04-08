newfile = open("sample.txt","r")
content =newfile.read()
print(content)
newfile.close()
newfile = open("new.txt","w")
newfile.write("hello world")
newfile.close()

#writelines
newlines = ["hello\n","world\n","how\n","are\n","you\n"]
newfile = open("new.txt","w")
newfile.writelines(newlines)
newfile.close()

#append
newfile = open("sample.txt","a")
newfile.write("my name is dhanush")
newfile.close()