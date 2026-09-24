#!/usr/bin/env python3
"""
Port Status Checker
Defensive network socket utility for checking TCP port status on a host.
Use only on systems you own or are authorized to assess.
"""

import argparse
import socket
import sys
from datetime import datetime

DEFAULT_TIMEOUT = 0.5
MAX_PORT = 65535

# Common connection error codes:
# Windows: 10061 = WSAECONNREFUSED, 10060 = WSAETIMEDOUT
# Linux:   111   = ECONNREFUSED
# macOS:   61    = ECONNREFUSED


def check_port(target: str, port: int, timeout: float):
    """Return OPEN, CLOSED, or FILTERED based on a TCP connection attempt."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        result = sock.connect_ex((target, port))

        if result == 0:
            return "OPEN"

        # Connection refused means the host responded but no service
        # accepted the connection on this TCP port.
        if result in (10061, 111, 61):
            return "CLOSED"

        # Windows timeout / common timeout indication.
        if result == 10060:
            return "FILTERED"

        # Other non-zero results are treated conservatively as filtered.
        return "FILTERED"

    except socket.timeout:
        return "FILTERED"

    except OSError:
        return "FILTERED"

    finally:
        sock.close()


def parse_port_range(value: str):
    """Parse '80' or '20-100' and validate the range."""
    try:
        if "-" in value:
            start_text, end_text = value.split("-", 1)
            start, end = int(start_text), int(end_text)
        else:
            start = end = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Port range must look like 80 or 20-100."
        )

    if not (1 <= start <= MAX_PORT and 1 <= end <= MAX_PORT):
        raise argparse.ArgumentTypeError(
            "Ports must be between 1 and 65535."
        )

    if start > end:
        raise argparse.ArgumentTypeError(
            "Start port cannot be greater than end port."
        )

    return start, end


def main():
    parser = argparse.ArgumentParser(
        description="Check TCP port status on an authorized target host."
    )

    parser.add_argument(
        "target",
        help="Hostname or IPv4 address, e.g. 127.0.0.1"
    )

    parser.add_argument(
        "ports",
        help="Port or range, e.g. 80 or 20-100"
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"TCP connection timeout in seconds (default: {DEFAULT_TIMEOUT})"
    )

    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("Timeout must be greater than 0.")

    # Check whether the target hostname can be resolved.
    try:
        socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"Error: Could not resolve target host '{args.target}'.")
        sys.exit(1)

    start, end = parse_port_range(args.ports)
    total = end - start + 1

    print("=" * 66)
    print("PORT STATUS CHECKER")
    print("=" * 66)
    print("Authorized defensive network audit utility")
    print(f"Target : {args.target}")
    print(f"Range  : {start}-{end}")
    print(f"Timeout: {args.timeout:.2f}s")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 66)
    print(f"{'PORT':<8}{'STATUS':<14}{'SERVICE':<20}{'DETAIL'}")
    print("-" * 66)

    open_count = 0
    closed_count = 0
    filtered_count = 0

    for port in range(start, end + 1):
        status = check_port(args.target, port, args.timeout)

        try:
            service = socket.getservbyport(port, "tcp")
        except OSError:
            service = "unknown"

        detail = {
            "OPEN": "TCP connection accepted",
            "CLOSED": "Connection refused",
            "FILTERED": "No response / blocked / timeout",
        }[status]

        print(
            f"{port:<8}{status:<14}{service:<20}{detail}"
        )

        if status == "OPEN":
            open_count += 1
        elif status == "CLOSED":
            closed_count += 1
        else:
            filtered_count += 1

    print("-" * 66)
    print(
        f"Summary: OPEN={open_count}  "
        f"CLOSED={closed_count}  "
        f"FILTERED={filtered_count}"
    )
    print(f"Checked {total} TCP port(s).")
    print("=" * 66)


if __name__ == "__main__":
    main()
