# HOBBYREGISTER – REFERENZTRANSFER REGISTERDESIGN V1

STAND: 2026-10-23
STATUS: BINDING

## Auftrag

Für Hobby Depot wird das bewährte Registerprinzip der bestehenden Referenz übernommen.
Übernommen werden ausschließlich:
- Informationsarchitektur;
- Seitenaufteilung;
- Interaktionsprinzip;
- Karten-/Hero-/Sidebar-Grunddesign;
- Relation „gleiche Gruppe“ / „ähnliche Einträge“.

Nicht übernommen werden:
- fachliche Begriffe;
- Bilder;
- Gruppenbezeichnungen;
- Kategorien;
- Datenmodelle;
- URLs;
- Pferde-/Rasseninhalte.

## Hobbyregister-Übersicht

Verbindliche Reihenfolge:
1. Breadcrumb;
2. Hero;
3. Suche;
4. A–Z;
5. acht Hobbygruppen;
6. „Hobbys im Überblick“;
7. 4-spaltige Karten auf Desktop;
8. 16 Hobbys je Seite;
9. Pagination.

Die acht Hobbygruppen sind die bestehenden geschützten Hobby-Depot-Welten:
**Gestalten · Fertigen · Technik · Forschen · Pflanzen · Tiere · Bewegen · Sammeln.**

Sie sind Register-Views über den zentralen Bestand, keine zweite persistente Hobby-Taxonomie.
Mehrfachzuordnung ist erlaubt, wenn zentrale Traits sie tragen.

## Detailseite

Verbindliche Aufteilung:
- Breadcrumb;
- breiter Hero mit Hobbyname und Bild;
- links „Auf einen Blick“;
- Hauptspalte mit Schema-F-Fließtext;
- Verweis auf die Hobbygruppe;
- „Aus derselben Hobbygruppe“;
- „Ähnliche Hobbys“;
- zurück zur Register-Startseite;
- Verweis ins Hobbymagazin.

F9 liefert die Schnellfakten.
F10 liefert Relationskarten aus dem zentralen Traitbestand.

## Technik

HD-007 bleibt die zuständige Laufzeitprojektion.
Keine 862 WordPress-Seiten als zweite Datenhaltung.
Keine neue Tabelle.
Keine DB-Writes.
Keine Cronjobs.
Keine Netzwerkabhängigkeit.

Frontendprofile werden read-only aus dem zentralen Register erzeugt.

## Prototypregel

Vor Massenproduktion werden genau zwei vollständige Detailtexte visuell/sprachlich geprüft:
- Buchbinden;
- Slacklining.

Andere Hobbyprofile dürfen im Prototyp bereits navigierbar sein, zeigen aber bis zur Freigabe nur das vorhandene Kurzprofil + strukturierte Fakten/Relationen.
