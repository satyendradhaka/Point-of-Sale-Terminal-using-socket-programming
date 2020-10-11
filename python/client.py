import sys
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
args= sys.argv
port= int(args[2])
ip = args[1]
s.connect((ip, port))
# s.send('hello from client'.encode('utf-8'))
print(s.recv(1024).decode())

while True:
    st=input("details for request to be sent to server(format is request_type upc number_of_items_to be_purchased): ").split()
    print('input scanned')
    request_type=int(st[0])
    if request_type==1:
        s.send(str(request_type).encode('utf-8'))
        print('request type is 1 and closing request about to send')
        amount_len=s.recv(1).decode()
        print('total amount of transaction is: '+s.recv(int(amount_len)).decode())
        print(s.recv(1024).decode())
        s.close()
        print('connection closed')
        break
    s.send(str(request_type).encode('utf-8'))
    upc=st[1]
    upc_len=len(upc)
    number_of_items=st[2]
    items_len=len(number_of_items)
    s.send(str(upc_len).encode('utf-8'))
    s.send(upc.encode('utf-8'))
    print('upc is sent')
    s.send(number_of_items.encode('utf-8'))
    print('number of item is sent')
    print(s.recv(1024).decode())


