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
