from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink

class CustomTopologyC(Topo):
    def build(self):
        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')

        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # Define links with bandwidth constraints
        self.addLink(s1, s2, bw=100, max_queue_size=50, use_htb=True, r2q=10)
        self.addLink(s2, s3, bw=50, max_queue_size=25, use_htb=True, r2q=5)
        self.addLink(s3, s4, bw=100, max_queue_size=50, use_htb=True, r2q=10)
        self.addLink(s2, s4, bw=100, max_queue_size=50, use_htb=True, r2q=10)

        # Hosts to switches
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s3)
        self.addLink(h5, s3)
        self.addLink(h6, s4)
        self.addLink(h7, s4)

if __name__ == '__main__':
    topo = CustomTopologyC()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    CLI(net)  # Start CLI for testing
    net.stop()
