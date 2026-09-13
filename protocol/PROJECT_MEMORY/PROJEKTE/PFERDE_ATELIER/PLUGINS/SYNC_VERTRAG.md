# PFERDE-ATELIER – PLUGINS – SYNC-VERTRAG

STAND: 2026-09-13
STATUS: VERBINDLICH

## Zweck

Jedes tatsächlich im Pferde-Atelier geführte Plugin soll als isoliertes aktuelles Ausgabeartefakt entnehmbar sein, ohne Fach-/Release-/LIVE-Wahrheit zu duplizieren.

## Physische Ablage

Die Binärartefakte liegen persistent außerhalb der GitHub-Campusakten unter:

`/Campus-Plugins/PFERDE_ATELIER/<PLUGIN-ID>/CURRENT.zip`

Dazu:
`/Campus-Plugins/PFERDE_ATELIER/<PLUGIN-ID>/MANIFEST.md`

Die GitHub-Akten dieses Büros sind Steuerung/Inventar. Die Library-Ablage ist nur der physische Plugin-Schrank.

## Autorität

`CURRENT.zip` ist niemals selbst Fach-/Release-/LIVE-Autorität.

Autorität bleibt die im `REGISTER.md` je Plugin benannte technische Hauptquelle bzw. das zuständige Fachbüro.

## Sync-Regel

Nach jeder tatsächlichen Pluginentwicklung oder jedem tatsächlichen Pluginupdate:
1. autoritative Quelle frisch lesen;
2. exakten neuen Pluginstand eindeutig binden;
3. isolierte Installations-ZIP aus genau diesem Stand beziehen/erzeugen;
4. ZIP-Struktur/Lesbarkeit prüfen;
5. Version/Pluginidentität prüfen;
6. SHA-256 bilden und gegen Release-/Fachbeleg vergleichen, soweit vorhanden;
7. erforderliche Positiv-/Negativ-/Regressionstests müssen tatsächlich PASS sein;
8. erst danach `CURRENT.zip` ersetzen;
9. `MANIFEST.md` aktualisieren;
10. persistente Kopie erneut lesen und Hash/ZIP prüfen;
11. `REGISTER.md` + `UPDATEPROTOKOLL.md` nachziehen.

## Fail closed

Bei fehlender/mehrdeutiger Quelle, Versionskonflikt, Hashabweichung, defekter ZIP oder fehlendem erforderlichem Test:
- alte gültige `CURRENT.zip` nicht ersetzen;
- keinen historischen Stand hochstufen;
- `ARTEFAKT_SYNC: BLOCKED`;
- ersten konkreten Blocker dokumentieren.

## Allgemeingültige Plugins

Allgemeingültige Hauptkerne bleiben autoritativ unter `ALLGEMEINGUELTIGE_BAUSTEINE/`.
Die Kopie hier ist ausschließlich die im Pferde-Atelier verwendete isolierte Ausgabekopie. Keine Umklassifizierung.

## Secrets

Keine API-Keys, Tokens, Passwörter, Lizenzschlüssel oder sonstigen Secrets in ZIP/Manifest/Campusakten ergänzen.
