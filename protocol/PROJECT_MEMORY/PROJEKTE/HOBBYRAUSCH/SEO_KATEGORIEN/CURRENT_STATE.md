# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-05
STATUS: V1.9.4 INSTALLIERT / FRONTEND-PUBLISH NOCH NICHT PASS / V1.9.6 INKREMENTELLER KANDIDAT LOKAL HARD PASS

## Harte Abnahmeregel

**Keine Abnahme ohne dokumentierte lokale Positiv- UND Negativsimulation und realen WordPress-/Frontend-Readback.**

## Zielvertrag

`ZIELVERTRAG_HD001_AUTOMATISCHE_SEO_HIERARCHIE_20261003.md`

Ziel:
Konzept → DataForSEO → Hauptportal + Magazin + HivePress → WordPress → Publish → Frontend-Navigation → Readback.

## Tatsächlicher aktueller Livezustand

Installiert ist weiterhin der bestehende V1.9.4-Bestand.

Wichtig:
- WordPress-Objekte wurden geschrieben und technisch zurückgelesen;
- das ist **nicht** gleichbedeutend mit veröffentlichter Frontend-Struktur;
- die reale Sichtprüfung ist noch offen;
- insbesondere darf der bisherige Status `deployed` nicht als `frontend published` interpretiert werden.

## V1.9.6 – lokaler Kandidat

Basis:
exakt verifizierte V1.9.4-Quelle.

Enthält V1.9.5:
- direkte Page-Publish-Migration;
- Publish-Status in Plan/Fingerprint/Readback;
- automatische Hard-Gate-Receipts;
- keine zusätzliche menschliche Review-/Deploy-Freigabeschleife im Normalweg.

Zusätzlich V1.9.6:
- echte inkrementelle Kategorie-Erweiterung;
- Erweiterungspaket enthält nur neue/geänderte Knoten;
- Server merged das Delta gegen die produktive Lifecycle-Baseline;
- nicht genannte Alt-Knoten bleiben vollständig erhalten;
- stabile `concept_id` bleibt Identität;
- neue Knoten = ADDED;
- Änderungen = UPDATED;
- Restbestand = UNCHANGED;
- fehlende Alt-Knoten sind **niemals** automatische Löschung;
- Delete-/Retirement-Intent im Extension-Vertrag = BLOCKED;
- falsche project_id = BLOCKED;
- optional falscher Baseline-Hash = BLOCKED;
- unbekannter Parent = BLOCKED.

Realer lokaler Buchbinden-Strukturtest:
- Baseline: 7 echte Buchbinden-Knoten;
- Sparse Extension: 1 synthetischer Test-Kindknoten;
- Ergebnis: 7 UNCHANGED + 1 ADDED;
- 0 RETIRED;
- automatic_delete=false.

Gesamttests:
- 263/263 PASS;
- Fresh-Source 263/263 PASS;
- Runtime Source↔Installer 23/23 byteidentisch;
- Installer PHP 17/17 PASS.

V1.9.6 Installer SHA-256:
`22d63c37ef61b42452751d40bb3fee11b7048241fb94e0706b76e5b5c8df8dc8`

V1.9.6 Source SHA-256:
`59d39226f2ef2f3ebaf97fb3802348677368e7ed07c48f9eacfeb20b16c3bfc8`

## Flexibilitätsvertrag

Der Kategorienbaum ist kein Einmalbau.

Spätere Ergänzungen müssen möglich sein für:
- neue Hobbyseiten;
- neue Zwischenebenen;
- neue Leaf-Kategorien;
- neue Magazin-Intents;
- neue HivePress-/Marketplace-Intents;
- kontrollierte Umbenennungen oder Parent-Verschiebungen.

Dafür darf niemals ein kompletter Neuaufbau des vorhandenen Baums erforderlich sein.

## Noch offen

Der Concept-Builder erzeugt weiterhin noch nicht automatisch den vollständigen 8-Welten-Gesamtbaum.
Die konzeptionelle obere Referenz für Buchbinden bleibt:
`Fertigen → Buch & Papier → Buchbinden`.

Frontend-Navigation ist weiterhin noch nicht real gebunden/readback-geprüft.

## NEXT ACTION

V1.9.6 über den aktuellen Pluginstand installieren.

Danach:
1. `Kategorien` öffnen;
2. **„Bestehenden Stand jetzt veröffentlichen“** ausführen;
3. realen WordPress-Readback prüfen;
4. anschließend Frontend-Sichtprüfung.

Erst danach wird der vollständige 8-Welten-/DataForSEO-Baum inkrementell erzeugt.
