from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from time import sleep

from custom_topology import CustomTopology

def run_multi_client_experiment():
    net = Mininet(topo=CustomTopology(), switch=OVSSwitch, controller=None)
    net.start()

    h1, h3, h4 = net.get('h1'), net.get('h3'), net.get('h4')  # Clients
    h7 = net.get('h7')  # Server

    print("Starting iPerf3 server on H7...")
    h7.cmd('iperf3 -s -D')
    sleep(2)  # Wait for server to initialize

    congestion_algorithms = ["bbr", "highspeed", "yeah"]

    for cc in congestion_algorithms:
        print(f"\nRunning test with congestion control: {cc}")

        # Set TCP congestion control individually per host
        for host in [h1, h3, h4]:
            host.cmd(f'echo {cc} > /proc/sys/net/ipv4/tcp_congestion_control')

        # Start tcpdump on the server to capture traffic
        h7.cmd(f'tcpdump -i any port 5201 -w b_{cc}.pcap &')
        sleep(2)  # Allow tcpdump to initialize

        # Start staggered clients
        print("Starting H1 at T=0s")
        h1.cmd(f'iperf3 -c {h7.IP()} -p 5201 -b 10M -P 10 -t 150 -C {cc} &')
        sleep(15)

        print("Starting H3 at T=15s")
        h3.cmd(f'iperf3 -c {h7.IP()} -p 5201 -b 10M -P 10 -t 120 -C {cc} &')
        sleep(15)

        print("Starting H4 at T=30s")
        h4.cmd(f'iperf3 -c {h7.IP()} -p 5201 -b 10M -P 10 -t 90 -C {cc} &')
        sleep(100)  # Wait for transfers to finish

        # Stop tcpdump and ensure PCAP is saved
        h7.cmd('killall -9 tcpdump')
        print(f"Test completed for {cc}. PCAP saved as b_{cc}.pcap")

        # Stop any running iPerf3 processes
        h7.cmd('killall -9 iperf3')

    print("\nExperiments completed. Check PCAP files.")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run_multi_client_experiment()
