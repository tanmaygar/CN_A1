cache_ip = "10.0.1.2"
client_ip = "10.0.1.1"
server_ip = "10.0.1.3"

import socket
key_val = dict()

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket_cache = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port_client = 12346
port_server = 12346
port_cache = 12346

# socket_server.connect((server_ip, port_server))
# print("Connection with server established")

socket_client.bind((cache_ip, port_server))
socket_client.listen(5)
print("Connection with client established")

while True:
    
    try:
        c, addr = socket_client.accept()
        print ('Got connection from: ', addr )
        while True:
            recvmsg = c.recv(1024).decode()
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
                    msg = "HTTP/1.1 200 OK\r\n\r\n" + key_val[rec_key]
                    c.send(msg.encode())
                else:
                    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket_server.connect((server_ip, port_server))
                    print("Connection with server established")

                    msg = "GET /assignment1?request={key} HTTP/1.1\r\n\r\n".format(key=rec_key)
                    socket_server.send(msg.encode())
                    print("Message sent to server: " + msg)
                    rec_msg = socket_server.recv(1024).decode()
                    socket_server.close()
                    print("Message received from server: " + rec_msg)

                    if rec_msg == "HTTP/1.1 404 Not Found\r\n\r\nNo such key exists!":
                        msg = "HTTP/1.1 404 Not Found\r\n\r\nNo such key exists!"
                        c.send(msg.encode())
                    else:
                        key_val[rec_key] = rec_msg
                        msg = "HTTP/1.1 200 OK\r\n\r\n" + key_val[rec_key]
                        c.send(msg.encode())

                    print("Connection with server closed")
                    

            elif rec_method == "PUT":
                rec_key = rec_url.split("/")[2]
                rec_val = rec_url.split("/")[3]
                key_val[rec_key] = rec_val

                socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket_server.connect((server_ip, port_server))
                print("Connection with server established")

                msg = "PUT /assignment1/{key}/{val} HTTP/1.1\r\n\r\n".format(key=rec_key, val=rec_val)
                socket_server.send(msg.encode())
                print("Message sent to server: " + msg)
                rec_msg = socket_server.recv(1024).decode()
                socket_server.close()
                print("Message received from server: " + rec_msg)
                c.send("HTTP/1.1 200 OK\r\n\r\nPush sucess!".encode())
                print("Connection with server closed")

            elif rec_method == "DELETE":
                rec_key = rec_url.split("/")[2]
                if rec_key in key_val:
                    key_val.pop(rec_key)
                    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket_server.connect((server_ip, port_server))
                    print("Connection with server established")
                    msg = "DELETE /assignment1/{key} HTTP/1.1\r\n\r\n".format(key=rec_key)
                    socket_server.send(msg.encode())
                    print("Message sent to server: " + msg)
                    rec_msg = socket_server.recv(1024).decode()
                    socket_server.close()
                    print("Message received from server: " + rec_msg)
                    c.send("HTTP/1.1 200 OK\r\n\r\nDelete success!".encode())
                    print("Connection with server closed")
                else:
                    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket_server.connect((server_ip, port_server))
                    print("Connection with server established")
                    msg = "DELETE /assignment1/{key} HTTP/1.1\r\n\r\n".format(key=rec_key)
                    socket_server.send(msg.encode())
                    print("Message sent to server: " + msg)
                    rec_msg = socket_server.recv(1024).decode()
                    socket_server.close()
                    print("Message received from server: " + rec_msg)

                    if rec_msg == "Delete success!":
                        c.send("HTTP/1.1 200 OK\r\n\r\nDelete success!".encode())
                    else:
                        c.send("HTTP/1.1 404 Not Found\r\n\r\nDelete failure!: Key does not exist".encode())
                    print("Connection with server closed")
                        
            else:
                c.send("HTTP/1.1 400 Bad Request\r\n\r\nInvalid request!: Command not found".encode())
            print("Key Val: ", key_val)
    except socket.error as e:
        print(e)
        #print("Connection failed")
        # socket_server.close()
        socket_client.close()
        # socket_cache.close()

        break
