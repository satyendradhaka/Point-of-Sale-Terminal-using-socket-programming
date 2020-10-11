import sys
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
args= sys.argv
port= int(args[2])
ip = args[1]
s.connect((ip, port))

while True:
    data=input("details for request to be sent to server(format is request_type upc number_of_items_to be_purchased): ")
    st=data.split()
    s.send(data.encode('utf-8'))
    response=s.recv(1024).decode()
    server_data=response.split()
    if server_data[0]=='1':
        print(' '.join([str(elem) for elem in server_data[1:]]))
    else:
        if st[0]=='1':
            print('total amount is: '+server_data[1])
            s.close()
            break
        else:
            print('product name is: '+server_data[1]+' and price of product is: '+server_data[2])

