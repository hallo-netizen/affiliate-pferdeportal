# Affiliate-Zentrale eBay KISS + Storage Cleanup – Zielvertrag 2026-09-30

Rolle: autoritative Zielquelle fuer den vom Nutzer am 2026-09-30 explizit geoeffneten eBay-Verschlankungs- und Speicherauftrag.

## Oberziel

eBay in der Affiliate-Zentrale radikal verschlanken, alte technische Recovery-/Migrationslast aus dem Normalbetrieb entfernen und das erneute Anwachsen der Datenbank begrenzen, ohne fachliche Funktion, Sicherheitsgate, PRIVATE/BUSINESS-Ausgabe, Affiliate-Links, Compliance, Qualitaetsregeln oder die in 6.72.166 erreichten Performanceoptimierungen zurueckzubauen.

## Verbindliche Basis

- technische Basis / Fallback: 6.72.166
- neuer Kandidat: 6.72.167
- aktive Quelle: release/affiliate-zentrale/current/affiliate-portal-router/
- kein neues Plugin, kein Wrapper, keine neue Architektur
- Ursache in der Affiliate-Zentrale selbst beheben

## Gebuendelter Cleanup-Block

1. eBay-Verbindungsstatus von Kanalpause/Laufstatus trennen; ein technischer OAuth-Test darf nicht wegen eines pausierten Ausgabekanals als Verbindungsfehler erscheinen.
2. Historische 6.4x/6.63.x eBay-Recovery-/Migrationspfade aus dem heutigen Normalpfad entfernen; generische aktuelle Fail-Closed-/Checkpoint-Sicherheit bleibt bestehen.
3. Alte terminale Run-Zustaende duerfen den aktuellen Adminstatus nicht dauerhaft als scheinbar aktuellen Fehler dominieren; Historie bleibt begrenzt erhalten.
4. eBay-Housekeeping: beendete, nicht public/listing-gebundene Rohpayloads frueh und begrenzt verdichten; aktive/oeffentliche/manuell relevante Daten bleiben unangetastet.
5. Bestehende 6.72.166 Performancepfade unveraendert erhalten.
6. Nach technischem PASS: gleicher realer Datenbank-/Performancevergleich wie zuvor.

## Harte Grenzen

- keine Abschwaechung der fachlichen eBay-Klassifikation;
- keine Abschwaechung des BUSINESS-Coverage-/Public-Gates;
- keine Abschwaechung PRIVATE-Kapazitaet, Frische oder Sichtbarkeit;
- keine Entfernung der Marketplace Account Deletion/Closure Compliance;
- keine Aenderung an anderen Providern ausser unmittelbar notwendiger provider-neutraler Statuslogik;
- keine manuelle Datenbankloeschung als Ersatz fuer Plugin-Housekeeping;
- keine zweite Architektur, kein Helferplugin.

## Abnahme

PASS nur wenn gleichzeitig:
- OAuth-Verbindungstest kann Verbindung unabhaengig von einer Kanalpause pruefen;
- Runtime-Zugriffe respektieren Kanalpause weiterhin fail-closed;
- alte terminale Runs werden bounded archiviert statt als aktueller Hauptfehler mitgeschleppt;
- heutiger kanonischer Lauf, Checkpoint und Fail-Closed-Sicherheit bleiben erhalten;
- eBay-ended Storage-Compaction betrifft nur eindeutig terminale, nicht public/listing-gebundene Daten;
- PHP/Syntax und gezielte positive/negative Regressionen PASS;
- 6.72.166 Performanceoptimierungen bleiben im Source-Delta erhalten.
