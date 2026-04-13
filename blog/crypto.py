"""Asymmetric encryption for eval logs using age (via pyrage).

Public key  (age.pub)  — committed to the repo; anyone can encrypt logs with it.
Private key (age.key)  — gitignored; only the repo owner holds this.

Usage:
  uv run python -m blog.crypto keygen                    # generate age.pub + age.key
  uv run python -m blog.crypto encrypt <src> <dst>       # encrypt one file
  uv run python -m blog.crypto decrypt <enc_dir> <dec_dir>  # decrypt all .enc files
"""

import sys
from pathlib import Path

PUB_KEY_FILE = Path("age.pub")
PRIV_KEY_FILE = Path("age.key")


def _load_public_key() -> str:
    if not PUB_KEY_FILE.exists():
        raise RuntimeError(f"{PUB_KEY_FILE} not found. Run `make keygen` first.")
    return PUB_KEY_FILE.read_text().strip()


def _load_private_key():
    import pyrage
    if not PRIV_KEY_FILE.exists():
        raise RuntimeError(
            f"{PRIV_KEY_FILE} not found. "
            "Copy it to the repo root (it is gitignored)."
        )
    return pyrage.x25519.Identity.from_str(PRIV_KEY_FILE.read_text().strip())


def encrypt_file(src: Path, dst: Path) -> None:
    import pyrage
    recipient = pyrage.x25519.Recipient.from_str(_load_public_key())
    dst.write_bytes(pyrage.encrypt(src.read_bytes(), [recipient]))


def decrypt_dir(enc_dir: Path, dec_dir: Path) -> None:
    import pyrage
    identity = _load_private_key()
    dec_dir.mkdir(exist_ok=True)
    for enc_file in sorted(enc_dir.glob("*.enc")):
        dst = dec_dir / enc_file.stem  # strip .enc → original name
        dst.write_bytes(pyrage.decrypt(enc_file.read_bytes(), [identity]))
        print(f"  decrypted {enc_file.name} → {dst.name}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""

    if cmd == "keygen":
        import pyrage
        if PRIV_KEY_FILE.exists() or PUB_KEY_FILE.exists():
            print("age.key or age.pub already exists — delete them first.")
            sys.exit(1)
        identity = pyrage.x25519.Identity.generate()
        PRIV_KEY_FILE.write_text(str(identity) + "\n")
        PUB_KEY_FILE.write_text(str(identity.to_public()) + "\n")
        print(f"Private key → {PRIV_KEY_FILE} (gitignored, keep secret)")
        print(f"Public key  → {PUB_KEY_FILE} (commit this)")

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
