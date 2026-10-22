# HOBBY DEPOT – EIGENSCHAFTSSCHEMA 1.2 – DELTA 54 → 57

STAND: 2026-10-22
STATUS: **VERBINDLICH / 862 VON 862 KLASSIFIZIERT / PASS**

## Harte Integritätsprüfung

- ursprüngliche 54 Eigenschaftsdefinitionen **1:1 unverändert**;
- Gesamtzahl **57**;
- eindeutige Property-IDs **57/57 PASS**;
- weiterhin 8 Gruppen;
- 862/862 Hobbyidentitäten klassifiziert;
- 2.586/2.586 neue Einzelwerte vorhanden;
- 46.548 alte Traitwerte unverändert.

## Neue Merkmale

### 55. Pflege / Wartung der Ausrüstung
- ID: `equipment_maintenance`
- Gruppe: `platz_logistik`
- Typ: `enum`
- Werte: `keine | gering | mittel | hoch`
- Finder-Rolle: `soft_score`
- Bedeutung: regelmäßiger Pflege-, Reinigungs-, Kalibrier-, Reparatur- oder Wartungsaufwand der typischen Ausrüstung.
- Abgrenzung: nicht Pflege lebender Systeme; nicht bloße Vor-/Nachbereitung einer Einheit.

### 56. Kraftbedarf
- ID: `strength_need`
- Gruppe: `anforderung`
- Typ: `scale_1_5`
- Werte: `1 | 2 | 3 | 4 | 5`
- Finder-Rolle: `hard_candidate`
- Bedeutung: benötigte Muskelkraft unabhängig von Ausdauer und allgemeiner körperlicher Intensität.

### 57. Koordination / Balance
- ID: `coordination_balance_need`
- Gruppe: `anforderung`
- Typ: `scale_1_5`
- Werte: `1 | 2 | 3 | 4 | 5`
- Finder-Rolle: `soft_score`
- Bedeutung: Gleichgewicht, Ganzkörperkoordination, Hand-Auge-Koordination oder grobmotorische Steuerung.
- Abgrenzung: Feinmotorik bleibt separat in `fine_motor_need`.

## Klassifikationsregel

Die neuen Werte wurden aus dem bereits geprüften 54er-Bestand querklassifiziert und an hobbybezogenen Plausibilitätsregeln gegengeprüft. Keine bestehende Klassifikation wurde überschrieben.

Voll-Audit:
`EVIDENCE/HOBBY_SCHEMA12_FULL_862_AUDIT_20261022.json`
