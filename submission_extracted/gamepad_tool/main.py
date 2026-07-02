#!/usr/bin/env python3
"""Minimal prototype for Gamepad Cryptographic Multitool (CLI).

Features:
- Generate a seed phrase from a local wordlist
- Derive a secp256k1 private key & public key
- Build a prototype Bitcoin P2PKH address
- Export QR codes when qrcode is installed
- Simple text <-> binary conversions

This is a prototype for bounty work and not production-ready crypto tooling.
"""

import argparse
import hashlib
import binascii
import os
from pathlib import Path
from ecdsa import SigningKey, SECP256k1

try:
    import qrcode
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

WORDLIST = []

WORDLIST_FILE = Path(__file__).resolve().parent / 'bip39_wordlist.txt'
ALT_WORDLIST_FILE = Path(__file__).resolve().parent.parent / 'bip39_wordlist.txt'

for path in (WORDLIST_FILE, ALT_WORDLIST_FILE):
    if path.exists():
        with path.open('r', encoding='utf-8') as f:
            WORDLIST = [line.strip() for line in f if line.strip()]
        break

if not WORDLIST:
    raise FileNotFoundError(f'BIP-39 wordlist file not found: {WORDLIST_FILE} or {ALT_WORDLIST_FILE}')

if len(WORDLIST) != 2048:
    raise ValueError('BIP-39 wordlist must contain 2048 words.')

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def _to_bitstring(data: bytes) -> str:
    return ''.join(f'{b:08b}' for b in data)


