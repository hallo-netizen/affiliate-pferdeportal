# PFERDE-ATELIER – PLUGINS – HOBBYRAUM

STAND: 2026-09-15
STATUS: BLOCKED

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Arbeitsraum für die zentrale Plugin-Inventarisierung und Artefakt-Synchronisierung des Pferde-Ateliers.

**HIER BIST DU RICHTIG, WENN …**  
ein Plugin neu entwickelt/aktualisiert wurde oder der zentrale isolierte Pluginbestand vervollständigt werden soll.

**DU DARFST …**  
autoritative Fach-/Releasequellen frisch prüfen und daraus nur belegte isolierte Ausgabeartefakte synchronisieren.

**DU DARFST NICHT …**  
aus Altmastern raten, Fachstatus überschreiben oder einen fehlenden aktuellen Installer durch einen älteren Stand ersetzen.

**ALS NÄCHSTES …**  
`REGISTER.md` → nur Einträge mit `ARTEFAKT_SYNC: BLOCKED` bearbeiten.

## BEREITS REAL SYNCHRONISIERT

- PPA-001 Affiliate-Zentrale 6.72.19
- PPA-003 Bildzentrale 2.6.9
- PPA-004 Universal Research & Fill 1.9.9
- PPA-005 Portal SEO Topic Engine 0.56.25
- PPA-007 Pferde Atelier HivePress Anzeigensuche 2.1.5
- PPA-011 Pferde Atelier – Pferderassen Manager 0.2.7

Physische Ausgabekopien:
`/Campus-Plugins/PFERDE_ATELIER/<PLUGIN-ID>/CURRENT.zip`

Zu jedem synchronisierten Stand liegt dort `MANIFEST.md`.

PPA-011 wurde nach WordPress-LIVE-PASS synchronisiert und aus der persistenten Ablage erneut geprüft:
- `CURRENT.zip` vorhanden;
- `MANIFEST.md` vorhanden;
- SHA-256 PASS;
- ZIP-Lesetest PASS;
- Version 0.2.7 PASS.

## BLOCKED

- PPA-002 Pferde Design 1.50.472: exakter Installername + SHA belegt, Binärdatei aktuell nicht direkt erreichbar.
- PPA-006 Editorial Plan Compiler: 0.28.16 ist als Datei belegbar, historische spätere 0.28.17 ist aber keine CURRENT-Autorität; deshalb keine CURRENT.zip.
- PPA-008 Universal Product Comparison 0.8.0-prototype: hashgebundene aktuelle ZIP ist Fachautorität, Datei aktuell nicht in Library/GitHub erreichbar.
- PPA-009 Universal Product Knowledge: 0.5.0 ist als reale 0.8-Abhängigkeit belegt, exakte aktuelle Installer-ZIP + Hash noch nicht CURRENT-gebunden.

PPA-010 allgemeines Kategoriemodell 1.8.0 wird hier erst gespiegelt, wenn eine aktive Pferde-Projektanwendung frisch belegt ist.

## NEXT ACTION

Nur die vier verbleibenden BLOCKED-Einträge aus ihren autoritativen Quellen vervollständigen.

## RÜCKGABEWEG

Ein Eintrag darf erst auf `ARTEFAKT_SYNC: PASS`, wenn:
- exakter aktueller Quellstand belegt;
- isolierte ZIP real vorhanden;
- SHA-256 stimmt;
- ZIP-Lesetest PASS;
- erforderliche Fach-/Regressionstests belegt;
- persistente Ausgabekopie + Manifest readback-geprüft.
