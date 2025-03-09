from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from time import sleep

from custom_topology import CustomTopology

def run_single_client_experiment():
    net = Mininet(topo=CustomTopology(), switch=OVSSwitch, controller=None)
    net.start()

    h1 = net.get('h1')  # Client
    h7 = net.get('h7')  # Server

    print("Starting iPerf3 server on H7...")
    h7.cmd('iperf3 -s -D')  # Run as a daemon
    sleep(2)

    congestion_algorithms = ["bbr", "highspeed", "yeah"]

    for cc in congestion_algorithms:
        print(f"\nRunning test with congestion control: {cc}")

        # Set TCP congestion control
        h1.cmd(f'echo {cc} > /proc/sys/net/ipv4/tcp_congestion_control')

        # Start tcpdump to capture packets (non-blocking background process)
        h7.cmd(f'tcpdump -i any port 5201 -w a_{cc}.pcap &')
        sleep(1)  # Ensure tcpdump starts properly

        # Run iperf3 client on H1
        h1.cmd(f'iperf3 -c {h7.IP()} -p 5201 -b 10M -P 10 -t 60 -C {cc}')
        sleep(5)  # Give time for data transfer to settle

        # Stop tcpdump
        h7.cmd('killall -9 tcpdump')
        print(f"Test completed for {cc}. PCAP saved as a_{cc}.pcap")

        # Kill previous iperf3 process (if any)
        h7.cmd('killall -9 iperf3')

    print("\nExperiments completed. Check output files.")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run_single_client_experiment()
