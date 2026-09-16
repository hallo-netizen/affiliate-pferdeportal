# PFERDE-ATELIER – PLUGINS – UPDATEPROTOKOLL

STAND: 2026-09-16
ROLLE: ZENTRALES PLUGIN-ÄNDERUNGS-/SYNC-PROTOKOLL

## Regel

Für jede tatsächliche Pluginentwicklung oder jedes tatsächliche Pluginupdate genau ein Vorgang:
`PU-YYYYMMDD-NNN`.

Pflichtfelder:
- Plugin-ID / Name
- ART: ENTWICKLUNG / UPDATE
- Herkunft: EIGENENTWICKLUNG / DRITTANBIETER
- zuständiges Fachbüro
- VON_VERSION / AUF_VERSION
- autoritative Quelle / Branch / Release
- WARUM
- Abhängigkeiten / Schnittstellen
- relevante Fehler-/Rollbackbelege
- tatsächlich ausgeführte Positivprüfung
- tatsächlich ausgeführte Negativprüfung, soweit erforderlich
- Fach-/Regressionstest
- Artefakt-Sync nach `SYNC_VERTRAG.md`
- Ergebnis: PASS / FAIL / ROLLBACK / BLOCKED

## Initialisierung 2026-09-13

Dieser Büroaufbau ist keine Pluginentwicklung und kein Pluginupdate.
Real synchronisiert/readback-geprüft wurden PPA-001, PPA-003, PPA-004, PPA-005, PPA-007. PPA-002 / PPA-006 / PPA-008 / PPA-009 waren BLOCKED.

## PU-20260915-001 – Pferde Atelier – Pferderassen Manager

- PLUGIN-ID: `PPA-011`
- NAME: `Pferde Atelier – Pferderassen Manager`
- ART: UPDATE
- HERKUNFT: EIGENENTWICKLUNG
- FACHBÜRO: `../WISSENSDATENBANK/AKTENSCHRAENKE/PFERDERASSEN/`
- VON_VERSION: `0.2.1`
- AUF_VERSION: `0.2.7`
- AUTORITATIVE TECHNISCHE QUELLE: `../WISSENSDATENBANK/AKTENSCHRAENKE/PFERDERASSEN/TECHNIK_PFERDERASSEN_MANAGER_CURRENT.md`
- RELEASEARTEFAKT: `PFERDE_ATELIER_PFERDERASSEN_MANAGER_0.2.7_INSTALLIEREN.zip`
- SHA-256: `5f72308cb922756cac8ffa2a01a27bfc7f1f1cfbabf6fbf5b4a33728fc8e58f1`
- POSITIV/NEGATIV/FACHREGRESSION: PASS laut gebundenem Fachbeleg
- WORDPRESS-LIVE: PASS, Nutzerbestätigung 2026-09-15
- ARTEFAKT-SYNC: PASS
- ERGEBNIS: **PASS**

## PU-20260915-002 – Pferde Atelier Design / Universal-Interaktion

- PLUGIN-ID: `PPA-002`
- NAME: `Pferde Atelier Design`
- ART: UPDATE / FEHLERREPARATUR
- HERKUNFT: EIGENENTWICKLUNG
- FACHBÜRO: `../DESIGN/`
- VON_VERSION: real installierter Ausgangsstand **UNGEKLÄRT**
- ERZEUGTE KANDIDATEN: `1.50.529`, danach `1.50.530`
- BETROFFENE ALLGEMEINE ABHÄNGIGKEIT: `Universal Portal Design Suite 2.2.42` / MOD-003
- AUTORITATIVE FEHLERQUELLE: `../DESIGN/FEHLERQUELLEN.md` → `DESIGN-LIVE-20260915-001`

WARUM:
Pagination sollte auf 16 Einträge, oben+unten, für Pferderassen/Glossar standardisiert werden; zusätzlich Glossar-Startlink und Standard-Hover der Zurück/Vor-Navigation. Die Regel sollte auch im allgemeinen Designplugin verankert werden.

