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
Solange Codex nicht verfügbar ist: ausschließlich READ-ONLY-Altlasten-/Abhängigkeits-Audit des aktiven technischen 107007/107008-Unterbaus gegen Fehlerhistorie, Zielvertrag und Schutzliste. Keine Produktionsreparatur auf Verdacht, kein neuer Runner/Workflow/Gate/Executor, kein Merge. Danach bleibt der nächste technische Übergang die bewusste Integrationsentscheidung für PR #140; erst nach regulärer Übernahme auf `main` darf der bestehende produktive 7/7-Liveweg gestartet werden.

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
- **ZWISCHENTEST INTERN/EXTERN: PASS im belegten Umfang.** Internes unsigniertes HASH_BOUND-Paket + aktuelle H8-Provenance PASS; fehlende, falsche oder nicht-current H8-Provenance wird fail-closed blockiert; Qualitätsstufen inkl. Link/Tabelle/PPM unverändert; externe ED25519-Positiv-/Negativprüfung PASS. **Nicht stärker behaupten:** Ein kombinierter Angreifer-Test „Herkunft manipuliert + alle normalen Hashes passend neu berechnet“ ist im aktuell dauerhaft auffindbaren Testbestand nicht vollständig als eigener End-to-End-Negativtest belegt.
- **M01–M33 GESAMT PASS:** vorhandener Runner real ausgeführt gegen den Quellstand `3ed31aa…`; M01–M33 PASS, `LAST_REGRESSION PASS`, `GESAMT PASS`.
- M15-Negativtest enthielt einen Escape-/Zeilenumbruchfehler; ausschließlich dieser Testfehler wurde KISS in Commit `3ed31aa78978a2098f324eead6f2a5335a10e2d4` korrigiert. Der dokumentierte vollständige M01–M33-Re-Run erfolgte auf genau diesem Quellstand und endete PASS.
- **B06 gilt hart:** Hobbyraum-/PR-Head ist kein Live-/7/7-Testort; Production Preflight verlangt current `main`.
- Kein Live-7/7-PASS behauptet.

## Integrations-/Fehlschlag-Sicherheitsplan für PR #140

Solange PR #140 nicht ausdrücklich freigegeben ist: **kein Merge**.

Falls später ausdrücklich integriert wird:
1. Vorherigen `main`-Anker unverändert dokumentieren: `c8a96e7a2f598de69134d90b143257c3559bc98a`.
2. Regulär integrieren; kein paralleler Umbau.
3. Auf dem neuen current `main` zuerst bestehende Identitäts-/Preflight-Prüfung.
4. Danach **genau der bestehende produktive 7er-Lauf**; keine neue Canary-Route und kein alternativer Runner.
5. Beim **ersten realen Blocker sofort stoppen** und nur diesen gegen Fehlerhistorie/Zielvertrag analysieren.
6. Kein automatischer Rückbau. Falls der Merge selbst als Ursache belegt wird, ist der Merge-Commit gezielt reversierbar; Rücknahme nur mit ausdrücklicher Nutzerfreigabe.
7. Keine Aussage „PR #140 gelöst“, bevor echter 7/7 + 107008 auf demselben produktiven Stand belegt ist.

Damit wird die B06/B14-Testlücke nicht wegbehauptet, sondern operational begrenzt: Vor Merge nur Regression/Scope; nach Merge erster echter Live-Beweis mit klarer Rückkehrgrenze.

## Harte Altlasten-/Rückbau-Prüfung

Vor jedem Rückbau im aktiven TEXT-/STARTMASTER-Weg zwingend:

1. **Mikro:** Kandidat positiv/negativ prüfen; konkrete Funktion und Fehlerwirkung trennen.
2. **Abhängigkeiten:** direkte und indirekte Nutzer, Hashbindungen, Übergaben, Receipts und spätere Schritte prüfen.
3. **Fehlerprotokoll-Gegencheck:** die vollständige autoritative Fehlerquelle über FEHLERREGISTER lesen und ausdrücklich prüfen, welcher historische Fehler/Fix durch den Rückbau wieder geöffnet werden könnte.
4. **Schutzliste:** Textmaschine/Fachregeln, externe-Link-Regel, Tabellenstufe, LanguageTool, echter PPM 6.7.9, PSERC/PSTE, Dubletten/Kannibalisierung, SEO, Design, Publish-Sperre, Hash-/Herkunftsbindung und externe Signierung ab 107008 dürfen nicht verloren gehen oder gelockert werden.
5. **Makro:** vollständigen bestehenden Regressionstest auf demselben Kandidatenstand ausführen. Lokaler PASS allein reicht nicht.
6. **Realitätsgrenze:** Regression-PASS bleibt ausdrücklich kein Live-/7/7-PASS.

**Fail-closed:** Ist Notwendigkeit, Seiteneffekt oder historischer Fehlerbezug nicht belastbar geklärt, wird nicht zurückgebaut.
**KISS:** immer nur ein kausal abgegrenzter Kandidat; keine Sammel-Aufräumaktion.

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

**Paul-Pipeline-Prüfkarte:** `PAUL_PIPELINE_AUDIT_20260906.md` – priorisiert direkte Gate-/Vertragskollisionen gegenüber späteren WordPress/Public-Folgethemen.

## Altlasten-Audit – Zwischenstand 2026-09-06

**Noch kein zusätzlicher Rückbau freigegeben.**

