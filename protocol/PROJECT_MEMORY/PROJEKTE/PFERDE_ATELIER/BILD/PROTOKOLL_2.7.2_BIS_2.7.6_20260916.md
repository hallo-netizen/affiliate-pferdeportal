# BILD – PROTOKOLL 2.7.2 BIS 2.7.6 – 2026-09-16

## Ausgang

2.7.1 hatte den realen 2.7.0-Tabfehler (`cpt` fehlte im JS-Tabregister) minimal behoben. Danach wurde der Pferderassen-Hero-Weg in mehreren kleinen, jeweils lokal geprüften Schritten weiterentwickelt.

## 2.7.2

WAS:
Pferderassen-Hero-Regeln/Profilbindung und Migration für den gebundenen Rassenweg weitergeführt.

PRÜFUNG:
lokale Positiv-/Negativ-/Regressionsprüfung PASS.

## 2.7.3

WAS:
Der Magnific-Weg im Rassen-Hero-Prozess wurde korrigiert: ein zusätzlicher GET-Preflight, der real 404 erzeugte, wurde entfernt; der gebundene POST-Erzeugungsweg bleibt maßgeblich.

WARUM:
Der Preflight war kein notwendiger Vertragsbestandteil und blockierte einen ansonsten funktionierenden Erzeugungsweg.

PRÜFUNG:
lokal positiv/negativ + Mutation PASS.
WORDPRESS-LIVE: Nutzerbestätigung, dass der Weg danach funktioniert.

## 2.7.4

WAS:
Prompt/Framing für Pferderassenbilder so angepasst, dass das Pferdemotiv vollständiger und weniger angeschnitten erzeugt wird.

PRÜFUNG:
lokal PASS.

## 2.7.5

WAS:
`post_type_hero` erzeugt/übernimmt den Rassen-Hero nativ im Zielverhältnis **21:9 / 1260×540**; kein nachgelagerter lokaler 3:1-Recrop für diesen Weg.

GRENZE:
Bestehende Kategorie- und HivePress-Bildwege bleiben unverändert.

PRÜFUNG:
- Format-/Source-Pfad: PASS;
- kein lokaler Rassen-Recrop: PASS;
- Kategorie/HivePress byte-/regelbezogen unverändert: PASS;
- Negativ-/Mutationskontrollen: PASS.

## 2.7.6

WAS:
Für `pa_breed` wurde eine serielle Batch-Bedienung ergänzt:
- nächste 10 offene Rassen;
- ausschließlich Rassen ohne Featured Image;
- genau eine Aufgabe gleichzeitig;
- Statusanzeige für offen/laufend/abgeschlossen/Fehler;
- kein Überschreiben vorhandener Featured Images.

WARUM:
Die Einzelbedienung war für den vorhandenen Rassenbestand zu langsam; die Sicherheitsgrenzen des Einzelwegs sollen trotzdem erhalten bleiben.

PRÜFUNG LOKAL:
- Scope ausschließlich `pa_breed`: PASS;
- Batchgröße/Ermittlung der nächsten 10: PASS;
- serielle Verarbeitung: PASS;
- No-Overwrite-Hardlock: PASS;
- andere Profile/Wege unverändert: PASS;
- PHP-Lint/ZIP/Re-Extract/Version: PASS.

Release:
`ALLGEMEINE_BILDZENTRALE_2.7.6_RASSEN_BATCH_AUTOMATIK_INSTALLIEREN.zip`

SHA-256:
`12edc4405560ac3b149cf76a0b6e65694337b1533c0ea5e3a777d3b6c98ccbf0`

WORDPRESS-LIVE:
- Nutzer meldet `klappt`;
- Live-Screenshot zeigt einen 10er-Batch mit serieller Abarbeitung und 0 gemeldeten Fehlern zum sichtbaren Zeitpunkt.

GRENZE:
Kein Beleg, dass bereits alle Pferderassen bebildert sind. Belegt ist die Funktion des 2.7.6-Batchwegs.

## Artefaktsync

Aktueller Stand wurde am Abschlusscheck synchronisiert nach:
- `/Campus-Plugins/PFERDE_ATELIER/PPA-003/CURRENT.zip`
- `/Campus-Plugins/ALLGEMEINGUELTIGE_BAUSTEINE/BILDZENTRALE/CURRENT.zip`

Beide Ausgabekopien bleiben abgeleitete Artefakte; Fach-/Technikwahrheit liegt in den zuständigen CURRENT-/Protokollquellen.
