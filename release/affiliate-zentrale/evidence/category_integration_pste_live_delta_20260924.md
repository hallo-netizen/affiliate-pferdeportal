# Kategorieintegration – PSTE Live-Delta 2026-09-24

Rolle: Evidence/Protokoll. **Keine zweite CURRENT-/NEXT-ACTION-Wahrheit.** Aktueller Status und genau eine NEXT ACTION stehen ausschließlich in `control/release-governance/CURRENT_RELEASE.json`.

## 1. Frischecheck vor dem Live-Delta

- Branch: `affiliate-release-current`
- geprüfter Head vor dieser Nachholung: `787d747410cfde5db1e8b86740c5103264725281`
- Workflow: `Category Integration Hard Baseline`
- Run: `35970840150`
- Ergebnis: **SUCCESS**
- Run-Head: `787d747410cfde5db1e8b86740c5103264725281`

Damit war der committed Kategorie-Stand vor dem späteren WordPress-/PSTE-Live-Delta belastbar grün.

## 2. Bereits geschlossene Live-Verbraucher in diesem Chat

### Template Kit 1.50.559
- Kategorie-/Breadcrumb-Map auf **1149/1149** nachgezogen.
- Main SHA256: `2e6571e27f72a751899c88a47c1ffce682bb03971ba5b88899a42f2009f0d509`
- Map SHA256: `db0e278e45c48a6ed586c360e98e142cae1aa05ff5f2f2b2e2d4c196378c720f`
- Dry-Run PASS -> genau ein Apply -> neuer Request -> Readback PASS.
- Receipt: `category-1149-manifest-20260924-065947-2cc6016faa02.json`

### Portal Production Center 1.1.1
- Strukturbindung auf **1149 Portal-Kategorien / 9 Journal-Kategorien / 5790 Slots** nachgezogen.
- Dry-Run PASS -> genau ein Apply -> Readback PASS.
- Danach Build-Integrity wegen alter Manifest-Hashes korrekt blockiert.
- Build-Manifest/Trust-Root sauber neu gebunden und Ed25519-signiert; Schutz nicht abgeschaltet.
- finaler Build-Integrity-Readback: **PASS**
- Manifest SHA256: `09e3b29ea05cd89a470ca82a003bb1d65fb8c7435a73baf048525bc1070d6782`
- Signing key id: `ppc111-ed25519-5dd62b91470e1fc9`
- Receipt: `final-integrity-20260924-073634.json`

### übrige fünf Restverbraucher
Read-only Vollquell-Audit:
- Allgemeine Bildzentrale 2.7.6: keine statische Vollkopie der Kategorien.
- Portal Link Policy Runtime Verifier 1.0.0: keine statische Vollkopie.
- Portal Production Link Policy Gate 1.0.1: dynamischer/source-getriebener Kategoriepfad; keine Vollkopie mit 1149er Delta.
- Portal Category Structure Repair Guard 1.0.1: absichtlicher kleiner Repair-Vertrag, keine Vollkopie.
- Portal Production Center 1.1.1: war der einzige verbleibende echte 1124-Hardlock und wurde wie oben geschlossen.

## 3. PSTE-Live-Delta

### Ausgangspunkt / Fallback
Originaler, früher real E2E-geprüfter PSTE-0.57.6-Basisinstaller:
- Version: **0.57.6**
- vollständiger Pluginbaum: 131 Dateien
- SHA256: `71bae2436fc1c3d52c06cefe551517af32a89eeb005457331e2c44136a1c888f`
- Rolle: exakter E2E-Baseline-Rollback.

### 0.57.8 live beobachtet
Im Live-Backend wurde danach **Portal SEO Themenengine 0.57.8** angezeigt.
Die Aktion `Gesamtbestand neu erfassen` endete live mit:
- **Gesamtbestand erfasst.**

Damit ist der frühere WordPress-"kritischer Fehler" auf diesem konkreten Capture-Pfad im beobachteten 0.57.8-Lauf nicht erneut aufgetreten.

Direkt danach blockierte die Übersicht jedoch mit:
`PSTE_ADMIN_ANALYTICS_DATASET_TOO_LARGE_USE_FILTERED_THEMENPRUEFUNG`

Das ist kein WordPress-Fatal, aber ein zu grob platzierter neuer Schutzblocker.

Lokales 0.57.8-Paket:
- SHA256: `f2f4f9b4e09d3bb8301f12a3aee1f75e56d3a9f7cc2a750c525f62456367b6c7`
- 131 Dateien (+ 4 ZIP-Verzeichniseinträge)
- enthält die 1149er Kategorienableitung.

### 0.57.9 lokaler Kandidat – NICHT installiert
Ein lokaler Nachfolgekandidat wurde gebaut, um die zu grobe Large-Dataset-Admin-Sperre enger zu setzen:
- Version: **0.57.9**
- SHA256: `93cf1adc0a4d0e0a5b10e29bb9025d2b165210fe278c389254343fd5f3a6a2cd`
- 131 Dateien
- Status: **LOCAL CANDIDATE ONLY / NICHT INSTALLIERT**