Geprüft:
- `m.DUAL = SELF`: bewusster KISS-Kompatibilitätskleber zur Wiederverwendung der bestehenden Room-Bridge; löst/umgeht alte DUAL-Fachlogik. **BEHALTEN.**
- alte Recovery-/Existing-Article-Logik im `STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py`: im heutigen Current-Action-Workerpfad nicht aktiv. **Kein aktueller Fehlerverursacher; nicht anfassen.**
- `PPM679_PACKAGE_ZIP` / `PSERC_FIX_ZIP` Env-Overrides: Repo-Fallback + exakte SHA-Bindung vorhanden; kein belegter aktueller Fehler durch den Override. **Verdacht allein reicht nicht; nicht entfernen.**
- `test_fachworkflow_proof_handoff.py`: gegenüber dem seit 05.09. zwingenden realen `ppm679_binding` stale und nicht Bestandteil des aktuellen M01–M33-/PR-Beweises. **Testballast/Testlücke, kein aktiver Produktionsblocker.**
- B01-ID-Pflicht: numerische ID wurde erst mit dem realen PPM-Handoff am 04.09. als technische Vorbedingung eingeführt; historischer Kategorie-Hardlock verlangt Name + Slug + Taxonomy. #140 entfernt nur diese vorgezogene Produktionsvoraussetzung und nutzt eine Seed-ID ausschließlich im isolierten PPM-Testzustand. **Kausal begründeter Kandidat; Live-Beweis weiterhin offen.**

Konsequenz:
Bis zu einem neuen echten Live-Lauf keine weitere technische Bereinigung auf Verdacht in PR #140 aufnehmen.

### 107008-/Abschlussweg-Audit 2026-09-06

- Delivery/Recovery-Persistenz (`chat_delivery_payload.py` → `recovery_sources/<batch>`) entstand als Reaktion auf den realen B13-Endstempel/Auth-/Persistenzfehler nach dem belegten 7/7+107008-PASS. **BEHALTEN.**
- Hostseitige PSERC-Signatur und GitHub-ENDSTEMPEL sind keine identische Doppelprüfung: Host signiert/verifiziert den fachlichen `workflow_release`; GitHub signiert später das persistierte 7-Artikel-Manifest. **BEHALTEN; externe Signiergrenze ist geschützt.**
- PPM-/PSERC-Runtimepakete sind auch in 107008 hashgebunden, obwohl dort kein neuer PPM-Lauf stattfindet. Das ist ein möglicher Vereinfachungspunkt, kann aber zugleich die Identität desselben produktiven Standes absichern. **Keine belegte Störung / kein Rückbau.**
- gzip/base64/Import-Envelope transportiert die bereits geprüften sieben Artikel und den hostseitig geprüften Release in die dauerhafte GitHub-Quelle; die Artikelbytes werden gegen Produktionsplan und Hashes gegengeprüft. **Kein belegter unnötiger Transportlayer.**

**Audit-Ergebnis:** Außer B01 und der bereits ausgeführten B15-Signierbereinigung ist aktuell keine weitere aktive Altlast kausal oder sicher entfernbar belegt.

### Paul-Architekturmodell – neuer READ-ONLY-Audit-Kandidat 2026-09-06

Paul hat **unseren realen System-/Workflowtyp mit unseren Plugins und Verträgen** in seiner Testinfrastruktur end-to-end durchgespielt; der Artikel „Duschhocker kaufen“ war nur ein beliebiger Testdatensatz. Die dokumentierten Findings sind deshalb als **direkte Befunde zu unserem System** zu behandeln, soweit sie den jeweils geprüften aktuellen Modulstand betreffen:

**Gate-/Vertragskollision:** Zwei für sich sinnvolle Module können gemeinsam unerfüllbar werden, wenn sie unterschiedliche Zustände desselben Artefakts erwarten oder ein Gate nicht exakt das Artefakt prüft, das später weitergegeben wird.

Direkter STARTMASTER-Befund:
- Fachvertrag: PASS-Reuse nur bei identischem, hashgebundenem Input/Vertrag.
- Aktueller Handoff prüft bei Nicht-PPM-Stufen `input_sha256` nur auf formale 64-Hex-Gültigkeit.
- Er erzwingt dort nicht mechanisch, welches konkrete Artefakt dieser Hash bezeichnet oder wie es mit Vor-/Nachstufe zusammenhängt.
- PPM ist enger: dort wird `input_sha256` ausdrücklich auf den finalen Artikel-SHA gebunden.
- derselbe lose Nicht-PPM-Hashcheck existierte bereits auf den belegten früheren 7/7-Ständen `d841ed…` / `de21f6…`; daher **kein Beleg als Ursache des aktuellen B01-Livefehlers**, sondern latente Architektur-/Paritätslücke.
- B01 selbst passt jedoch zur von Paul reproduzierten Fehlerklasse „Downstream-Gate verlangt ein Feld/einen Zustand, den der gültige Upstream-Vertrag nicht liefern soll“: numerische WP-ID vs. semantischer Kategorievertrag.

Nächster READ-ONLY-Prüfgegenstand:
Für die bestehende 12-Stufen-Kette je Stufe bestimmen:
1. welches konkrete Eingangsartefakt geprüft wird;
2. welcher Hash dieses Artefakt identifiziert;
3. ob die Stufe das Artefakt verändern darf;
4. welches Ausgangsartefakt entsteht;
5. welches nachfolgende Gate genau dieses Ergebnis konsumiert;
6. ob die technische Prüfung diese Übergabe wirklich bindet oder nur einen beliebigen formal gültigen Hash akzeptiert.

**Keine neue Architektur / kein neuer Runner.**
Ergebnis zuerst nur als Wirkungskarte. Erst ein konkret reproduzierter Vertragskonflikt darf Fehler-/Rückbaukandidat werden.

