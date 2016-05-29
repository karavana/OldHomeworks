#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController
from mininet.cli import CLI

from sys import argv


class MultiSwitchTopo(Topo):
	"Multiple switches connected to 2 hosts.(h1 and h2 / client and server)"
	def __init__(self, n=5, bwidth = 18, l = 1, **opts):
		
		
		Topo.__init__(self, **opts)
		switches = range(1,n)

		#Add hosts
		h1 = self.addHost( 'h1' )
		h2 = self.addHost( 'h2' )


		linkopts = dict(bw= bwidth, delay='1ms', loss=l)	#default parameters


		# Add switches
		self.addSwitch( 's0' )
		self.addLink( 'h1' , 's0', **linkopts)	#connect first switch to host h1

		for i in switches:	#connect others to each other consecutively
			prev = i - 1
			self.addSwitch( 's%d' % i )
			self.addLink('s%d' % prev, 's%d' % i, **linkopts)

		self.addLink('s%d' % i, 'h2', **linkopts) #connect last switch to host h2


def simpleTest(client_file_name, server_file_name, switch_num, bandwidth, loss=1):	
	"Create and test a simple network"


	topo = MultiSwitchTopo(switch_num, bandwidth, loss)


	net = Mininet(topo, link=TCLink)
	net.start()


	h2 = net.get('h2')
	h2.cmd("python " + server_file_name + " 100")	#opened server process

	h1 = net.get('h1') 
	h1.cmd("python " + client_file_name + " 100")	#opened client porcess

	

	
	#write the result into file

	#with open('result_file.txt', 'a') as file:
	#	file.write(result)
	#	file.write("\n\n")
    	


	CLI(net)


	net.stop()

if __name__ == '__main__':
	# Tell mininet to print useful information
	#setLogLevel('info')

	#argv -->[server_file_name, client_file_name, switch_num, bandwidth, loss]

	client_file_name = argv[1]

	server_file_name = argv[2] 

	switch_num = int(argv[3])

	bandwidth = int(argv[4])

	if len(argv) > 5:
		loss = int(argv[5])
	else:
		loss = 1

	simpleTest(client_file_name, server_file_name, switch_num, bandwidth, loss)
