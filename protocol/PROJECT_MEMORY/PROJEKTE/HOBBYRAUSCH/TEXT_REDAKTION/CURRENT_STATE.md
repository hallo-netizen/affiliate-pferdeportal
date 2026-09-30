# HOBBYRAUSCH – TEXT_REDAKTION – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-30
STATUS: PSTE 0.57.14 EDITORIAL OWNERSHIP GATE LOKAL HARD PASS / LIVE-ABNAHME OFFEN

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_TEXT_REDAKTION`.

## Aktueller belastbarer Stand

Hobby Depot übernimmt keine Pferde-Atelier-Fachbestände. Verwendet wird ausschließlich der allgemeingültige technische PSTE-Kern als Basis.

Exakte Basis:
`PSTE 0.57.13 DATABASE_STORAGE_CLEANUP_PERFORMANCE_COMPAT_RECHECK_HARD_PASS`

Aktueller Entwicklungskandidat:
`PSTE 0.57.14 EDITORIAL OWNERSHIP GATE`

Installer:
`PSTE-0.57.14-EDITORIAL-OWNERSHIP-GATE_HARD_LOCAL_PASS.zip`

SHA-256:
`3c0d39011911a7d663adc35dad8724f81dacf671c4b971d4719e221928345871`

## Was V0.57.14 ergänzt

- liest den allgemeinen `APKW_EDITORIAL_INTENT_OWNERSHIP_HANDOFF_V1` read-only;
- bindet Artikelkandidaten an `owner_concept_id`;
- verlangt einen `semantic_intent_key` vor Artikelpromotion;
- gleicher semantischer Intent darf nicht mehrfach vergeben werden;
- bestehende exakte Duplicate-/Answer-Equivalent-Prüfung bleibt aktiv;
- Frageform besitzt ausdrücklich keine FAQ-/Kategorie-Owner-Autorität;
- kein Erzeugen/Umbenennen von Kategorien;
- keine Text-/Designregel verändert.

Damit kann z. B. eine Frage wie `Was kostet Buchbinden?` dem Owner `Einstieg` gehören, ohne wegen der Frageform automatisch als FAQ behandelt zu werden.

## Veränderungsfläche gegen 0.57.13

Exakt 6 Dateien:
- ADD `contracts/upstream-editorial-ownership-v1.json`;
- MOD `includes/class-pste-admin.php`;
- ADD `includes/class-pste-article-ownership-gate.php`;
- MOD `includes/class-pste-compiler-read-capability.php`;
- MOD `portal-seo-topic-engine.php`;
- MOD `uninstall.php`.

Alle anderen Dateien der 0.57.13-Basis bleiben byte-identisch.

## Lokale harte Prüfung

- gezielte Ownership Positiv/Negativ: 10/10 PASS;
- Fresh-Unpack Ownership: 10/10 PASS;
- Fresh-Unpack PHP-Lint: 79/79 PASS;
- Worktree ↔ Fresh-Unpack: 135/135 Dateien byte-identisch;
- Funktionserhalt außerhalb der 6 gezielten Dateien: PASS;
- unerwartete Änderungen: 0;
- WordPress-Write: keiner;
- Artikel-/Kategorieerzeugung: keine.

## Beleggrenze

V0.57.14 ist lokal hart geprüft, aber noch nicht auf einer echten Hobby-Depot-WordPress-Installation abgenommen.

## Erster offener Blocker

Kein Entwicklungsblocker mehr.

Offen ist die reale Abnahme zusammen mit dem V1.9.1-Kategorie-Handoff.

## NEXT ACTION

V1.9.1 Kategorie-Workflow live sauber zurückrollen/retesten und danach dessen Editorial-Handoff in PSTE 0.57.14 importieren.

Dann den Buchbinden-Pilot real prüfen:
- Owner-Kategorie;
- semantischer Intent;
- vorhandene/geplante Dublette;
- FAQ nur bei eigenständigem Restintent.
