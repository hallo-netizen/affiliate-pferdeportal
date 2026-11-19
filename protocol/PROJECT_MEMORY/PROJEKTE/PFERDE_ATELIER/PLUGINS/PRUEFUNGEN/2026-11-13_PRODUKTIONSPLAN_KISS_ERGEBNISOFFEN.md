# Pferde Atelier – KISS: Produktionsplan ergebnisoffen hinterfragen
**Stand:** 13.11.2026. **Status:** Nur Konzept-/Workflowprüfung. Keine Plugin-Änderung, keine WordPress-Änderung, keine Installationsfreigabe. Keine weitere Current-Autorität.

## Tatsächlicher Nutzer-Workflow und Regal-Modell
1. **Unverändert:** PSTE recherchiert Themen anhand Keywords/Kategorien/Bestand, entscheidet einmalig über Suchabsicht und Artikelart. Genehmigte Themen werden als einzelne feste Datensätze in WordPress gespeichert (auch tausende).
2. **Entnahme:** Ein vorhandener Export-/Arbeitsprozess nimmt beispielsweise 20 genehmigte Themen aus dem Vorrat und markiert sie **einmalig als in Bearbeitung**. „Aus Regal genommen“ heißt nicht WordPress-Datensatz löschen, sondern für weitere normale Entnahmen sperren.
3. **K0:** Schreibt die Texte zur exportierten Datei; Thema, Suchabsicht, Kategorie, Artikelart bleiben unverändert.
4. **Rückgabe:** WordPress importiert die Texte als Entwürfe und markiert die betreffenden ursprünglichen Aufträge erledigt. Doppelte Anlieferung ergibt nicht zwei Entwürfe.

## Wozu wäre ein Produktionsplan da?
Der bisherige PPM-Produktionsplan weist `canonical_article_id`/`plan_slot` einem Artikelplatz im Produktionsplan zu, der für die bestehende Weiterverarbeitung und K0-Handoff benutzt wird. Dies ist keine belegte Veröffentlichungsterminplanung. Die lokale Codeprüfung der bisherigen PSTE-/PSERC-Speichermethoden bestätigt: Vorreservierung wurde in PSTE geschrieben, nicht nativ in PPM; die eigentliche PPM-Buchung ist nicht live belegt.
PPM 6.7.9 ist als eigenes WordPress-Plugin im WP-Performance-Bericht vom 12.11.2026 enthalten. Der Editorial Guard 0.1.1-quarantine ist ein **weiteres** Plugin; seine notwendigen Schutzfunktionen sind ohne dessen Originalcode noch nicht vollständig geprüft.

## Kritischer Test, auch ohne Inhaltsbewertung
- **Doppel-Entnahme:** Zwei gleichzeitige Exportaufrufe dürfen dieselben 20 Blätter nicht beide erhalten. Einträge **vor Ausgabe dauerhaft reservieren**; Reservierung der Charge muss gegen Parallelstart geschützt sein.
- **Exportdatei verloren / K0-Abbruch:** Blatt darf nicht verschwinden; zugeordneter Auftrag und gespeicherter Status müssen für eine gezielte Wiederaufnahme bleiben. Nicht automatisch wieder allgemein freigeben, solange ein späterer Rücklauf möglich ist.
- **Doppelt importierte Ergebnisdatei:** Derselbe Auftrag darf keinen zweiten WordPress-Entwurf erzeugen. Stabile Auftragskennung im Export und Rücklauf; Import ersetzt/behandelt dieselbe ID eindeutig.
- **Teilrückgabe:** Bei 20 exportierten und 13 zurückgekehrten Artikeln müssen 13 erledigt und 7 weiterhin offen sein, ohne erneute Recherche.
- **Datenbindung:** Einmal freigegebene Suchabsicht/Kategorie/Artikelart nicht nachträglich durch einen Worker entscheiden lassen.
- **K0-Kompatibilität:** Der verbindliche bestehende Handoff-Vertrag erwartet `title`, `target_keyword`, `category`, `article_type`, `plan_slot`. Solange K0 nicht angepasst wird, muss der stabile Platzbezug geliefert werden; eine beliebige neu erfundene ID ungeprüft an `plan_slot` zu hängen wäre nicht zulässig.
- **PPM/Import-Abhängigkeiten:** Bestehender PPM-Draft-/Import-/Sicherheitscode kann den alten kanonischen Plan zwingend verlangen. Vor einem Entfernen nachweisen, ob diese Zugriffe noch benötigt werden oder ob die bestehende eindeutige Auftragskennung sie ersetzen darf.

