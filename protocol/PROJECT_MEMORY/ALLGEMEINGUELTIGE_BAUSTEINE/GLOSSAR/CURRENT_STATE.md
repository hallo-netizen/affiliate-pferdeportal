# UNIVERSAL GLOSSAR ENGINE – CURRENT_STATE

STAND: 2026-09-13
STATUS: 0.2.7 TECHNISCHER KANDIDAT / FRESH + IN-PLACE HARDTEST PASS / LIVE-RELEASE OFFEN

## Belastbarer Stand

- Modul: `MOD-008 – Universal Glossar Engine`.
- Neutraler wiederverwendbarer WordPress-Core; Pferde Atelier ist erste Projektanwendung.
- Eigener Glossar-Inhaltstyp und eigene hierarchische Oberbereiche.
- Vorhandene Seite kann als Glossar-Hauptseite gebunden werden.
- Eigene Zieladresse je veröffentlichtem Begriff.
- Suche, A–Z, Oberbereiche, Karten/Aufklapper, SEO-Felder und JSON-Import/Export vorhanden.
- Kein Bildzwang, kein Auto-Publish; Import bleibt Entwurf.

## Aktueller technischer Kandidat

Version:
`0.2.7`

Rewrite-Schema:
`5`

Branch:
`hobbyroom/glossar-027-release-hardtest-20260913`

Getesteter Commit:
`7191f15358cc73a78231652e9479f3a9fb5a9c37`

Autoritativer Run:
`34749231699`

Fresh-Install Job:
`103702569466` → PASS

Echter WordPress-In-place-Updateweg 0.2.5 → 0.2.7:
`103702569602` → PASS

Gated Package Job:
`103702749853` → PASS

Inneres Plugin-ZIP:
`universal-glossary-engine-0.2.7.zip`

SHA-256:
`e9c32fc64db3c64c3b85e0d2692ff200e8f6d60e5827d7ab514657adff2ae831`

Actions-Artefakt-ID:
`10315142446`

Äußerer Actions-Artefakt-Hash:
`975cc771cc109b62b56abafddc9e05334a4fd6f8b26535655c3fee4d3e8ed174`

Details:
`TESTPROTOKOLL_0.2.7_20260913.md`

## Versionsstatus

0.2.6 bleibt Entwicklungs-/Testhistorie und ist **kein aktueller Übergabekandidat**.

Grund:
0.2.6 wurde im Entwicklungsverlauf mehrfach als Kandidatenkennung verwendet. Deshalb wurde der erste übergabefähige Stand neu als 0.2.7 gebaut und vollständig erneut geprüft.

Dauerregel:
**Unterschiedliche Paketbytes = unterschiedliche Pluginversion.**

## Hart bewiesen

Fresh-Install:
- WordPress + MySQL + Astra;
- Version 0.2.7 / Schema 5;
- Policy-/Seed-Positiv-/Negativmatrix;
- echte Einzelbegriffsseiten mit Artikelmarkup/Inhalt;
- A–Z, Kartenlinks, Preview, Draft-/404-Sperren;
- AJAX positiv/negativ;
- Kategorie-/Begriffskollision;
- normale WordPress-Beiträge unverändert;
- Hero-Abstand, responsive Hero-Darstellung, Breadcrumb-Achse.

Upgrade 0.2.5 → 0.2.7:
- Rewrite-Regel unter 0.2.5 absichtlich entfernt → bekannter Begriff 404 / Schema 4;
- echter WordPress-Plugin-Updater installiert 0.2.7;
- installierte Dateien zeigen Version 0.2.7 / Schema 5;
- sofortiger Apache-Request wird wegen möglichem OPcache-Altbytecode sichtbar protokolliert und nicht als versteckter PASS gewertet;
- nach normaler OPcache-Timestamp-Revalidierung zwingend Schema 4 → 5;
- Rewrite-Regel wieder vorhanden;
- bekannter Begriff wieder echte 200-Artikelseite;
- danach komplette Positiv-/Negativ-/Regression-/Acceptance-Matrix erneut PASS.

Exaktes erzeugtes Artefakt anschließend lokal erneut geprüft:
- äußerer Hash PASS;
- innerer ZIP-Hash PASS;
- ZIP-Struktur PASS;
- Version 0.2.7 PASS;
- Rewrite-Schema 5 PASS;
- negativ: Pluginheader enthält keine aktuelle Version 0.2.6.

## Modulklasse

Formal weiterhin:
`UNGEKLÄRT / ZIEL ALLGEMEINGÜLTIG`.

Für formale Hochstufung fehlt weiterhin ein separates zweites reales Portal.

## Noch offen

- Pferde-Atelier-Installation/Readback des exakt hashgebundenen 0.2.7-Kandidaten;
- reale Sicht-/Funktionsabnahme der vier gemeldeten Pferde-Frontendpunkte;
- exakte Live-Rootcause der zuvor weißen Einzelbegriffseite ist nicht behauptet;
- aktueller Astra+Yoast-Kombinationstest, soweit für endgültigen Release erforderlich;
- realer Campus-Wissensdatenbankimport;
- größerer Bestands-/Performance-Test;
- separates zweites reales Portal.

Kein Pferde-Atelier-LIVE-PASS und kein endgültiger allgemeiner Release-PASS vor den gebundenen Realprüfungen.
