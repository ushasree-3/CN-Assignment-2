from mininet.net import Mininet
from mininet.cli import CLI
from topology3 import Topology
import time

def run_test_c():
    net = Mininet(topo=Topology())
    net.start()

    server = net.get('h7')
    clients = ["h1", "h3", "h4"]  # Test case (c)
    cc = ["bbr"]  

    server.cmd('iperf3 -s &')
    time.sleep(2)

    for scheme in cc:
        print(f"Running experiment with {scheme} congestion control...")
        pcap_file = f"$(pwd)/outputs/c_2c_{scheme}.pcap"
        tcpdump_pid = server.cmd(f'tcpdump -i h7-eth0 -w {pcap_file} & echo $!').strip()
        time.sleep(2)

        for client_name in clients:
            client = net.get(client_name)
            client.cmd(f'iperf3 -c {server.IP()} -p 5201 -b 10M -P 10 -t 150 -C {scheme} &')

        time.sleep(155)
        server.cmd(f'kill {tcpdump_pid}')
        print(f"PCAP file saved: outputs/c_2c_{scheme}.pcap")

    print("Experiment complete.")
    net.stop()

if __name__ == '__main__':
    run_test_c()
