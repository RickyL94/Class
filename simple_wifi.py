#!/usr/bin/python

from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import Controller

def topology():
    "Create a simple Wi-Fi network"
    
    # 1. Initialize the network
    net = Mininet_wifi(controller=Controller)

    info("*** Creating nodes\n")
    # Add a generic controller
    c0 = net.addController('c0')
    
    # Add an Access Point (mode 'g' = 802.11g)
   # 'passwd' must be exactly 5 or 13 characters for WEP
    ap1 = net.addAccessPoint('ap1', ssid='myssid', mode='g', channel='1', 
                         encrypt='wep', passwd='12345', position='10,10,0')
    
    # Add a Station (Client)
    sta1 = net.addStation('sta1', position='10,20,0')

    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])

    info("*** Running CLI\n")
    # This gives you the 'mininet-wifi>' prompt to run commands manually
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
