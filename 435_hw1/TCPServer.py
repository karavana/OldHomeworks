import socket
import sys


def packet_loss_calc(transmitted, received):
    return 100-(float((100*received))/transmitted)


#create socket
try:
	tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM --> TCP
	print 'Socket created'
except socket.error, message :
    print 'Could not create socket. Error code : ' + str(message[0]) + ' Message ' + message[1]
    sys.exit()


#bind the socket to the server

tcp_server_host = '10.0.0.2'
tcp_server_port = 10000


try:
    tcp_server_socket.bind((tcp_server_host, tcp_server_port))
    print 'Socket binding done'
except socket.error , message:
    print 'Bind failed. Error Code : ' + str(message[0]) + ' Message ' + message[1]
    sys.exit()


#listen--> putting socket into server mode
try:
    tcp_server_socket.listen(1); #the argument 1 shows how many requests can be queued up before refusing outside connections.
    #We will be connected only to our own tcp client
    print 'Socket Listening'
except socket.error , message:
    print 'Listening failed. Error Code : ' + str(message[0]) + ' Message ' + message[1]
    sys.exit()




#socket waits for connections from outside
(connection_socket, client_address) = tcp_server_socket.accept() #returns an open connection between server and client
#this connection is actually a different socket on some another port

print 'got connection from', client_address

#now get the data from the connection
try:
    received_count = 0
    tcp_server_socket.settimeout(5)

    for i in range(0,100):

        data = connection_socket.recv(1024)

        if data:
            received_count += 1
            connection_socket.send(data) #ack
            print 'ok got the data here at server side'


except socket.timeout:
    connection_socket.close()
       
finally:
    # Clean up the connection (socket)
    packet_loss = packet_loss_calc(100, received_count)
    with open("tcp_results2.txt", "a") as file:
        file.write("Packet loss: " + str(packet_loss) + "%\n")
        file.write("Received count: " + str(received_count))
        file.write("\n\n")
    connection_socket.close()





