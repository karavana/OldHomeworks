def printConfiguration(net):
    print "Host\tInterface\tIP\t\tMAC"
    hostlist = net.items()
    for h in hostlist:
        nod = net.get(str(h[1]))
	itf = nod.intfNames()
	for i in itf:
		print nod, "\t", i, "\t", nod.IP(str(i)), "\t", nod.MAC(str(i))
		
    print "\nLINKS"
#    links = net.topo.links(withInfo = True, withKeys = True, sort=True )
    links = net.topo.links()
    print "From-To\t\tBandwidth\tDelay\tLoss\tInterfaces"
    for l in links:
#	attr = l[3]
        src = net.get(l[0])
        dest = net.get(l[1])
	conn =src.connectionsTo(dest)
#	print src, "-", dest, "\t", attr['bw'], "Mbps\t", attr['delay'], "\t", attr['loss'], "%\t", conn
	print src, "-", dest, "\t", conn, " " , l
    print "\nRouting table of h1"	
    print net.get("h1").cmd("route -n")


def configureRouting(net):
    h1 = net.get('h1') 
    h2 = net.get('h2') 
    s0 = net.get('s0') 
    s1 = net.get('s1') 
    s2 = net.get('s2') 
    s3 = net.get('s3') 
    

    s0.cmd( 'sysctl net.ipv4.ip_forward=1' )
    s1.cmd( 'sysctl net.ipv4.ip_forward=1' )
    s2.cmd( 'sysctl net.ipv4.ip_forward=1' )
    s3.cmd( 'sysctl net.ipv4.ip_forward=1' )

    h1.setIP('192.168.2.1', 24, 'h1-eth0')
    s0.setIP('192.168.2.2', 24, 's0-eth0')
    s0.setIP('192.168.4.1', 24, 's0-eth1')
    s1.setIP('192.168.4.2', 24, 's1-eth0')
    s1.setIP("192.168.8.1", 24, "s1-eth1")
    h2.setIP("192.168.8.2", 24, "h2-eth0")
    h1.setIP("192.168.16.1", 24, "h1-eth1")
    s2.setIP("192.168.16.2", 24, "s2-eth0")
    s2.setIP("192.168.32.1", 24, "s2-eth1")
    s3.setIP("192.168.32.2", 24, "s3-eth0")
    s3.setIP("192.168.64.1", 24, "s3-eth1")
    h2.setIP("192.168.64.2", 24, "h2-eth1")

    h1.setMAC('00:00:00:00:01:00', 'h1-eth0')
    h1.setMAC('00:00:00:00:01:01', 'h1-eth1')
    h2.setMAC('00:00:00:00:02:00', 'h2-eth0')
    h2.setMAC('00:00:00:00:02:01', 'h2-eth1')
    s0.setMAC('AA:AA:AA:AA:00:00', 's0-eth0')
    s0.setMAC('AA:AA:AA:AA:00:01', 's0-eth1')
    s1.setMAC('AA:AA:AA:AA:01:00', 's1-eth0')
    s1.setMAC('AA:AA:AA:AA:01:01', 's1-eth1')
    s2.setMAC('AA:AA:AA:AA:02:00', 's2-eth0')
    s2.setMAC('AA:AA:AA:AA:02:01', 's2-eth1')
    s3.setMAC('AA:AA:AA:AA:03:00', 's3-eth0')
    s3.setMAC('AA:AA:AA:AA:03:01', 's3-eth1')


    h1.cmd('route add -net 192.168.2.0 netmask 255.255.255.0 gw 192.168.2.2 dev h1-eth0')
    h1.cmd('route add -net 192.168.4.0 netmask 255.255.255.0 gw 192.168.2.2 dev h1-eth0')
    h1.cmd('route add -net 192.168.8.0 netmask 255.255.255.0 gw 192.168.2.2 dev h1-eth0')
    s0.cmd('route add -net 192.168.2.0 netmask 255.255.255.0 gw 192.168.2.1 dev s0-eth0')
    s0.cmd('route add -net 192.168.4.0 netmask 255.255.255.0 gw 192.168.4.2 dev s0-eth1')
    s0.cmd('route add -net 192.168.8.0 netmask 255.255.255.0 gw 192.168.4.2 dev s0-eth1')
    s1.cmd('route add -net 192.168.2.0 netmask 255.255.255.0 gw 192.168.4.1 dev s1-eth0')
    s1.cmd('route add -net 192.168.4.0 netmask 255.255.255.0 gw 192.168.4.1 dev s1-eth0')
    s1.cmd('route add -net 192.168.8.0 netmask 255.255.255.0 gw 192.168.8.2 dev s1-eth1')
    h2.cmd('route add -net 192.168.2.0 netmask 255.255.255.0 gw 192.168.8.1 dev h2-eth0')
    h2.cmd('route add -net 192.168.4.0 netmask 255.255.255.0 gw 192.168.8.1 dev h2-eth0')
    h2.cmd('route add -net 192.168.8.0 netmask 255.255.255.0 gw 192.168.8.1 dev h2-eth0')
    h1.cmd('route add -net 192.168.16.0 netmask 255.255.255.0 gw 192.168.16.2 dev h1-eth1')
    h1.cmd('route add -net 192.168.32.0 netmask 255.255.255.0 gw 192.168.16.2 dev h1-eth1')
    h1.cmd('route add -net 192.168.64.0 netmask 255.255.255.0 gw 192.168.16.2 dev h1-eth1')
    s2.cmd('route add -net 192.168.16.0 netmask 255.255.255.0 gw 192.168.16.1 dev s2-eth0')
    s2.cmd('route add -net 192.168.32.0 netmask 255.255.255.0 gw 192.168.32.2 dev s2-eth1')
    s2.cmd('route add -net 192.168.64.0 netmask 255.255.255.0 gw 192.168.32.2 dev s2-eth1')
    s3.cmd('route add -net 192.168.16.0 netmask 255.255.255.0 gw 192.168.32.1 dev s3-eth0')
    s3.cmd('route add -net 192.168.32.0 netmask 255.255.255.0 gw 192.168.32.1 dev s3-eth0')
    s3.cmd('route add -net 192.168.64.0 netmask 255.255.255.0 gw 192.168.64.2 dev s3-eth1')
    h2.cmd('route add -net 192.168.16.0 netmask 255.255.255.0 gw 192.168.64.1 dev h2-eth1')
    h2.cmd('route add -net 192.168.32.0 netmask 255.255.255.0 gw 192.168.64.1 dev h2-eth1')
    h2.cmd('route add -net 192.168.64.0 netmask 255.255.255.0 gw 192.168.64.1 dev h2-eth1')

    net.staticArp()
 

   

configureRouting(net)
printConfiguration(net)