WICHTIG:
Dieser Kandidat adressiert den Admin-Large-Dataset-Renderpfad, aber der danach belegte Kategorieauflösungsfehler ist darin noch **nicht** nachgewiesen behoben. Deshalb **0.57.9 derzeit nicht installieren**.

## 4. Neuer harter Blocker – Kategorieauflösung der Keywordrecherche

Direkt aus dem im aktuellen Chat bereitgestellten Keyword-Export, ohne Bibliothek ausgewertet:

- Ergebniszeilen mit Status: **500**
- `BLOCKED_FOR_CATEGORY`: **496**
- `AUTO_RESOLVED`: **4**
- Vorkommen `pferdesaettel`: **0**
- Vorkommen `trensen`: **0**
- Vorkommen `offenstallbau`: **0**
- Vorkommen `paddockbau`: **0**
- Vorkommen `reitplatzbau`: **0**

Zusätzlich werden auch bekannte Altziele blockiert, z. B.:
- `Beratung Gebisse`
- `Beratung Hafer`
- `Beratung Winterdecken`
- Journal-Ziele wie `Pferdegesundheit verstehen` und `Pferdewissen & Grundlagen`

Nur einzelne alte Ziele werden `AUTO_RESOLVED`.

Damit ist der Fehler **nicht** nur "25 neue Kategorien fehlen". Die PSTE-Kategorieauflösung/Zuordnungslogik ist im aktuellen Live-/Exportzustand allgemein unvollständig oder falsch gebunden.

Die exakte technische Ursache ist **noch nicht bewiesen**. Nicht raten.

## 5. PSERC / Linkrefresh / E2E

PSERC 0.28.23 hatte vor diesem Live-Delta weiterhin einen Metadatenstand mit 1124 Kategorien. Der 25er-Dynamic-Gate-Pfad selbst war bereits PASS.

Solange PSTE die Kategoriezuordnung nicht korrekt auflöst:
- **kein PSERC-Finalrefresh**
- **kein Linkregistry-Finalrefresh**
- **kein Gesamt-Kategorie-E2E**
- **keine finale Produktionsfreigabe**

Diese Schritte bleiben nach der PSTE-Reparatur offen.

## 6. Exakter nächster technischer Schritt

**Nur lokal / read-only gegen den exakt beobachteten 0.57.8-Stand und den 500-Zeilen-Export:**

1. Den Codepfad bestimmen, der `BLOCKED_FOR_CATEGORY` erzeugt.
2. Für mindestens einen blockierten Altfall und alle fünf neuen Familien die Kategorieauflösung Schritt für Schritt gegen die 1149er Map/Live-Baseline nachvollziehen.
3. Positivtest: bekannte alte Kategorie muss wieder korrekt auflösen.
4. Positivtest: jede der fünf neuen Familien muss ihre neuen Kategorien finden.
5. Negativtest: tatsächlich unbekannte/fremde Kategorie bleibt fail-closed.
6. Erst nach reproduziertem Ursachenfix einen **einzigen konsolidierten PSTE-Kandidaten** bauen, der den noch nicht live installierten 0.57.9-Adminfix und den Kategorie-Resolver-Fix gemeinsam enthält.
7. Vor Live-Installation: ZIP/Version/SHA + lokale Regression + sicherer 0.57.6-Rollback bestätigen.

**Keine weitere Live-Aktion und 0.57.9 nicht installieren, bis dieser lokale Ursachenfix PASS ist.**

## 7. Fehlernachtrag

### Fehler Z – PSTE 0.57.6 Gesamtbestand konnte im Live-Backend kritisch abbrechen
Die alte synchrone Baseline-Erfassung hatte große ungebremste Datenmengen in einem Request. Daraufhin wurden lokale Stabilitätsänderungen vorbereitet. Der beobachtete 0.57.8-Live-Lauf konnte `Gesamtbestand neu erfassen` erfolgreich abschließen.

### Fehler AA – Schutzbremse 0.57.8 zu grob
Nach erfolgreichem Gesamtbestand blockierte die Übersicht mit `PSTE_ADMIN_ANALYTICS_DATASET_TOO_LARGE_USE_FILTERED_THEMENPRUEFUNG`.
Ein lokaler 0.57.9-Kandidat setzt diese Large-Dataset-Verarbeitung enger/batchweise um; **nicht installiert**.

### Fehler AB – Keyword-Kategorieauflösung weiterhin massiv blockiert
500-Zeilen-Export: 496 `BLOCKED_FOR_CATEGORY`, nur 4 `AUTO_RESOLVED`; die fünf neuen Familien 0× vorhanden.
Ursache noch offen. Das ist der **erste aktuelle Blocker**.

## 8. Nicht anfassen

- keine erneute Template-Kit-Korrektur
- kein erneuter Production-Center-Apply
- keine bereits geschlossenen Affiliate-/PPM-/PSTE-Map-Hardtests wiederholen
- kein PSERC-/Link-/E2E-Abschluss vor PSTE-Resolver-PASS
- keine Texte/Design-/Provider-/Ranking-/Bannerarbeit
- keine Bibliothek als Quelle
