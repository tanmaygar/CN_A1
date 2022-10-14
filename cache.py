cache_ip = "10.0.1.2"
client_ip = "10.0.1.1"
server_ip = "10.0.1.3"

import socket
key_val = dict()

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket_cache = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port_client = 12346
port_server = 12346
port_cache = 12346

# socket_server.connect((server_ip, port_server))
# print("Connection with server established")

socket_client.bind((cache_ip, port_client))
socket_client.listen(5)
print("Connection with client established")
tmp = ""
while True:
    isPresent = True
    
    try:
        c, addr = socket_client.accept()
        print ('Got connection from: ', addr )
        while True:
            recvmsg = c.recv(1024).decode()
            tmp = recvmsg
            print('Cache received: '+ recvmsg)
            if recvmsg == "q":
                print('Client has been disconnected')
                break
            if recvmsg == "KeyboardInterrupt":
                print('Client has been disconnected due to interrupt')
                break

            rec_req = recvmsg.split(" ")
            rec_method = rec_req[0]
            rec_url = rec_req[1]
            if rec_method == "GET":
                rec_key = rec_url.split("=")[1]
                if rec_key in key_val:
                    c.send(key_val[rec_key].encode())
                else:
                    isPresent = False
                    break
                    # socket_server.connect((server_ip, port_server))
                    # print("Connection with server established")
                    # socket_server.send(recvmsg.encode())
                    # rec_val = socket_server.recv(1024).decode()
                    # if rec_val == "No such key exists!":
                    #     c.send(rec_val.encode())
                    # else:
                    #     key_val[rec_key] = rec_val
                    #     c.send(rec_val.encode())
                    # print("Connection with server closed")
                    # socket_server.close()

            elif rec_method == "PUT":
                rec_key = rec_url.split("/")[2]
                rec_val = rec_url.split("/")[3]
                key_val[rec_key] = rec_val
                socket_server.send(recvmsg.encode())
                c.send("Push sucess!".encode())

            elif rec_method == "DELETE":
                rec_key = rec_url.split("/")[2]
                if rec_key in key_val:
                    key_val.pop(rec_key)
                    socket_server.send(recvmsg.encode())
                    c.send("Delete success!".encode())
                else:
                    socket_server.send(recvmsg.encode())
                    recmsg = socket_server.recv(1024).decode()
                    if recmsg == "Delete success!":
                        c.send("Delete success!".encode())
                    else:
                        c.send("Delete failure!: Key does not exist".encode())
                        
            else:
                c.send("Invalid request!".encode())
        if isPresent == False:
            print("not here")
            socket_server.connect((server_ip, port_server))
            print("Connection with server established")
            socket_server.send(tmp.encode())
            rec_val = socket_server.recv(1024).decode()
            if rec_val == "No such key exists!":
                c.send(rec_val.encode())
            else:
                key_val[rec_key] = rec_val
                c.send(rec_val.encode())
            # socket_server.close()


    except socket.error as e:
        print(e)
        #print("Connection failed")
        socket_server.close()
        socket_client.close()
        # socket_cache.close()

        break
