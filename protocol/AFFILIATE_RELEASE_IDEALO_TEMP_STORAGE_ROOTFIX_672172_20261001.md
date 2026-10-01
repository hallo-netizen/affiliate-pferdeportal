# AFFILIATE RELEASE – IDEALO TEMP STORAGE ROOTFIX 6.72.172 – 2026-10-01

## Ziel
Die belegten verwaisten `ppar-idealo-feed-*.tmp` dürfen sich nicht erneut dauerhaft im Upload-Root ansammeln.

## Unverändert
Ranking, Relevanz, Providerwahl, Produktkarten, Banner, Slots, Veto/Control, Tracking, Publish-Verhalten, Importlogik und bestehender Bildcache-Housekeeping-Pfad.

## Änderung
Bestehender täglicher Housekeeping-Lauf erhält einen eng begrenzten Idealo-Feed-Temp-Sweep:
- nur direkter Upload-Root;
- nur exakter Dateiname;
- nur reguläre Datei;
- keine Symlinks;
- Alter >= 24h;
- kein aktiver Idealo-Refresh-Lock;
- höchstens 50 passende Dateien je Lauf.

## Abnahme
1. lokale Positiv-/Negativsimulation;
2. kompletter lokaler Housekeeping-Disk-Durchlauf;
3. PHP-Lint der geänderten PHP-Datei;
4. exakte Source-Manifest-Bindung;
5. kein Live-Handoff ohne exakte Paket-/Quellprüfung.
