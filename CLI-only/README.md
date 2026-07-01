# Gamepad Cryptographic Multitool — Prototype

This is a minimal CLI prototype implementing core features requested by the bounty:

- Generate a seed phrase from a built-in wordlist
- Derive a secp256k1 private key and public key
- Derive a prototype Bitcoin P2PKH address
- Export QR codes when `qrcode` is installed
- Convert text to/from binary

Quick start:

1. Run the CLI directly with the existing Python runtime:

```bash
C:/Users/plumb/AppData/Local/Python/pythoncore-3.14-64/python.exe main.py seed
```

1. Example commands:

```bash
C:/Users/plumb/AppData/Local/Python/pythoncore-3.14-64/python.exe main.py seed --words 12
C:/Users/plumb/AppData/Local/Python/pythoncore-3.14-64/python.exe main.py derive --seed "your twelve word seed"
C:/Users/plumb/AppData/Local/Python/pythoncore-3.14-64/python.exe main.py derive --seed "your twelve word seed" --out-qr public.png
C:/Users/plumb/AppData/Local/Python/pythoncore-3.14-64/python.exe main.py encode --mode text-to-binary --text "hello"
C:/Users/plumb/AppData/Local/Python/pythoncore-3.14-64/python.exe main.py encode --mode binary-to-text --binary "01101000 01100101 01101100 01101100 01101111"
```

Notes:

- The tool is intentionally minimal and prototype-quality.
- `qrcode` support is optional for QR export.
- This implementation uses BIP-39 mnemonic generation and BIP-32 derivation for educational/demo use.
