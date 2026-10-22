# SEO – CURRENT STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-22
STATUS: META-SCHABLONEN FESTGELEGT / PLUGIN 1.0.0 GEBAUT UND LOKAL GEPRÜFT / NOCH NICHT LIVE INSTALLIERT

## SEO-Titel

Für alle indexierbaren Inhalte:

[Originaltitel] - Hobby Depot

- Originaltitel unverändert.
- Keine individuelle SEO-Umschreibung.
- Einfacher Bindestrich mit Leerzeichen.
- Gilt für Beiträge, Seiten, Glossar, Kategorien und weitere indexierbare Inhaltstypen.

## Meta-Description

Grundmuster:

[Originaltitel] - [erste sinnvolle inhaltsspezifische Kernaussage]

Quellen-Priorität:
1. bewusste manuelle SEO-Description, falls vorhanden;
2. Einleitung oder Excerpt;
3. erster sinnvoller Satz des Hauptinhalts;
4. bei Kategorien erster sinnvoller Satz der Kategorienbeschreibung bzw. des Intros;
5. ohne belastbare Textquelle keine künstliche Standardfloskel.

## Ziel-Automatik

- Neue Beiträge, Seiten, Glossarbegriffe und Kategorien erhalten die Metadaten automatisch.
- Titeländerung aktualisiert den SEO-Titel automatisch.
- Inhalts- oder Einleitungsänderung aktualisiert die automatisch abgeleitete Description.
- Manuelle Description kann die Automatik später gezielt überschreiben.
- Keine doppelte Ausgabe von Title, Description oder Canonical.

## Technische Umsetzung

Plugin:
`HOBBY_DEPOT_SEO_1.0.0_META_AUTOMATIK.zip`

SHA-256:
`32bceb07a98ddb27f92371316be3395257e195e7fecf7e64f3ce6c2b373c0a33`

Größe:
4.316 Bytes.

Umfang:
- automatische SEO-Titel für öffentliche Beiträge, Seiten, öffentliche Custom Post Types und öffentliche Taxonomien;
- automatische Meta-Description aus Excerpt/Einleitung/Inhalt bzw. Kategorienbeschreibung;
- optionale manuelle Meta-Description im Backend;
- eigener Backend-Hinweis unter Einstellungen → Hobby Depot SEO;
- keine Änderung an Canonicals, Sitemaps, Robots oder Schema.

Lokale Prüfung:
- PHP-Syntax PASS;
- Beitragstitel PASS;
- automatische Beitrags-Description PASS;
- manuelle Description-Überschreibung PASS;
- Kategorietitel PASS;
- automatische Kategorie-Description PASS;
- ZIP-Integrität PASS.

## Status

Plugin fertig und im SEO-Büro abgelegt. Noch nicht live installiert.

## NEXT ACTION

**Nach Wiederherstellung des WordPress-Uploads Plugin 1.0.0 installieren und Frontend-Ausgabe auf einem Beitrag, einer Seite, einem Glossarbegriff und einer Kategorie live prüfen.**
