from pathlib import Path

files = [
    Path('CLI-only/main.py'),
    Path('gamepad/main.py'),
    Path('gamepad_tool/main.py'),
]

wordlist_block = """WORDLIST = []

WORDLIST_FILE = Path(__file__).resolve().parent / 'bip39_wordlist.txt'

if WORDLIST_FILE.exists():
    with WORDLIST_FILE.open('r', encoding='utf-8') as f:
        WORDLIST = [line.strip() for line in f if line.strip()]
    if len(WORDLIST) != 2048:
        raise ValueError('BIP-39 wordlist must contain 2048 words.')
else:
    raise FileNotFoundError(f'BIP-39 wordlist file not found: {WORDLIST_FILE}')

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
"""

seed_function = """def _to_bitstring(data: bytes) -> str:
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
"""

seed_to_privkey = """def seed_to_privkey(seed):
    seed_bytes = mnemonic_to_seed(seed)
    return seed_bytes[:32]
"""

for path in files:
    text = path.read_text(encoding='utf-8')
    if 'from pathlib import Path' not in text:
        text = text.replace('import os\nfrom ecdsa import SigningKey, SECP256k1\n',
                            'import os\nfrom pathlib import Path\nfrom ecdsa import SigningKey, SECP256k1\n')

    if 'WORDLIST = [' in text:
        start = text.index('WORDLIST = [')
        end = text.index("BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'", start)
        text = text[:start] + wordlist_block + text[end:]
    elif 'WORDLIST = []' not in text:
        raise RuntimeError(f'Could not find WORDLIST declaration in {path}')

    if 'def generate_seed_phrase(word_count=12):' in text:
        start = text.index('def generate_seed_phrase(word_count=12):')
        end = text.index('generate_seed = generate_seed_phrase', start) + len('generate_seed = generate_seed_phrase\n')
        text = text[:start] + seed_function + text[end:]
    else:
        raise RuntimeError(f'Could not find generate_seed_phrase in {path}')

    if 'def seed_to_privkey(seed):' in text:
        start = text.index('def seed_to_privkey(seed):')
        end = text.index('def privkey_to_pubkey(privkey_bytes):', start)
        text = text[:start] + seed_to_privkey + '\n' + text[end:]
    else:
        raise RuntimeError(f'Could not find seed_to_privkey in {path}')

    path.write_text(text, encoding='utf-8')
    print(f'Patched {path}')
