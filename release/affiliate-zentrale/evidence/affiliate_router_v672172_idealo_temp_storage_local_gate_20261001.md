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


## Exakter Installationskandidat

Ausgangspunkt war ausschließlich der bereits final gegatete Installer 6.72.171 mit SHA-256
`dbe630c72f5273abb5c3b48223bbed00498be0a0578f18eca3f001e92bb03fba`.

Für 6.72.172 wurden gegenüber diesem Installer exakt drei Plugin-Dateien verändert:
- `includes/trait-ppar-housekeeping.php` -> SHA-256 `0216897c626953919a5adf51f6b7622b2236f88935dde5de26fc79d8eb80b551`
- `pferdeportal-affiliate-router.php` -> SHA-256 `2b3bca221e48fdba7e1b3b69ee87da8e4c396ecc9f2e351df839cffc15759f82`
- `readme.txt` -> SHA-256 `374552a098d4fc010354ac83b53cbcd92e6f6b7ab14983f1c70f3f4d4b9e0fc8`

Der gebaute Handoff-Installer:
- Datei: `AFFILIATE_ZENTRALE_6.72.172.zip`
- SHA-256: `c9fd44b97793422890a46b87dcdcbc88ce52ae26437b77173a64c9d976b73a25`
- Größe: 766700 Bytes
- Source-Manifest-Identität: 27/27 PASS
- Fresh-Unpack-Identität: 27/27 PASS
- Fresh-Unpack PHP-Lint: 21/21 PASS
- Header-/Runtime-Version: 6.72.172 / 6.72.172 PASS
- ZIP-Integrität: PASS

Die automatischen alten 6.72.170/171-Workflows sind für 6.72.172 nicht als Release-Gate verwendbar, weil sie ihre erwartete Versionsnummer fest verdrahten. Belegt: Governance-/Source-/Tree-/Start-Checks PASS; Abbruch erst beim harten `grep Version: 6.72.171`. Die Workflowdateien wurden wegen Scope-/KISS-Grenze nicht umgebaut.

Repository-Binärsync des neuen ZIP ist über den verfügbaren Schreibweg nicht bytegenau ausgeführt. Das ändert die geprüften Handoff-Bytes nicht; Live-Status bleibt bis Installation + WordPress-Readback 6.72.171.
