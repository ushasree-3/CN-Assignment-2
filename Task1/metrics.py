import os
import subprocess
import csv

def extract_metrics(pcap_file):
    # Extract goodput (only considering TCP data packets, no retransmissions)
    cmd_goodput = f"tshark -r {pcap_file} -Y 'tcp.analysis.retransmission == 0 && tcp.analysis.duplicate_ack == 0' -T fields -e frame.len"
    result_goodput = subprocess.run(cmd_goodput, shell=True, capture_output=True, text=True)
    
    goodput_bytes = sum(int(pkt_len) for pkt_len in result_goodput.stdout.splitlines() if pkt_len.isdigit())

    # Extract total TCP packets
    cmd_total_tcp = f"tshark -r {pcap_file} -Y 'tcp' | wc -l"
    total_tcp_packets = int(subprocess.run(cmd_total_tcp, shell=True, capture_output=True, text=True).stdout.strip())

    # Extract lost packets using TCP retransmissions and duplicate ACKs
    cmd_lost = f"tshark -r {pcap_file} -Y 'tcp.analysis.retransmission || tcp.analysis.duplicate_ack' | wc -l"
    lost_packets = int(subprocess.run(cmd_lost, shell=True, capture_output=True, text=True).stdout.strip())

    # Compute packet loss rate
    packet_loss_rate = (lost_packets / total_tcp_packets) * 100 if total_tcp_packets > 0 else 0

    # Extract maximum window size using tshark
    cmd_window = f"tshark -r {pcap_file} -Y 'tcp' -T fields -e tcp.window_size_value"
    result_window = subprocess.run(cmd_window, shell=True, capture_output=True, text=True)
    
    max_window_size = max([int(size) for size in result_window.stdout.splitlines() if size.isdigit()], default=0)

    return goodput_bytes / 1e6, packet_loss_rate, max_window_size  # Convert goodput to Mbps

def process_and_store_metrics(directory, csv_file):
    os.makedirs("results", exist_ok=True)
    
    # Open CSV file to store results
    with open(csv_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Experiment", "Algorithm", "Goodput (Mbps)", "Packet Loss Rate (%)", "Max Window Size (Bytes)"])

        for file in os.listdir(directory):
            if file.endswith(".pcap"):
                file_path = os.path.join(directory, file)
                exp_name, algorithm = file.rsplit('_', 1)[0], file.rsplit('_', 1)[-1].replace('.pcap', '')

                goodput_mbps, packet_loss_rate, max_window_size = extract_metrics(file_path)
                
                # Write results to CSV
                writer.writerow([exp_name, algorithm, f"{goodput_mbps:.2f}", f"{packet_loss_rate:.2f}", max_window_size])

# Run script
pcap_directory = "/mnt/e/CN/Assg2/Mine/Task1/pcap_files"
csv_filename = "results/congestion_metrics.csv"

process_and_store_metrics(pcap_directory, csv_filename)
