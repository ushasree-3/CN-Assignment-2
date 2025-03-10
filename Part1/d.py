from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from time import sleep
from mininet.link import TCLink

from custom_topology_c import CustomTopologyC  # Import topology

def run_experiment(loss):
    net = Mininet(topo=CustomTopologyC(loss=loss), switch=OVSSwitch, link=TCLink, controller=None)
    net.start()

    h3 = net.get('h3')
    h7 = net.get('h7')  # Server

    print("Starting iPerf3 server on H7...")
    h7.cmd('iperf3 -s -D &')

    sleep(2)
    congestion_algorithms = ["bbr", "highspeed", "yeah"]
    for cc in congestion_algorithms:
        print(f"\nTesting with TCP congestion control: {cc} and loss={loss}%")

        # === Condition 1: H3 (Client) -> H7 (Server) ===
        h3.cmd(f'echo {cc} > /proc/sys/net/ipv4/tcp_congestion_control')
        
        # Start tcpdump for packet capture
        h7.cmd(f'tcpdump -i any -w d1_{cc}_loss{loss}.pcap &')
        sleep(2)  # Allow tcpdump to initialize

        print("Running test: H3 -> H7")
        h3.cmd(f'iperf3 -c {h7.IP()} -p 5201 -b 10M -P 10 -t 150 -C {cc} &')

        sleep(20)

        # Stop tcpdump and save PCAP file
        h7.cmd('killall -9 tcpdump')
        print(f"Test completed for {cc} with loss={loss}%. PCAP saved as d1_{cc}_loss{loss}.pcap")

        # Ensure no lingering iPerf3 processes
        h7.cmd('killall -9 iperf3')

    print("Test completed.")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    for loss in [1, 5]:  # Run for both 1% and 5% loss
        print(f"\nRunning experiment with link loss {loss}% on S2-S3...")
        run_experiment(loss)
