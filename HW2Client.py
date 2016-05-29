import socket
import threading
import hashlib
import time
import os

input_read_lock = threading.Lock()
window_lock = threading.Lock()
window = {}

start = time.time()



class read_and_send(threading.Thread):
	def __init__(self,socket, dest, file_name):
		threading.Thread.__init__(self)
		self.file = file_name	
		self.socket = socket
		self.dest = dest
		self.start()		



	def create_packet(self, data, line_num):
		

		m = hashlib.md5()

		seq_num = line_num

		#print "pack_seq: " +seq_num
		#seq_num = (32-len(str(seq_num)))*"0" + str(seq_num)

		m.update(data + seq_num)

		checksum = m.digest()		#checksum of ACK and the seq_num

		#print "cre_check: "+checksum
		

		#seq_num = struct.pack('=I',line_num)		#4 byte seq_num


		#checksum = struct.pack('=H',checksum_to_put)		# 2 byte checksum
		
		packet = seq_num + checksum + data #bytes(data)

		return packet


	dicil = "0"*32  #common between threads

	def run(self):

		#print threading.current_thread().getName()

		input_read_lock.acquire()
		data = self.file.read(952)
		
		line_num = read_and_send.dicil

		read_and_send.dicil = str(int('9' + read_and_send.dicil) + 1)[1:]
		#print "line: " +str(line_num) + " , data: "+ data 

		#print "dicil: "+ read_and_send.dicil

		input_read_lock.release()

		#print str(threading.current_thread()) +"  first data:         "+str(len(data))

		#reading a line from input file and creating the packet, putting it in window
		while len(data) != 0:

			packet = self.create_packet(data, line_num)		#packet with seq_num and checksum along with the data created

			#print line_num
			#print "line_num: "+line_num

			window_lock.acquire()

			window[line_num] = [packet, float(time.time()), threading.current_thread().getName()]


			window_lock.release()


			#sending packet to the server
			
			self.socket.sendto(packet,self.dest)
			
			input_read_lock.acquire()

			data = self.file.read(952)
			
			line_num = read_and_send.dicil
			read_and_send.dicil = str(int('9' + read_and_send.dicil) + 1)[1:]

			#print str(line_num) + " , "+ data 
			input_read_lock.release()

			#print "second data :    "+ str(len(data))

			#print window.keys()

			if len(data) == 0:
				break

		

		

		#print len(window)

		#resend the packets still residing in the window until none is left without an ACK

		while len(window):
			
			for k in window.keys():

				#print k

				window_lock.acquire()
				
				self.socket.sendto(window[k][0], self.dest) if k in window.keys() else True
				if k in window.keys():
					#print type(window[k][1])
				 	window[k][1] = time.time()  								#updating time of sending to properly calculate rtt
					window[k][2] = threading.current_thread().getName() 			#updating the current thread sending it
				window_lock.release()



		#send a packet to notify that we have sent the whole file--> END! packet


		window_lock.acquire()

		read_and_send.dicil = str(int('9' + read_and_send.dicil) + 1)[1:]
		packet = self.create_packet("END!", read_and_send.dicil)

		window[read_and_send.dicil] = [packet, time.time(), threading.current_thread().getName()]

		read_and_send.dicil = str(int('9' + read_and_send.dicil) + 1)[1:]
		window_lock.release()

		

		#while len(window):

		#for i in range(0,10):

		#self.socket.settimeout(5)
		while 1:
			try:
				
				self.socket.sendto(window[window.keys()[0]][0], self.dest) if len(window)>0 else True

				#print threading.current_thread()
			except socket.error :
				#print "error  " + str(threading.current_thread().getName())

				break

		#self.socket.close()





class ack_receiver(threading.Thread):

	def __init__(self, sock):

		threading.Thread.__init__(self)
		self.socket = sock
		self.start()	


	def torn_packet(self, packet):

		#seq_num = struct.unpack('=I', packet[0:4])
		seq_num = packet[0:32]

		#checksum = struct.unpack('=h', packet[4:6])		#checksum of ACK and the seq_num
		checksum =  packet[32:48]
		#data = struct.unpack('=H', packet[6:])	
		data = packet[48:]
		return seq_num, checksum, data


	flag = True

	rtt_eth0 =0

	num0 =0

	num1 = 0

	rtt_eth1 =0

	def run(self):

		
		while ack_receiver.flag:

			received_ack, server_addr = self.socket.recvfrom(1024)

			seq_num, checksum, ack_str = self.torn_packet(received_ack)

			m = hashlib.md5()

			m.update(ack_str+ seq_num)

			exp_checksum = m.digest()	

			if exp_checksum == checksum  and ack_str == "DONE!":	#ack of the end packet-> time to close down

				#print ack_str

				window_lock.acquire()

				if len(window):
					del window[window.keys()[0]]

				#window.clear()
				ack_receiver.flag = False

				window_lock.release()

				#print str(threading.current_thread().getName())

				

				break

			m = hashlib.md5()

			m.update(ack_str + seq_num)

			rec_checksum = m.digest()		#checksum of ACK and the seq_num

		 	if checksum == rec_checksum and seq_num in window.keys() and ack_str != "DONE":

		 			window_lock.acquire()

		 			if seq_num in window.keys():
		 				#print seq_num
		 				t = time.time()
		 				rtt = t- window[seq_num][1]

		 				#print rtt

		 				if window[seq_num][2] == "Thread-1":

		 					ack_receiver.rtt_eth0 += rtt
		 					ack_receiver.num0 +=1
		 					#print ack_receiver.rtt_eth0

		 				elif window[seq_num][2] == "Thread-2":
		 					ack_receiver.rtt_eth1 += rtt
		 					ack_receiver.num1 +=1
		 					#print ack_receiver.rtt_eth1

						del window[seq_num]  

					window_lock.release()

			#print str(threading.current_thread().getName()) + str(ack_receiver.flag)


		#print "closing time bitchees"

		#self.socket.setsockopt(socket.SOL_SOCKET, socket. SO_REUSEADDR,1)

		#self.socket.close()
		
		end = time.time()

		total = end-start

		print "total time: " + str(total)

		#print rtt_eth0

		#print rtt_eth1

		print "mean rtt of eth0: " +str(ack_receiver.rtt_eth0 / ack_receiver.num0)

		print "mean rtt of eth1: " +str(ack_receiver.rtt_eth1 / ack_receiver.num1)

		os._exit(0)


				


	
if __name__ == '__main__':	

	client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	
	
	client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	host1 = "192.168.2.1"

	host2 = "192.168.16.1"

	port1 = 8001

	port2 = 8002

	dest1_host = "192.168.8.2"

	dest2_host = "192.168.64.2"

	client_socket1.bind((host1,port1))

	client_socket2.bind((host2,port2))

	dest1 = (dest1_host,port1)

	dest2 = (dest2_host, port2)

	input_file =  open("inputb.txt", "rb")

	start = time.time()

	send_bir = read_and_send(client_socket1, dest1, input_file)

	send_iki = read_and_send(client_socket2, dest2, input_file)

	receive_bir = ack_receiver(client_socket1)

	receive_iki = ack_receiver(client_socket2)


	send_bir.join()

	send_iki.join()

	receive_bir.join()

	receive_iki.join()

	if client_socket1:
		client_socket1.close()

	if client_socket2:
		client_socket2.close()

