"""Compile a proof from scratch. Does the kernel accept it?"""
import hashlib
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

CLOSED = "Closed under the global context"
ACCEPTED, REJECTED, NOT_CHECKED = "accepted", "rejected", "not_checked"


@dataclass
class Certificate:
    verdict: str
    detail: str
    source: str

    @property
    def ok(self):
        return self.verdict == ACCEPTED

    @property
    def sha256(self):
        return hashlib.sha256(self.source.encode()).hexdigest()


def _probe(compiler):
    path = shutil.which(compiler)
    if path is None:
        return None, f"no {compiler} on PATH"
    try:
        r = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, f"{compiler} at {path} does not run: {e}"
    if r.returncode != 0:
        return None, f"{compiler} at {path} returned {r.returncode}"
    return path, r.stdout.strip().split("\n")[0]


def certify(source, timeout=300, compiler="coqc"):
    exe, why = _probe(compiler)
    if exe is None:
        return Certificate(NOT_CHECKED, why, source)
    with tempfile.TemporaryDirectory(prefix="dark-synth-") as work:
        path = Path(work) / "Cert.v"
        path.write_text(source)
        try:
            proc = subprocess.run([exe, str(path)], capture_output=True, text=True,
                                  timeout=timeout, cwd=work)
        except subprocess.TimeoutExpired:
            return Certificate(NOT_CHECKED, f"timed out after {timeout}s", source)
        except OSError as e:
            return Certificate(NOT_CHECKED, f"compiler did not run: {e}", source)
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        return Certificate(REJECTED, out.strip()[-400:], source)
    if CLOSED not in out:
        return Certificate(REJECTED, "proof rests on an axiom or an Admitted proof", source)
    return Certificate(ACCEPTED, "kernel accepted; closed under the global context", source)


def backends():
    out = {}
    for name in ("coqc", "lean"):
        path, status = _probe(name)
        out[name] = {"path": path, "status": status, "available": path is not None}
    return out
