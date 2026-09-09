# ACM – PRODUKTIONSADOPTION / MINIMALER ZIELVERTRAGS-KANDIDAT

Stand: 2026-09-09
Status: KANDIDAT – KEINE ÄNDERUNG DER PRODUKTIVEN AUTORITATIVEN ZIELQUELLE

## Ausgangslage

Autoritative Produktionsreferenz:
`protocol/STARTMASTER0107_H8_FINAL/02_ZIELVERTRAG_STARTMASTER0107_H8_20260831.md`

Unverändert übernommen:
- Chat hat keine Workflowentscheidung
- keine freie Navigation
- keine freie Recherche
- keine freie Texterstellung
- keine freie Paketerzeugung
- keine freie WordPress-/GitHub-Produktionsaktion
- bestehender Fachworkflow bleibt unverändert
- Research/Fact-Pack bleibt
- Textmaschinenvertrag bleibt
- Artikeltyp/Struktur bleibt
- Tabellen bleiben
- interne Links bleiben
- LanguageTool bleibt
- PPM/PSERC/PSTE bleiben
- Dubletten-/Kannibalisierung bleibt
- SEO bleibt
- Design/Format bleibt
- Publish-Sicherheit bleibt
- fail-closed bleibt

## Einzige fachneutrale ACM-Änderung für Produktionsadoption

Bisheriger Endstempelweg:
`vollständiger Fachworkflow -> Nutzerreview 107008 -> Endstempel -> finale JSON -> WordPress-Verifikation`

ACM-Kandidat:
`vollständiger Fachworkflow -> PPM prepare(no write) -> kanonische finale Artikeldaten -> externer Endstempel -> WordPress verifiziert vor erstem Draft-Write -> Draft -> Readback/DOM -> Nutzerreview -> STOP ohne Auto-Publish`

Begründung:
- Signatur schützt exakt die Bytes, die WordPress schreiben darf.
- Kein Inhalt wird nach Signierung frei verändert.
- WordPress besitzt nur den festen Public Key.
- Privater Schlüssel bleibt ausschließlich beim externen/GitHub-Signer.
- Nutzerreview bleibt erhalten.
- Publish bleibt gesperrt.
- Keine Textmaschinen-/Fachregel wird verändert.
- Keine neue Route, kein neuer Runner, kein neuer Controller und kein zweiter Handoff.

## Finale Dateiausgabe

Verbindlicher neutraler Kandidatenname:
`PFERDE_ATELIER_SIGNED_ARTICLE_BATCH_FINAL.json`

Pfadprinzip:
`.pferde-release/<batch_sha256>/PFERDE_ATELIER_SIGNED_ARTICLE_BATCH_FINAL.json`

Die Artikelzahl ist niemals Teil des Dateinamens oder ein Laufzeitlimit.
Die tatsächliche Artikelzahl wird ausschließlich im signierten Manifest als `article_count` gebunden.

## Adoptionsregel

Diese Datei ist nur der geprüfte ACM-Kandidat.
Die autoritative Produktions-Zielquelle darf erst in einem separaten kontrollierten Adoptionsschritt versioniert werden.

Bis dahin:
- keine Änderung an main
- keine Änderung an CURRENT_STATE
- keine Änderung der Parallelroute
- kein Auto-Publish


## Echt-Einstieg-Beweis

Aktueller produktiver `main` wurde ausschließlich in einem temporären detached Worktree geprüft.

Ergebnis:
- offizieller Codex-Environment-Preflight PASS
- offizieller Runtime-Entry PASS
- `CURRENT_BOUND_ACTION_READY` real erreicht
- aktuelles Item:
  - canonical_article_id: `article:a8282e69ecd43b615de17eb1`
  - plan_slot: `9c229b0e6a784a482575e3deb16d105e3b5355becbbbb8ecfc8e1f600b529c56`
  - Titel: `Das Wichtigste über Hindernisstangen für Pferde`
  - Target Keyword: `Hindernisstangen für Pferde`
  - Beitragsart: `Beratung`
- vorhandener Handoff-Pfad real gebunden
- Worker-Rolle: `CURRENT_CODEX_IS_BOUND_FACHWORKFLOW_WORKER`
- publish_allowed=false

Der echte Handoff selbst wird erst dann als echt gewertet, wenn die realen Fachprodukte für dieses gebundene Item erzeugt wurden. Fixture- oder Recovery-Daten werden dafür nicht als Ersatz akzeptiert.


## Verbindliche Klarstellungen aus Abschlussprüfung 2026-09-09

### Redaktionsplan bleibt Ursprung
Der SEO-Redaktionsplan bleibt die vorgelagerte autoritative Fachplanung.
Er bindet insbesondere Beitragsart, Kategorie, plan_slot, Target Keyword und Titel.
ACM darf diese Werte nicht frei ersetzen.
Bestehender Inventar-/Dubletten-/Keyword-Ownership-Abgleich bleibt erhalten.

### Claude gehört nicht zum Zielsystem
Claude war externe Zusatzberatung und ist strukturell nicht erforderlich.

Für ACM gilt:
- keine Claude-Abhängigkeit
- kein Claude-Reviewer als Pflicht
- keine Claude-Freigabe
- kein Claude-Gate
- keine Workflowautorität für Claude

Ein historischer, explizit aktivierbarer Sonderzweig im unveränderten PPM wird nicht gebunden.
Nur zu dessen physischer Entfernung wird PPM/Textmaschine nicht verändert.

### Ziel-Nutzerfluss
Der einfache Zielablauf lautet:

`Redaktionsplan -> Fachworkflow/Textmaschine -> alle maschinellen Gates -> eine signierte JSON -> manueller Upload in WordPress -> Signatur-/Hashprüfung vor erstem Write -> Entwurf -> Readback/DOM -> Nutzer-Sichtprüfung -> manuelle Freigabe`

Keine automatische Veröffentlichung.

### Aktueller Adoptionsblock
Die isolierte One-JSON-Seam ist technisch PASS.
Im echten WordPress-Runtime/Admin-Weg fehlen aber noch:
1. die reale Verdrahtung des One-JSON-Verifiers vor den bestehenden Normal-Draft-Import,
2. der nachgewiesene kontrollierte manuelle Freigabe-/Publish-Punkt.

Deshalb bleibt diese Datei Kandidat und ist noch keine produktive Zielquelle.

### LanguageTool
LanguageTool-Vertrag und Evidence bleiben unverändert.
Für unbeaufsichtigte Vollautomatik muss zusätzlich die fest gehashte LanguageTool-6.8-Runtime reproduzierbar gebunden sein.
Kein neuer Qualitätsweg und kein Fallback-Provider.
