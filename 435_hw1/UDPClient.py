import socket  
import sys  
import time


def mean_rtt_calc(list):
    sum = 0
    for x in list:
        sum += x
    if len(list)>0 :
	mean = sum / len(list)
    	return str(mean*1000) #in miliseconds
    else:
	return 'None'


rtt_list = []
 
# create udp socket
try:
    udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #SOCK_DGRAM --> UDP
except socket.error:
    print 'Failed to create socket'
    sys.exit()


#no need to bind in UDP

udp_server_host = '10.0.0.2'
udp_server_port = 6677


try : 
    for i in range(0,100):

        #directly connect to the address of the server and send its message

        message = "insallah allah seni o geride biraktigin karinla terbiye etmesin"
        #message = "ne yaptiniz ulan siz? ne yaptiniz? nerde ne yaptin?"    88
        #message = "beni dovduler abi dedigin zaman pezevenklerin elinden gittim aldim" 103
        
        #print message.__sizeof__()
        start =time.time()
	try:
		udp_client_socket.settimeout(0.9)
	
        	udp_client_socket.sendto(message, (udp_server_host, udp_server_port))
         
        # receive reply from server
        	print i
		(server_reply,server_address) = udp_client_socket.recvfrom(1024)
        	if server_reply:
			end = time.time()
       			rtt = end - start
        		rtt_list.append(rtt)
	except socket.timeout:
		continue
	

    mean_rtt = mean_rtt_calc(rtt_list)
	
    print mean_rtt
    with open('result3.txt','a') as file:
	file.write('mean RTT value: '+ mean_rtt)
	file.write('\n\n')
 
except socket.error, message:
    print 'Error Code : ' + str(message[0]) + ' Message ' + message[1]
    sys.exit()

finally:
    print 'Closing the udp client socket'
    udp_client_socket.close()



