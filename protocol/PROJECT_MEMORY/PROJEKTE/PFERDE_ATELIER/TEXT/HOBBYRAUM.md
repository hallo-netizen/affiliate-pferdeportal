# TEXT – HOBBYRAUM

STAND: 2026-09-06
STATUS: AKTIV / HOBBYRAUM-REGRESSION PASS / LIVE-PROOF ERST AUF MAIN MÖGLICH

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros TEXT.

**HIER BIST DU RICHTIG, WENN …**  
du den aktuell gebundenen TEXT/SEO-Arbeitsbereich, Branch und nächsten Schritt sehen musst.

**DU DARFST …**  
den aktuellen Auftrag und alle autoritativen Quellen lesen und ausschließlich im gebundenen Hobbyraum-Branch prüfen/reparieren.

**DU DARFST NICHT …**  
main verändern, zu Paul wechseln, Paul-Dateien/-Branch benutzen, einen neuen Workflow/Runner/Gate/Executor bauen oder Fach-/SEO-/Textmaschinenregeln verändern.

**ALS NÄCHSTES …**  
Keine weiteren Live-/7/7-Versuche aus dem Hobbyraum. Der Kandidat ist regressionsseitig geprüft. Nächster technischer Übergang ist ausschließlich die bewusste Integrationsentscheidung für PR #140; erst nach regulärer Übernahme auf `main` darf der bestehende produktive 7/7-Liveweg gestartet werden. Kein Merge ohne ausdrückliche Nutzerfreigabe.

## ARBEITSKONTROLLPUNKT – NUR DIE AKTUELLE ARBEIT

- **BÜROSTAND:** `CURRENT_STATE.md`
- **AKTUELLER AUFTRAG / NEXT ACTION:** ausschließlich diese `HOBBYRAUM.md`
- **CURRENT_BLOCKER:** nicht hier duplizieren → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → autoritative Quelle
- **AKTIVER ZIELVERTRAG:** nicht hier duplizieren → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`
- **NICHT ANFASSEN / WARUM:** Ziel-/Originalquelle + `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`

## Aktuelle Arbeitsbindung

Aktiver Arbeiter:
**normaler TEXT-Arbeitschat**

**Paul ist für diesen Auftrag tabu und nicht gebunden.**

Gebundener Hobbyraum-Branch:
`hobbyroom/b01-semantic-category-seed`

Draft-PR:
`#140`

Aktueller Arbeits-Head:
`3ed31aa78978a2098f324eead6f2a5335a10e2d4`

main bleibt unverändert:
`c8a96e7a2f598de69134d90b143257c3559bc98a`

## Aktueller Prüfstand

- B01-KISS-Fix bleibt enthalten: keine vorgezogene WordPress-ID im echten Produktionsplan; interne Seed-ID nur für den isolierten lokalen PPM-Testzustand.
- M15/M31 waren stale und wurden auf den aktuellen gebundenen Request-/Handoff-Weg korrigiert.
- M26/M28 waren ebenfalls noch auf den alten Direkt-Receipt-/Prepass-Weg ausgerichtet und wurden auf Request → realer PPM → erst danach PASS/Receipt korrigiert.
- **Interne Signieraltlasten wurden aus dem aktiven 107007-Vorlauf entfernt:** H8-Bootstrap, Provenance, Runtime-Guard, Codex-Preflight und das gebundene Generation-1-H8-Paket verlangen keine ED25519-Signatur, keinen Signer und keinen Schlüssel mehr. Herkunft/Integrität bleiben hash- und batchgebunden.
- M22/M23 wurden entsprechend auf H8-Provenance/Integrität statt interner Signatur ausgerichtet.
- **Unverändert:** Textmaschine, Linkregel, Tabellenstufe, LanguageTool, PPM, PSERC/PSTE, SEO/Design und Publish-Sperre.
- **Externe Signierung bleibt unangetastet:** hostseitige Finalisierung erst nach 107008 sowie GitHub-ENDSTEMPEL/WordPress-Verifikation.
- GitHub `hardlock` und `hardlock-base` auf Head `3ed31aa…`: PASS.
- **SCOPE-PASS internes Signierkonzept:** aktiver Call-Graph bis 107007 ohne ED25519-/Signer-/Key-/`SIGNED`-Pflicht; gebundenes H8-Paket `WORKFLOW_SUPERVISOR_RELEASE_V2_HASH_BOUND` ohne Signaturfelder; Host-Signer erscheint erst im 107008-Endzustand.
- **ZWISCHENTEST INTERN/EXTERN: PASS.** Internes unsigniertes HASH_BOUND-Paket + aktuelle H8-Provenance PASS; manipulierte H8-/Batch-Herkunft bleibt selbst nach Neuberechnung aller normalen Hashes BLOCKED; Qualitätsstufen inkl. Link/Tabelle/PPM unverändert; externe ED25519-Positiv-/Negativprüfung PASS.
- **M01–M33 GESAMT PASS:** vorhandener Runner real ausgeführt gegen den Quellstand `3ed31aa…`; M01–M33 PASS, `LAST_REGRESSION PASS`, `GESAMT PASS`.
- M15-Negativtest enthielt einen Escape-/Zeilenumbruchfehler; ausschließlich dieser Testfehler wurde KISS korrigiert und der komplette Runner danach erneut vollständig PASS ausgeführt.
- **B06 gilt hart:** Hobbyraum-/PR-Head ist kein Live-/7/7-Testort; Production Preflight verlangt current `main`.
- Kein Live-7/7-PASS behauptet.

## Single Writer

- Dieser normale TEXT-Arbeitschat ist für den aktuellen B01-Hobbyraumauftrag der einzige aktive technische Schreiber.
- Paul wird nicht benutzt.
- main wird nicht verändert.
- Andere Büros/Arbeitsbereiche bleiben unangetastet.
- Erst nach belastbarer Prüfung werden offizieller Stand und nächste Aktion weitergeschrieben.

## Globale Arbeitsort-Sperre

**Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.**

Autorität:
`protocol/PROJECT_MEMORY/BAUCONTAINER/EINGANGSSTANDARD.md` → **Backup-/Tresor-/Archiv-Sperre**.

