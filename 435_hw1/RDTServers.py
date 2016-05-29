from socket import *
import sys
import sctp
import errno

PORT = 670

class Server():
    def __init__(self, protocol_type):
        self._p = protocol_type
        if self._p == "TCP":
            self._s = socket(AF_INET, SOCK_STREAM)
            self._s.bind(('10.0.0.1', PORT))
            self._s.listen(1)
            conn, address = self._s.accept()
            while 1:
                try:
                    data = conn.recv(100)
                    if not data: break
                    #print "received data:", data
                    conn.send(data)  # echo
                except error as e:
                    if e.errno != errno.ECONNRESET:
                        raise # Not error we are looking for
                    #print "ECONNRESET"
                    continue   
            conn.close()
        elif self._p == "UDP":
            self._s = socket(AF_INET, SOCK_DGRAM)
            self._s.bind(('10.0.0.1',PORT))
            while 1:
                self._s.settimeout(10)
                try:
                    data, addr = self._s.recvfrom(100)
                    self._s.settimeout(None)
                    print "address: ", addr
                    print "received message:", data
                    self._s.sendto(data, addr)
                except timeout, e:
                    print e
                    break
            self._s.close()
        elif self._p == "SCTP":
        	self._s = sctp.sctpsocket_tcp(AF_INET)
        	self._s.bind(('10.0.0.1', PORT))
        	self._s.listen(1)
        	conn, address = self._s.accept()
        	while 1:
        		data = conn.recv(100)
        		if not data: break
        		print "received data:", data
        		conn.send(data)  # echo
        	conn.close()
        	pass        

def main(argv):
    
    if len(sys.argv) != 2:
        print "Usage: python RDTServers.py <protocol_type>"
        return
    if sys.argv[1] == "TCP":
        Server("TCP")
    elif sys.argv[1] == "UDP":
        Server("UDP")
    elif sys.argv[1] == "SCTP":
        Server("SCTP")
    else:
    	print "Dude what?"

if __name__ == '__main__':
    main(sys.argv)
