# PROJEKTGEBÄUDE – PFERDE-ATELIER

STAND: 2026-09-13
STATUS: AKTIV

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Das Projektgebäude für das Pferde-Atelier.

**HIER BIST DU RICHTIG, WENN …**  
deine Aufgabe konkret zum Pferde-Atelier gehört.

**DU DARFST …**  
das Projekt lesen, das zuständige Büro auswählen und dort nach dessen Regeln arbeiten.

**DU DARFST NICHT …**  
am Gebäudeeingang quer durch mehrere Büros ändern, Fachgrenzen ignorieren oder ungeklärte Zuständigkeiten selbst erfinden.

**ALS NÄCHSTES …**  
das zuständige Büro auswählen und dessen `START_HERE.md` öffnen.

## AUTORITÄTSPLAN – NICHT DOPPELN

Für jedes Büro gilt genau eine Quelle pro Frage:

- **Was ist der aktuelle Fach-/Bestandsstand?** → Büro-`CURRENT_STATE.md`
- **Was wird JETZT bearbeitet / was ist NEXT ACTION?** → Büro-`HOBBYRAUM.md`
- **Welche Fehler sind bekannt?** → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → jeweilige Originalquelle
- **Welches Ziel gilt?** → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md` → Hauptquelle
- **Warum wurde etwas geändert?** → `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md` bzw. fachlokale Entscheidungsquelle, wenn die Regel ausschließlich einem Büro gehört
- **Was ist historisch?** → `protocol/PROJECT_MEMORY/ARCHIV/REGISTER.md`
- **Welche allgemeinen Module gibt es?** → `protocol/PROJECT_MEMORY/ALLGEMEINGUELTIGE_BAUSTEINE/MODULREGISTER.md`
- **Welche Pluginentwicklung/-aktualisierung wurde im Pferde-Atelier tatsächlich ausgeführt?** → `PLUGINS/UPDATEPROTOKOLL.md`; Fach-/Release-/LIVE-Wahrheit bleibt im jeweiligen Fachbüro

Der Gebäudeeingang selbst führt **keine zweite aktuelle Fachwahrheit**.

## Büroplan

- `TEXT/START_HERE.md` → Textmaschine / Artikelproduktion
- `PRODUKTVERGLEICH/START_HERE.md` → Produktvergleichs-Konzept / Vergleichsdefinition / Faktendossier / Übergabe an TEXT
- `WISSENSDATENBANK/START_HERE.md` → zentraler Themenpool, Recherche-Steuerung, Trust-Regeln und tatsächlich recherchierte Wissens-Aktenschränke
- `GLOSSAR/START_HERE.md` → öffentliches Glossar: Struktur, Kurzfassungen, SEO-Felder, WordPress-/Design-Anbindung
- `DESIGN/START_HERE.md` → Portaldesign
- `BILD/START_HERE.md` → projektspezifische Nutzung der allgemeinen Bildzentrale
- `AFFILIATE/START_HERE.md` → Affiliate-Zentrale / Release
- `HIVEPRESS/START_HERE.md` → Anzeigenmarkt / HivePress
- `GEMEINSAM/START_HERE.md` → echte projektübergreifende Regeln/Referenzen innerhalb des Pferde-Ateliers
- `PLUGINS/START_HERE.md` → Inventar-/Update-/Ausgabepult für tatsächlich entwickelte/aktualisierte Pferde-Atelier-Plugins; keine zweite Fach-/LIVE-Wahrheit

Historische Adresse `PFERDERASSEN/START_HERE.md` bleibt als Weiterweiser zum Aktenschrank `WISSENSDATENBANK/AKTENSCHRAENKE/PFERDERASSEN/` bestehen.

## Gemeinsame Regeln

- nicht raten;
- vorhandenen Arbeitsweg verwenden;
- keine Ersatzarchitektur erfinden;
- fremde Büros lesen erlaubt;
- fremde Büros nicht eigenmächtig verändern;
- ein Hobbyraum pro Fachbüro;
- Fehler/Änderungen dauerhaft referenzieren;
- Maschinenraum nur mit ausdrücklichem Fachauftrag;
- Masterdateien vollständig verwerten und zuordnen;
- bei tatsächlicher Pluginentwicklung/-aktualisierung PLUGINS-Büro nach dessen Regeln synchronisieren; isolierte `CURRENT.zip` bleibt nur abgeleitete hashgebundene Ausgabekopie.

## Dauerhafte Routingregel

Der Gebäudeeingang enthält keine temporären Chat-Zustände.

Für jedes Fachbüro gilt:
`START_HERE.md` → `CURRENT_STATE.md` → `HOBBYRAUM.md` → gebundener Arbeitsweg.

Parallel arbeitende Chats/Worker werden ausschließlich im zuständigen Büro/Hobbyraum oder Paul-Eingang gebunden.

## Globale Arbeitsort-Sperre

**Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.**

Autorität:
`protocol/PROJECT_MEMORY/BAUCONTAINER/EINGANGSSTANDARD.md` → **Backup-/Tresor-/Archiv-Sperre**.
