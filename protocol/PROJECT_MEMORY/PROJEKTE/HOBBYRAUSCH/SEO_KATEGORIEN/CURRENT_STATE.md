# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE ALTER SNAPSHOT / 1.14.12 REALER WORDPRESS-DRY-RUN BLOCKED / URSACHE EXAKT ISOLIERT / 1.14.13 LOCAL HARD PASS / KEIN SYNC**

## Zielvertrag

Aktiv:
`ZV-HOBBYRAUSCH-HD001-001` – Fassung **2.8 / 2026-10-17**.

Verbindlich für die unterste Hobby-Content-Ebene:
- kein starres Einheitsschema;
- bestehende gute Fachbereiche bleiben erhalten;
- Einstieg/Grundlagen und FAQ werden sichtbar abgedeckt;
- Vergleich & Kaufberatung wird bei jedem Hobby geprüft; eigener Leaf nur bei mindestens 3 eigenständigen Beratungs-/Vergleichsintents;
- Ausrüstung/Kosten wird sinnvoll abgedeckt, ohne künstliche Doppelung;
- Pflege, Wartung, Sicherheit, Fehler, Materialien, Methoden, Projekte, Orte, Lernen usw. nur, wenn sie fachlich zum Hobby passen, mindestens 3 eigenständige Intents tragen und keinen vorhandenen Bereich duplizieren;
- Anfänger und Fortgeschrittene müssen beide einen sichtbaren, sinnvollen Pfad erhalten.

## Verbindlicher V7.1-Zielbaum

V7.1 bleibt fachlich unverändert:
- 3517 logische Zielknoten;
- 3487 physische Zielobjekte;
- 862 aufgelöste Hobbyidentitäten;
- 383 CORE-Identitäten;
- 381 terminale Hobbyseiten;
- 2995 sichtbare CORE-Content-Kategorien;
- 381/381 Einstieg/Grundlagen;
- 381/381 FAQ;
- 381/381 Ausrüstung/Kosten-Abdeckung;
- 381/381 Vergleich & Kaufberatung;
- 381/381 mindestens zwei Fach-/Profi-Vertiefungsbereiche;
- pro Hobby 6–10 sichtbare Content-Leafs;
- jeder Leaf mindestens 3 eigenständige Beitragsintentionen;
- 0 TargetTree-Errors / 0 Warnings;
- Registry-/Renderer-Simulation 0 Abweichungen.

Wichtig:
Diese Zahlen beschreiben die geprüfte Zielstruktur, nicht ein starres Kategorienmuster.

## Reales WordPress-Ergebnis mit HD-001 1.14.12

Der Nutzer hat 1.14.12 installiert und den Finalen Delta-Dry-Run ausgeführt.

Reales Ergebnis:
- Status BLOCKED;
- Zielobjekte 2642;
- CREATE 279;
- ADOPT 4;
- UPDATE 2357;
- UNCHANGED 0;
- ARCHIVE 0;
- kein Apply/Sync.

Blocker:
- Libellenbeobachtung: vorhandene Seite mit demselben Slug war noch an ihre frühere Zielidentität gebunden;
- Nachtvogel-Beobachtung: vorhandene Seite mit demselben Slug war noch an ihre frühere Zielidentität gebunden.

Zusätzlich beweist die Zahl 2642, dass der reale Final-Dry-Run nicht den eingebetteten V7.1-Zielbaum mit 3487 Zielobjekten verwendet hat, sondern noch einen älteren extern gebundenen Zielprofilstand.

## Ursache

Keine neue Fachstruktur ist nötig.

Es liegen genau zwei technische Altbindungsprobleme vor:

1. Der Final-Dry-Run akzeptierte weiterhin einen extern gesetzten Zielprofilpfad und konnte dadurch den alten 2642er Stand statt des eingebetteten V7.1-Profils verwenden.
2. Beim Wechsel der 51 neu stabil gebundenen Proposal-Hobbyseiten auf ihre neue Identität wurde eine vorhandene frühere Target-Bindung nicht als zulässige Legacy-Bindung erkannt. Dadurch wurden bei Libellenbeobachtung und Nachtvogel-Beobachtung vorhandene korrekte Seiten fälschlich als Fremdkollision behandelt.

