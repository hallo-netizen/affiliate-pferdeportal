# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE ALTER SNAPSHOT / 1.14.12 REALER DRY-RUN BLOCKED / 1.14.13 WEGEN ADMIN-LAST VERWORFEN / 1.14.14 HARD SIM PASS / KEIN SYNC**

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

Fachlich unverändert:
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
- jeder Leaf mindestens 3 eigenständige Beitragsintentionen.

## Reales WordPress-Ergebnis 1.14.12

Vom Nutzer ausgeführt:
- BLOCKED;
- Zielobjekte 2642;
- CREATE 279;
- ADOPT 4;
- UPDATE 2357;
- ARCHIVE 0;
- kein Apply/Sync.

Blocker:
- Libellenbeobachtung;
- Nachtvogel-Beobachtung.

Beide Slugs existieren bereits und tragen noch ihre frühere Target-Bindung.

## Nachprüfung 1.14.13 – wichtiger neuer Befund

1.14.13 ist **verworfen**.

Nicht wegen der Fachstruktur, sondern wegen eines von der lokalen Vorprüfung übersehenen Admin-Lastfehlers:

Beim bloßen Öffnen der Seite `Finaler Zielbaum` wurde jedes Mal der komplette Frontend-/Struktur-Readback ausgeführt.

1:1-Simulation des echten Admin-Renderpfads mit V7.1:
- 762 Seitenlesungen;
- 1524 Seiten-Metalesungen;
- 2995 Termlesungen;
- 11980 Term-Metalesungen;
- zusätzlich Navigation-/URL-Auflösung;
- alles bereits beim normalen Seitenaufruf, ohne Klick auf Dry-Run.

Das erklärt die vom Nutzer gemeldete extreme Backend-Langsamkeit und die Gateway-Timeout-Gefahr.

Zusätzlich blieb der gespeicherte alte 1.14.12-Dry-Run sichtbar. Dadurch wurden weiterhin 2642 und die alten zwei Kollisionen angezeigt, obwohl dies kein neu ausgeführter 1.14.13-Nachweis war.

## Korrigierter Kandidat 1.14.14

Artefakt:
`HD001_V1.14.14_HOBBY_DEPOT_V7_1_BACKEND_LOAD_FIX_HARDPASS.zip`

SHA-256:
`fdcca9282b0edcb5e0bb557b9f1fc5ec6cfc3c127afb40b6dc531340f653642a`

V7.1-Profil unverändert:
SHA-256:
`23c707b38f1892703f959c5374b736c7b85fa4db56023a22e987debdc215911f`

Korrektur:
- normaler Admin-Seitenaufruf führt keinen Voll-Readback mehr aus;
- bereits beim Sync gespeicherter Readback wird nur wiederverwendet;
- alter gespeicherter Dry-Run einer früheren Pluginversion wird nicht mehr als aktuelles Ergebnis angezeigt;
- Final-Dry-Run bleibt hart an V7.1 gebunden;
- Legacy-Bindungen für die 51 Proposal-Hobbyseiten bleiben erhalten;
- keine Fachstruktur, kein Navigationsmodell und keine Architektur geändert.

## Harte Simulation 1.14.14

Admin-Aufruf mit altem 2642er gespeicherten Ergebnis:
- Seitenlesungen 0;
- Seiten-Metalesungen 0;
- Termlesungen 0;
- Term-Metalesungen 0;
- alter 2642er Ergebnisblock wird nicht als aktueller Dry-Run angezeigt;
- stattdessen Hinweis: alter Prüflauf, neu ausführen.

Kompletter V7.1-Dry-Run gegen den letzten vollständig synchronisierten 2357er Bestand plus die beiden real beobachteten alten Target-Seiten:
- PASS;
- 3517 logisch;
- 3487 physisch;
- 862 Entities;
- 383 CORE;
- CREATE 1126;
- ADOPT 3;
- UPDATE 2358;
- ARCHIVE 1;
- Errors 0;
- Libellenbeobachtung = vorhandene Altseite wird UPDATE/reuse;
- Nachtvogel-Beobachtung = vorhandene Altseite wird UPDATE/reuse;
- Trainspotting / Modellraketen / Pflanzenbestimmung = ADOPT.

Negativ:
- wirklich fremd gebundener gleicher Slug = BLOCKED;
- doppelte Legacy-Target-Bindung = BLOCKED.

PHP 33/33 PASS.
ZIP-Roundtrip 44/44 PASS.

## Navigation

Keine neue Navigationsidee und kein Architekturumbau.

Live bleibt weiterhin der alte aktive Snapshot. Deshalb kann die neue V7.1-Navigation noch nicht vollständig sichtbar sein. Der Renderer-/Mega-Menü-Stand bleibt separat unverändert; zuerst muss der V7.1-Dry-Run sauber sein und danach der ausdrücklich bestätigte Sync erfolgen.

## ERSTER OFFENER BLOCKER

**Echter WordPress-V7.1-Dry-Run mit 1.14.14 fehlt.**

## EXAKT EINE NEXT ACTION

**HD-001 1.14.14 über die aktuell installierte Fassung installieren, Seite `Finaler Zielbaum` neu öffnen und ausschließlich den Finalen Delta-Dry-Run ausführen. Keinen Apply/Sync bestätigen.**

Abnahme:
- Backend-Seite muss ohne den bisherigen Voll-Readback laden;
- alter 2642er Prüflauf darf nicht als aktuelles Ergebnis erscheinen;
- neuer Dry-Run muss 3487 Zielobjekte verwenden;
- Libellenbeobachtung und Nachtvogel-Beobachtung dürfen nicht mehr als LIVE_COLLISION erscheinen.
