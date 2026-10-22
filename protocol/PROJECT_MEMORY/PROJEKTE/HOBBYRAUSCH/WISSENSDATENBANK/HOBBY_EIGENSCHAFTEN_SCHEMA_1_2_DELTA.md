# HOBBY DEPOT – EIGENSCHAFTSSCHEMA 1.2 – DELTA 54 → 57

STAND: 2026-10-22
STATUS: FACHLICH BESCHLOSSENER SCHEMA-DELTA / KEINE ZWEITE DATENAUTORITÄT

## Zweck

Ergänzung des bestehenden zentralen 54er-Eigenschaftsschemas um genau drei Merkmale, die in der Gegenprüfung nicht sauber durch bestehende Traits abgedeckt werden.

## Neue Merkmale

### 55. Wartungs-/Pflegeaufwand der Ausrüstung

- ID: `equipment_maintenance`
- Gruppe: `kosten`
- Typ: `enum`
- Werte: `keine | gering | mittel | hoch`
- Finder-Rolle: `soft_score`
- SEO-View: nein
- Bedeutung: Regelmäßiger Aufwand für Reinigen, Warten, Schärfen, Kalibrieren, Laden, Reparieren oder anderweitige Pflege typischer Hobbyausrüstung.
- Abgrenzung: Nicht Vor-/Nachbereitung einer einzelnen Einheit (`setup_cleanup`) und nicht laufende Geldkosten (`running_cost`).

### 56. Kraftbedarf

- ID: `strength_need`
- Gruppe: `anforderung`
- Typ: `scale_1_5`
- Werte: `1 | 2 | 3 | 4 | 5`
- Finder-Rolle: `soft_score`
- SEO-View: ja
- Bedeutung: Typischer Bedarf an Muskelkraft unabhängig von Ausdauer und allgemeiner körperlicher Intensität.
- Abgrenzung: `physical_intensity` beschreibt Gesamtbelastung, `endurance_need` Ausdauer; Kraft wird separat bewertet.

### 57. Koordination / Balance

- ID: `coordination_balance`
- Gruppe: `anforderung`
- Typ: `scale_1_5`
- Werte: `1 | 2 | 3 | 4 | 5`
- Finder-Rolle: `soft_score`
- SEO-View: ja
- Bedeutung: Typischer Bedarf an Gleichgewicht, Ganzkörperkoordination, Hand-Auge-Koordination oder Bewegungssteuerung.
- Abgrenzung: `fine_motor_need` bleibt ausschließlich für präzise Finger-/Handarbeit zuständig.

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
- alle drei Merkmale erzeugen zusätzliche Vergleichbarkeit;
- keine weitere Eigenschaft wurde als zwingende Lücke festgestellt.

## Harte Regel

Die bisherigen 54 Klassifikationen bleiben unverändert.
Die drei neuen Werte werden hobbyweise geprüft ergänzt; UNKNOWN bleibt zulässig und darf niemals als false bzw. niedriger Wert geraten werden.
