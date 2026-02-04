from mininet.log import setLogLevel
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import OVSKernelAP
from mn_wifi.cli import CLI

def run():
    ssid = input("Enter SSID: ")

    proto = input("Protocol (open/wep/wpa/wpa2): ").lower()

    passwd = None
    encrypt = None

    if proto == "wep":
        encrypt = 'wep'
        passwd = input("Enter WEP key (10 or 26 hex chars): ")
    elif proto == "wpa":
        encrypt = 'wpa'
        passwd = input("Enter WPA passphrase: ")
    elif proto == "wpa2":
        encrypt = 'wpa2'
        passwd = input("Enter WPA2 passphrase: ")
    else:
        encrypt = None

    net = Mininet_wifi(accessPoint=OVSKernelAP)

    sta1 = net.addStation('sta1', position='10,10,0')
    ap1 = net.addAccessPoint(
        'ap1',
        ssid=ssid,
        mode='g',
        channel='6',
        encrypt=encrypt,
        passwd=passwd,
        position='15,15,0'
    )

    net.configureWifiNodes()
    net.build()
    ap1.start([])

    print("\n📡 Virtual Wi‑Fi network running")
    print("📁 PCAPs will be saved per interface\n")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
