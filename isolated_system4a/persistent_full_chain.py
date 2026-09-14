from __future__ import annotations

from typing import Any

from full_chain import FullChainSupervisor, _require
from persistent_capsule import PersistentCapsuleController
from system4_readonly import System4ReadOnlyChecks


class PersistentProductionFullChainSupervisor(FullChainSupervisor):
    """Production FullChain using the same orchestration with supervisor-only durable capsule state."""

    def __init__(self, authority_store: Any) -> None:
        _require(callable(getattr(authority_store, 'authority_key', None)), 'AUTHORITY_STORE_INVALID')
        _require(callable(getattr(authority_store, 'save_state', None)), 'AUTHORITY_STORE_INVALID')
        _require(callable(getattr(authority_store, 'load_state', None)), 'AUTHORITY_STORE_INVALID')
        self._authority_store = authority_store
        super().__init__(mode='production')

    def _activate_production_backend(self) -> None:
        _require(self._mode == 'production', 'PRODUCTION_BACKEND_MODE_REQUIRED')
        _require(not self._started, 'PRODUCTION_BACKEND_AFTER_START_FORBIDDEN')
        if self._controller is None:
            checks = System4ReadOnlyChecks()
            self._checks = checks
            self._controller = PersistentCapsuleController(
                self._authority_store.authority_key(),
                checks,
                self._authority_store,
            )
