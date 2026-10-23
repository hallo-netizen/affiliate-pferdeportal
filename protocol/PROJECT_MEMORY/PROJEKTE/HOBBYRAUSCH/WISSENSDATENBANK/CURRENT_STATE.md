# HOBBYRAUSCH – WISSENSDATENBANK – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-22
STATUS: **HOBBYREGISTER 862/862 / SCHEMA 1.2 MIT 57 TRAITS VOLLSTÄNDIG KLASSIFIZIERT / VOLL-AUDIT PASS / SCHEMA F V1 FEST**

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_WISSENSDATENBANK`.

Fester Registervertrag:
`HOBBYREGISTER.md`

Eigenschaftsvertrag:
`HOBBY_EIGENSCHAFTEN_SCHEMA_1_2_DELTA.md`

Register-Seitenvertrag:
`HOBBYREGISTER_SCHEMA_F_V1.md`

Textvertrag:
`HOBBYREGISTER_TEXTREGELN_V1.md`

Design-/Referenztransfer:
`HOBBYREGISTER_REFERENZTRANSFER_V1.md`

## Zentraler Hobbybestand

- **862** kanonische Hobbyidentitäten;
- **57** Eigenschaften in 8 Gruppen;
- **862/862** Hobbys mit **57/57** klassifizierten Traits;
- **862/862** Hobbys mit **4/4** Kurzprofilfeldern;
- Aliasnamen erzeugen keine zweite Hobbyidentität.

Die bisherigen 54 Traits wurden bei der Erweiterung nicht verändert.

## Schema 1.2 – Abschluss 2026-10-22

Neu vollständig klassifiziert:
1. `equipment_maintenance` – Pflege / Wartung der Ausrüstung;
2. `strength_need` – Kraftbedarf;
3. `coordination_balance_need` – Koordination / Balance inkl. Hand-Auge-/Ganzkörperkoordination.

Ergebnis:
- neue Einzelwerte: **2.586/2.586**;
- alte Traitwerte geprüft: **46.548**;
- alte Traitwerte verändert: **0**;
- eindeutige Registry-IDs: **PASS**;
- 57/57 Traits je Hobby: **PASS**;
- ungültige neue Werte: **0**;
- UNKNOWN bei neuen Traits: **0**;
- Gesamtprüfung: **PASS**.

Vollaudit:
`EVIDENCE/HOBBY_SCHEMA12_FULL_862_AUDIT_20261022.json`

Exakte neue Traitwerte:
- `EVIDENCE/HOBBY_SCHEMA12_VALUES_PART_01.json` – 216 Hobbys;
- `EVIDENCE/HOBBY_SCHEMA12_VALUES_PART_02.json` – 216 Hobbys;
- `EVIDENCE/HOBBY_SCHEMA12_VALUES_PART_03.json` – 216 Hobbys;
- `EVIDENCE/HOBBY_SCHEMA12_VALUES_PART_04.json` – 214 Hobbys.

GitHub-Readback:
- **862** Zeilen;
- **862** eindeutige Registry-IDs;
- **0** Dubletten;
- alle zulässigen Wertemengen vollständig geprüft.

Bestehender 54er Register-SHA:
`4deb4be2b235db450d58f02485ec40e780fc2671f9dfc6edf8cbbba0f738af78`

Geprüfter zusammengeführter 57er Kandidat:
`05fc1c5d7ab9282a43de2b43372c378f629fac4b71c98b78fe1bec00a4f46179`

Geprüftes Schema 1.2:
`c4e2dc719ee7b017f0da9de08bfa2251124cbbb61894dad42afad1ce758ba68a`

## Schema F V1

Schema F ist fest und gilt für alle 862 Hobbys.
Die 57 Merkmale werden als strukturierte Grundlage für verständlichen Fließtext, Vergleichsblock und ähnliche Hobbys verwendet; keine 57-Felder-Wand.

## Hobbyfinder

Der bestehende 8-Schritte-Hauptfunnel bleibt unverändert funktionsfähig.
Die drei neuen Traits stehen zusätzlich für Feinfilter, Vergleich und Schema F zur Verfügung.

## Frontend-Prototyp 2026-10-23

HD-007 1.1.1 ist lokal als read-only Registerprototyp HARD PASS:
- vollständige 862er Übersicht;
- Suche/A–Z/acht Icon-Gruppen;
- virtuelle Profile;
- 862/862 Detailprofile mit acht nichtleeren Schema-F-Fließtextabschnitten;
- Buchbinden und Slacklining bleiben die redaktionell ausformulierten Musterprofile.

Die physische Runtime-Basis bleibt hash-identisch bei 54 Basistraits. Die drei Schema-1.2-Zusatztraits werden nur dort ausgegeben, wo sie in HD-007 bereits explizit gebunden sind; keine Werte werden geraten.
Vor dem finalen 57/57-Rollout muss HD-007 die vollständige geprüfte Schema-1.2-Laufzeitprojektion binden.

## EXAKT EINE NEXT ACTION

**HD-007 1.1.1 live auf Register-Startseite und mehrere normale Detailprofile abnehmen. Danach die vollständige 57er Laufzeitprojektion binden und die 862 Hobbys gegen CORE-/Hauptseiten auf SEO-Owner mappen; im Zweifel gewinnt CORE.**
