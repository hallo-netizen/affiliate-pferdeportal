# V96 Workflow Lock

1. Bindende Basis für den nächsten Design-Arbeitsblock sind die V96-Master und die in `BASELINE_SHA256.txt` festgehaltenen Hashes.
2. Vor jeder weiteren Änderung muss `CURRENT_PLUGIN_SOURCE` vollständig gegen einen Fresh-Unpack des aktuellen Installers verglichen werden.
3. Eine Abweichung zwischen Master, Current Source, Installer oder GitHub-Baseline führt zu `BLOCKED`; es wird kein neuer Installer gebaut.
4. Journal-Root, Journal-Kategoriearchive und Einzelbeitragstabellen bleiben getrennte Scopes.
5. V96 verändert ausschließlich den Journal-Kategorie-Beitragskarten-Scope und die allgemeingültige Journal-Term-Entsprechung.
6. `main` bleibt unverändert; dieser Stand liegt nur auf `fix/table-rendering-contract-v94-20260821`.
7. Keine Live-Freigabe ohne Nutzersichtprüfung der installierten Pferde-Version 1.50.461.
