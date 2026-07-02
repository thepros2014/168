import importlib.util
import pathlib
import binascii

files = {
    'cli': pathlib.Path(__file__).resolve().parent.parent / 'CLI-only' / 'main.py',
    'gamepad': pathlib.Path(__file__).resolve().parent.parent / 'gamepad' / 'main.py',
    'gamepad_tool': pathlib.Path(__file__).resolve().parent.parent / 'gamepad_tool' / 'main.py',
}

results = {}
for name, path in files.items():
    try:
        spec = importlib.util.spec_from_file_location(name + '_mod', path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        # Run core functions if present
        out = {'imported': True}
        if hasattr(mod, 'generate_seed'):
            s = mod.generate_seed(word_count=12)
            out['seed'] = s
        if hasattr(mod, 'mnemonic_to_seed'):
            sb = mod.mnemonic_to_seed(out.get('seed', ''))
            out['seed_bytes_len'] = len(sb)
        if hasattr(mod, 'seed_to_privkey'):
            priv = mod.seed_to_privkey(out.get('seed', ''))
            out['priv_len'] = len(priv)
        if hasattr(mod, 'privkey_to_pubkey'):
            pub = mod.privkey_to_pubkey(priv)
            out['pub_len'] = len(pub)
        if hasattr(mod, 'pubkey_to_p2pkh_address'):
            out['address'] = mod.pubkey_to_p2pkh_address(pub)
        results[name] = ('ok', out)
    except Exception as e:
        results[name] = ('error', repr(e))

for k, v in results.items():
    print(k, v)

# Quick checks for expected resources
from pathlib import Path
root = pathlib.Path(__file__).resolve().parent.parent
wl = root / 'bip39_wordlist.txt'
print('wordlist exists:', wl.exists(), 'size:', wl.stat().st_size if wl.exists() else 'n/a')

# Check requirements files
for sub in ('CLI-only', 'gamepad', 'gamepad_tool'):
    req = root / sub / 'requirements.txt'
    print(sub, 'requirements exists:', req.exists())
