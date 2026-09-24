# Port Status Checker

## Objective

A beginner-friendly Python TCP socket utility that checks whether specified ports on an authorized target host are **OPEN, CLOSED, or FILTERED**.

> **Safety:** Run this only against localhost, your own devices, lab systems, or systems for which you have explicit permission.

## What's included

- `port_scanner.py` — main Python source code
- `execution_log.txt` — execution proof/template
- `test_cases.txt` — test cases
- `PROJECT_REPORT.md` — project report
- `viva_questions.md` — viva preparation
- `requirements.txt` — dependency information
- `run_demo.bat` — Windows demo launcher
- `run_demo.ps1` — PowerShell demo launcher

## Requirements

- Python 3.9+
- No third-party packages

## Windows PowerShell

Do NOT run the Python file using:

```text
/usr/bin/env python3
```

That command is for Unix-like systems.

Use:

```powershell
python "C:\path\to\port_scanner.py" 127.0.0.1 1-100
```

Example:

```powershell
python "C:\Users\user\Downloads\Port_Status_Checker_Project\port_status_checker\port_scanner.py" 127.0.0.1 1-100
```

## Safe OPEN-port demonstration

### Terminal 1

Start a local HTTP server:

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

Keep this terminal open.

### Terminal 2

Run:

```powershell
python port_scanner.py 127.0.0.1 7995-8005
```

Port `8000` should normally appear as:

```text
8000    OPEN          http-alt            TCP connection accepted
```

The other ports may be CLOSED or FILTERED depending on the Windows system.

## Status meaning

| Status | Meaning |
|---|---|
| OPEN | TCP connection was accepted by a listening service |
| CLOSED | Target responded but refused the TCP connection |
| FILTERED | No definitive response was received, commonly because of timeout/filtering |

## Windows error-code correction

This version correctly handles common connection results:

- `10061` = Windows connection refused → CLOSED
- `10060` = Windows connection timeout → FILTERED
- `111` = Linux connection refused → CLOSED
- `61` = macOS connection refused → CLOSED

This correction is important when running the project on Windows PowerShell.

## Example

```powershell
python port_scanner.py 127.0.0.1 8000
```

If the local HTTP server is running:

```text
PORT    STATUS        SERVICE             DETAIL
------------------------------------------------------------------
8000    OPEN          http-alt            TCP connection accepted
------------------------------------------------------------------
Summary: OPEN=1  CLOSED=0  FILTERED=0
Checked 1 TCP port(s).
```

## Learning outcomes

1. Understand Python socket programming.
2. Understand TCP connection attempts.
3. Understand connection timeout handling.
4. Interpret basic TCP port states.
5. Generate execution evidence for a defensive networking project.
