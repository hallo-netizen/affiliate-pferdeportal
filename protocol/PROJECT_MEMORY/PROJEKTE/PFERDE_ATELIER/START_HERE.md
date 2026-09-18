# PROJEKTGEBÄUDE – PFERDE-ATELIER

STAND: 2026-09-16
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

## AUTORITÄTSPLAN – EINE WAHRHEIT

Einzige Routingautorität für die Frage **„Wo liegt die aktuelle Wahrheit dieses Büros?“**:
`protocol/PROJECT_MEMORY/AUTORITAETSPLAN.json`.

Der Gebäudeeingang enthält selbst keinen dynamischen Bürostatus.

Pflichtweg:
`Büro-START_HERE → AUTORITAETSPLAN → genau eine Current-Autorität → Frischecheck → NEXT ACTION`.

`HOBBYRAUM.md` ist nur abgeleitete Ausführungsfläche und darf Current-Status oder NEXT ACTION nicht als zweite Autorität führen.

CAMPUS_SINGLE_TRUTH_ENTRY_V1

## Büroplan

- `TEXT/START_HERE.md` → Textmaschine / Artikelproduktion
- `TEXTSYSTEM_4A/START_HERE.md` → isolierter Universalitäts-/Vereinfachungsprototyp für den vollständigen Artikelworkflow; keine eigene Fach-/Design-/Qualitätsautorität
- `PRODUKTVERGLEICH/START_HERE.md` → Produktvergleichs-Konzept / Vergleichsdefinition / Faktendossier / Übergabe an TEXT
- `WISSENSDATENBANK/START_HERE.md` → zentraler Themenpool, Recherche-Steuerung, Trust-Regeln und tatsächlich recherchierte Wissens-Aktenschränke
- `DESIGN/START_HERE.md` → Portaldesign
- `BILD/START_HERE.md` → projektspezifische Nutzung der allgemeinen Bildzentrale
- `AFFILIATE/START_HERE.md` → Affiliate-Zentrale / Release
- `HIVEPRESS/START_HERE.md` → Anzeigenmarkt / HivePress
- `TECHNIK/START_HERE.md` → WordPress-/Hosting-Betrieb, Speicher-/Backupdiagnose und sichere technische Wartung ohne Fachinhaltsänderung
- `PLUGINS/START_HERE.md` → zentraler Plugin-Bestand, Updatekontrolle und isolierte aktuelle Ausgabeartefakte
- `GEMEINSAM/START_HERE.md` → echte projektübergreifende Regeln/Referenzen innerhalb des Pferde-Ateliers

Historische Adresse `PFERDERASSEN/START_HERE.md` bleibt als Weiterweiser zum Aktenschrank `WISSENSDATENBANK/AKTENSCHRAENKE/PFERDERASSEN/` bestehen.

## Gemeinsame Regeln

- nicht raten;
- vorhandenen Arbeitsweg verwenden;
- keine Ersatzarchitektur erfinden;
- fremde Büros lesen erlaubt;
- fremde Büros nicht eigenmächtig verändern;
- ein Hobbyraum pro Büro;
- Fehler/Änderungen dauerhaft referenzieren;
- Maschinenraum nur mit ausdrücklichem Fachauftrag;
- Masterdateien vollständig verwerten und zuordnen.

### Plugin-Pflicht bei echter Pluginänderung

Wenn ein Chat im Pferde-Atelier tatsächlich ein Plugin entwickelt oder auf eine neue Version aktualisiert, muss er vor Abschluss zusätzlich `PLUGINS/START_HERE.md` lesen und den neuen belastbaren Stand nach `PLUGINS/SYNC_VERTRAG.md` synchronisieren.

Keine Pluginänderung → PLUGINS-Büro nicht künstlich ändern.
Fehlende/eindeutig nicht bindbare aktuelle ZIP → `Plugins: BLOCKED`, niemals raten.

## Dauerhafte Routingregel

Der Gebäudeeingang enthält keine temporären Chat-Zustände.

Für jedes Büro gilt:
`START_HERE.md` → `AUTORITAETSPLAN.json` → genau eine Current-Autorität → Frischecheck → deren NEXT ACTION → nur falls gebunden: Ausführungsfläche.

Parallel arbeitende Chats/Worker werden ausschließlich im zuständigen Büro/Hobbyraum oder Paul-Eingang gebunden.

## Globale Arbeitsort-Sperre

**Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.**

Autorität:
`protocol/PROJECT_MEMORY/BAUCONTAINER/EINGANGSSTANDARD.md` → **Backup-/Tresor-/Archiv-Sperre**.
