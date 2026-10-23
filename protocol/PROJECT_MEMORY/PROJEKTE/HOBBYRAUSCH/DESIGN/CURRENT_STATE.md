# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **MAGAZIN-ZIELSEITEN LIVE BEANSTANDET / HD-003 1.50.722 HARDROUTE LOKAL HARD PASS / CYBERDUCK-INSTALLATION OFFEN**

Zielvertrag:
**ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.5 / 2026-10-19**

## Live-Beanstandung

Die Magazin-Zielseiten zeigten trotz 1.50.721 weiterhin nicht den geforderten Magazin-Hubaufbau:
- kein Hero;
- kein Kachelbild als Hero;
- keine Brush-/Schreibschrift;
- keine grüne Lead-Box;
- kein Aufklapper.

1.50.721 ist nicht freigegeben.

## Neuer Kandidat 1.50.722

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.722_UPDATE_MAGAZIN_ZIELSEITEN_HARDROUTE.zip`

SHA-256:
`15e0bfa3fc861cf1dee11c8a8059d10dad4c743d4f52efeff28f091a233b184e`

Größe:
2,104,172 Bytes.

### Technische Ursache/Fix

Der bisherige Weg konnte ausfallen, wenn die Magazin-Zielseite vor dem Template-Routing nicht als normale WordPress-Seite klassifiziert wurde.

Reproduktion:
- 1.50.721 im Failure Mode: 0/12 Ziele übernehmen das HD-003-Template.
- 1.50.722 im identischen Failure Mode: 12/12 PASS.

1.50.722 bindet deshalb ausschließlich die 12 realen Magazin-Zielslugs direkt an `/magazin/<slug>/` bzw. den historischen `/journal/<slug>/`-Fallback.

### Verbindliches Zielseitendesign

Für jede Magazin-Zielseite:
- dasselbe Asset wie die Startseitenkachel;
- bestehender Hub2-Hero;
- grüne Schreibschrift + Brush/Bogen;
- erklärender Hero-Text;
- darunter grüne Lead-Box;
- Resttext nativ aufklappbar;
- danach passende Unteransichten/Beiträge/Monetarisierung.

Renderprüfung normale Ziele: 11/11 vollständig PASS.
Routingprüfung aller Ziele inkl. Hobbyfinder: 12/12 PASS.

### Paket

Hauptordner unverändert:
`affiliate-portal-template-kit/`

16 Dateien, inklusive Content-Template und aller benötigten Magazinbilder/Brush.

Plugin-Evidence:
`../PLUGINS/PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/EVIDENCE_1.50.722.md`

## EXAKT EINE NEXT ACTION

**1.50.722 per Cyberduck einspielen und anschließend eine Zielseite live abnehmen.**
