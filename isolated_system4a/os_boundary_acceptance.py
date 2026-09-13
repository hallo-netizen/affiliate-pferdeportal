from __future__ import annotations

import hashlib
import hmac
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# TEST ONLY. This proves only the OS authority boundary. It contains no
# Pferde-Atelier fach/design/quality rules and is not a production runner.
PHASES = [
    "RESEARCH_REQUIRED",
    "FACTS_REQUIRED",
    "CONTEXT_REQUIRED",
    "DRAFT_REQUIRED",
    "ARTICLE_PASS",
]


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def seal(key: bytes, state: dict) -> str:
    return hmac.new(key, canon(state), hashlib.sha256).hexdigest()


def server(sock_path: Path, state_dir: Path, ready: Path) -> None:
    state_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(state_dir, 0o700)
    key = os.urandom(32)
    (state_dir / "authority.key").write_bytes(key)
    os.chmod(state_dir / "authority.key", 0o600)
    state = {
        "capsule_id": "cap-1",
        "phase": PHASES[0],
        "revision": 0,
        "publish_allowed": False,
    }

    def persist() -> None:
        state["seal"] = seal(key, {k: v for k, v in state.items() if k != "seal"})
        path = state_dir / "state.json"
        path.write_text(json.dumps(state, sort_keys=True), encoding="utf-8")
        os.chmod(path, 0o600)

    persist()
    try:
        sock_path.unlink()
    except FileNotFoundError:
        pass
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(str(sock_path))
    os.chmod(sock_path, 0o666)
    sock.listen(8)
    ready.write_text("ready", encoding="utf-8")

    while True:
        conn, _ = sock.accept()
        with conn:
            raw = b""
            while not raw.endswith(b"\n"):
                chunk = conn.recv(65536)
                if not chunk:
                    break
                raw += chunk
            try:
                req = json.loads(raw.decode())
                op = req.get("op")
                if op == "stop":
                    conn.sendall(b'{"status":"STOP"}\n')
                    break
                if op == "status":
                    out = {
                        "status": "OK",
                        "capsule_id": state["capsule_id"],
                        "phase": state["phase"],
                        "revision": state["revision"],
                        "publish_allowed": False,
                    }
                elif op == "submit":
                    if set(req) != {"op", "capsule_id", "content"}:
                        raise ValueError("WORKER_SCHEMA_INVALID")
                    if req["capsule_id"] != state["capsule_id"]:
                        raise ValueError("CAPSULE_INVALID")
                    if state["phase"] == "ARTICLE_PASS":
                        raise ValueError("OUTPUT_ALREADY_PASS")
                    if not isinstance(req["content"], str) or not req["content"].strip():
                        raise ValueError("CONTENT_EMPTY")
                    index = PHASES.index(state["phase"])
                    state["phase"] = PHASES[index + 1]
                    if state["phase"] == "ARTICLE_PASS":
                        state["revision"] += 1
                    persist()
                    out = {"status": "ACCEPTED", "phase": state["phase"]}
                elif op == "export":
                    if state["phase"] != "ARTICLE_PASS":
                        raise ValueError("OUTPUT_GATE_CLOSED")
                    out = {
                        "status": "PASS",
                        "capsule_id": state["capsule_id"],
                        "revision": state["revision"],
                        "publish_allowed": False,
                    }
                else:
                    raise ValueError("OP_FORBIDDEN")
            except Exception as exc:
                out = {"status": "BLOCKED", "error": str(exc)}
            conn.sendall(json.dumps(out, separators=(",", ":")).encode() + b"\n")
    sock.close()


def call(sock_path: Path, payload: dict, user: str | None = None, cwd: Path | None = None) -> dict:
    code = (
        "import socket,json,sys; "
        "s=socket.socket(socket.AF_UNIX); s.connect(sys.argv[1]); "
        "s.sendall((sys.argv[2]+'\\n').encode()); "
        "print(s.recv(65536).decode().strip())"
    )
    cmd = [sys.executable, "-c", code, str(sock_path), json.dumps(payload, separators=(",", ":"))]
    if user:
        cmd = ["runuser", "-u", user, "--"] + cmd
    cp = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if cp.returncode:
        raise RuntimeError(cp.stderr)
    return json.loads(cp.stdout)


