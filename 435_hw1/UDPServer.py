import socket
import sys

udp_server_host = '10.0.0.2'  
udp_server_port = 6677


def packet_loss_calc(transmitted, received):
    return 100-(float((100*received))/transmitted)


#creating socket
try :
    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #SOCK_DGRAM --> UDP
    print 'Socket created'
except socket.error, message :
    print 'Could not create socket. Error code: ' + str(message[0]) + ' Message ' + message[1]
    sys.exit()
 

 #in case of UDP, no listening for and accepting connection from the server
 
# We only bind the socket to the server address
try:
    udp_server_socket.bind((udp_server_host, udp_server_port))
    print 'Socket binding done'
except socket.error , message:
    print 'Bind failed. Error Code : ' + str(message[0]) + ' Message ' + message[1]
    sys.exit()
     


#talking with the client without building the connection
try:
    received_count = 0

    udp_server_socket.settimeout(10)
    for i in range(0, 100):
        # receive data from client (data, addr)
        (data,client_address) = udp_server_socket.recvfrom(1024)

       # print data
       # print client_address
      
      
        if data:
            print 'Got the data from udp client'
            received_count += 1
             
            udp_server_socket.sendto(data , client_address)
	    print "sent server reply"
    

except socket.timeout:
    udp_server_socket.close()	    
finally: 
    packet_loss = packet_loss_calc(100, received_count)    
    with open('result3.txt','a') as file:
	file.write('packet loss: ' + str(packet_loss) + "%\n")
	file.write('received packet count: '+ str(received_count)+'\n\n')
    print 'Closing the udp server socket' 
    udp_server_socket.close()
