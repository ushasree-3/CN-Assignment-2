from mininet.net import Mininet
from mininet.cli import CLI
from topology2 import Topology
import time

def run_experiment():
    net = Mininet(topo=Topology())
    net.start()

    server = net.get('h7')
    client = net.get('h3')  # Changed client to h3

    # Start TCP server in the background
    server.cmd('iperf3 -s &')

    # Congestion control schemes
    cc = ["bbr", "highspeed", "yeah"]

    for scheme in cc:
        print(f"Running experiment with {scheme} congestion control...")

        # Save PCAP in the same directory as the script
        pcap_file = f"$(pwd)/outputs/c_{scheme}.pcap"
        tcpdump_pid = server.cmd(f'tcpdump -i h7-eth0 -w {pcap_file} & echo $!').strip()
        time.sleep(2)  # Allow tcpdump to initialize

        # Start iperf3 client in the background
        client.cmd(f'iperf3 -c {server.IP()} -p 5201 -b 10M -P 10 -t 150 -C {scheme} &')
        time.sleep(155)  # Wait for iperf3 to complete

        # Stop tcpdump after test
        server.cmd(f'kill {tcpdump_pid}')
        time.sleep(5)  # Ensure all packets are written to PCAP

        print(f"PCAP file saved at: outputs/c_{scheme}.pcap")

    print("Experiment complete.")
    net.stop()  # Stop Mininet

if __name__ == '__main__':
    run_experiment()
