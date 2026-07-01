# Cryptographic Multitool Prototype (168)

This repository contains a minimal prototype CLI and optional gamepad interface for BIP-39 seed phrase generation and key/address derivation.

Prerequisites
- Python 3.11+ recommended
- Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Quick usage

Generate a 12-word seed (CLI-only):

```bash
python CLI-only/main.py seed --words 12
```

Derive keys and address from an existing seed:

```bash
python CLI-only/main.py derive --seed "your mnemonic words here"
```

Gamepad mode (requires `pygame`):

```bash
python gamepad_tool/main.py gamepad
```

Launcher menu

Run the top-level launcher to pick a variant via a simple interactive menu:

```bash
python launcher.py
```

The launcher lets you run `CLI-only`, `Gamepad`, or `Gamepad Tool` and can start gamepad variants in simulated mode when no gamepad is available.

Notes
- `qrcode` is optional. If `qrcode` is not installed, the tools will write the QR data as plain text to the provided output path and print a warning.
- `pygame` is optional and only required for gamepad interactive mode.
- Tests: run `pytest` in the project root to run the core smoke tests.

CI
- A GitHub Actions workflow is included at `.github/workflows/ci.yml` to run tests on push/PR.

Claim preparation
- `claim_submission.txt` contains the current draft claim notes.
