import socket
import sys
import sctp
#import pysctp
#import pysctp.sctp as sctp

#with pysctp can build the server as in TCP

def packet_loss_calc(transmitted, received):
    return 100-(float((100*received))/transmitted)


#create socket
try:
	sctp_server_socket = sctp.sctpsocket_tcp(socket.AF_INET);
	print 'Socket created'
except socket.error , message :
    print 'Could not create socket. Error code : ' + str(message[0]) + ' Message ' + message[1]
    sys.exit()


#bind the socket to the server

sctp_server_host1  = 'localhost'
sctp_server_port1 = 11223
sctp_server_host2 = ''
sctp_server_port2 = 11224

try:
    sctp_server_socket1.bind((sctp_server_host1, sctp_server_port1))
	sctp_server_socket2.bind((sctp_server_host2, sctp_server_port2))
    print 'Socket binding done'
except socket.error , message:
    print 'Bind failed. Error Code : ' + str(message[0]) + ' Message ' + message[1]
    sys.exit()


#listen--> putting socket into server mode
try:
    sctp_server_socket1.listen(1); 
	sctp_server_socket2.listen(1); 
    print 'Socket Listening'
except socket.error , message:
    print 'Listening failed. Error Code : ' + str(message[0]) + ' Message ' + message[1]
    sys.exit()

	


#socket waits for connections from outside
(connection_socket, client_address) = sctp_server_socket.accept() #returns an open connection between server and client
#this connection is actually a different socket on some another port

print 'got connection from', client_address

#now get the data from the connection
try:
	received_count = 0
	sctp_server_socket.settimeout(5)

	for i in range(0,10):
	    data = connection_socket.recv(1024)

	    if data:
	    	received_count += 1
	    	#print 'ok got the data here at server side'
	    	#print data
	        #print 'sending data back to the client'
	        connection_socket.sendall("suck it bitch") #ack

except socket.timeout:
    connection_socket.close()  
        
finally:
    # Clean up the connection (socket)
    packet_loss = packet_loss_calc(10, received_count)
    with open("sctp_results.txt", "a") as file:
        file.write("Packet loss: " + str(packet_loss) + "%\n")
        file.write("Received packet count: " + str(received_count))
        file.write("\n\n")
    connection_socket.close()


