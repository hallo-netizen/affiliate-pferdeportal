# P34 – FINALER PROTOTYP-GO / KISS-ZIELBILD

Datum: 2026-09-08
Status: PROTOTYP GO – NOCH KEINE PRODUKTIONSFREIGABE

## Wichtigste KISS-Regel

P0–P34 sind PRÜF- UND BEWEISAKTEN.

Sie sind NICHT:
- 34 Produktionsstufen
- 34 neue Gates
- 34 neue Worker
- eine neue Raumarchitektur

Im späteren Echtbetrieb soll daraus genau EIN einfacher Weg entstehen.

## Das Zielbild

```
bestehender Chat/Codex-Start
        |
        v
EINE zentrale deterministische Zustandsmaschine
        |
        v
bestehender gebundener Fachworkflow
(Textmaschine / PSTE / PSERC / PPM unverändert in ihrer Zuständigkeit)
        |
        v
PPM prepare() – noch KEIN WordPress-Write
        |
        v
EINE externe Signatur
        |
        v
Signatur + Hash + exakter Prepared-Payload verifizieren
        |
        v
WordPress DRAFT schreiben
        |
        v
Readback + Rendered-DOM/Style-Prüfung
        |
        v
STOP: AWAITING USER REVIEW / publish_allowed=false
```

## Was die Zentralmaschine darf

Nur:
- feste Reihenfolge besitzen
- genau einen kanonischen Jobzustand besitzen
- genau das nächste gebundene Item/Mikroschritt freigeben
- PASS oder BLOCKED fortschalten

Nicht:
- Texte bewerten
- SEO frei entscheiden
- Regeln verändern
- Reparaturwege wählen
- Worker auswählen
- alternative Übergaben bauen
- publishen

## Was NICHT neu gebaut wird

- kein neuer Codex-Start
- kein neuer Datei-Handoff
- kein zweiter Fachworkflow-Executor
- keine neue Textmaschine
- kein neues Tabellen-Gate
- kein neues Link-Gate
- kein neues LanguageTool-Gate
- kein neues SEO-Dubletten-Gate
- kein neues Design-Gate
- kein interner Signer
- kein neues H8-System wegen alter Fehler
- keine Parallel-Current-State-Wahrheit

Vorhandene geprüfte Bausteine werden wiederverwendet.

## 0,0 Freiheit

PROTOTYP: PASS.

Bewiesen u.a.:
- keine caller-selected route
- kein caller-selected validator
- kein set_next_step
- kein freier zweiter Executor
- Worker attestiert seinen PASS nicht selbst
- PSERC hat keine Content-/Design-Autorität
- PSTE hat keine Artikel-/Design-Autorität
- Ziel-PPM-Modus hat keinen freien externen AI-Reviewer
- User Visual kann technischen FAIL nicht überstimmen

## Sicherheit gegen Einfluss von außen

PROTOTYP: PASS.

- Prepared-Payload besitzt festen Fingerprint.
- Externe Ed25519-Signatur liegt zwischen prepare und WordPress-Write.
- Mutation nach Signatur blockiert.
- Selbst Mutation + Neuberechnung des normalen Hashes blockiert.
- Producer besitzt keinen privaten Signierschlüssel.
- Importer besitzt nur öffentlichen Schlüssel.
- Kein Auto-Publish.

## Skalierung

PROTOTYP: PASS.

Harter Test:
1000 signierte Job-Items akzeptiert.

Keine feste Artikelgrenze im Controller gefunden.

Verarbeitungsmodell:
`SEQUENTIAL_ITEMS_NO_FIXED_COUNT_LIMIT`

Korrekte Formulierung:
Die Architektur hat keine fest eingebaute Artikelobergrenze und kann beliebig große endliche Batches nacheinander verarbeiten.

Nicht behauptet:
physikalisch unendlich viele Artikel gleichzeitig.
Reale CPU-/RAM-/Zeitgrenzen bleiben natürlich bestehen.

## Themenunabhängigkeit

PROTOTYP: PASS für die Architektur.

Die Zentralmaschine enthält keine Pferde-/Reitsport-Domainlogik.

Für ein anderes Thema bleibt gleich:
- Steuerung
- Job-/Hash-/Signaturprinzip
- PASS/BLOCKED
- Restartprinzip
- WordPress-Sicherheitsgrenze

Themenspezifisch sind nur die jeweils autoritativen Fach-/Datenbausteine.

Keine Themenlogik in den Controller verschieben.

## Restart

KISS-Prinzip:
kein komplizierter Zwischencheckpoint-Zoo.

- fertiges signiertes Item -> überspringen
- unvollständiges Item -> von seinem ersten festen Schritt neu starten

Damit entfällt eine ganze Klasse alter PREPARED-/Restore-Probleme.

## Historische Fehler M01–M33

Alle 33 wurden mit dem vorhandenen Runner auditiert.

Aktuelles paralleles main:
- 28 PASS
- 5 FAIL: M15, M16, M17, M22, M26

Diese fünf werden in dieser Route NICHT repariert und erzeugen KEINE neuen Architekturschichten.

Ihre zugrunde liegenden Sicherheitsziele sind im KISS-Crosswalk
`35_P33_M01_M33_KISS_CROSSWALK.md`
der Zielarchitektur zugeordnet.

## Isolation

Startbasis:
`914638e67a265cf2e8951b1177a7d80fdf904e98`

Geprüfter Alternativ-Head für den finalen Makrolauf:
`8a6f5801975176a62abba5eae23073a91a7e6c72`

Compare-Ergebnis:
Alle Änderungen seit Startbasis liegen ausschließlich unter:

`control/seo-text-buero/alternative-central-machine/`

Keine bestehende Produktionsdatei des anderen Weges wurde auf diesem Branch verändert.

Der Laborworkflow selbst liegt separat auf dem Labor-Base-Branch.

## Gesamturteil

### Sicherheit
GO.

### Nachhaltigkeit
GO.

### KISS / Überschaubarkeit
GO, wenn die Produktionsumsetzung beim obigen EINEN Zielweg bleibt.

### Automatisierung
GO.

### 0,0 Workflowfreiheit
GO.

### beliebige Batchgröße
GO ohne festes Architekturlimit.

### andere Themen
GO auf Architekturebene.

### Textmaschine unverändert
GO.

### bestehender Chat/Codex-Start wiederverwenden
GO.

### bestehende Dateiübergabe wiederverwenden
GO.

## Harte STOP-Regel für die nächste Entwicklungsphase

Die nächste Phase darf NICHT wieder anfangen, für jede Erkenntnis einen neuen Gate/Runner/Handoff/Room zu bauen.

Zulässig ist nur:

1. vorhandene Infrastruktur wiederverwenden
2. genau eine dünne Zentralsteuerung
3. vorhandene Fachbausteine fest anbinden
4. externe Signaturgrenze
5. bestehender WordPress-Draft-/Readback-/DOM-Weg

Wenn dafür zusätzliche Architektur nötig zu werden scheint:
erst prüfen, ob ein vorhandener Baustein das bereits kann.

Nicht bauen, bevor diese Prüfung negativ ist.

## Nächste Entwicklungsphase

Minimaler Realintegrations-Prototyp.

Nicht mehr Konzept verbreitern.

Ziel:
den oben eingefrorenen EINEN Weg mit einem realen gebundenen Item von Eingang bis signiertem Draft-Readback verbinden, weiterhin vollständig isoliert und ohne main-Merge.

Erst 1 Item.
Dann kleiner Batch.
Erst danach Skalierung.
