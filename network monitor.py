import subprocess
import platform
import time
import csv
import os
from datetime import datetime

# Devices to monitor
DEVICES = {
    "Gateway": "10.17.53.1",
    "Google DNS": "8.8.8.8",
    "Cloudflare DNS": "1.1.1.1"
}

# Log file
LOG_FILE = "network_status.csv"


def ping_device(ip):
    """Ping a device and return its status and response time."""

    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", "1", "-w", "1000", ip]
    else:
        command = ["ping", "-c", "1", "-W", "1", ip]

    start_time = time.time()

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        response_time = round(
            (time.time() - start_time) * 1000, 2
        )

        if result.returncode == 0:
            return "Online", response_time
        else:
            return "Offline", None

    except Exception as error:
        print(f"Error checking {ip}: {error}")
        return "Error", None


def create_log_file():
    """Create the CSV log file with column headings if it doesn't exist."""

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Date",
                "Time",
                "Device",
                "IP Address",
                "Status",
                "Response Time (ms)"
            ])


def log_result(device, ip, status, response_time):
    """Save monitoring results to the CSV log file."""

    now = datetime.now()

    with open(LOG_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            device,
            ip,
            status,
            response_time if response_time else "N/A"
        ])


def monitor_network():
    """Check all configured devices."""

    print("\n" + "=" * 70)
    print("                 NETWORK MONITORING TOOL")
    print("=" * 70)

    for device, ip in DEVICES.items():

        status, response_time = ping_device(ip)

        if response_time:
            print(
                f"{device:<20} "
                f"{ip:<16} "
                f"{status:<10} "
                f"{response_time} ms"
            )
        else:
            print(
                f"{device:<20} "
                f"{ip:<16} "
                f"{status:<10} "
                f"N/A"
            )

        # Save result
        log_result(
            device,
            ip,
            status,
            response_time
        )

    print("\nMonitoring results saved to:")
    print(LOG_FILE)


# Start the program
if __name__ == "__main__":

    create_log_file()

    monitor_network()