def main() -> int:
    if os.geteuid() != 0:
        print("SYSTEM4A_OS_BOUNDARY_BLOCK:ROOT_REQUIRED_FOR_CROSS_UID_TEST")
        return 2

    worker_user = "nobody"
    with tempfile.TemporaryDirectory(prefix="s4a-os-boundary-") as td:
        root = Path(td)
        os.chmod(root, 0o755)
        state_dir = root / "supervisor-private"
        worker_dir = root / "worker-empty"
        worker_dir.mkdir()
        os.chmod(worker_dir, 0o755)
        sock = root / "supervisor.sock"
        ready = root / "ready"
        proc = subprocess.Popen([sys.executable, __file__, "--server", str(sock), str(state_dir), str(ready)])
        try:
            for _ in range(100):
                if ready.exists():
                    break
                time.sleep(0.02)
            assert ready.exists(), "SERVER_NOT_READY"

            # POSITIVE: worker can advance only through the one narrow interface.
            status = call(sock, {"op": "status"}, worker_user, worker_dir)
            assert status["phase"] == "RESEARCH_REQUIRED"
            for expected in ["FACTS_REQUIRED", "CONTEXT_REQUIRED", "DRAFT_REQUIRED", "ARTICLE_PASS"]:
                result = call(
                    sock,
                    {"op": "submit", "capsule_id": "cap-1", "content": "bound content"},
                    worker_user,
                    worker_dir,
                )
                assert result["phase"] == expected
            exported = call(sock, {"op": "export"}, worker_user, worker_dir)
            assert exported["status"] == "PASS" and exported["publish_allowed"] is False

            # NEGATIVE: state and authority key are physically inaccessible cross-UID.
            for target in [state_dir / "state.json", state_dir / "authority.key"]:
                cp = subprocess.run(["runuser", "-u", worker_user, "--", "cat", str(target)], capture_output=True, text=True)
                assert cp.returncode != 0, "WORKER_READ_PRIVATE_STATE_SUCCEEDED"
                cp = subprocess.run(
                    ["runuser", "-u", worker_user, "--", "sh", "-c", f"echo tamper >> {target}"],
                    capture_output=True,
                    text=True,
                )
                assert cp.returncode != 0, "WORKER_WRITE_PRIVATE_STATE_SUCCEEDED"

            # NEGATIVE: worker cannot kill/inspect supervisor, replace socket, or create private state.
            cp = subprocess.run(["runuser", "-u", worker_user, "--", "kill", "-TERM", str(proc.pid)], capture_output=True, text=True)
            assert cp.returncode != 0, "WORKER_KILL_SUPERVISOR_SUCCEEDED"
            cp = subprocess.run(["runuser", "-u", worker_user, "--", "cat", f"/proc/{proc.pid}/environ"], capture_output=True)
            assert cp.returncode != 0, "WORKER_READ_SUPERVISOR_ENV_SUCCEEDED"
            cp = subprocess.run(["runuser", "-u", worker_user, "--", "rm", "-f", str(sock)], capture_output=True, text=True)
            assert cp.returncode != 0 and sock.exists(), "WORKER_REPLACE_SOCKET_SUCCEEDED"
            cp = subprocess.run(
                ["runuser", "-u", worker_user, "--", "sh", "-c", f"echo fake > {state_dir}/fake-state.json"],
                capture_output=True,
                text=True,
            )
            assert cp.returncode != 0 and not (state_dir / "fake-state.json").exists(), "WORKER_CREATE_PRIVATE_STATE_SUCCEEDED"

            # NEGATIVE: route/PASS injection is rejected at the protocol boundary.
            injected = call(
                sock,
                {"op": "submit", "capsule_id": "cap-1", "content": "x", "phase": "ARTICLE_PASS"},
                worker_user,
                worker_dir,
            )
            assert injected["status"] == "BLOCKED" and "WORKER_SCHEMA_INVALID" in injected["error"]
            forbidden = call(sock, {"op": "set_state", "phase": "ARTICLE_PASS"}, worker_user, worker_dir)
            assert forbidden["status"] == "BLOCKED" and "OP_FORBIDDEN" in forbidden["error"]

            raw = json.loads((state_dir / "state.json").read_text(encoding="utf-8"))
            key = (state_dir / "authority.key").read_bytes()
            state_seal = raw.pop("seal")
            assert hmac.compare_digest(state_seal, seal(key, raw)), "STATE_SEAL_INVALID_AFTER_ATTACKS"
            assert raw["phase"] == "ARTICLE_PASS"

            print("SYSTEM4A_EXTERNAL_SUPERVISOR_OS_BOUNDARY_PASS: POSITIVE_ROUTE + 10_NEGATIVE_AUTHORITY_CHECKS")
            return 0
        finally:
            try:
                call(sock, {"op": "stop"})
            except Exception:
                pass
            proc.wait(timeout=3)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--server":
        server(Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
    else:
        raise SystemExit(main())
