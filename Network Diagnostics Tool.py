import threading
import time
import platform
import psutil
import requests
import speedtest
from scapy.all import ARP, Ether, srp
from dns import resolver
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

# Initialize an empty list to store speed test history
speed_test_history = []

# -------------------------------
# Core Diagnostic Functions
# -------------------------------
def test_network_speed(callback=None):
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        ping = st.results.ping

        # Inform the user about the ongoing test
        update_output("Testing download speed to the closest server...\n")
        download_speed = st.download() / 1_000_000  # Mbps
        update_output(f"Download Speed: {download_speed:.2f} Mbps\n")

        update_output("Testing upload speed to the closest server...\n")
        upload_speed = st.upload() / 1_000_000  # Mbps
        update_output(f"Upload Speed: {upload_speed:.2f} Mbps\n")

        geolocation = get_geolocation()
        update_output(f"Your geolocation: {geolocation}\n")

        test_result = {
            "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "Download Speed (Mbps)": download_speed,
            "Upload Speed (Mbps)": upload_speed,
            "Ping (ms)": ping,
            "Geolocation": geolocation
        }
        speed_test_history.append(test_result)

        check_network_speed(download_speed, upload_speed)
    except Exception as e:
        update_output(f"Error during network speed test: {e}\n")
    finally:
        if callback:
            callback()  # Re-enable buttons if needed

def check_network_speed(download_speed, upload_speed):
    if download_speed < 10.0 or upload_speed < 1.0:
        update_output("Your network speed is below recommended levels.\n")
        update_output("Recommendations:\n")
        update_output("- Consider upgrading your internet plan.\n")
        update_output("- Check for network congestion or interference.\n")
        update_output("- Ensure your router and modem are up to date.\n")
        update_output("- Contact your internet service provider for assistance.\n")
    elif download_speed < 50.0 or upload_speed < 5.0:
        update_output("Your network speed is acceptable, but there's room for improvement.\n")
        update_output("Recommendations:\n")
        update_output("- Consider upgrading to a higher-speed plan for better performance.\n")
        update_output("- Optimize your Wi-Fi network for better connectivity.\n")
    else:
        update_output("Your network speed is good. No further action is needed.\n")

def get_geolocation():
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()
        return data.get("loc", "N/A")
    except Exception as e:
        return f"Error: {e}"

def get_system_info():
    try:
        system = platform.system()
        release = platform.release()
        version = platform.version()
        cpu_info = f"CPU: {platform.processor()}"
        mem = psutil.virtual_memory()
        mem_info = f"Memory (RAM) Total: {mem.total / (1024 ** 3):.2f} GB, Available: {mem.available / (1024 ** 3):.2f} GB"
    
        output = (
            f"Operating System: {system} {release}\n"
            f"System Version: {version}\n"
            f"{cpu_info}\n"
            f"{mem_info}\n"
        )
        update_output(output)
    except Exception as e:
        update_output(f"Error getting system information: {e}\n")

def network_device_discovery():
    try:
        local_network = "192.168.1.0/24"  # Change if necessary
        arp = ARP(pdst=local_network)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp
        result = srp(packet, timeout=3, verbose=0)[0]
    
        update_output("Network Device Discovery:\n")
        for sent, received in result:
            update_output(f"IP: {received.psrc}, MAC: {received.hwsrc}\n")
    except Exception as e:
        update_output(f"Failed to discover devices: {e}\n")

def dns_resolution():
    host = simpledialog.askstring("DNS Resolution", "Enter a domain or IP address to resolve:")
    if not host:
        return
    try:
        answers = resolver.resolve(host, "A")
        update_output(f"DNS Resolution for {host}:\n")
        for rdata in answers:
            update_output(f"IP Address: {rdata.address}\n")
    except Exception as e:
        update_output(f"Failed to resolve {host}: {e}\n")

def display_speed_history():
    if not speed_test_history:
        update_output("No speed test history available.\n")
    else:
        update_output("Speed Test History:\n")
        for i, test in enumerate(speed_test_history, start=1):
            update_output(f"Test #{i}:\n")
            for key, value in test.items():
                update_output(f"  {key}: {value}\n")
            update_output("\n")

# -------------------------------
# Tkinter GUI Functions
# -------------------------------
def update_output(message):
    """Append text to the output text area."""
    output_text.configure(state='normal')
    output_text.insert(tk.END, message)
    output_text.see(tk.END)
    output_text.configure(state='disabled')

def run_in_thread(target_func):
    """Helper to run a function in a separate thread."""
    thread = threading.Thread(target=target_func)
    thread.daemon = True
    thread.start()

def disable_buttons():
    for btn in buttons:
        btn.config(state='disabled')

def enable_buttons():
    for btn in buttons:
        btn.config(state='normal')

def on_test_network_speed():
    disable_buttons()
    run_in_thread(lambda: test_network_speed(callback=enable_buttons))

def on_get_system_info():
    disable_buttons()
    run_in_thread(lambda: [get_system_info(), enable_buttons()])

def on_network_device_discovery():
    disable_buttons()
    run_in_thread(lambda: [network_device_discovery(), enable_buttons()])

def on_dns_resolution():
    disable_buttons()
    run_in_thread(lambda: [dns_resolution(), enable_buttons()])

def on_display_speed_history():
    disable_buttons()
    run_in_thread(lambda: [display_speed_history(), enable_buttons()])

# -------------------------------
# Main Tkinter Application Setup
# -------------------------------
root = tk.Tk()
root.title("Network Diagnostics Tool")
root.geometry("700x500")

# Create a frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Define buttons and assign commands
buttons = []
btn_test_speed = tk.Button(button_frame, text="Test Network Speed", width=20, command=on_test_network_speed)
btn_test_speed.grid(row=0, column=0, padx=5, pady=5)
buttons.append(btn_test_speed)

btn_system_info = tk.Button(button_frame, text="Get System Information", width=20, command=on_get_system_info)
btn_system_info.grid(row=0, column=1, padx=5, pady=5)
buttons.append(btn_system_info)

btn_device_discovery = tk.Button(button_frame, text="Network Device Discovery", width=20, command=on_network_device_discovery)
btn_device_discovery.grid(row=1, column=0, padx=5, pady=5)
buttons.append(btn_device_discovery)

btn_dns = tk.Button(button_frame, text="DNS Resolution", width=20, command=on_dns_resolution)
btn_dns.grid(row=1, column=1, padx=5, pady=5)
buttons.append(btn_dns)

btn_history = tk.Button(button_frame, text="Display Speed Test History", width=20, command=on_display_speed_history)
btn_history.grid(row=2, column=0, padx=5, pady=5)
buttons.append(btn_history)

btn_exit = tk.Button(button_frame, text="Exit", width=20, command=root.quit)
btn_exit.grid(row=2, column=1, padx=5, pady=5)
buttons.append(btn_exit)

# Create a scrolled text area for output
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', width=80, height=20)
output_text.pack(padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
