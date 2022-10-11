client_ip = "10.0.1.1"

import socket
import http.client
import time
# from socket import *

cacheIP = "10.0.1.2"

dst_ip = "10.0.1.2" #str(input("Enter dstIP: "))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(dst_ip)

port = 12346



#Write your code here:
#1. Add code to send HTTP GET / PUT / DELETE request. The request should also include KEY.
#2. Add the code to parse the response you get from the server.
# s.close()
# try:
    # s.connect((dst_ip, port))
    # print("Connection established")
    # s.send('Hello server'.encode())
    # print ('Client received '+ s.recv(1024).decode())


s.connect((dst_ip, port))
print("Connection established")
while True:
    try:
        
        req = input("Enter request as '<method> <key/val>': ")#"GET /assignment1?request=key1 HTTP/1.1" #input("Enter request: ")
        og_req = req

        # if request is q then close and break
        if req == "q":
            print("Closing Program")
            s.close()
            break
        req = req.split(" ")

        # if request is not of length 3 then invalid
        if len(req) != 2: #len(req) != 3:
            print("Invalid request")
            continue

        # if request is get and http/1.1
        #elif req[0] == "GET" and req[2] == "HTTP/1.1":
        elif req[0] == "GET":
            print("get")
            #req_2 = req[1].split("=")
            req_2 = req[1]

            # if put request is not /assignment1?request={key} then invalid
            # if len(req_2) != 2 or req_2[0] != "/assignment1?request":
            #     print("Invalid request")
            #     continue
            og_req = "GET /assignment1?request={key} HTTP/1.1".format(key=req_2)
            print("Request: ", og_req )
            s.send(og_req.encode())
            print("Client received " + s.recv(1024).decode())

        # if request is put and http/1.1
        # elif req[0] == "PUT" and req[2] == "HTTP/1.1":
        elif req[0] == "PUT":
            print("put")
            # req_2 = req[1].split("/")
            req_2 = req[1].split("/")
            # if put request is not /assignment1/{key}/{value} then invalid
            # if len(req_2) != 4 or req_2[1] != "assignment1":
            if len(req_2) != 2:
                print("Invalid request")
                continue
            og_req = "PUT /assignment1/{key}/{val} HTTP/1.1".format(key=req_2[0], val=req_2[1])
            print("Request: ", og_req )
            s.send(og_req.encode())
            print("Client received " + s.recv(1024).decode())


        # if request is delete and http/1.1
        # elif req[0] == "DELETE" and req[2] == "HTTP/1.1":
        elif req[0] == "DELETE":
            print("delete")
            # req_2 = req[1].split("/")
            req_2 = req[1]
            # if put request is not /assignment1/{key} then invalid
            # if len(req_2) != 3 or req_2[1] != "assignment1":
            #     print("Invalid request")
            #     continue
            og_req = "DELETE /assignment1/{key} HTTP/1.1".format(key=req_2)
            print("Request: ", og_req )
            s.send(og_req.encode())
            print("Client received " + s.recv(1024).decode())

        else:
            print("Invalid request")
            continue
    
        #s.close()

    except socket.error as e:
        print("Connection closed: ", e)
        s.close()
        break
