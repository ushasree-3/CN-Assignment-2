from mininet.net import Mininet
from mininet.cli import CLI
from topology import Topology
import time

def run_experiment():
    net = Mininet(topo=Topology())
    net.start()

    server = net.get('h7')
    client1 = net.get('h1')
    client2 = net.get('h3')
    client3 = net.get('h4')

    # Start TCP server in the background
    server.cmd('iperf3 -s &')

    # Congestion control schemes
    cc = ["bbr","highspeed","yeah"]

    for scheme in cc:
        print(f"Running experiment with {scheme} congestion control...")

        # Save PCAP in the same directory as the script
        pcap_file = f"$(pwd)/outputs/b_{scheme}.pcap"  # Uses current working directory
        server.cmd(f'tcpdump -i h7-eth0 -w {pcap_file} &')
        time.sleep(2)  # Allow tcpdump to initialize

        # Start iperf3 clients in a staggered manner
        client1.cmd(f'iperf3 -c {server.IP()} -p 5201 -b 10M -P 10 -t 150 -C {scheme} &')
        time.sleep(15)  # Wait 15s before starting next client

        client2.cmd(f'iperf3 -c {server.IP()} -p 5201 -b 10M -P 10 -t 120 -C {scheme} &')
        time.sleep(15)  # Wait 15s before starting next client

        client3.cmd(f'iperf3 -c {server.IP()} -p 5201 -b 10M -P 10 -t 90 -C {scheme} &')

        # Wait for all clients to complete
        time.sleep(160)  # Max duration (H1 runs for 150s)

        # Stop tcpdump after test
        server.cmd('pkill -f tcpdump')
        time.sleep(5)  # Ensure all packets are written to PCAP

        print(f"PCAP file saved at: {scheme}.pcap")

    print("Experiment complete.")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    run_experiment()