def _checksum_bits(entropy: bytes) -> str:
    digest = hashlib.sha256(entropy).digest()
    return _to_bitstring(digest)[: len(entropy) * 8 // 32]


def entropy_to_mnemonic(entropy: bytes) -> str:
    if len(entropy) not in (16, 20, 24, 28, 32):
        raise ValueError('Entropy must be 128, 160, 192, 224, or 256 bits.')
    bits = _to_bitstring(entropy) + _checksum_bits(entropy)
    return ' '.join(WORDLIST[int(bits[i:i + 11], 2)] for i in range(0, len(bits), 11))


def mnemonic_to_seed(mnemonic: str, passphrase: str = '') -> bytes:
    salt = b'mnemonic' + passphrase.encode('utf-8')
    return hashlib.pbkdf2_hmac('sha512', mnemonic.encode('utf-8'), salt, 2048, dklen=64)


def generate_seed_phrase(word_count=12):
    if word_count not in (12, 15, 18, 21, 24):
        raise ValueError('Word count must be one of 12, 15, 18, 21, or 24.')
    entropy_lengths = {12: 16, 15: 20, 18: 24, 21: 28, 24: 32}
    entropy = os.urandom(entropy_lengths[word_count])
    return entropy_to_mnemonic(entropy)


generate_seed = generate_seed_phrase


def init_gamepad():
    import importlib
    try:
        pygame = importlib.import_module('pygame')
    except ImportError:
        raise RuntimeError('Gamepad support requires pygame. Install it with pip install pygame.')
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        raise RuntimeError('No gamepad detected. Connect a gamepad and retry.')
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    return pygame, joystick


def detect_gamepad_available() -> bool:
    """Return True if a gamepad is available; false otherwise. Does not raise on ImportError."""
    try:
        import pygame
    except Exception:
        return False
    try:
        pygame.init()
        pygame.joystick.init()
        count = pygame.joystick.get_count()
        return count > 0
    except Exception:
        return False


def gamepad_interactive_loop(simulate=None):
    """Interactive loop. If simulate=True, use keyboard-driven mode instead of real gamepad."""
    # If simulate is None, auto-detect presence of a gamepad
    if simulate is None:
        simulate = not detect_gamepad_available()

    if simulate:
        print('Simulated gamepad mode. Press:')
        print('  0 -> Generate a seed phrase')
        print('  1 -> Derive keys from a seed phrase')
        print('  2 -> Convert text to binary')
        print('  3 -> Convert binary to text')
        print('  q -> Quit')
        while True:
            cmd = input('\nPress key: ').strip()
            if not cmd:
                continue
            if cmd == '0':
                print('\nSeed phrase:', generate_seed_phrase())
            elif cmd == '1':
                seed = input('\nEnter seed phrase: ').strip()
                if not seed:
                    print('Seed phrase is required.')
                    continue
                priv = seed_to_privkey(seed)
                pub = privkey_to_pubkey(priv)
                print('Private key (hex):', binascii.hexlify(priv).decode())
                print('Public key (hex, uncompressed):', binascii.hexlify(pub).decode())
                print('Prototype Bitcoin P2PKH address:', pubkey_to_p2pkh_address(pub))
            elif cmd == '2':
                text = input('\nEnter text to convert to binary: ')
                print(text_to_binary(text))
            elif cmd == '3':
                binary = input('\nEnter binary string to convert to text: ')
                print(binary_to_text(binary))
            elif cmd.lower() == 'q':
                print('Exiting simulated gamepad mode.')
                break
            else:
                print('Unknown key')
        return

    # real gamepad path
    pygame, joystick = init_gamepad()
    print('Detected gamepad:', joystick.get_name())
    print('Button mappings:')
    print('  Button 0 -> Generate a seed phrase')
    print('  Button 1 -> Derive keys from a seed phrase')
    print('  Button 2 -> Convert text to binary')
    print('  Button 3 -> Convert binary to text')
    print('  Button 4 -> Quit')

    active = True
    while active:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                btn = event.button
                if btn == 0:
                    print('\nSeed phrase:', generate_seed_phrase())
                elif btn == 1:
                    seed = input('\nEnter seed phrase: ').strip()
                    if not seed:
                        print('Seed phrase is required.')
                        continue
                    priv = seed_to_privkey(seed)
                    pub = privkey_to_pubkey(priv)
                    print('Private key (hex):', binascii.hexlify(priv).decode())
                    print('Public key (hex, uncompressed):', binascii.hexlify(pub).decode())
                    print('Prototype Bitcoin P2PKH address:', pubkey_to_p2pkh_address(pub))
                elif btn == 2:
                    text = input('\nEnter text to convert to binary: ')
                    print(text_to_binary(text))
                elif btn == 3:
                    binary = input('\nEnter binary string to convert to text: ')
                    print(binary_to_text(binary))
                elif btn == 4:
                    active = False
                    print('Exiting gamepad control mode.')
                    break
        pygame.time.wait(100)

def seed_to_privkey(seed):
    seed_bytes = mnemonic_to_seed(seed)
    return seed_bytes[:32]

def privkey_to_pubkey(privkey_bytes):
    sk = SigningKey.from_string(privkey_bytes, curve=SECP256k1)
    vk = sk.get_verifying_key()
    return b'\x04' + vk.to_string()


def base58_encode(data):
    num = int.from_bytes(data, 'big')
    encoded = ''
    while num > 0:
        num, rem = divmod(num, 58)
        encoded = BASE58_ALPHABET[rem] + encoded
    for byte in data:
        if byte == 0:
            encoded = '1' + encoded
        else:
            break
    return encoded


def base58_check_encode(data):
    checksum = hashlib.sha256(hashlib.sha256(data).digest()).digest()[:4]
    return base58_encode(data + checksum)


def pubkey_to_p2pkh_address(pubkey_bytes):
    sha = hashlib.sha256(pubkey_bytes).digest()
    ripemd = hashlib.new('ripemd160', sha).digest()
    versioned = b'\x00' + ripemd
    return base58_check_encode(versioned)


def save_qr(data, out_path):
    if QR_AVAILABLE:
        qrcode.make(data).save(out_path)
        return
    # Fallback: write the data as plain text so user still has output
    try:
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(str(data))
        print('Warning: qrcode not installed; wrote data as text to', out_path)
    except Exception as e:
        raise RuntimeError('Failed to save fallback QR data: ' + str(e))


def text_to_binary(text, encoding='utf-8'):
    return ' '.join(format(b, '08b') for b in text.encode(encoding))


def binary_to_text(binary_str, encoding='utf-8'):
    parts = binary_str.split()
    data = bytes(int(p, 2) for p in parts)
    return data.decode(encoding, errors='replace')


def main():
    parser = argparse.ArgumentParser(description='Gamepad Cryptographic Multitool (prototype)')
    sub = parser.add_subparsers(dest='cmd')

    p_seed = sub.add_parser('seed', help='Generate a seed phrase')
    p_seed.add_argument('--words', type=int, default=12, choices=[12, 15, 18, 21, 24], help='Number of words to generate')

    p_derive = sub.add_parser('derive', help='Derive keys and addresses from a seed')
    p_derive.add_argument('--seed', required=True, help='Seed phrase')
    p_derive.add_argument('--out-qr', help='Save pubkey/address as QR to this path')

    p_gamepad = sub.add_parser('gamepad', help='Use a connected gamepad to control the tool')
    p_gamepad.add_argument('--simulate', action='store_true', help='Simulate gamepad input via keyboard')

    p_qr = sub.add_parser('qr', help='Save QR code for arbitrary data')
    p_qr.add_argument('--data', required=True)
    p_qr.add_argument('--out', required=True)

    p_enc = sub.add_parser('encode', help='Text/binary encoding helpers')
    p_enc.add_argument('--mode', choices=['text-to-binary', 'binary-to-text'], required=True)
    p_enc.add_argument('--text')
    p_enc.add_argument('--binary')

    args = parser.parse_args()

    if args.cmd == 'seed':
        seed = generate_seed(word_count=args.words)
        print(seed)

    elif args.cmd == 'derive':
        seed = args.seed
        priv = seed_to_privkey(seed)
        pub = privkey_to_pubkey(priv)
        pub_hex = binascii.hexlify(pub).decode()
        priv_hex = binascii.hexlify(priv).decode()
        print('Private key (hex):', priv_hex)
        print('Public key (hex, uncompressed):', pub_hex)
        print('Prototype Bitcoin P2PKH address:', pubkey_to_p2pkh_address(pub))
        if args.out_qr:
            save_qr(pub_hex, args.out_qr)
            print('Saved QR to', args.out_qr)

    elif args.cmd == 'gamepad':
        try:
            gamepad_interactive_loop(simulate=getattr(args, 'simulate', False))
        except RuntimeError as e:
            raise SystemExit(str(e))

    elif args.cmd == 'qr':
        save_qr(args.data, args.out)
        print('Saved QR to', args.out)

    elif args.cmd == 'encode':
        if args.mode == 'text-to-binary':
            if not args.text:
                print('Provide --text')
                return
            print(text_to_binary(args.text))
        else:
            if not args.binary:
                print('Provide --binary')
                return
            print(binary_to_text(args.binary))

    else:
        parser.print_help()


if __name__ == '__main__':
    try:
        main()
    except FileNotFoundError as e:
        print('Required resource missing:', e)
        print('Ensure bip39_wordlist.txt exists in the script folder or project root (168/).')
        raise SystemExit(2)
    except ValueError as e:
        print('Input error:', e)
        raise SystemExit(2)
    except RuntimeError as e:
        print('Runtime error:', e)
        raise SystemExit(3)
    except Exception as e:
        print('Unexpected error:', type(e).__name__, e)
        raise
