# ZV-HOBBYRAUSCH-HD001-001 – AUTOMATISCHE DATAFORSEO-SEO-HIERARCHIE BIS FRONTEND

STAND: 2026-10-03
STATUS: AKTIV
FASSUNG: 1.0

## Geltungsbereich

HOBBYRAUSCH / SEO_KATEGORIEN / HD-001 Kategorie-Workflow.

## Ausgangsstand

- V1.9.4 bleibt der produktiv installierte und readback-verifizierte Live-Basisstand.
- Der produktive Buchbinden-Pilot bleibt bestehen und wird nicht zurückgerollt.
- Dieser Zielvertrag erklärt V1.9.4 ausdrücklich NICHT zum neuen Ziel-PASS.
- Für den neuen Zielrahmen ist noch kein V1.9.5-/Nachfolgekandidat belegt.

Fachlicher Planungsinput:
`campus/hobbyfinder/konzept-und-ideen/KATEGORIEPLUGIN_HANDOFF.md`
auf Commit
`df54718078ab699783c495d2d79221006b7ca4fe`
(PR #358, Planungsquelle; keine Current-Autorität).

## Verbindliches Endziel

Bestehendes Hobby-Depot-Konzept
→ DataForSEO
→ automatisch erzeugte SEO-Hierarchie
→ Hauptportal + Magazin + HivePress
→ WordPress
→ Veröffentlichung
→ sichtbare Frontend-Navigation
→ Readback.

## Rollen

Das Konzept bestimmt Geschäftslogik, Nutzerwege und Strukturprinzip.

DataForSEO bestimmt innerhalb dieser Grenzen die konkreten sichtbaren Bezeichnungen und die hierarchische Einordnung nach unten.

DataForSEO muss insbesondere unterscheiden:
- Synonyme und Dubletten;
- Unterformen;
- eigenständige Suchräume;
- Search Intent;
- Parent-/Child-Beziehungen;
- Kannibalisierung und eindeutiges Ownership.

Ein Parent darf nicht allein wegen höheren Suchvolumens gewählt werden. Die Bezeichnung muss semantisch und nach Suchintention zu den darunterliegenden Clustern passen.

## Strukturprinzip

Grundform:
`SEITE → SEITE → SEITE → KATEGORIE → BEITRÄGE`.

Die Tiefe darf nicht künstlich mit inhaltsleeren Ebenen gefüllt werden. Der Workflow muss echte variable Mehr-Ebenen-Strukturen verarbeiten können und darf nicht auf „Root + vier direkte Kinder“ begrenzt bleiben.

Im selben Gesamtprozess:
- Hauptportal / Hobbywelten;
- Magazin / Journal;
- HivePress / Anbieterkategorien.

Der Hobbyfinder bleibt vom SEO-Kategorienbaum getrennt. Er benötigt für die spätere Verknüpfung nur eine stabile Hobby-Identität.

## Automatik

Der Normalweg ist vollautomatisch.

Menschliche Sichtfreigaben dürfen nicht als zwingende Standardstufe des neuen Normalwegs vorausgesetzt werden. Ein manueller Eingriff bleibt nur als bewusster Ausnahme-/Override-Weg zulässig.

Unsichere oder widersprüchliche Evidenz darf nicht geraten werden. Der Lauf muss in solchen Fällen fail-closed stoppen.

## WordPress- und Frontend-Ziel

Erfolg bedeutet nicht nur erzeugte WordPress-Objekte.

Erforderlich sind:
- korrekte Seiten und Taxonomien;
- veröffentlichter statt bloß als Draft angelegter Zielbestand;
- erzeugte sichtbare Frontend-Navigation;
- korrekte Parent-/Child-Beziehungen;
- Readback des WordPress- und Frontend-Endzustands.

## Harte Abnahme

Kein Ziel-PASS ohne vollständige lokale Positiv- UND Negativ-E2E-Simulation bis zum Frontend-Endzustand.

Die Negativstrecke muss mindestens nachweisen, dass falsche Synonymzusammenführung, falscher Parent, reine Volumenentscheidung, Kannibalisierung, Strukturdrift, manipulierte Plan-/Readback-Daten, fehlende Navigation und unzulässiger Publish-Zustand fail-closed blockieren.

Zusätzlich zu prüfen:
- Idempotenz;
- Drift-Erkennung;
- Rollback;
- wiederholter Readback;
- kein Verlust des bestehenden V1.9.4-Livebestands.

Nach lokaler Abnahme bleibt ein realer WordPress-/Frontend-Readback für den produktiven Endzustand erforderlich.

## Technische Startgrenze

Die technische Weiterentwicklung darf erst auf der exakt gebundenen V1.9.4-Quelle beginnen.

Erwarteter Source-SHA-256:
`12dcce406d842bd7b8a6cde5af6a54dff2a4bbff3e27528c04231898a8f02e01`.

Die Source-Bytes sind in der aktuellen HD-001-Originalablage noch nicht vorhanden. Bis sie bytegleich gebunden sind, ist kein Nachfolgekandidat zulässig.