## Vorläufige KISS-Bewertung
**Für die beschriebenen 20er-Chargen ist ein eigenständiger Produktionsplan inhaltlich nicht notwendig, wenn eine kleine zentrale Auftragsverwaltung die obigen Zustände und Identitäten sicher hält.** Ein Produktionsplan kann sinnvoll sein für weitere technische Sicherheits-/Import-Funktionen oder kapazitäts-/terminorientierte Planung, ist aber für diesen seriellen Regal-Ablauf nicht als fachliche Pflicht nachgewiesen. Daher keine voreilige Löschung von PPM, PSERC oder Editorial Guard.

**Ein minimaler notwendiger Prozess:** `VORRAT → RESERVIERT/EXPORTIERT → ENTWURF_IMPORTIERT` und ein `WIEDERAUFNAHME`-Pfad für Abbrüche. Keine neue fachliche Entscheidung, keine zusätzlichen Worker und keine gesonderte Artikelplatzplanung nur um der Planung willen.

## Nächste begrenzte, sichere Trockenübung
Mit vorhandenen tatsächlichen Freigaben und dem bestehenden K0-/Import-Vertrag simulieren: 5.000 Vorrat, 20 eindeutige Entnahmen, konkurrierenden Export, Abbruch nach 13/20, wiederholten Import, identisches `plan_slot`/Artikel-ID-Handoff. Die Suche/Kategorien/Intention nicht neu prüfen. **Nur bei bestandener tatsächlicher Export-/Import-Abnahme entscheiden**, ob Produktionsplan und zugehörige Plugin-Funktionen entfallen oder in eine zentrale Auftragsverwaltung überführt werden. Kein Neubau auf Verdacht.


## Ergänzung 13.11.2026 – Endgültiges Zielbild der ergebnisoffenen KISS-Prüfung

**Fachliche Kernfunktionen (kein Vorgriff auf technische Realisierungsfreigabe):**

1. **PSTE-Recherche / Redaktion, EIN fachlicher Eigentümer:** Themen recherchieren, Portalbezug/Suchintention prüfen, vorhandene Themen/Artikel auf dieselbe Leserabsicht vergleichen, Kategorie und Artikelart einmal zuweisen; Themenverteilung nach Nachfrage und sinnvollem Bedarf steuern. Eine pauschale Gleichverteilung pro Kategorie ist **kein** Qualitätsziel.
2. **Regal mit freigegebenen Aufträgen:** WordPress bewahrt alle freigegebenen Themen mitsamt eingefrorener Kategorie, Suchabsicht, Zielkeyword, Artikelart und dauerhafter eindeutiger Auftragskennung auf; kann 5.000+ Einträge enthalten.
3. **Externer Titelworker:** Erst nach Freigabe genau einen passenden Titel formulieren, keine erneute fachliche Entscheidung oder Kategorienwechsel.
4. **Chargen-Worker / Export:** Entnimmt X freie Aufträge ohne doppelte Entnahme; erhält ursprüngliche IDs; markiert dauerhaft `RESERVIERT`/`EXPORTIERT`; wiederholbar ohne Datenverlust.
5. **Externe Fabrik K0:** Verändert nicht Freigabe/Suchabsicht/Kategorie; schreibt Text nach den bestehenden 81 Regeln und dem bestehenden Fünf-Felder-Handoff.
6. **Import & technische Qualität:** Ordnet jeden Rücklauf demselben Auftrag zu, erstellt WordPress-ENTWURF statt automatischer Veröffentlichung, stoppt bei Identitäts-/Formatfehlern, wiederholter Import erzeugt keine Duplikate. Veröffentlichung erst nach bestehender Qualitätsfreigabe.

**KISS-/Worker-Prinzip:** Einzelne Aufgaben strikt trennen, aber nicht je Aufgabe ein eigenes Plugin oder eine zweite Entscheidung. Ein gemeinsamer WordPress-Kern mit klaren internen Schritten kann sinnvoll sein; eine Zusammenlegung von PSTE/PSERC oder ein Entfernen von PPM ist **noch nicht** freigegeben. Kein K0-Umbau. Bestehende Pflichtfelder einschließlich `plan_slot` dürfen bis zum geprüften Kompatibilitätsnachweis nicht stillschweigend entfernt/umbenannt werden.

**Offene technische Beweisfragen:** Native PPM-6.7.9-Plan- und Import-Abhängigkeiten; vollständiger Schutzumfang Editorial Guard; sichere einmalige Exportreservierung und idempotenter Import in echten Daten; unveränderte 5-Felder-Annahme bei K0. Erst bestehende Funktionen gegen diesen Soll-Ablauf prüfen, dann minimal umbauen.

**Vorläufiges Ergebnis:** Ein separates Werkzeug zur Produktions-**planung** ist für seriellen Export/Import fachlich nicht erforderlich. Eine verlässliche Auftrags-**verwaltung** ist notwendig. Noch **nicht bewiesen**, dass der vorhandene PPM-/Import-Code unverändert ohne Produktionsplan arbeiten kann.
