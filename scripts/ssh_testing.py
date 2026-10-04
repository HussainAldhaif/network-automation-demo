import csv
import getpass
from concurrent.futures import ThreadPoolExecutor, as_completed
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

def test_ssh(ip: str, user: str, secret: str, timeout: int = 5) -> tuple[bool, str]:
    """Attempts an SSH connection to test credentials and reachability using Netmiko."""
    device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": user,
        "password": secret,
        "conn_timeout": timeout,
    }
    
    try:
        connection = ConnectHandler(**device)
        connection.disconnect()
        return True, "Connection successful"
    except NetmikoAuthenticationException:
        return False, "Authentication failed"
    except NetmikoTimeoutException:
        return False, "Device unreachable / connection timed out"
    except Exception as e:
        return False, f"Error: {e}"



def test_all_concurrent(devices: list[dict], user: str, secret: str, max_workers: int = 15):
    """Runs test_ssh across all devices concurrently."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Map each future task to device metadata so we can print its name/ip
        future_to_device = {}
        for dev in devices:
           task = executor.submit(test_ssh, dev["ip"], user, secret) 
           future_to_device[task] = dev

        for future in as_completed(future_to_device):
            dev = future_to_device[future]
            success, message = future.result()
            status = "[SUCCESS]" if success else "[FAILED] "
            print(f"{status} {dev['name']:<18} ({dev['ip']}) -> {message}")

def main():
    inventory_file = "devices.csv"

    # 1. Prompt interactively so credentials are never written to disk
    username = input("Enter SSH Username: ").strip()
    password = getpass.getpass("Enter SSH Password: ")

    if not username or not password:
        print("Error: Username and password cannot be empty.")
        return

    # 2. Read inventory into a list
    print(f"\n--- Reading targets from {inventory_file} ---")
    try:
        with open(inventory_file, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            devices = []
            for row in reader:
                cleaned_ip = row.get("ip", "").strip()
                cleaned_name = row.get("name", "").strip() or "Unknown"
                if cleaned_ip:
                    devices.append({
                        "name": cleaned_name,
                        "ip": cleaned_ip,    
        })
                           
    except FileNotFoundError:
        print(f"Error: Could not find inventory file '{inventory_file}'.")
        return

    # 3. Run concurrent execution
    test_all_concurrent(devices, username, password, max_workers=15)

if __name__ == "__main__":
    main()