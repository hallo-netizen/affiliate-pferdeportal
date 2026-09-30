# Affiliate-Zentrale 6.72.168 – Recovery Sweep + manuelle Speicherpflege

Datum: 2026-09-30

## Ziel

Auf Basis der freigegebenen 6.72.167 weitere historische Reparaturarchitektur aus dem Normalbetrieb entfernen und den bereits vorhandenen zentralen Housekeeping-Lauf im KISS-Backend kontrolliert manuell ausführbar machen.

## Entfernen

- AFF-ERR-039 schreibende Recovery-State-/Worker-/Admin-Pfade.
- AFF-ERR-043 schreibende Historical-Restore-State-/Worker-/Admin-/Auto-Init-Pfade.
- AFF-ERR-044 6.72.114/115 Restore-State-/Admin-Pfade.
- Zugehoerige Runtime-Hooks, Admin-Post-Handler, Panels und alte Recovery-State-Optionen/Cron-Hooks.
- Keine Entfernung des derzeit noch benoetigten read-only Incident-Fallbacks fuer category_product_1..3, solange dessen Live-Unabhaengigkeit nicht bewiesen ist.

## Beibehalten

- `aff039_incident_evidence()` + `aff039_incident_proven()` nur fuer den read-only Incident-Fallback.
- hashgebundener AFF043-Snapshot + `aff043_snapshot()` nur fuer denselben read-only Fallback.
- normale eBay-/Idealo-/Awin-/ADCELL-Funktion.
- PRIVATE/BUSINESS-, Coverage-, Quality-, Affiliate-, Compliance- und Veto-Gates.
- 6.72.166/6.72.167 Performancepfade.
- 6.72.167 eBay KISS/Storage-Regeln.

## Manuelle Speicherpflege

Unter `Affiliate-Zentrale → Steuerung & System` wird der bereits vorhandene zentrale `run_housekeeping()` sicher ausloesbar:
- nur manage_options + Nonce;
- respektiert weiterhin `housekeeping_is_busy()`;
- kein separater Cleanup-Algorithmus;
- zeigt Status sowie db_deleted, db_compacted, files_deleted und bytes_deleted;
- keine manuelle SQL-Loeschung ausserhalb des vorhandenen Housekeeping-Vertrags.

## Nachhaltige Altlastenbereinigung

Der zentrale Housekeeping-Lauf entfernt ausserdem nur die jetzt obsoleten Recovery-State-Optionen/Locks/Schedules von AFF039/AFF043/AFF044. Die Incident-Evidence-Optionen fuer den vorlaeufig erhaltenen read-only Fallback bleiben unangetastet.

## Abnahme

- alter Recovery-Code aus Runtime/Admin nicht mehr erreichbar;
- kein automatischer AFF043-State-Restore mehr auf init;
- read-only Incident-Fallback weiterhin byte-/funktionsgebunden;
- bestehende eBay-/Provider-/Frontend-Regressionen PASS;
- manuelle Speicherpflege positiv + busy-negativ PASS;
- WordPress 7.1.2 + MariaDB PASS;
- finaler Installer nur nach Full Gate.
