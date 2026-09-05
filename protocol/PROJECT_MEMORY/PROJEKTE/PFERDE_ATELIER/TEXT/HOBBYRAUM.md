# TEXT – HOBBYRAUM

STAND: 2026-09-05
STATUS: AKTIV / NORMALER TEXT-ARBEITSCHAT – INTERNES SIGNIERKONZEPT SCOPE-PASS / GESAMTREGRESSION AUSSTEHEND

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
Auf exakt dem aktuellen Hobbyraum-Head den **bestehenden** M01–M33-Runner ausführen. Nur den ersten echten FAIL bearbeiten. Danach erneut derselbe Runner; erst nach M01–M33 + `hardlock` + `hardlock-base` darf Hobbyraum-PASS behauptet werden. Ein echter 7/7-Lauf bleibt der Livebeweis.

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
`7990029428399e8ba01d88a6543ce068812e9218`

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
- GitHub `hardlock` und `hardlock-base` auf Head `7990029…`: PASS.
- **SCOPE-PASS internes Signierkonzept:** aktiver Call-Graph bis 107007 ohne ED25519-/Signer-/Key-/`SIGNED`-Pflicht; gebundenes H8-Paket `WORKFLOW_SUPERVISOR_RELEASE_V2_HASH_BOUND` ohne Signaturfelder; Host-Signer erscheint erst im 107008-Endzustand.
- **Noch nicht ausgeführt/belegt:** kompletter M01–M33-Lauf auf Head `7990029…`.
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

