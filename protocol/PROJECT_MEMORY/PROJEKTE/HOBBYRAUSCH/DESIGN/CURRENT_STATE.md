# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **LIVE HD-003 1.50.711 / 1.50.716 UPDATE LOKAL HARD PASS / CYBERDUCK-INSTALLATION OFFEN**

Zielvertrag:
**ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.5 / 2026-10-19**

## Live

Aktuell live und zuletzt belastbar:
**HD-003 1.50.711**.

## Lokaler Kandidat 1.50.716

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.716_UPDATE_MAGAZIN_STARTSEITE.zip`

SHA-256:
`072fdbe2fff7b8b4ef32ea3f70f08e1e1de700fb17d784b7e821e2735a1335f1`

Größe:
577,195 Bytes.

Das Paket ist ein **UPDATE**, kein Full-Plugin. Hauptordner bleibt immer:
`affiliate-portal-template-kit`.

### Magazin-Startseite

Die bereits vorhandene Magazinseite erhält jetzt eine eigene Hub-Darstellung in der bestehenden Hobby-Depot-Designsprache.

Exakt die vorhandenen 12 Magazin-Ziele werden verwendet:
1. Hobbyfinder
2. Alter & Lebensphasen
3. Geschichte & Herkunft
4. Hobby-Porträts
5. Hobby-Ideen & Inspiration
6. Menschen & Geschichten
7. Neue Hobbys & Trends
8. Saison, drinnen & draußen
9. Ungewöhnliche & skurrile Hobbys
10. Vergleiche & Alternativen
11. Wissen & Glossar
12. Zeit, Budget & Platz

Keine neue Kategorie erfunden oder angelegt.

Design:
- großes eigenes Magazin-Hero mit vorhandenem Hobby-Depot-Fotoasset;
- 12 bebilderte Themenkacheln;
- Desktop 3 Spalten, Tablet 2, Mobil 2;
- aktuelle Magazinbeiträge als redaktionelles Kartenraster;
- gleiche Typografie, Petrolfarbe, Radien und Abstände wie der aktuelle Hobby-Depot-Auftritt.

Monetarisierung:
- Bannerfläche über vorhandenen Slot `journal_banner`;
- Produktfläche über `journal_product_1–3`;
- Affiliate-Artikel-/Kaufberatungsbereich für entsprechend markierte/erkannte Beiträge;
- bestehende direkte Werbefläche über Placement `journal`;
- leere Affiliatebereiche bleiben öffentlich unsichtbar, eingeloggte Admins sehen Prüfvorschauen.

### Aus 1.50.715 erhalten

- Footer 4 Spalten;
- PB one öffnet neues Fenster;
- FAQ-Seite 6 Bereiche / 30 Fragen;
- kein neues Zusatzplugin.

## Lokale Prüfung

- UPDATE-ZIP exakt 2 Dateien;
- PHP-Lint PASS;
- Fresh-Unpack PASS;
- alle verwendeten Bildpfade vorhanden;
- vorhandene Journal-Slot-Matrix wiederverwendet;
- keine neue Magazin-/Affiliate-Architektur.

Plugin-Evidence:
`../PLUGINS/PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/EVIDENCE_1.50.716.md`

Kein Live-PASS für 1.50.716 behaupten.

## EXAKT EINE NEXT ACTION

**1.50.716-UPDATE per Cyberduck in den bestehenden Pluginordner einspielen und danach die Magazin-Startseite live abnehmen.**
