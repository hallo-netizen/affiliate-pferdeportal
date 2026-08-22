# VERBINDLICHER PRÜFUNGSABBAU OHNE QUALITÄTS-/SICHERHEITSVERLUST – STARTMASTER0058

## Grundsatz

**Überflüssige Prüfungen müssen wegfallen. Kein Qualitäts- oder Sicherheitsgate darf wegfallen.**

Eine Prüfung ist nur dann „überflüssig“, wenn sie bei identischem Input, identischer Contract-/Toolversion und vorhandenem unverfälschtem PASS-Beleg keinerlei neue Information liefern kann.

## Klasse A – IMMER FRISCH

Diese Prüfungen dürfen nicht gecacht/übersprungen werden, wenn der konkrete Produktionslauf sie benötigt:

- aktueller WordPress-Inventarstatus / Inventory Revision
- aktueller READY-/Plan-Snapshot
- Terminal-/Publish-/Draft-Existenzschutz
- Dubletten/Kannibalisierung gegen aktuellen Bestand
- Paket-Hash/Tamper/Signatur bei jedem Intake
- Supervisor-Freigabe für das konkrete Paket
- Request Identity, Replay, Double Submit, Lease/Resume
- PPM-Schreibvorgang
- WordPress-Readback des konkreten Schreibvorgangs
- Publish-Sperre bzw. explizite Nutzerveröffentlichung außerhalb des automatischen Produktionslaufs

## Klasse B – HASH-CACHE ZULÄSSIG

Nur wenn **Inputhash + Contracthash + Tool-/Versionhash + Outputhash + PASS-Beleg** identisch und vollständig sind:

- statische Vertrags-/Schemasichtungen
- unveränderte Source-Lesung für bereits belegte unveränderte Funktion
- statische Portal-Link-Registry, solange Registryhash identisch ist
- unveränderte Artikel-/Fact-Pack-Artefakte zwischen Resume-Schritten
- LanguageTool-Evidence bei identischem sichtbaren Text-Hash und identischer LT-Version/Regelkonfiguration
- nicht zeitkritische Quellensnapshots nur, wenn Freshness-Vertrag Wiederverwendung ausdrücklich erlaubt

## Klasse C – WIEDERHOLUNG ENTFÄLLT IM NORMALEN PRODUKTIONSLAUF

Diese Checks werden weiterhin bei Release-/Codeänderungen ausgeführt, aber **nicht vor jedem normalen Artikelbatch**:

- vollständige MASTER-Dateimanifest-Verifikation
- Source↔Installer-Byteparität
- PHP-Syntaxlauf über komplettes Plugin
- vollständige Package-Integritätsprüfung unveränderter Installer
- Fresh-Unpack eines unveränderten Installers
- historische Vollregressionen unveränderter Produktionsmodule
- vollständige Rule-1-Code-Deltascope-Prüfung, wenn keinerlei Code-/Contractdatei verändert wurde
- wiederholtes Lesen der gesamten GitHub-Historie ohne konkreten Konflikt/Änderung

## Batch-Beschleunigung

- ein Live-Inventarsnapshot pro unveränderter Inventory Revision
- ein Titel-/Dubletten-Korpus pro Batch
- Titel batchweise prüfen statt Bestand je Titel neu laden
- unabhängige Recherche parallel, Provenienz je Position getrennt
- statische Contracts einmal pro Hash
- ein einziges Produktionspaket statt mehrfacher manueller Einzelartefaktzuordnung, solange der aktuelle Contract dies vorsieht

## Invalidierung

Cache sofort ungültig bei jeder Änderung von MASTER-SHA, relevantem Source-/Installer-Hash, Contract-/Schemahash, Tool-/Regelversion, Artikel-/Fact-Pack-/Visible-Text-Hash, Inventory Revision / Livebestand oder Plan-/READY-Snapshot.

Unbekannt = BLOCKED.

## Zeitmessung

Jeder Produktionslauf protokolliert zukünftig je Phase `started_at`, `ended_at`, `duration_ms`, `cache_hit`, `cache_reason`, `invalidated_by`. Optimierung erfolgt nur auf Basis dieser Daten.
