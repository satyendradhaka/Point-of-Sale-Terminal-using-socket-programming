import threading
import sys
import socket

threads = []

# def sayHello(n):
#     print(f"Hello {i}")

# for i in range(10):
#     thread=threading.Thread(target=sayHello,args=[i])
#     threads.append(thread)
#     thread.start()

# for thread in threads:
#     thread.join()

 



#command line arguments accepted
args= sys.argv
port= int(args[1])

#socket initialisation
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', port))

#managing database
f= open("database.txt", "r")
text = f.read().splitlines()
db={}
for i in text:
    i=i.split()
    temp=[i[1], i[2]]
    db[i[0]]=temp

#start socket for listening
s.listen(5)
print('waiting for connections')


def kam(c,addr,amount):
    while True:
        request=c.recv(1024).decode()
        client_data=request.split()
        print(amount.get(addr))
        if client_data[0]=='1':
            response='0 '+str(amount[addr])
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
                    amount[addr]+=float(item_details[1])*float(number_of_items)
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
#starting communication between server and client
amount={}
while True:
    c, addr = s.accept()
    print(addr)
    print(amount.get(addr))
    if amount.get(addr) == None:
        amount[addr]=0
    
    print('connection accepted')
    th=threading.Thread(target=kam,args=[c, addr, amount])
    th.start()
    
