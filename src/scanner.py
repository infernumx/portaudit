import re
import socket
from src.console import console
from typing import List, Union
from dataclasses import dataclass


@dataclass
class Port:
    port: int
    is_open: bool = False


class PortScanner:
    def __init__(self, ip: str, timeout: int):
        self.ip: str = ip
        self.timeout: int = timeout
        self.ports: List[Port] = []

        self.load_ports()

    def load_ports(self) -> None:
        with open("data/ports.csv") as f:
            content = f.read()
            for port in content.split(","):
                if port_range := re.search(r"(\d+)-(\d+)", port):
                    for _port in range(*map(int, port_range.groups())):
                        self.ports.append(Port(_port))
                else:
                    self.ports.append(Port(int(port)))

    def scan_port(self, port: Port) -> None:
        console.print(f"[#ff57c7]Scanning port {port.port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(self.timeout)
            if sock.connect_ex((self.ip, port.port)) == 0:
                port.is_open = True
                console.print("[green]Open")

    def show_open_ports(self) -> None:
        for port in self.ports:
            if port.is_open:
                console.print(f"[green]{port.port}")
