"""
Multithreaded TCP Port Scanner
-------------------------------
Only scan hosts you own or are explicitly authorized to test
(e.g. scanme.nmap.org, or your own LAN devices / localhost).
"""

import socket
import threading
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed


def resolve_host(host: str) -> str:
    """Resolve hostname to an IP once, fail fast with a clear message."""
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        print(f"[!] Could not resolve host: {host}")
        sys.exit(1)


def scan_port(ip: str, port: int, timeout: float = 1.0) -> bool:
    """Return True if the port is open, False otherwise."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        return s.connect_ex((ip, port)) == 0


def scan_range(host: str, start_port: int, end_port: int,
                max_threads: int = 100, timeout: float = 1.0) -> list[int]:
    """
    Scan [start_port, end_port] (inclusive) on `host`.
    Returns a sorted list of open ports.
    """
    ip = resolve_host(host)
    ports = range(start_port, end_port + 1)
    total = len(ports)
    open_ports = []
    lock = threading.Lock()
    completed = 0

    print(f"[*] Scanning {host} ({ip}) — ports {start_port}-{end_port} "
          f"with {max_threads} threads\n")

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_port = {
            executor.submit(scan_port, ip, port, timeout): port
            for port in ports
        }

        for future in as_completed(future_to_port):
            port = future_to_port[future]
            with lock:
                completed += 1
                if completed % 50 == 0 or completed == total:
                    print(f"[*] Progress: {completed}/{total} ports checked",
                          end="\r")
            try:
                if future.result():
                    open_ports.append(port)
            except OSError as e:
                print(f"\n[!] Error scanning port {port}: {e}")

    print()
    return sorted(open_ports)


def main():
    parser = argparse.ArgumentParser(description="Multithreaded TCP port scanner")
    parser.add_argument("host", help="Target hostname or IP (must be authorized)")
    parser.add_argument("-p", "--ports", default="1-1024",
                         help="Port range, e.g. 1-1024 or a single port like 443")
    parser.add_argument("-t", "--threads", type=int, default=100,
                         help="Max concurrent threads (default: 100)")
    parser.add_argument("--timeout", type=float, default=1.0,
                         help="Per-connection timeout in seconds (default: 1.0)")
    args = parser.parse_args()

    if "-" in args.ports:
        start_str, end_str = args.ports.split("-", 1)
        start_port, end_port = int(start_str), int(end_str)
    else:
        start_port = end_port = int(args.ports)

    open_ports = scan_range(args.host, start_port, end_port,
                             max_threads=args.threads, timeout=args.timeout)

    if open_ports:
        print(f"[+] Open ports on {args.host}:")
        for port in open_ports:
            print(f"    {port}/tcp open")
    else:
        print(f"[-] No open ports found in range {start_port}-{end_port}")


if __name__ == "__main__":
    main()
