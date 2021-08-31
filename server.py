import sys
import socket


#command line arguments accepted
args= sys.argv
if(len(args)<2):
    print("please provide which port value")
    sys.exit()
port= int(args[1])

#socket initialisation
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

#start socket for listening
s.listen(5)
print("socket is listening")
print('waiting for connections')

#starting communication between server and client
while True:
    c, addr = s.accept()
    print("connection accepted from ", addr)
    c.send('hello from server'.encode('utf-8'))
    amount=0
    while True:
        request=c.recv(1024).decode()
        client_data=request.split()
        if client_data[0]=='1':
            response='0 '+str(amount)
            c.send(response.encode('utf-8'))
            print('total amount sent, now closing connection with '+addr[0])
            c.close()
            break
        elif client_data[0]=='0':
            if len(client_data)==3:
                upc=client_data[1]
                number_of_items=client_data[2]
                try:
                    item_details=db[upc]
                    amount+=float(item_details[1])
                    response='0 '+item_details[0]+' '+item_details[1]
                    c.send(response.encode('utf-8'))
                except Exception:
                    response='1 '+'upc not found in database'
                    c.send(response.encode('utf-8'))
            else:
                response='1 '+'invalid request, format should be: \n for closing connection: 1\n for sending item details: 0 upc no._of_items_to_be_purchased'
                c.send(response.encode('utf-8'))
        else:
            response='1 '+ 'invalid request'
            c.send(response.encode('utf-8'))
