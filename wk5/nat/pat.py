from mininet.net import Mininet
from mininet.node import Node
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.node import OVSKernelSwitch

class StaticNATTopo(Topo):
    def build(self):
        # Switches
        s1 = self.addSwitch('s1')  # Internal
        s2 = self.addSwitch('s2')  # External

        # Hosts
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='192.168.0.2/24')

        # Router (NAT device)
        r1 = self.addHost('r1')  # No IPs yet

        # Links
        self.addLink(h1, s1)
        self.addLink(r1, s1)  # Internal interface
        self.addLink(r1, s2)  # External interface
        self.addLink(h2, s2)

def run():
    topo = StaticNATTopo()
    net = Mininet(topo=topo, link=TCLink, switch=OVSKernelSwitch)
    net.start()

    h1, h2, r1 = net.get('h1', 'h2', 'r1')

    # Assign IPs to router interfaces
    r1.cmd('ifconfig r1-eth0 10.0.0.254/24')     # Internal
    r1.cmd('ifconfig r1-eth1 192.168.0.100/24')  # External

    # Setup host default routes
    h1.cmd('ip route add default via 10.0.0.254')
    h2.cmd('ip route add default via 192.168.0.100')

    # Enable IP forwarding on router
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Set public IP on external interface
    r1.cmd('ifconfig r1-eth1 192.168.0.100/24')

    # PAT/NAT Overload using MASQUERADE
    r1.cmd('iptables -t nat -A POSTROUTING -o r1-eth1 -j MASQUERADE')

    # Allow forwarding between interfaces
    r1.cmd('iptables -A FORWARD -i r1-eth0 -o r1-eth1 -j ACCEPT')
    r1.cmd('iptables -A FORWARD -i r1-eth1 -o r1-eth0 -m state --state ESTABLISHED,RELATED -j ACCEPT')


    print("\nTest NAT: h1 should be able to ping h2")
    net.ping([h1, h2])

    CLI(net)
    net.stop()

    # we can test application communication with nc from xterm
    # xterm h1 h2

if __name__ == '__main__':
    from mininet.cli import CLI
    setLogLevel('info')
    run()
