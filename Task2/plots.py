import pandas as pd
import matplotlib.pyplot as plt

def plot_connection_duration(csv_filename, output_filename):
    # Load the CSV file
    data = pd.read_csv(csv_filename, delimiter="\t", names=["time", "src", "dst", "sport", "dport", "duration"])
    
    # Convert time and duration to float
    data["time"] = data["time"].astype(float)
    data["duration"] = data["duration"].astype(float)
    
    # Sort data by connection start time
    data = data.sort_values("time")
    
    # Plot connection duration vs. connection start time
    plt.figure(figsize=(10, 6))
    plt.scatter(data["time"], data["duration"], marker="o", label="Connections", color="b", alpha=0.5)
    
    # Add vertical lines to indicate attack start (20s) and end (120s)
    plt.axvline(x=data["time"].min() + 20, color="r", linestyle="--", label="Attack Start")
    plt.axvline(x=data["time"].min() + 120, color="g", linestyle="--", label="Attack End")
    
    plt.xlabel("Connection Start Time (Epoch Seconds)")
    plt.ylabel("Connection Duration (Seconds)")
    plt.title("Connection Duration vs. Connection Start Time")
    plt.legend()
    
    # Save the plot to a file
    plt.savefig(output_filename)
    plt.close()
    print(f"Plot saved as {output_filename}")


plot_connection_duration("extracted_connections.csv", "syn_flood_attack_plot.png")
plot_connection_duration("extracted_mitigated_connections.csv", "syn_flood_attack_mitigation_plot.png")
