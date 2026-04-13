"""Symmetric encryption for eval logs (Fernet / AES-128-CBC + HMAC).

Key resolution order:
  1. MASK_BLOG_KEY environment variable (base64-encoded Fernet key)
  2. eval_logs.key file in the repo root (gitignored)

Usage:
  uv run python -m blog.crypto keygen          # generate and save a key
  uv run python -m blog.crypto encrypt <src> <dst>   # encrypt one file
  uv run python -m blog.crypto decrypt <enc_dir> <dec_dir>  # decrypt all
"""

import os
import sys
from pathlib import Path

KEY_FILE = Path("eval_logs.key")
KEY_ENV = "MASK_BLOG_KEY"


def _load_key() -> bytes:
    if KEY_ENV in os.environ:
        return os.environ[KEY_ENV].encode()
    if KEY_FILE.exists():
        return KEY_FILE.read_bytes().strip()
    raise RuntimeError(
        f"No key found. Run `make keygen` to create {KEY_FILE}, "
        f"or set the {KEY_ENV} environment variable."
    )


def encrypt_file(src: Path, dst: Path) -> None:
    from cryptography.fernet import Fernet
    dst.write_bytes(Fernet(_load_key()).encrypt(src.read_bytes()))


def decrypt_dir(enc_dir: Path, dec_dir: Path) -> None:
    from cryptography.fernet import Fernet
    dec_dir.mkdir(exist_ok=True)
    f = Fernet(_load_key())
    for enc_file in sorted(enc_dir.glob("*.enc")):
        dst = dec_dir / enc_file.stem  # strip .enc → original name
        dst.write_bytes(f.decrypt(enc_file.read_bytes()))
        print(f"  decrypted {enc_file.name} → {dst.name}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""

    if cmd == "keygen":
        from cryptography.fernet import Fernet
        if KEY_FILE.exists():
            print(f"{KEY_FILE} already exists — delete it first if you want a new key.")
            sys.exit(1)
        KEY_FILE.write_bytes(Fernet.generate_key())
        print(f"Key written to {KEY_FILE} (keep this secret, do not commit)")

    elif cmd == "encrypt":
        src, dst = Path(sys.argv[2]), Path(sys.argv[3])
        encrypt_file(src, dst)
        print(f"Encrypted {src} → {dst}")

    elif cmd == "decrypt":
        enc_dir, dec_dir = Path(sys.argv[2]), Path(sys.argv[3])
        decrypt_dir(enc_dir, dec_dir)

    else:
        print(__doc__)
        sys.exit(1)
