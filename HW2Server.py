import socket
import threading
import hashlib
import struct
import os

buffer_lock = threading.Lock()
adinibufferkoydum ={}

class check_and_ack(threading.Thread):

	def __init__(self,socket, dest):
		threading.Thread.__init__(self)	
		self.socket = socket
		self.dest = dest
		self.start()		



	def torn_packet(self, packet):

		#seq_num = struct.unpack('=I', packet[0:4])
		seq_num = packet[0:32]

		#print "torn_seq: "+ seq_num

		#checksum = struct.unpack('=H', packet[4:6])		#checksum of ACK and the seq_num
		checksum =  packet[32:48]
		
		#print "torn_check: "+ checksum

		data = packet[48:]
		return seq_num, checksum, data


	def create_ack_packet(self, line_num, data):

		m = hashlib.md5()

		#seq_num = struct.pack('=I', num)
		seq_num = line_num
		#seq_num = (32-len(str(seq_num)))*"0" + str(seq_num)

		if data != "END!":
			
			m.update("ACK" + seq_num)

			checksum = m.digest()		#checksum of ACK and the seq_num

			#checksum = struct.pack('=h',checksum_to_put)		


			packet = seq_num + checksum + "ACK"

		else:

			m.update("DONE!" + seq_num)

			checksum = m.digest()		#checksum of ACK and the seq_num

			#checksum = struct.pack('=h',checksum_to_put)		

			packet = seq_num + checksum + "DONE!"


		return packet


	not_finished = True

	def run(self):

		while check_and_ack.not_finished:

			received_ack, server_addr = self.socket.recvfrom(1000)

			seq_num, checksum, data = self.torn_packet(received_ack)
			'''
			if data == "END!":
				print threading.current_thread()
			'''
			#print data
			
			m = hashlib.md5()

			m.update(data + seq_num)

			exp_checksum = m.digest()		#expected checksum of data and seq_num
			'''
			if checksum != exp_checksum:
				#print checksum
				print seq_num
				print data
				break
			'''
			#print "seq_num: " +seq_num

			#print data

			#print checksum == exp_checksum


			if(data == "END!"):

 				#END! packet received, send DONE! packet

				packet = self.create_ack_packet(seq_num, data)

							
				for i in range(0,10):

					try:
						self.socket.sendto(packet, self.dest)

					except socket.error:
						break

				

				check_and_ack.not_finished = False

 				break


		 	if checksum == exp_checksum :	#packet is not corrupted (if it is already in the buffer, we replace it and send a new ACK)
		 			
		 			#print "if e girdi!!!"

		 			#print seq_num

		 			

		 			buffer_lock.acquire()

					adinibufferkoydum[seq_num] =  data

					buffer_lock.release()

					#print adinibufferkoydum.keys()

					ack_packet = self.create_ack_packet(seq_num,data)

					self.socket.sendto(ack_packet, self.dest)
			
					#print "hey"
		

		#print threading.current_thread()
					
		self.socket.close()

		os._exit(0)




	
if __name__ == '__main__':	
	
	server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	
	
	server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	host1 = "192.168.8.2"

	host2 = "192.168.64.2"

	port1 = 8001

	port2 = 8002

	dest1_host = "192.168.2.1"

	dest2_host = "192.168.16.1"

	server_socket1.bind((host1,port1))

	server_socket2.bind((host2,port2))

	dest1 = (dest1_host,port1)

	dest2 = (dest2_host, port2)

	

	receive_bir = check_and_ack(server_socket1, dest1)

	receive_iki = check_and_ack(server_socket2, dest2)


	receive_bir.join()

	receive_iki.join()


	output_file =  open("output.txt", "wb")

	#sort the keys

	keylist = adinibufferkoydum.keys()

	keylist.sort()

	#write into the output file

	for k in keylist:

		output_file.write(adinibufferkoydum[k])

	output_file.close()