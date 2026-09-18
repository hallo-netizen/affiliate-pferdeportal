# KONZEPT 0 — REKONSTRUIERTE SCHRITT-FÜR-SCHRITT-STEUERUNG

## Grundprinzip — hart belegt

Das System vom 28.08.2026 war keine freie Textproduktion.

Die Steuerung war:

1. ROOT `PFERDE_ATELIER_START_HERE.json` lesen.
2. hashgebundenen `CURRENT_STATE.json` lesen.
3. ausschließlich `NEXT_ALLOWED_STEP` akzeptieren.
4. genau diesen Schritt ausführen.
5. Ergebnis prüfen.
6. Nur bei PASS darf der Controller den Zustand auf den nächsten Schritt setzen.
7. BLOCKED bleibt BLOCKED; kein Ersatzschritt, kein Seitensprung, kein Raten.
8. Bereits hashgebundene unveränderte PASS-Stufen dürfen wiederverwendet werden.
9. Innerhalb eines freigegebenen Blocks keine Chat-Zwischenstopps.
10. Kein Auto-Publish.

Diese Steuerlogik ist direkt durch STARTMASTER0102/0103 belegt.

## Artikelkette — rekonstruierter Abhängigkeitsweg

Die folgenden Artefakte/Stufen sind für den erfolgreichen 6er-Lauf nachweislich beteiligt. Die Reihenfolge wird dort, wo keine einzelne Original-Steuerdatei erhalten ist, aus ihren zwingenden Abhängigkeiten rekonstruiert.

### K0-001 — Eingang / Autorität
**Belegstatus: ORIGINALPRINZIP BELEGT**

- ROOT lesen.
- CURRENT_STATE-Hash prüfen.
- NEXT_ALLOWED_STEP identisch in ROOT/State.
- Kein freier Workflowentscheid.

PASS -> K0-010.

### K0-010 — gebundenes READY-Item übernehmen
**Belegstatus: AUGUST-METADATEN BELEGT**

Für jeden Artikel bleiben Titel, Target-Keyword, Kategorie und gebundene Metadaten unverändert.

PASS -> K0-020.

### K0-020 — PASS-Reuse / Nullpunkt prüfen
**Belegstatus: DIREKT BELEGT**

- existiert ein exakt hash-identischer bereits freigegebener Artikelkörper, darf er wiederverwendet werden;
- andernfalls ist frische Fach-/Textarbeit zwingend.

Beim realen 6er-Test wurde für keinen der sechs Artikel ein wiederverwendbarer Artikelkörper gefunden.

REUSE_PASS -> K0-050.
FRESH_REQUIRED -> K0-030.

### K0-030 — frische Fachgrundlage / Fact-Pack
**Belegstatus: ARTEFAKT BELEGT, EXAKTE ALTE STEUERDATEI FEHLT**

STARTMASTER0102 dokumentiert ausdrücklich, dass für die sechs Artikel neue Fact-Packs benötigt wurden.

PASS -> K0-040.

### K0-040 — finalen Artikelkörper erstellen
**Belegstatus: FINALER ARTIKELKÖRPER ALS PFLICHTARTEFAKT BELEGT; AUTORENPROMPT STARTMASTER0086 NICHT WIEDERGEFUNDEN**

- Textmaschine/Fachregeln unverändert anwenden.
- kein Ersatz durch spätere Konzepte.
- Artikelkörper ist danach eingefrorener Kandidat für artikelabhängige Prüfungen.

PASS -> K0-050.

### K0-050 — LanguageTool 6.8 am finalen Text
**Belegstatus: DIREKT BELEGT**

- gepinnte LT-6.8-Abhängigkeit darf hashgebunden wiederverwendet werden;
- die konkrete Prüfung muss für jeden finalen Artikel neu erfolgen.

PASS -> K0-060.
FAIL -> lokale Textkorrektur -> erneut K0-050.

### K0-060 — Produktionspaket bilden
**Belegstatus: DIREKT BELEGT**

Erforderliche gebundene Komponenten umfassen mindestens:
- Fact-Pack-Bundle,
- Produktionsplan,
- Workflow-Release/Qualitätsbelege,
- Hashbindungen.

PASS -> K0-070.

### K0-070 — Paketgrenze / Preflight
**Belegstatus: STARTMASTER0039 DIREKT BELEGT; 0103-PREFLIGHT AB ENDE DES 6ER-LAUFS ZUSÄTZLICH BELEGT**

- STARTMASTER0039-Paketgrenze muss PASS sein.
- Kategorie-Name, Slug, Taxonomy und Quelle müssen korrekt gebunden sein.
- Scope/plan_slot/Release/Hashes fail-closed prüfen.

PASS -> K0-080.

### K0-080 — PSERC Workflow Supervisor
**Belegstatus: ERFOLGREICHER 6ER-LAUF DIREKT BELEGT**

Supervisor-Freigabe muss PASS sein.

PASS -> K0-090.

### K0-090 — PSERC -> PPM Bridge
**Belegstatus: ERFOLGREICHER 6ER-LAUF DIREKT BELEGT**

Bridge muss tatsächlich ausgeführt werden.

EXECUTED -> K0-100.

### K0-100 — PPM 6.7.9 Normal Draft
**Belegstatus: ERFOLGREICHER 6ER-LAUF DIREKT BELEGT**

Wichtig:
- ein vorgelagerter Paket-/Generator-PASS ist KEIN Normal-Draft-PASS;
- der echte PPM-Normal-Draft-Pfad einschließlich Kategorieidentität muss laufen.

PASS -> K0-110.

### K0-110 — Draft Readback
**Belegstatus: ERFOLGREICHER 6ER-LAUF DIREKT BELEGT**

WordPress-Draft nach Erstellung wieder einlesen und Identität/Inhalt prüfen.

PASS -> K0-120.

### K0-120 — Nutzerprüfung / Ende ohne Publish
**Belegstatus: DIREKT BELEGT**

Der reale 6er-Lauf endete in:
`USER_CONTENT_REVIEW_6_DRAFTS_17123_17128_NO_PUBLISH`

Kein automatisches Publish.

---

## Was noch fehlt

Der größte fehlende Originalbaustein ist nicht die Ablaufsteuerung, sondern die konkrete alte **Autor-/Textmaschinenanweisung STARTMASTER0086** bzw. deren vollständige Originaldatei.

Daher ist die Steuerung jetzt rekonstruierbar, aber die Autorenstufe K0-040 muss bis zum Fund/Beweis von STARTMASTER0086 als **rekonstruiert** gekennzeichnet bleiben.
