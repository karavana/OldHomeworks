import socket
import sys
import time

def mean_rtt_calc(list):
    sum = 0
    for x in list:
        sum += x

    mean = sum / len(list)
    return mean



rtt_list = []

#create socket
try:
	tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM --> TCP
	print 'Socket created'
except socket.error, message :
    print 'Could not create socket. Error code : ' + str(message[0]) + ' Message ' + message[1]
    sys.exit()


#connect the socket to the server address

tcp_server_host = '10.0.0.2'
tcp_server_port = 10000

tcp_client_socket.connect((tcp_server_host, tcp_server_port))
print 'connected to the server'


#cannot do this whole try part in a while true loop since we need to create  new socket after closing one and before connecting

try:
	for i in range(0,100):
		#send data through this connection

		try:
			tcp_client_socket.settimeout(2)

			message = 'bjbertydfghrtydfghertydfghcvbfghdfgxcvbxcxcvbdfghcvbcvfgytyvbgh'

			#print message.__sizeof__()
			  
			start = time.time() 
			tcp_client_socket.send(message)

			ack = tcp_client_socket.recv(1024)
			end = time.time()

			rtt = end-start
			rtt_list.append(rtt)

			

		except socket.timeout:
			continue 

finally:
   	#closing the socket
	tcp_client_socket.close()
   	mean_rtt = mean_rtt_calc(rtt_list)

   	with open("tcp_results2.txt", "a") as file:
   		file.write("Mean rtt: " + str(mean_rtt))
   		file.write("\n\n")

   


