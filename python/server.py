import sys
import socket


#command line arguments accepted
args= sys.argv
port= int(args[1])

#socket intialisation
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("socket is intialised")
s.bind(('', port))
print("socket is binded to: "+ str(port))


#managing database
f= open("database.txt", "r")
text = f.read().splitlines()
db={}
for i in text:
    i=i.split()
    temp=[i[1], i[2]]
    db[i[0]]=temp
print('database has been connected')


#socket is lisenting for connections
s.listen(5)
print("socket is listening")
print("waiting for connections")


while True:
    c, addr = s.accept()
    amount=0
    print("connection accepted from ", addr)
    c.send('hello from server'.encode('utf-8'))
    

    #after accepting connection data transaction started between the client and server
    while True:
        try:
            request_type=c.recv(1).decode()
        except Exception:
            request_type=c.recv(1).decode()
            c.send('0 error')
        print('request type recieved')
        print(request_type)
        if request_type=='1':
            c.send(str(len(str(amount))).encode('utf-8'))
            c.send(str(amount).encode('utf-8'))
            c.send('thank u for using our services'.encode('utf-8'))
            c.close()
            print('connection closed with client')
            break
        upc_len=c.recv(1).decode()
        upc=c.recv(int(upc_len)).decode()
        number_of_items=c.recv(1024).decode()
        print('upc is:'+ upc)
        print('number of items requested to purchase are '+ number_of_items)
        price=float(db[upc])
        amount+= price*int(number_of_items)
        c.send('data recieved'.encode('utf-8'))
    c.close()