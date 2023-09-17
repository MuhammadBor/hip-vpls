#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, OVSController, OVSKernelSwitch, OVSSwitch
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):
    def build( self, **_opts ):
        router1 = self.addNode( 'r1', cls=LinuxRouter )
        router2 = self.addNode( 'r2', cls=LinuxRouter )
        router3 = self.addNode( 'r3', cls=LinuxRouter )
        router4 = self.addNode( 'r4', cls=LinuxRouter )
        s1, s2, s3, s4, s5 = [ self.addSwitch( s, cls=OVSKernelSwitch ) for s in ( 's1', 's2', 's3', 's4', 's5' ) ]
        self.addLink( s5, router1,
                intfName2='r1-eth1',
                params2={ 'ip' : '192.168.3.1/29' } )
        self.addLink( s5, router2,
                intfName2='r2-eth1',
                params2={ 'ip' : '192.168.3.2/29' } )
        self.addLink( s5, router3,
                intfName2='r3-eth1',
                params2={ 'ip' : '192.168.3.3/29' } )
        self.addLink( s5, router4,
                intfName2='r4-eth1',
                params2={ 'ip' : '192.168.3.3/29' } )
        self.addLink( s1, router1, intfName2='r1-eth0',
                      params2={ 'ip' : '192.168.1.1/24' } )
        self.addLink( s2, router2, intfName2='r2-eth0',
                params2={ 'ip' : '192.168.1.2/24' } )
        self.addLink( s3, router3, intfName2='r3-eth0',
                params2={ 'ip' : '192.168.1.3/24' } )
        self.addLink( s4, router4, intfName2='r4-eth0',
                params2={ 'ip' : '192.168.1.4/24' } )
        h1 = self.addHost( 'h1', ip='192.168.1.100/24',
                           defaultRoute='via 192.168.1.1' )
        h2 = self.addHost( 'h2', ip='192.168.1.101/24',
                           defaultRoute='via 192.168.1.1' )
        h3 = self.addHost( 'h3', ip='192.168.1.102/24',
                           defaultRoute='via 192.168.1.1' )
        h4 = self.addHost( 'h4', ip='192.168.1.103/24',
                           defaultRoute='via 192.168.1.1' )
        for h, s in [ (h1, s1), (h2, s2), (h3, s3), (h4, s4) ]:
            self.addLink( h, s )
from time import sleep
def run(switch, tx, rx, sg):
    topo = NetworkTopo()
    net = Mininet(topo=topo, switch=switch, controller = OVSController)
    net.start()


    info( net[ 'r1' ].cmd( '/sbin/ethtool -K r1-eth0 rx off tx off sg off' ) )
    r1, r2, r3, r4 = net[ 'r1' ], net[ 'r2' ], net[ 'r3' ], net[ 'r4' ]
    h1, h2, h3, h4 = net[ 'h1' ], net[ 'h2' ], net[ 'h3' ], net[ 'h4' ]
    print("#######################")
    info( r1.cmd( 'ifconfig r1-eth1 192.168.3.1 netmask 255.255.255.248' ) )
    info( r2.cmd( 'ifconfig r2-eth1 192.168.3.2 netmask 255.255.255.248' ) )
    info( r3.cmd( 'ifconfig r3-eth1 192.168.3.3 netmask 255.255.255.248' ) )
    info( r4.cmd( 'ifconfig r4-eth1 192.168.3.4 netmask 255.255.255.248' ) )
    print("##########Start_ Router _Change ###############")
    for r in r1, r2, r3, r4:
        print("The below line prints the data for intf attribute")
        info( r.cmd(f'/sbin/ethtool -K {r}-eth0 rx {rx} tx {tx} sg {sg}' ) )
        info( r.cmd(f'/sbin/ethtool -K {r}-eth1 rx {rx} tx {tx} sg {sg}' ) )
    print("##########End_ Router _Change ###############")
    print("##########Start_ Host _Change ###############")
    for h in h1, h2, h3, h4:
        info( h.cmd( f'/sbin/ethtool -K {h}-eth0 rx {rx} tx {tx} sg {sg}' ) )
        info( h.cmd( f'ifconfig {h}-eth0 mtu 1400' ) )
    info( '*** Routing Table on Router:\n' )
    info( r1.cmd( 'route' ) )
    info( '*** Routing Table on Router:\n' )
    info( r2.cmd( 'route' ) )
    info( '*** Running HIPLS on router 1 *** \n')
    info( r1.cmd( 'cd router1 && python3 switchd.py &' ) )
    info( '*** Running HIPLS on router 2 *** \n')
    info( r2.cmd( 'cd router2 && python3 switchd.py &' ) )
    info( '*** Running HIPLS on router 3 *** \n')
    info( r3.cmd( 'cd router3 && python3 switchd.py &' ) )
    info( '*** Running HIPLS on router 4 *** \n')
    info( r4.cmd( 'cd router4 && python3 switchd.py &' ) )
    info(h1.cmd(f'ping -c20 192.168.1.101'))
    print(f"Result for tx:{tx}, and rx:{rx}, and sg:{sg}")
    info(h2.cmd(f'iperf -s >> server_output.txt &'))
    info(h1.cmd(f'echo tx={tx}, rx={rx}, sg={sg}  >>  client_output.txt'))
    info(h1.cmd(f'iperf -t20 -c 192.168.1.101  >>  client_output.txt'))
    info(h1.cmd(f'echo +++++++++++++++++++++++++>>  client_output.txt'))

    #CLI( net )
    net.stop()

setLogLevel( 'info' )
# Run HIPLS Test
results = []
for switch in OVSSwitch, OVSKernelSwitch:
    for tx in 'on','off':
        for rx in 'on','off':
            for sg in 'on','off':
                print('*** Testing', switch.__name__, 'tx:', tx, 'rx:', rx)
                result = run( switch, tx, rx, sg )
                #results.append( ( switch.__name__, tx, rx, result ) )


# print("Final REsult")
# print(results)

