from socket import *
import sys
import sctp
import time

#IP = '127.0.0.1'
PORT = 670

class Client():
    def __init__(self, protocol_type):
        self._p = protocol_type
        self._loss = 0
        if self._p == "TCP":
            self._s = socket(AF_INET, SOCK_STREAM)
            self._s.connect(('10.0.0.1', PORT))
            data = "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"
            print "Sending " + str(data) + "..."
            start = time.time()
            for i in range(1000):
                self._s.send(data)
                try:
                    self._s.settimeout(0.5)
                    response = self._s.recv(100)
                    self._s.settimeout(None)
                    #print "server response: ", response
                except timeout, e:
                    print e
                    self._loss += 1
                self._s.settimeout(None)
                print i
            end = time.time()
            self._rtt = (end-start)*1000.0
            
            print "RTT: ", self._rtt
            print "Loss: ", self._loss/10.0
            self._s.close()
        elif self._p == "UDP":
            self._s = socket(AF_INET, SOCK_DGRAM)
            #connectionless
            data = "12345678901234567890"
            print "Sending " + str(data) + "..."
            start = time.time()
            #for i in range(10):
            for i in range(100):
                self._s.sendto(data, ('10.0.0.1', PORT))
                try:
                    self._s.settimeout(1)
                    response, addr = self._s.recvfrom(100)
                    self._s.settimeout(None)
                    print "received"
                    #if not response:
                    #    self._loss += 1
                except timeout, e:
                    print e
                    self._loss += 1
            end = time.time()
            self._rtt = (end-start)*1000.0
            #self._loss = self._loss/10.0
            print "server response: ", response
            print "RTT: ", self._rtt
            print "Loss: ", self._loss
        elif self._p == "SCTP":
            self._s = sctp.sctpsocket_tcp(AF_INET)
            self._s.connect(('10.0.0.1', PORT))
            data = "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"
            print "Sending " + str(data) + "..."
            start = time.time()
            for i in range(10):
                self._s.send(data)
                response = self._s.recv(100)
                if not response:
                    self._loss += 1
            end = time.time()
            self._rtt = (end-start)*1000.0
            self._loss = self._loss/10.0
            print "server response: ", response
            print "RTT: ", self._rtt
            self._s.close()
            pass

def main(argv):
    
    if len(sys.argv) != 2:
        print "Usage: python RDTClients.py <protocol_type>"
        return
    if sys.argv[1] == "TCP":
        Client("TCP")
    elif sys.argv[1] == "UDP":
        Client("UDP")
    elif sys.argv[1] == "SCTP":
        Client("SCTP")

if __name__ == '__main__':
    main(sys.argv)
