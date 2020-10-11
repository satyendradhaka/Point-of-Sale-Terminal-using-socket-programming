f= open("database.txt", "r")
text = f.read().splitlines()
db={}
for i in text:
    i=i.split()
    temp=[i[1], i[2]]
    db[i[0]]=temp
print(db)
