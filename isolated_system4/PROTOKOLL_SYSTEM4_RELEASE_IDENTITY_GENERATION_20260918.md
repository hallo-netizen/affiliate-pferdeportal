# System 4 – Release-Identität vor Codex – 18.09.2026

## Befund

Der gebundene 7er-Batch bleibt unverändert:

`7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a`

Die Kollision entstand, weil sichtbare Ausgabe, dauerhafte Ausgabe, Recovery-Quelle und GitHub-ENDSTEMPEL nur nach dem Batch-Hash benannt wurden. Für denselben Batch existiert bereits ein historischer Release.

## Minimale Reparatur

Keine neue Route und kein neuer Batch-Hash.

Die bereits vorhandene Runtime-`generation` wird als Lauf-/Ausgabeidentität verwendet:

`Batch-SHA256 + runtime_generation`

Beispiel des aktuellen neuen Laufs:

`.../<batch>/generation-000001/...`

GitHub-ENDSTEMPEL:

`endstempel-<batch>-g000001`

Ein späterer erneuter Lauf desselben Batchs erhält über den bestehenden Runtime-Lifecycle Generation 2 usw.

## Unverändert

- sieben Themen, Titel, Keywords, Kategorien, Artikeltypen und Slots
- Point 0
- Textmaschine
- LanguageTool
- PPM
- PSERC
- WordPress-Regeln
- Auto-Publish bleibt verboten
- alte Recovery-Artikel bleiben als Schreibquelle verboten

## Prüfbeweise

- System-4-Vollprüfung Run `35361139485` → PASS
- Zielgerichteter Pre-Codex-Lauf Run `35361249579` → PASS
- Bereinigter Deterministic Entrance Gate Run `35361368650` → PASS

Im zielgerichteten Lauf ausdrücklich bewiesen:

- 1 / 3 / 25 / 1000 Artikel → PASS
- gleicher Batch, Generation 1 und 2 → getrennte Ausgabe → PASS
- Wiederholung derselben Generation → BLOCKED
- Generation/Pfad-Mismatch → BLOCKED
- Source-Count-Mismatch → BLOCKED
- Zero-Count → BLOCKED
- Output-Quarantäne → PASS
- WordPress-Importvertrag → PASS
- Point 0 200/401/403 → PASS
- Point-0-/Prewrite-Manipulation → BLOCKED
- alte Artikel/Kandidaten als aktive Produktionsquelle → BLOCKED
- jeder Acceptance-Lauf an frische Artikelquellen gebunden → PASS

## Noch nicht ausgeführt

- kein Codex-Produktionslauf
- kein Publish
- kein Merge von PR #315

## Integrationsgrenze

PR #315 ändert notwendigerweise `.github/workflows/pferde-atelier-endstempel.yml`, weil der alte GitHub-Release-Tag selbst nur aus dem Batch-Hash gebildet wird.

Der aktive Immutable Base Hardlock blockiert Änderungen unter `.github/workflows/**` ohne normalen Bypass. Laut bestehendem Hardlock-Protokoll ist für eine absichtliche Workflow-Wartung ein bewusster Repository-Admin-Schritt am GitHub-Ruleset erforderlich.

Der Hardlock darf nicht verdeckt umgangen werden. Nach der einmaligen freigegebenen Wartungsänderung muss er wieder vollständig aktiv sein.

## Nächster zulässiger Ablauf

1. Admin-Wartung für genau diese notwendige Workflow-Änderung freigeben.
2. PR #315 nur nach ausdrücklicher Nutzerfreigabe mergen.
3. Immutable Base Hardlock sofort wieder vollständig aktivieren.
4. Gemergten Main, Current-Hash, 107007/107008-Hashes und NEW-Schutz nochmals frisch prüfen.
5. Codex weiterhin nicht starten, bis der Nutzer ihn ausdrücklich freigibt.
