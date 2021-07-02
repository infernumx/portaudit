#!/usr/bin/env python3

from src.scanner import PortScanner
from src.console import console
from rich.prompt import Prompt
import sys
from typing import Optional, Callable, Any
from threading import Thread
from datetime import datetime


def finish(scanner: PortScanner) -> None:
    choice = Prompt.ask("Select option", choices=["dump", "print"], default="print")
    if choice == "dump":
        time = datetime.strftime(datetime.now(), "%H%M%S")
        with open(f"portaudit-{time}.txt", "w+") as f:
            for port in scanner.ports:
                if port.is_open:
                    f.write(f"{port.port}\n")
    elif choice == "print":
        scanner.show_open_ports()


def main(ip: str, timeout: Optional[int] = 1) -> None:
    try:
        scanner = PortScanner(ip, timeout)
        threads = []

        for port in scanner.ports:
            thread = Thread(target=scanner.scan_port, args=(port,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        finish(scanner)
    except KeyboardInterrupt:
        finish(scanner)


def argv_getter(idx, converter: Optional[Callable] = None) -> Any:
    try:
        if converter:
            return converter(sys.argv[idx])
        return sys.argv[idx]
    except Exception:
        return None


if __name__ == "__main__":
    if len(sys.argv) == 1:
        console.print(
            "[red]Usage:[/red] [blue]./scan.py[/blue] [green]<ip>[/green] [grey50]<timeout = 1>[/grey50]"
        )
        sys.exit()

    main(sys.argv[1], argv_getter(2, int))
