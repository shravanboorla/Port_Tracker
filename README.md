This project is a custom TCP-based port scanner developed using Python socket programming.
It scans a target host for open ports and identifies active network services using TCP connect scanning. The project demonstrates practical understanding of:
TCP handshake mechanism
Socket programming
Network service detection
Multi-threaded scanning
Timeout handling
This tool was built for educational and lab purposes to understand how port scanning works internally.

Features:
TCP Connect Scan implementation
Multi-threaded port scanning for improved performance
Open port detection
Timeout handling for faster scans
Optional banner grabbing (if implemented)
Result validation using Nmap

Tech Stack:
Python 3
Socket Programming
Threading
TCP/IP Networking

How It Works:
User inputs:
Target IP / domain
Port range

For each port:
A TCP socket connection attempt is made.
If connection succeeds → Port is marked OPEN.
If connection fails → Port is CLOSED.

Multi-threading is used to:
Scan multiple ports simultaneously
Reduce overall scanning time
Results are displayed in structured format.

How to Run:
python scanner.py
Then enter:
Target IP address
Starting port
Ending port

Example:
Target: 192.168.1.1
Start Port: 1
End Port: 1000

Sample Output:
Scanning 192.168.1.1...
Port 22 → OPEN
Port 80 → OPEN
Port 443 → OPEN

Validation:
Scan results were verified using:
nmap <target-ip>
Comparison confirmed accuracy of open port detection.




## Changelog

**v2** — Refactored for reliability and correctness:
- Fixed a threading bug where `join()` only waited on the last-created thread instead of all threads, so the scan could report completion before every port had actually been checked
- Replaced raw thread-per-port with a bounded `ThreadPoolExecutor` to avoid spawning thousands of unmanaged threads on large port ranges
- Added hostname resolution with proper error handling instead of crashing on bad input
- Added a CLI (`argparse`) so the tool runs like `python3 port_scanner.py <host> -p 1-1000`



Usage:python3 port_scanner.py scanme.nmap.org -p 1-1000 -t 100
