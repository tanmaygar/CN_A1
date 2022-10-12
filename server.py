server_ip = "10.0.1.3"

import socket
import http.server

#WRITE CODE HERE:
#1. Create a KEY-VALUE pairs (Create a dictionary OR Maintain a text file for KEY-VALUES).
key_val = dict()



dst_ip = "10.0.1.3"#str(input("Enter Server IP: "))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket successfully created")

dport = 12346

s.bind((dst_ip, dport))
print ("socket binded to %s" %(dport))

s.listen(5)
print ("socket is listening")

while True:
  
  try:
    c, addr = s.accept()
    print ('Got connection from', addr )
    # recvmsg = c.recv(1024).decode()
    # print('Server received '+ recvmsg)
    while True:
      recvmsg = c.recv(1024).decode()
      print('Server received '+ recvmsg)
      
      # c.send('Hello client'.encode())

      #Write your code here
      #1. Uncomment c.send 
      #2. Parse the received HTTP request

      #3. Do the necessary operation depending upon whether it is GET, PUT or DELETE
      #4. Send response

      rec_req = recvmsg.split(" ")
      rec_method = rec_req[0]
      rec_url = rec_req[1]

      if rec_method == "GET":
        rec_key = rec_url.split("=")[1]
        if rec_key in key_val:
          c.send(key_val[rec_key].encode())
        else:
          c.send("No such key exists!".encode())
      elif rec_method == "PUT":
        rec_key = rec_url.split("/")[2]
        rec_val = rec_url.split("/")[3]
        key_val[rec_key] = rec_val
        c.send("Push sucess!".encode())
      elif rec_method == "DELETE":
        rec_key = rec_url.split("/")[2]
        if rec_key in key_val:
          key_val.pop(rec_key)
          c.send("Delete success!".encode())
        else:
          c.send("Delete failure!".encode())
      else:
        c.send("Invalid request!".encode())
      print("Key Val: ", key_val)

      ##################

    c.close()
  except:
    # print("Error while accepting connection")
    c.close()
    break
  #break