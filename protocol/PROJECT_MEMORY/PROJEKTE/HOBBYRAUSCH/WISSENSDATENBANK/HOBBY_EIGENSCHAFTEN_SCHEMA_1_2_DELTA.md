# HOBBY DEPOT – EIGENSCHAFTSSCHEMA 1.2 – DELTA 54 → 57

STAND: 2026-10-22
STATUS: FACHLICH BESCHLOSSENER SCHEMA-DELTA / KEINE ZWEITE DATENAUTORITÄT

## Zweck

Ergänzung des bestehenden zentralen 54er-Eigenschaftsschemas um genau drei Merkmale, die in der Gegenprüfung nicht sauber durch bestehende Traits abgedeckt werden.

## Harte Integritätsprüfung

- ursprüngliche 54 Eigenschaftsdefinitionen gegen Schema 1.1 geprüft;
- die ersten 54 Definitionen sind in der lokalen 1.2-Fassung **1:1 unverändert**;
- neue Gesamtzahl: **57**;
- eindeutige Property-IDs: **57/57 PASS**;
- bestehende 8 Gruppen bleiben unverändert.

## Neue Merkmale

### 55. Pflege / Wartung der Ausrüstung

- ID: `equipment_maintenance`
- Gruppe: `platz_logistik`
- Typ: `enum`
- Werte: `keine | gering | mittel | hoch`
- Finder-Rolle: `soft_score`
- SEO-View: nein
- Bedeutung: regelmäßiger Pflege-, Reinigungs-, Kalibrier-, Reparatur- oder Wartungsaufwand der typischen Ausrüstung.
- Abgrenzung: Vor-/Nachbereitung einer einzelnen Einheit bleibt `setup_cleanup`.

### 56. Kraftbedarf

- ID: `strength_need`
- Gruppe: `anforderung`
- Typ: `scale_1_5`
- Werte: `1 | 2 | 3 | 4 | 5`
- Finder-Rolle: `hard_candidate`
- SEO-View: nein
- Bedeutung: benötigte körperliche Kraft unabhängig von Ausdauer und allgemeiner Bewegungsintensität.
- Abgrenzung: `physical_intensity` = Gesamtbelastung, `endurance_need` = Ausdauer.

### 57. Koordination / Balance

- ID: `coordination_balance_need`
- Gruppe: `anforderung`
- Typ: `scale_1_5`
- Werte: `1 | 2 | 3 | 4 | 5`
- Finder-Rolle: `soft_score`
- SEO-View: nein
- Bedeutung: Gleichgewicht, Ganzkörperkoordination und grobmotorische Steuerung.
- Abgrenzung: `fine_motor_need` bleibt für präzise Hand-/Fingerarbeit zuständig.

## Gegenprüfung

Bewusst gegen unterschiedliche Hobbytypen geprüft:
- Stricken
- 3D-Druck
- Wandern
- Bogenschießen
- Ameisenhaltung
- Buchbinden
- Kanutouren
- RC-Segelboote
- Tabletop Wargaming
- Goldwaschen
- Kunstschmieden
- Slacklining

Ergebnis:
- kein neues Merkmal ist durch die bisherigen 54 vollständig ersetzbar;
- alle drei Merkmale erhöhen die Vergleichbarkeit;
- keine weitere zwingende Lücke wurde gefunden.

## Harte Regel

Die bisherigen 54 Klassifikationen bleiben unverändert.
Die drei neuen Werte werden hobbyweise ergänzt.
UNKNOWN bleibt zulässig und darf niemals als false bzw. niedriger Wert geraten werden.
