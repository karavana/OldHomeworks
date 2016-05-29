#!/usr/bin/python

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink

class homework2Topology( Topo ):
    
    def __init__( self, **kwargs ):
        Topo.__init__( self, **kwargs )
	maxq = 800
        h1 = self.addHost( 'h1' )
	h2 = self.addHost( 'h2' )
        s0 = self.addHost( 's0' )
        s1 = self.addHost( 's1' )
        s2 = self.addHost( 's2' )
        s3 = self.addHost( 's3' )
	
	self.addLink( h1, s0, bw=100, delay='1ms', loss=1, max_queue_size= maxq  )
	self.addLink( s0, s1, bw=10, delay='5ms', loss=10, max_queue_size= maxq  )
	self.addLink( s1, h2, bw=100, delay='1ms', loss=1, max_queue_size= maxq    )

	self.addLink( h1, s2, bw=100, delay='1ms', loss=1, max_queue_size= maxq    )
	self.addLink( s2, s3, bw=10, delay='5ms', loss=10, max_queue_size= maxq   )
	self.addLink( s3, h2, bw=100, delay='1ms', loss=1, max_queue_size= maxq    )
	
topos = { 'homework2Topology': ( lambda **args: homework2Topology(**args) ) }
