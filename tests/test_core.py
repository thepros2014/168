import importlib.util
import pathlib


def load_module(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ROOT = pathlib.Path(__file__).resolve().parent.parent


def test_cli_generate_and_derive():
    p = ROOT / 'CLI-only' / 'main.py'
    mod = load_module(p)
    seed = mod.generate_seed(word_count=12)
    assert isinstance(seed, str) and len(seed.split()) == 12
    seed_bytes = mod.mnemonic_to_seed(seed)
    assert len(seed_bytes) == 64
    priv = mod.seed_to_privkey(seed)
    assert len(priv) == 32
    pub = mod.privkey_to_pubkey(priv)
    assert len(pub) in (33, 65)


def test_gamepad_tool_generate_and_derive():
    p = ROOT / 'gamepad_tool' / 'main.py'
    mod = load_module(p)
    seed = mod.generate_seed(word_count=12)
    assert isinstance(seed, str) and len(seed.split()) == 12
    seed_bytes = mod.mnemonic_to_seed(seed)
    assert len(seed_bytes) == 64
    priv = mod.seed_to_privkey(seed)
    assert len(priv) == 32
    pub = mod.privkey_to_pubkey(priv)
    assert len(pub) in (33, 65)
