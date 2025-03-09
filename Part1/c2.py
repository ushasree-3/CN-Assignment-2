from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from time import sleep

from custom_topology_c import CustomTopologyC

def run_experiment():
    net = Mininet(topo=CustomTopologyC(), switch=OVSSwitch, controller=None)
    net.start()

    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')
    h7 = net.get('h7')

    print("Starting iPerf3 server on H7...")
    h7.cmd('iperf3 -s -D &')  # Start iPerf3 server in daemon mode
    sleep(2)

    congestion_algos = ['bbr', 'highspeed', 'yeah']

    # Define conditions with respective clients
    conditions = {
        "2a": ["H1", "H2"],
        "2b": ["H1", "H3"],
        "2c": ["H1", "H3", "H4"]
    }

    # Run experiments for each congestion control algorithm
    for cc in congestion_algos:
        print(f"\nTesting congestion control: {cc}")
        for condition, clients in conditions.items():
            print(f"Running test: {', '.join(clients)} -> H7 with {cc}")

            # Set congestion control algorithm for each client
            for client in clients:
                host = net.get(client.lower())
                host.cmd(f'echo {cc} > /proc/sys/net/ipv4/tcp_congestion_control')

            # Start packet capture for this condition
            h7.cmd(f'tcpdump -i any -w condition{condition}_{cc}.pcap &')

            # Start iPerf3 clients
            for client in clients:
                host = net.get(client.lower())
                host.cmd(f'iperf3 -c {h7.IP()} -p 5201 -b 10M -P 10 -t 150 &')

            sleep(20)  # Allow time for the test to complete
            h7.cmd('killall -9 tcpdump')  # Stop packet capture

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run_experiment()
