# P3 Embedded Systems Workspace

This repository contains multiple MicroPython subprojects for Raspberry Pi Pico.

Each subproject should contain its own `main.py` that is uploaded to the Pico.

## 1) Activate the virtual environment (Linux/macOS)

From the workspace root:

```bash
source .venv/bin/activate
```

To leave the environment:

```bash
deactivate
```

## Python dependency: pyserial

`pyserial` is useful (and often required) when you use Python-based serial tools from the terminal.

- If you work only with the **MicroPico VS Code extension**, `pyserial` is usually not required.
- If you use serial tooling (for example `mpremote`, custom scripts, or `serial.tools.*`), install it in the venv.

Install/check:

```bash
pip install pyserial
pip show pyserial
```

## 2) Run a subproject on the Pico

These are **MicroPython** projects, so code runs on the Pico board (not directly on your PC Python).

### Option A: Use MicroPico in VS Code (recommended)

1. Connect your Pico via USB.
2. Open the subproject folder you want to run (example: `BlinkWithExternalHardwareReset`).
3. Open that subproject's `main.py`.
4. Use the Command Palette (`Ctrl+Shift+P`):
   - `MicroPico: Upload current file to Pico` (or upload the whole project).
5. Reset the Pico (or save again if auto-upload is enabled).

When `main.py` is on the board, it starts automatically after reset/power-on.

### Option B: Paste into MicroPython REPL

If you use another tool/REPL, run the selected subproject's `main.py` directly on the Pico.

## Notes

- Ensure MicroPython firmware is installed on the Pico.