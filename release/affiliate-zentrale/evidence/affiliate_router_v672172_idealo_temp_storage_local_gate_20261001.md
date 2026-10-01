# Affiliate-Zentrale 6.72.172 – Idealo Temp Storage Rootfix – Local Gate – 2026-10-01

## Ausgangsbefund
- Live-Speicheranalyse 2026-10-01 11:47–11:48 UTC: fünf Dateien `wp-content/uploads/ppar-idealo-feed-*.tmp`, zusammen 749.350.091 Bytes.
- Vier der fünf Dateinamen/Größen waren bereits im Baseline-Scan vom 29.09. vorhanden.
- 6.72.171 löscht den normalen Downloadpfad bei regulärem Erfolg/HTTP-Fehler, hatte aber keinen zentralen Sweep für durch Prozessabbruch verwaiste Feed-Tempdateien.

## KISS-Fix
Nur bestehende Affiliate-Zentrale / bestehender Housekeeping-Lauf.
Kein neues Plugin, kein Runner, keine neue Architektur.

Der Disk-Pass prüft im Upload-Root nur das exakte Muster:
`^ppar-idealo-feed-[A-Za-z0-9]+\.tmp$`

Löschung nur wenn:
- reguläre Datei;
- kein Symlink;
- direkt im Upload-Root, kein Unterordner;
- mindestens 24 Stunden alt;
- kein aktiver `IDEALO_REFRESH_LOCK`;
- maximal 50 passende Kandidaten pro Housekeeping-Lauf.

## Lokale Positiv-/Negativsimulation
PHP 8.4 lokal.

PASS:
- zwei alte exakte Idealo-Tempdateien gelöscht;
- Byte-Zählung exakt;
- frische exakte Tempdatei erhalten;
- falscher Prefix erhalten;
- nicht-alphanumerischer Name erhalten;
- passende Datei im Unterordner erhalten;
- Symlink und Ziel erhalten;
- aktiver Idealo-Worker-Lock blockiert Feed-Temp-Cleanup;
- nach Lock-Freigabe wird die alte exakte Tempdatei gelöscht.

## Lokaler kompletter Housekeeping-Disk-Durchlauf
PASS:
- alter Root-Idealo-Temp gelöscht;
- bestehender alter Bild-Temp-Pfad weiterhin gelöscht;
- altes unreferenziertes Bild weiterhin gelöscht;
- frischer Bild-Temp erhalten;
- referenziertes Bild erhalten;
- unrelated Root-TMP erhalten;
- Unterordner/Symlink erhalten;
- Worker-Lock schützt Root-Feedtemp.

Ergebnis: `LOCAL_FULL_HOUSEKEEPING_POSITIVE_NEGATIVE_PASS`.

## Releasegrenze
Noch kein Live-Install und keine Löschung der fünf realen Tempdateien durch den Kandidaten vor exakter Paket-/Quellprüfung. 6.72.171 bleibt Live-Rollbackbasis.
