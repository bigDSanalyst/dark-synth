"""Charter validation rules. One place; nothing else reimplements them."""
import yaml
from pathlib import Path

PLACEHOLDER_EPOCH = "YYYY-MM-DD"
PLACEHOLDER_FP = "PENDING"
VALID_FORMATIONS = ("solo", "multi")
VALID_SOURCES = ("V", "A", "P", "t", "run")
VALID_STATUSES = ("proved", "open", "accepted", "superseded", "framing")
VALID_TRACKS = ("main", "known-reduction", "architectural", "draft")
VALID_ADMISSIONS = ("V-proved", "kernel-proved", "hand-proved-charter-v1")


def load(path):
    return yaml.safe_load(Path(path).read_text()) or {}


def is_unprovisioned_template(cfg):
    if cfg.get("signer_fingerprint", PLACEHOLDER_FP) not in (PLACEHOLDER_FP, ""):
        return False
    if not cfg.get("vaults"):
        return True
    return False


def formation_ok(cfg):
    signers = cfg.get("signers") or []
    declared = (cfg.get("governance") or {}).get("formation")
    if is_unprovisioned_template(cfg):
        return True, ""
    if declared not in VALID_FORMATIONS:
        return False, f"governance.formation is {declared!r}; must be 'solo' or 'multi'"
    if declared == "solo" and len(signers) > 1:
        return False, f"formation: solo but {len(signers)} signers"
    if declared == "multi" and len(signers) < 2:
        return False, f"formation: multi but {len(signers)} signer(s)"
    return True, f"formation: {declared}, {len(signers)} signer(s)"


def signing_epoch(cfg):
    epoch = (cfg.get("governance") or {}).get("signing_since")
    if not epoch or epoch == PLACEHOLDER_EPOCH:
        return None, "governance.signing_since is not set (YYYY-MM-DD)"
    return str(epoch), ""
