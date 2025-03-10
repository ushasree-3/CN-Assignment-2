from mininet.net import Mininet
from topology3 import Topology
import time

def run_test(test_name, clients, cc=["bbr", "highspeed","yeah"]):
	"""Runs an experiment with given clients and congestion control scheme."""
	net = Mininet(topo=Topology())
	net.start()

	server = net.get('h7')
    
	for scheme in cc:
    	print(f"Running {test_name} with {scheme} congestion control...")
   	 
    	# Start server
    	server.cmd('iperf3 -s &')
    	time.sleep(2)

    	# Start packet capture
    	pcap_file = f"$(pwd)/outputs/{test_name}_{scheme}.pcap"
    	tcpdump_pid = server.cmd(f'tcpdump -i h7-eth0 -w {pcap_file} & echo $!').strip()
    	time.sleep(2)

    	# Start clients
    	for client_name in clients:
        	client = net.get(client_name)
        	client.cmd(f'iperf3 -c {server.IP()} -p 5201 -b 10M -P 10 -t 150 -C {scheme} &')

    	time.sleep(155)

    	# Stop packet capture
    	server.cmd(f'kill {tcpdump_pid}')
    	server.cmd('pkill iperf3')  # Ensure iperf3 is fully terminated
    	print(f"PCAP file saved: outputs/{test_name}_{scheme}.pcap")

	net.stop()

if __name__ == '__main__':
	test_cases = {
    	"c_2a": ["h1", "h2"],
    	"c_2b": ["h1", "h3"],
    	"c_2c": ["h1", "h3", "h4"]
	}
    
	for test_name, clients in test_cases.items():
    	run_test(test_name, clients)
    	time.sleep(5)  # Short break between tests to clear packets

