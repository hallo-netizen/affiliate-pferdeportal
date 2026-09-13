# TEXTSYSTEM 4A – ZIELVERTRAG

STAND: 2026-09-13
STATUS: VERBINDLICHER HÄRTUNGSMASSSTAB FÜR KONZEPT 4

## Ziel

`4a` bezeichnet ab jetzt **keine zweite Textmaschine**, sondern den Prüfmaßstab, mit dem Konzept 4 auf die kleinste robuste Laufzeitarchitektur reduziert wird.

Inhalt, Design und Qualität bleiben vollständig unangetastet.

## Unveränderlich

- Inhaltliche/Textmaschinen-Regeln bleiben unverändert.
- Design, Theme/CSS und Produktionsmarkup bleiben unverändert.
- Echte Qualitätsprüfer bleiben unverändert und alleinige PASS-Autorität.
- Kein Auto-Publish.
- Kein Einfluss von außen auf Route, Regeln, nächsten Schritt oder Toolchain.
- Kein zweiter Workflow-Besitzer neben dem einen Produktionscontroller.

## Architekturziel

`1 Produktionscontroller + N unabhängige Artikelzustände + bestehende reale Prüfer als interne Aufrufe + 1 finaler Ausgang`

Ein Artikelzustand enthält dauerhaft Identität und belegten Stand genau eines Artikels. Prüfer liefern PASS oder konkrete Findings, verändern aber weder Route noch Zustand selbst.

**Mehrere Dateien/Module sind erlaubt. Mehrere Laufzeitautoritäten oder frei wählbare Produktionsstraßen sind nicht erlaubt.**

## Flexibilitätsziel

Der Produktionscontroller darf weder konkrete Artikelzahl noch Beitragsart hardcoden. Neue freigegebene Beitragsarten werden ausschließlich durch die bestehenden autoritativen SEO-/PPM-/Textmaschinenregeln zugelassen. Fehlt die Freigabe, wird fail-closed blockiert.

Die aktuell noch vorhandene 7er-/`Beratung`-Bindung in System 4 ist separat zu entfernen und zählt nicht als Argument für 4a.

## Automatisierungsziel

Nach gültigem Produktionsanstoß läuft die Kette ohne manuelle Chatnavigation bis entweder:
- konkretes fail-closed BLOCK/FAIL mit erster Ursache, oder
- finale geprüfte WordPress-Importdatei im Elternchat.

Reparaturen bleiben beim selben Artikel. Kein Gesamtneustart wegen eines reparierbaren Einzelartikelfehlers.

## Verbindlicher Gesamtworkflow

`gebundener SEO/WordPress-Metadatenbatch`
→ `kanonischer Artikelzustand`
→ `Codex-Recherche + reale Evidence`
→ `Fakten + Fact-Pack`
→ `Text unter unveränderter Textmaschine`
→ `FULL-Prüfung mit echten unveränderten Prüfern`
→ bei Finding `Same-Article-Repair → FULL-Prüfung`
→ `Artikelbytes einfrieren`
→ `artikelübergreifende Prüfung`
→ `SYSTEM4_WORDPRESS_HANDOFF_V1.json`
→ `bytegleich in den Elternchat`
→ `Portal SEO Editorial Plan Compiler 0.28.23`
→ `WordPress-Entwürfe / publish_allowed=false`.

## Skalierungsziel

Architektonisch identischer Weg für 1, 3, 25, 1000 und darüber hinaus. Ein Batch ist nur die Menge der gebundenen Artikelzustände plus notwendige Querschnittsprüfung, keine zweite Fach-Zustandsmaschine.

## Finaler Dateivertrag

Die finale Datei bindet mindestens:
- Batch-/Snapshot-Identität;
- `publish_allowed=false`;
- Direct-Import-Bereitschaft;
- pro Artikel `title`, `target_keyword`, `category`, `article_type`, `plan_slot`, finalen Body und Body-Hash, Revision, Produktionskontext/Fact-Pack und echte LT-/PPM-/weitere Prüfnachweise;
- artikelübergreifenden PASS;
- exakt dieselben final geprüften Artikelbytes.

## Abbruchkriterium für ein eigenständiges 4a-System

Ein separates 4a-System wird **nicht gebaut**, solange Konzept 4 durch Entfernen seiner Parallelwege auf dieses Ziel gebracht werden kann.

Nur wenn nach dieser Bereinigung ein irreduzibler, nachweisbarer struktureller Nachteil von Konzept 4 verbleibt, darf ein eigenständiger 4a-Prototyp erneut geprüft werden.
