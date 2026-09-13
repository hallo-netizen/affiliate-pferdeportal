# MOD-008 – WAS / WARUM

STAND: 2026-09-13
STATUS: DAUERHAFTE ENTSCHEIDUNG

## WAS

Das öffentliche Glossar wird als eigener WordPress-Funktionsbaustein entwickelt:
`MOD-008 – Universal Glossar Engine`.

Architektur:
- ein neutraler, wiederverwendbarer Core;
- Pferde Atelier nur als erste Projektkonfiguration;
- kein Umbau des bestehenden Designplugins zur Glossar-Engine;
- keine zweite Glossar-Faktendatenbank;
- Fachdaten bleiben in der Wissensdatenbank;
- WordPress speichert nur die Veröffentlichungsfassung;
- eigener Glossar-Inhaltstyp und eigene Oberbereiche;
- vorhandene WordPress-Seite `Glossar` bleibt Haupt-/Einstiegsseite;
- Einzelbegriffe werden nicht als normale Beiträge oder manuell angelegte Seiten gepflegt;
- Felder, Gruppen, URL-Basis, SEO-Schemata und Designwerte sind konfigurierbar/erweiterbar;
- Import/Export strukturiert; Import ausschließlich als Entwurf;
- keine automatische Veröffentlichung.

## WARUM

Das bestehende Designplugin bleibt von Datenhaltung, URL-/SEO-Logik und Glossar-Backend getrennt. Der neutrale Core trennt Fachwissen, Veröffentlichungsdaten, Design und Portal-Konfiguration.

## VERSIONIERUNGS- UND UPDATE-REGEL AB 2026-09-13

WAS:
Materiell verschiedene Pluginpakete dürfen niemals unter derselben Versionsnummer ausgegeben oder als gleichwertig behandelt werden.

WARUM:
Bei 0.2.5 und anschließend während der 0.2.6-Entwicklung wurden Kandidatenstände unter bereits benutzten Versionskennungen erzeugt. Damit war die Versionsnummer allein nicht mehr ausreichend eindeutig.

KORREKTUR:
- 0.2.6 bleibt Entwicklungs-/Testhistorie und ist kein aktueller Übergabekandidat.
- Der erste eindeutig gebundene Übergabekandidat ist `0.2.7`.
- Unterschiedliche Paketbytes = unterschiedliche Pluginversion.

REGEL:
- Jede materielle Paketänderung erhält eine neue Pluginversion.
- Rewrite-relevante Änderungen erhalten zusätzlich eine neue `REWRITE_SCHEMA_VERSION`.
- Ein Kandidat wird an exakten ZIP-SHA-256 gebunden.
- Vor Ausgabe zwingend Fresh-Install UND echter WordPress-In-place-Updateweg positiv/negativ.
- Reines HTTP 200 reicht für Einzelbegriffe nicht; echter Glossar-Artikelinhalt muss nachgewiesen werden.
- Der Paketjob darf erst nach den gebundenen Fresh-/Upgrade-Hardtests laufen.
- Nach Paketbau wird das exakt erzeugte Actions-Artefakt nochmals lokal auf Hash, ZIP-Struktur, Version und Schema geprüft.

BELEG AKTUELL:
`TESTPROTOKOLL_0.2.7_20260913.md`
Run `34749231699`.

## PRÜFSTATUS

Technischer Kandidat 0.2.7:
- Fresh-Install PASS;
- echter WordPress-In-place-Updateweg 0.2.5 → 0.2.7 PASS;
- absichtlich defekter Rewritezustand unter 0.2.5 reproduziert;
- nach Update und normaler OPcache-Revalidierung Schema 4 → 5 bewiesen;
- komplette Frontend-/Regression-/Acceptance-Matrix erneut PASS;
- gated Package PASS;
- innerer Plugin-ZIP SHA-256: `e9c32fc64db3c64c3b85e0d2692ff200e8f6d60e5827d7ab514657adff2ae831`;
- exaktes Actions-Artefakt lokal erneut geprüft.

Kein Pferde-Atelier-LIVE-PASS behauptet.

Autoritative aktuelle Standquelle:
`CURRENT_STATE.md`

Aktuelle Arbeit:
`HOBBYRAUM.md`
