# FocusGuard 🛡️
 
Silent background focus timer that blocks distracting sites system-wide.
No browser extension needed — works everywhere, every browser.
 
## Run
```bash
# Windows: run PowerShell as Administrator
# Mac/Linux: prefix with sudo
python focusguard.py 25   # 25 minute session
python focusguard.py 60   # 1 hour session
```
 
## How it works
Edits your system hosts file to redirect blocked domains to 127.0.0.1.
Automatically cleans up when the timer ends or you press Ctrl+C.
 
## Edit your block list
Add or remove domains from `sites.txt` — one per line.
 
## No dependencies
Pure Python standard library. Nothing to install.
 
## Stack
![Python](https://img.shields.io/badge/Python-000?style=flat&logo=python&logoColor=white)

