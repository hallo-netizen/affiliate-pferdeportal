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
