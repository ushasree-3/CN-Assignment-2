from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from time import sleep

from custom_topology_c import CustomTopologyC

def run_experiment(loss):
    net = Mininet(topo=CustomTopologyC(loss=loss), switch=OVSSwitch, controller=None)
    net.start()

    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')
    h7 = net.get('h7')

    print(f"Starting iPerf3 server on H7 with S2-S3 loss={loss}%...")
    h7.cmd('iperf3 -s -D &')  # Start iPerf3 server in daemon mode
    sleep(2)

    congestion_algos = ['bbr', 'highspeed', 'yeah']
    conditions = {
        "2a": ["H1", "H2"],
        "2b": ["H1", "H3"],
        "2c": ["H1", "H3", "H4"]
    }

    for cc in congestion_algos:
        print(f"\nTesting congestion control: {cc} with S2-S3 loss={loss}%")
        for condition, clients in conditions.items():
            print(f"Running test: {', '.join(clients)} -> H7 with {cc}")

            for client in clients:
                host = net.get(client.lower())
                host.cmd(f'echo {cc} > /proc/sys/net/ipv4/tcp_congestion_control')

            h7.cmd(f'tcpdump -i any -w d_{condition}_{cc}_loss{loss}.pcap &')

            for client in clients:
                host = net.get(client.lower())
                host.cmd(f'iperf3 -c {h7.IP()} -p 5201 -b 10M -P 10 -t 150 &')

            sleep(20)
            h7.cmd('killall -9 tcpdump')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    for loss in [1, 5]:  # Run experiment with 1% and 5% loss
        run_experiment(loss)