## Korrigierter Kandidat HD-001 1.14.13

Artefakt:
`HD001_V1.14.13_HOBBY_DEPOT_V7_1_LIVE_COLLISION_FIX_LOCALPASS.zip`

SHA-256:
`c543ac655f12d4fcb0d5cb581b3f8a3410103988655a87bb62bab9cbd9995fa3`

Eingebettetes V7.1-Profil nach Migrationsergänzung:
SHA-256:
`23c707b38f1892703f959c5374b736c7b85fa4db56023a22e987debdc215911f`

Korrektur:
- Finaler Hobby-Depot-Dry-Run verwendet für diesen Pfad hart das eingebettete V7.1-Profil und kann nicht mehr durch den alten externen Profilpfad ersetzt werden;
- 51 bereits bekannte Proposal-Hobbyseiten besitzen zusätzlich ihre frühere Target-Identität als reine Migrationsbindung;
- Dry-Run und späterer bestätigter Sync können eine vorhandene Seite über diese frühere Target-Bindung sauber wiederverwenden;
- eine wirklich fremd gebundene Seite mit gleichem Slug blockiert weiterhin fail-closed;
- doppelte/mehrdeutige Legacy-Bindungen blockieren weiterhin fail-closed;
- keine Fachstruktur, keine Leaf-Inhalte und keine Architektur wurden geändert.

## Lokale Prüfung 1.14.13

PASS:
- PHP 33/33;
- ZIP-Roundtrip PASS;
- V7.1 3517 / 3487 / 862 / 383 / 381 / 2995 unverändert;
- 381/381 FAQ;
- 381/381 Vergleich & Kaufberatung;
- Anfängerabdeckung 381/381;
- Leaf-Breite 6–10 unverändert;
- simuliertes altes externes 2642er Profil kann den Final-Dry-Run nicht mehr übersteuern;
- Libellenbeobachtung wird über ihre frühere Target-Bindung wiederverwendet;
- Nachtvogel-Beobachtung wird über ihre frühere Target-Bindung wiederverwendet;
- alle 51 Proposal-Hobbyseiten mit früherer Target-Bindung simuliert: PASS;
- fremde Slug-Kollision: BLOCKED;
- mehrdeutige Legacy-Bindung: BLOCKED;
- Provider Calls 0;
- WordPress Structure Writes 0;
- Dry-Run startet keinen Apply.

## Mega-Struktur

Unverändert:
Gestalten 7 · Fertigen 10 · Technik 9 · Forschen 8 · Pflanzen 9 · Tiere 7 · Bewegen 8 · Sammeln 9.

## Identitäten / Magazin

Unverändert:
- 51/51 neue CORE-Hobbyseiten stabil gebunden;
- stale Overrides 0;
- Plane Spotting → Spotting & Verkehr;
- Sondeln + Metalldetektion = eine kanonische Hobbyidentität;
- Magazin-Audit 77 Kandidaten / 35 eindeutige Porträt-Owner / 0 offene Owner-Reviews.

## ERSTER OFFENER BLOCKER

**Der echte WordPress-V7.1-Dry-Run mit HD-001 1.14.13 fehlt.**

## EXAKT EINE NEXT ACTION

**HD-001 1.14.13 über die aktuell installierte 1.14.12 installieren und anschließend ausschließlich den Finalen Delta-Dry-Run ausführen. Keinen Apply/Sync bestätigen.**

Abnahme direkt danach:
- Zielobjekte müssen 3487 sein, nicht 2642;
- die beiden bisherigen Kollisionen Libellenbeobachtung/Nachtvogel-Beobachtung dürfen nicht mehr auftreten;
- erst dann das vollständige reale Dry-Run-Ergebnis gegen V7.1 prüfen.
