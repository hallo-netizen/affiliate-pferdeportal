from __future__ import annotations

import copy
from typing import Any

from capsule import CapsuleController, _require


class PersistentCapsuleController(CapsuleController):
    """Capsule controller with supervisor-only durable state.

    The workflow semantics stay in CapsuleController. This subclass only persists
    each already HMAC-sealed state and reloads it after a supervisor restart.
    """

    def __init__(self, authority_key: bytes, checks: Any, store: Any) -> None:
        _require(
            callable(getattr(store, 'save_state', None))
            and callable(getattr(store, 'load_state', None)),
            'STATE_STORE_INVALID',
        )
        self._authority_store = store
        super().__init__(authority_key, checks)

    def _reseal(self, state: dict[str, Any]) -> None:
        super()._reseal(state)
        self._authority_store.save_state(copy.deepcopy(state))

    def _state(self, capsule_id: str) -> dict[str, Any]:
        if capsule_id not in self._states:
            loaded = self._authority_store.load_state(capsule_id)
            if loaded is not None:
                self._states[capsule_id] = loaded
        return super()._state(capsule_id)
