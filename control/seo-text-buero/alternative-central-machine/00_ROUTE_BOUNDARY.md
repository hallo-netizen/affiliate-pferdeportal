# SEO/TEXT-BÜRO – ALTERNATIVROUTE ZENTRALMASCHINE

Status: AKTIV – ausschließlich Konzept-/Hobbyraumroute
Branch: `alternative/seo-text-central-machine-20260908`
Ausgangsbasis: `914638e67a265cf2e8951b1177a7d80fdf904e98`
Datum: 2026-09-08

## Harte Trennung

Diese Route ist absichtlich vom laufenden STARTMASTER-/Reparaturweg getrennt.

VERBOTEN auf dieser Route:
- kein Schreiben auf `main`
- kein Merge nach `main` ohne ausdrückliche spätere Freigabe
- keine Änderung an Textmaschine, PPM, PSERC, PSTE oder LanguageTool
- keine Änderung an bestehenden Fach-, Inhalts-, SEO-, Qualitäts-, Design-, Tabellen-, Link-, Dubletten-/Kannibalisierungs- oder Publish-Regeln
- keine Änderung an CURRENT_STATE oder aktiven STARTMASTER-Step-Bundles
- keine WordPress-Schreibaktion
- kein Auto-Publish
- keine Nutzung dieser Route als Ersatzroute für einen BLOCKED-Zustand im laufenden Produktionsworkflow

## Unverhandelbare Zielregeln

1. Chat/KI hat 0,0 Workflow-Entscheidungsfreiheit.
2. Jeder Worker darf nur genau seinen gebundenen Mikroschritt ausführen.
3. Kein Worker darf Reihenfolge, Folgeschritt, Regeln oder Reparaturweg wählen.
4. Keine Worker-zu-Worker-Kommunikation.
5. Ein technischer, nicht-intelligenter Steuerkern besitzt allein Reihenfolge und Zustand.
6. Prüfer dürfen nur mechanisch nach festem Vertrag PASS oder BLOCKED liefern.
7. Bestehende Textmaschine bleibt unangetastet und autoritativ.
8. Das Konzept muss themenunabhängig, automatisierbar, nachhaltig und erweiterbar sein.
9. Nach Dateiausgabe muss eine manipulationssichere Übergabe bis WordPress vorgesehen werden; externe Signierung bleibt grundsätzlich erhalten.
10. Interne Signierung wird nicht als Voraussetzung wieder eingeführt.
11. Jede Konzeptänderung wird lokal positiv und negativ getestet, bevor sie als Kandidat gilt.

## Zweck

Nicht den bestehenden Produktionsweg reparieren.

Hier wird ausschließlich geprüft, ob eine alternative Architektur dieselben oder stärkere Sicherheitsgarantien mit weniger fehleranfälliger Übergabelogik erreichen kann.

Alle Ergebnisse dieses Chats werden ausschließlich in diesem Ordner/Branch dokumentiert.
