from __future__ import annotations

import json
import os
import secrets
import sqlite3
from pathlib import Path
from typing import Any, Mapping


class AuthorityStoreError(RuntimeError):
    pass


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise AuthorityStoreError(code)


def _canonical(value: Mapping[str, Any]) -> str:
    return json.dumps(dict(value), ensure_ascii=False, sort_keys=True, separators=(',', ':'))


class SupervisorAuthorityStore:
    """Single durable state store owned by the external supervisor only."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(self.root, 0o700)
        _require((self.root.stat().st_mode & 0o077) == 0, 'AUTHORITY_ROOT_PERMISSIONS_INVALID')
        self.key_path = self.root / 'authority.key'
        self.db_path = self.root / 'supervisor.sqlite3'
        self._key = self._load_or_create_key()
        self._init_db()

    def _load_or_create_key(self) -> bytes:
        if self.key_path.exists():
            _require(self.key_path.is_file(), 'AUTHORITY_KEY_NOT_FILE')
            _require((self.key_path.stat().st_mode & 0o077) == 0, 'AUTHORITY_KEY_PERMISSIONS_INVALID')
            key = self.key_path.read_bytes()
            _require(len(key) == 32, 'AUTHORITY_KEY_LENGTH_INVALID')
            return key
        key = secrets.token_bytes(32)
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        fd = os.open(self.key_path, flags, 0o600)
        try:
            os.write(fd, key)
            os.fsync(fd)
        finally:
            os.close(fd)
        os.chmod(self.key_path, 0o600)
        return key

    def _connect(self) -> sqlite3.Connection:
        con = sqlite3.connect(self.db_path)
        con.execute('PRAGMA journal_mode=WAL')
        con.execute('PRAGMA synchronous=FULL')
        return con

    def _init_db(self) -> None:
        con=self._connect()
        try:
            with con:
                con.execute(
                    'CREATE TABLE IF NOT EXISTS capsules ('
                    'capsule_id TEXT PRIMARY KEY NOT NULL, '
                    'state_json TEXT NOT NULL)'
                )
        finally:
            con.close()
        os.chmod(self.db_path, 0o600)
        for suffix in ('-wal', '-shm'):
            p = Path(str(self.db_path) + suffix)
            if p.exists():
                os.chmod(p, 0o600)

    def authority_key(self) -> bytes:
        return bytes(self._key)

    def save_state(self, state: Mapping[str, Any]) -> None:
        cid = state.get('capsule_id')
        _require(isinstance(cid, str) and cid, 'CAPSULE_ID_INVALID')
        raw = _canonical(state)
        con=self._connect()
        try:
            with con:
                con.execute(
                    'INSERT INTO capsules(capsule_id,state_json) VALUES(?,?) '
                    'ON CONFLICT(capsule_id) DO UPDATE SET state_json=excluded.state_json',
                    (cid, raw),
                )
        finally:
            con.close()

    def load_state(self, capsule_id: str) -> dict[str, Any] | None:
        _require(isinstance(capsule_id, str) and capsule_id, 'CAPSULE_ID_INVALID')
        con=self._connect()
        try:
            row = con.execute('SELECT state_json FROM capsules WHERE capsule_id=?', (capsule_id,)).fetchone()
        finally:
            con.close()
        if row is None:
            return None
        try:
            value = json.loads(row[0])
        except Exception as exc:
            raise AuthorityStoreError('CAPSULE_STATE_JSON_INVALID') from exc
        _require(isinstance(value, dict), 'CAPSULE_STATE_OBJECT_REQUIRED')
        return value

    def list_capsule_ids(self) -> list[str]:
        con=self._connect()
        try:
            rows = con.execute('SELECT capsule_id FROM capsules ORDER BY capsule_id').fetchall()
        finally:
            con.close()
        return [str(row[0]) for row in rows]
