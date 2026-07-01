Gamepad‑Controlled Cryptographic Multitool (Prototype 168)

Overview:  
This submission delivers a fully functional prototype of a cryptographic multitool capable of BIP‑39 seed generation, key/address derivation, and optional gamepad‑driven interaction. The tool includes both a CLI‑only mode and a pygame‑powered gamepad mode, with automatic fallback to simulation when no physical controller is detected.

Key Features Delivered:

BIP‑39 Seed Generation  
Supports 12‑word mnemonic creation using the included wordlist.

Key & Address Derivation  
Deterministic derivation from any provided seed phrase.

Gamepad Auto‑Detect System  
Automatically detects connected controllers; defaults to simulation mode when none are present.

Simulated Gamepad Mode  
Allows full testing and usage without hardware.

Unified Launcher Menu  
A top‑level launcher.py provides a simple interactive menu for selecting CLI, Gamepad, or Gamepad Tool variants.

Fallback Logic  
Ensures the tool remains usable even when optional dependencies (pygame, qrcode) are missing.

Documentation Included  
README, submission statement, manifest, and claim notes included in the repo.

Testing + CI Pipeline  
Smoke tests via pytest and a GitHub Actions CI workflow for validation on push/PR.

Technical Strengths:

Python‑only implementation (100%)

Modular structure

Clear separation between CLI, gamepad, and launcher components

Robust error handling and fallback behavior

Realistic user‑focused design choices

Submission Files Included:

SUBMISSION_STATEMENT.txt

SUBMISSION_GUID.txt

claim_submission.txt

submission-manifest.txt

Full source code + tests

Startup Guide

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
