import sys
import time
import signal
import platform
from pathlib import Path
from datetime import datetime, timedelta

if platform.system() == "Windows":
    HOSTS = Path("C:/Windows/System32/drivers/etc/hosts")
else:
    HOSTS = Path("/etc/hosts")

REDIRECT = "127.0.0.1"
MARKER_START = "# FocusGuard START"
MARKER_END = "# FocusGuard END"


def load_sites():
    with open("sites.txt") as f:
        return [l.strip() for l in f if l.strip() and not l.startswith("#")]


def block(sites):
    with open(HOSTS, "r") as f:
        content = f.read()
    if MARKER_START in content:
        return
    entries = "\n".join(f"{REDIRECT} {s}" for s in sites)
    block_text = f"\n{MARKER_START}\n{entries}\n{MARKER_END}\n"
    with open(HOSTS, "a") as f:
        f.write(block_text)
    print(f"[FocusGuard] Blocked {len(sites)} sites.")


def unblock():
    with open(HOSTS, "r") as f:
        lines = f.readlines()
    inside = False
    cleaned = []
    for line in lines:
        if MARKER_START in line:
            inside = True
            continue
        if MARKER_END in line:
            inside = False
            continue
        if not inside:
            cleaned.append(line)
    with open(HOSTS, "w") as f:
        f.writelines(cleaned)
    print("[FocusGuard] Sites unblocked. Session complete.")


def countdown(minutes):
    total = minutes * 60
    end_time = datetime.now() + timedelta(minutes=minutes)
    print(f'[FocusGuard] Session ends at {end_time.strftime("%H:%M:%S")}')
    try:
        while total > 0:
            mins, secs = divmod(total, 60)
            print(f"  Remaining: {mins:02d}:{secs:02d}", end="\r")
            time.sleep(1)
            total -= 1
        print("\n[FocusGuard] Time up!")
    except KeyboardInterrupt:
        print("\n[FocusGuard] Interrupted — unblocking...")


def main():
    if len(sys.argv) < 2:
        print("Usage: python focusguard.py <minutes>")
        print("Example: python focusguard.py 25")
        sys.exit(1)
    minutes = int(sys.argv[1])
    sites = load_sites()
    print(f"[FocusGuard] Starting {minutes}-minute focus session")
    block(sites)

    def cleanup(sig, frame):
        unblock()
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    countdown(minutes)
    unblock()


if __name__ == "__main__":
    main()
