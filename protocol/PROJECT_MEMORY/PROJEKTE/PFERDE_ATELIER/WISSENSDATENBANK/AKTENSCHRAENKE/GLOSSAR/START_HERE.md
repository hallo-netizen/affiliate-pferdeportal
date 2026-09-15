# AKTENSCHRANK GLOSSAR

STAND: 2026-09-15
STATUS: AKTIV / FACHWÖRTERBUCH-MODELL

## WAS IST DAS?

Die zentrale quellengebundene Fachbegriffs-Datenbasis des Pferde-Ateliers.

Das öffentliche Glossar ist **kein zweites Pferde-Atelier in klein**, sondern ein Fachwörterbuch.

## BEGRIFFSGRENZE

Ein Begriff gehört als eigene Glossarseite hierher, wenn sein Hauptzweck die Erklärung eines Fachworts ist und die wesentliche Nutzerfrage mit einer kompakten Definition/Einordnung beantwortet werden kann.

Nicht als eigene Glossarseite anlegen, wenn der Begriff selbst bereits ein größeres Themenfeld, eine starke Portal-/Kategorie-/Rassengruppenseite oder einen eigenständigen Ratgebergegenstand bildet. Dann bleibt die Erklärung auf dieser Hauptseite; das Glossar darf später als Wegweiser dorthin verweisen.

Beispiel: `Warmblüter` → keine zusätzliche Glossarseite; Erklärung auf der Rassengruppenseite Warmblüter.

## PFLICHTBEZIEHUNGEN

Jeder öffentliche Glossarbegriff besitzt:
- genau eine primäre **Themenwelt** (`uge_group`);
- mindestens einen **verwandten Begriff**;
- optional genau eine **passende Hauptseite** (WordPress-Seite oder Kategorie), wenn eine starke thematische Heimat existiert.

Synonyme sind Aliase und keine zweiten Datensätze.

## RECHERCHE + TEXT

Ein Glossar-Worker recherchiert und formuliert denselben Begriff in einem Arbeitsschritt. Verbindlich ist `../../RECHERCHE_STANDARD.md`.

Kurzvertrag:
- 150–200 Wörter;
- individueller Einstieg;
- Begriff fachlich erklären und sauber abgrenzen;
- keine Generator-/Schablonenphrasen;
- kein Keyword-Stuffing;
- 0 Bodylinks;
- individuelle SEO-Titel und Meta-Description;
- Quellen bleiben gebunden;
- unsichere Fakten → `NACHRECHERCHE`, niemals raten.

## PRODUKTIONSWEG

`Begriffspool → Begriffsabgrenzung → Recherche + Text → Campus-Datensatz → PA_GLOSSARY_BATCH_V2 → Glossar-Manager → WordPress-Draft → Readback → Freigabe`

Die alte autonome Discovery-/Cron-/Loopback-Automation ist **nicht mehr Produktionsweg**. Technische Wahrheit dazu: `TECHNIK_GLOSSAR_MANAGER_CURRENT.md`.

## AKTUALISIERUNG

Jeder Begriff führt `last_verified_at` und ein Prüfintervall:
- 6 Monate: Medizin/Gesundheit sowie andere zeit- oder risikosensitive Fachthemen;
- 12 Monate: normale Fachbegriffe;
- 24 Monate nur für ausdrücklich stabile historische/terminologische Inhalte.

`Glossar → Prüfbedarf` zeigt fällige Begriffe. Die Prüfungsliste ändert keine Inhalte automatisch; jede Aktualisierung läuft wieder durch Recherche, Validator und Readback.

## ABLAGE

- Strukturvertrag: `GLOSSAR_STRUKTUR.md`
- Register: `GLOSSAR_REGISTER.md`
- Datensätze: `DATEN/`
- Technik/WordPress: `TECHNIK_GLOSSAR_MANAGER_CURRENT.md`
