# Network Diagnostics Tool

A multi-feature Python-based network diagnostics tool with a graphical user interface (GUI). This tool performs several network and system diagnostic tasks, including:

- **Network Speed Test:** Measures download/upload speeds and ping.
- **System Information:** Displays OS, CPU, and memory details.
- **Network Device Discovery:** Performs an ARP scan on your local network.
- **DNS Resolution:** Resolves a given domain name to its IP addresses.
- **Speed Test History:** Keeps a record of network speed test results.

## Features

- **Graphical User Interface:** Built with [tkinter](https://docs.python.org/3/library/tkinter.html).
- **Background Processing:** Uses threading to run diagnostic tasks without freezing the GUI.
- **Easy to Use:** Simple buttons to execute various diagnostic functions.
- **Real-Time Output:** Displays results and logs in a scrollable text area.

## Requirements

The following Python packages are required:

- Python 3.x
- [speedtest-cli](https://pypi.org/project/speedtest-cli/)
- [psutil](https://pypi.org/project/psutil/)
- [scapy](https://pypi.org/project/scapy/)
- [dnspython](https://pypi.org/project/dnspython/)
- [requests](https://pypi.org/project/requests/)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/network-diagnostics-tool.git
   cd network-diagnostics-tool
