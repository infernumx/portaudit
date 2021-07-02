#!/usr/bin/env python3

from src.scanner import PortScanner
from src.console import console
from typing import Optional, Callable, Any
from threading import Thread
import sys
import os


def main(ip: str, timeout: Optional[int] = 1) -> None:
    if timeout is None:
        timeout = 1
    try:
        scanner = PortScanner(ip, timeout)
        threads = []

        for port in scanner.ports:
            thread = Thread(target=scanner.scan_port, args=(port,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        scanner.finish()
    except KeyboardInterrupt:
        scanner.finish()


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
