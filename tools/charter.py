#!/usr/bin/env python3
"""Sign and verify the Dark Synth charter.

The charter is a YAML file with axioms, admission rules, and guard settings.
Its signature is Ed25519 over the canonical JSON of the charter body (all
fields except signature, signer_fingerprint, signed_at).
"""
import argparse
import base64
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
except ImportError:
    print("charter needs pyyaml and cryptography: pip install pyyaml cryptography", file=sys.stderr)
    sys.exit(1)

SIGNATURE_FIELDS = ("signature", "signer_fingerprint", "signed_at")


def _canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _fingerprint(pub):
    raw = pub.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return hashlib.sha256(raw).hexdigest()


def load(path):
    return yaml.safe_load(path.read_text()) or {}


def is_signed(cfg):
    if not cfg.get("signature"):
        return False, "charter is unsigned (signature field is empty)"
    if not cfg.get("signer_fingerprint"):
        return False, "charter has a signature but no fingerprint"
    return True, "signed by " + cfg["signer_fingerprint"][:16] + "..."


def verify(path):
    """Axiom 23: verification requires the external pin. Missing pin = refusal."""
    cfg = load(path)
    ok, msg = is_signed(cfg)
    if not ok:
        return False, msg
    body = {k: v for k, v in cfg.items() if k not in SIGNATURE_FIELDS}
    try:
        sig = base64.b64decode(cfg["signature"])
    except Exception as e:
        return False, "signature is not valid base64: " + str(e)
    key_path = path.parent.parent / "owner.pub"
    if not key_path.exists():
        return False, "owner.pub is missing from the repo root (Axiom 23: external pin required)"
    try:
        pub = serialization.load_ssh_public_key(key_path.read_bytes())
    except Exception as e:
        return False, "owner.pub is not a valid SSH public key: " + str(e)
    try:
        pub.verify(sig, _canonical(body))
        return True, "signature valid against owner.pub; signed by " + cfg["signer_fingerprint"][:16] + "..."
    except Exception as e:
        return False, "signature does not verify against owner.pub: " + str(e)


def sign(path, key_path):
    cfg = load(path)
    body = {k: v for k, v in cfg.items() if k not in SIGNATURE_FIELDS}
    key_bytes = key_path.read_bytes()
    priv = serialization.load_pem_private_key(key_bytes, password=None)
    sig = priv.sign(_canonical(body))
    pub = priv.public_key()
    cfg["signature"] = base64.b64encode(sig).decode()
    cfg["signer_fingerprint"] = _fingerprint(pub)
    cfg["signed_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    path.write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True))
    print("signed charter with fingerprint " + cfg["signer_fingerprint"][:16] + "...")


def keygen(out):
    priv = Ed25519PrivateKey.generate()
    pem = priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(pem)
    out.chmod(0o600)
    pub = priv.public_key().public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH,
    )
    (out.parent / "owner.pub").write_bytes(pub)
    print("wrote " + str(out) + " and " + str(out.parent / "owner.pub"))
    print("fingerprint: " + _fingerprint(priv.public_key()))


def main(argv=None):
    ap = argparse.ArgumentParser(description="sign/verify/keygen the Dark Synth charter")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("sign")
    p.add_argument("--charter", default="charter/charter.yaml")
    p.add_argument("--key", required=True)
    v = sub.add_parser("verify")
    v.add_argument("--charter", default="charter/charter.yaml")
    k = sub.add_parser("keygen")
    k.add_argument("--out", default="~/.dark-synth-owner.pem")
    a = ap.parse_args(argv)

    if a.cmd == "keygen":
        keygen(Path(a.out).expanduser())
        return 0
    if a.cmd == "sign":
        sign(Path(a.charter), Path(a.key).expanduser())
        return 0
    if a.cmd == "verify":
        ok, msg = verify(Path(a.charter))
        print(msg)
        return 0 if ok else 1


if __name__ == "__main__":
    _argv = sys.argv[1:] if sys.argv and sys.argv[0].endswith(".py") else []
    sys.exit(main(_argv))
