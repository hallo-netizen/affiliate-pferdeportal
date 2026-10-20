# HOBBYRAUSCH – WORDPRESS_TECHNIK – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-20
STATUS: **HOBBYFINDER-RUNTIME LOKAL HARD PASS / LIVE-INSTALLATION OFFEN**

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_WORDPRESS_TECHNIK`.

## Laufzeitarchitektur

KISS-Vertrag:
- zentrale fachliche Hobbydaten bleiben im Hobbyregister der Wissensdatenbank;
- **HD-007 Hobbyregister Core 1.0.0** = schlanke read-only WordPress-Laufzeitprojektion;
- **HD-003 1.50.704** = Darstellung/Finder und liest HD-007;
- **HD-004** bleibt zentrale read-only Kategorie-/Objektauflösung;
- keine neue Tabelle;
- keine zweite Hobby-Datenbank;
- keine Cronjobs;
- kein Netzwerkzugriff;
- keine Kategorie-Writes.

## HD-007

Artefakt:
`/Hobby Depot/Plugin-Büro/HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.0.0_READONLY_LOCALPASS.zip`

SHA:
`3887c914b5193f35e1ac5297fa96e2917d0d70effaae51de59501de0d3dcb8ba`

Lokale QA:
862/862 Runtime PASS; PHP 2/2; keine DB-Writes/Cron/Netzwerk; ZIP PASS.

## HD-003 1.50.704

Artefakt:
`/Hobby Depot/Plugin-Büro/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.704_HOBBYFINDER_RUNTIME_LOCALPASS.zip`

SHA:
`558ed2a17cd5123cdad5c7719d2554d64e413f628f29a07a1d06e6b4dca476fc`

Lokale Integration:
- 862 Finder-Datensätze;
- 862 Kurzprofile;
- Finder-Route PASS;
- fehlendes HD-007 fail-closed PASS;
- JS Syntax PASS;
- 383 zentrale CORE-Ziele im Harness auflösbar;
- keine erfundenen URLs.

## ERSTER OFFENER BLOCKER

Live fehlen Installation/Aktivierung und echter Frontend-Readback.

## EXAKT EINE NEXT ACTION

**HD-007 1.0.0 installieren/aktivieren → HD-003 1.50.704 installieren → Hobbyfinder real prüfen. Kein HD-001-Sync als Teil dieses Schritts.**
