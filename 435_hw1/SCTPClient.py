import socket
import sys
import sctp
import time
#import pysctp
#import pysctp.sctp as sctp

def mean_rtt_calc(list):
    sum = 0
    for x in list:
        sum += x

    mean = sum / len(list)
    return mean



rtt_list = []


#create socket
try:
	sctp_client_socket = sctp.sctpsocket_tcp(socket.AF_INET)
	print 'Socket created'
except socket.error, message :
    print 'Could not create socket. Error code : ' + str(message[0]) + ' Message ' + message[1]
    sys.exit()

#connect the socket to the server address

sctp_server_host = 'localhost'
sctp_server_port = 11223

sctp_client_socket.connect((sctp_server_host, sctp_server_port))
print 'connected to the server'


try:
	#send data through this connection
	for i in range(0,10):
		try:
			message = 'Message coming from SCTP Client'
			 
			sctp_client_socket.settimeout(0.8)

			start = time.time()
			sctp_client_socket.send(message)


			reply = sctp_client_socket.recv(1024)
			end = time.time()

			print reply

			rtt = end-start
			rtt_list.append(rtt)

		except socket.timeout:
			continue 


	mean_rtt = mean_rtt_calc(rtt_list)

   	with open("tcp_results.txt", "a") as file:
   		file.write("Mean rtt: " + str(mean_rtt))
   		file.write("\n\n")


except socket.error, message:
    print 'Error Code : ' + str(message[0]) + ' Message ' + message[1]
    sys.exit()

finally:
   	#closing the socket
    sctp_client_socket.close()