REALER FEHLERBEFUND:
Nach Ausgabe/Installation im Änderungszug meldete der Nutzer, dass Pferderassen-Seite und Glossar nicht mehr auffindbar bzw. zerschossen sind.

TATSÄCHLICH BELASTBARE POSITIVPRÜFUNG:
**NICHT AUSREICHEND BELEGT.** Die im Chat behaupteten lokalen Prüfungen werden nicht als Abnahme übernommen, da kein reproduzierbarer autoritativer Gesamtbeleg der realen Plugin-Kombination vorliegt.

TATSÄCHLICH BELASTBARE NEGATIVPRÜFUNG:
**NICHT AUSREICHEND BELEGT.** Insbesondere war vor der Ausgabe nicht belastbar bewiesen, dass ein Ausfall von Pferderassen oder Glossar in der realen Kombination erkannt wird.

FACH-/REGRESSIONSTEST:
**FAIL / LIVE-REGRESSION.** Nutzer meldet realen Ausfall beider kritischen Seitenwelten.

ARTEFAKT-SYNC:
**BLOCKED.** 1.50.529/1.50.530 dürfen `CURRENT.zip` nicht ersetzen. Für Universal 2.2.42 darf ebenfalls kein freigegebener allgemeiner CURRENT-Status aus diesem Vorgang abgeleitet werden.

NEXT ACTION:
Installierte Versionen beider Designplugins frisch bestimmen → exakte Kombination reproduzieren → Positiv/Negativ/Kombinationsregression für Pferderassen + Glossar → Ursache isolieren → minimaler Fix → ZIP/Version/Install-over-old → realer WordPress-Readback → erst dann Artefaktsync.

ERGEBNIS: **BLOCKED**

## PU-20260916-001 – WordPress Speicheranalyse

- PLUGIN-ID: `PPA-014`
- NAME: `WordPress Speicheranalyse`
- ART: UPDATE
- HERKUNFT: EIGENENTWICKLUNG; Ausgangsinstaller 1.0.1 vom Nutzer bereitgestellt
- FACHBÜRO: `../TECHNIK/`
- VON_VERSION: `1.0.1`
- AUF_VERSION: `1.1.0`
- AUTORITATIVE TECHNISCHE QUELLE: `../TECHNIK/CURRENT_STATE.md` + bereitgestellte 1.0.1-Basis + daraus erzeugter 1.1.0-Quellstand
- WARUM: Der Speicher-Scan belegt rund 5,15 GB physische WPvivid-Backupdateien, von denen die WPvivid-Oberfläche nur einen Teil zeigt. Ohne FTP/SSH wird ein eng begrenzter, sichtbarer Löschweg im bestehenden Diagnoseplugin benötigt.
- ABHÄNGIGKEIT/SCHNITTSTELLE: ausschließlich WordPress-Admin + `wp-content/wpvividbackups/`; keine WPvivid-API-Manipulation
- FEHLER-/ROLLBACKGRENZE: kein Auto-Delete; bei WordPress-LIVE-Problem bleibt 1.0.1 die bekannte Ausgangsversion
- POSITIVPRÜFUNG: reguläre Datei im erlaubten WPvivid-Ordner listen/löschen PASS
- NEGATIVPRÜFUNG: Pfadtraversal PASS; Symlink PASS; Datei außerhalb des erlaubten Ordners PASS
- FACH-/REGRESSIONSTEST: bestehende Analysefunktion im Quellstand unverändert fortgeführt; PHP-Syntax PASS; ZIP-Integrität PASS
- ARTEFAKT: `/Campus-Plugins/PFERDE_ATELIER/PPA-014/CURRENT.zip`
- SHA-256: `3acb62811ec8e7ea1940ec0968e5b51fc2cb0d1ae2f9e86eeeb6718c11873891`
- ARTEFAKT-SYNC: PASS
- WORDPRESS-LIVE: OFFEN – Installation/Bedienung und realer Re-Scan stehen aus
- ERGEBNIS: **BLOCKED bis WordPress-LIVE-Readback**, lokaler Kandidat und Artefaktsync PASS
