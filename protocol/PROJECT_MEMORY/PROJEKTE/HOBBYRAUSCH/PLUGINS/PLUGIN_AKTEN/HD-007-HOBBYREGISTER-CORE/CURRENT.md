# HD-007 – HOBBYREGISTER CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-24
STATUS: **HD-007 1.2.16 LAUT WORDPRESS-LISTE AKTIV / 862 INDIVIDUELLE HEADING-KORREKTUREN IN GITHUB VORBEREITET / KEIN LIVE-EINBAU ODER NEUE VOLL-ZIP VERIFIZIERT**

Plugin-ID:
`HD-007-HOBBYREGISTER-CORE`

Basis:
**1.2.14** war der tatsächliche jüngste Bildstand vor dieser Änderung.

Aktuelles Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.2.16_SEARCH_WIDTH_HARDPASS.zip`

SHA-256:
`3e5f46b1c2a7183df1b49d987ee8712c7c059eda18507de31de6d2a782cab78a`

Pluginroot:
`hd-hobbyregister-core/`

## Datenstand unverändert
- 862/862 Hobbys;
- 57/57 Traits;
- 862 statische Artikel, jeweils 8 Abschnitte;
- 24 final verifizierte Masterbilder aus 1.2.14 bleiben erhalten;
- Bildstatus-/Auditdateien bleiben erhalten.

## 1.2.15
- Register-Banner zwischen Suche/A–Z und Hobbygruppen.
- Schreibschrift + Brush auf Übersicht und Einzelprofil.
- Einzelprofil-Hero 238 px Desktop / 190 px mobil.
- exklusive Register-AJAX-Suche.

## 1.2.16
- sichtbare Überschrift „Hobby suchen“ entfernt;
- Placeholder im Eingabefeld: „Hobby suchen …“;
- Eingabefeld erhält `width:100%` und füllt wieder die komplette verfügbare Suchspalte bis zum Suchbutton;
- AJAX-Suche aus 1.2.15 funktional unverändert.

## QA
- echter 862er Datenbestand geladen: PASS;
- Register-Render: Suche → Banner → Hobbygruppen Reihenfolge PASS;
- Einzelprofil-Render inkl. Brush/Claim und flacher Hero-Höhe PASS;
- serverseitiger AJAX-Endpunkt: nur Register-URLs PASS;
- Client-Suchskript mit simuliertem Fetch: PASS;
- Render-Test: keine sichtbare Label-Zeile, Placeholder PASS, aria-label PASS;
- Browser-Geometrietest bei 1600 / 1024 / 760 / 390 px: Inputbreite = komplette verfügbare Feldbreite, PASS;
- Daten und Assets byteidentisch zu 1.2.15;
- Fresh-Unpack bytegleich zum getesteten Stand;
- PHP 4/4 PASS; ZIP CRC PASS; exakt ein Root `hd-hobbyregister-core/`.

## WordPress-Inventarabgleich 01.11.2026

Die vom Betreiber gelieferte vollständige WordPress-Pluginliste zeigt **Version 1.2.16 als aktiv**. Der zuvor dokumentierte Entwicklungs-/Teststand 1.2.16 ist versionsgleich, aber nicht dadurch funktional live-geprüft. Ein unabhängiger Server-Quellcode-/ZIP-Readback und ein Live-Funktionstest wurden in diesem Abgleich nicht ausgeführt. Keine Plugininstallation oder Campus-CURRENT.zip-Synchronisierung. Beleg: `../../EVIDENCE_WP_PLUGINLISTE_20261101.md`; operative WordPress-Current: `../../../WORDPRESS_TECHNIK/CURRENT_STATE.md`.

## EXAKT EINE NEXT ACTION

**Die aktive 1.2.16 read-only auf Frontend und Registrierungsfunktion prüfen; keine weitere Ordnerüberschreibung ohne aktuellen Bytevergleich.**


## 24.10.2026 – Bildproduktion Wiedereinstieg frisch geprüft
- Aktiver Server-/Arbeitsstand bleibt HD-007 1.2.16; die Suchfeldkorrektur hat Bilddaten und Assets gegenüber 1.2.14 nicht verändert.
- `hobby-image-production-status-v1.json`: 862 Gesamt, 24 DONE verifiziert, 838 offen.
- offene Aufteilung: 79 vorhandene CORE-Motive semantisch passend, aber technisch zu klein; 295 CORE-Motive semantisch verworfen; 464 ohne CORE-Motiv.
- aktiver abgeschlossener Master-Batch: `HD007_1.2.14_UNIQUE_MASTER_BATCH_02`.
- 24 finale Masterdateien sind im Plugin vorhanden.
- Kein neuer Bildbatch wurde beim Design-/Suchfix stillschweigend begonnen; keine Doppelproduktion.

## 01.11.2026 – Vollständige Überschriften-Korrekturliste, noch KEIN Plugin-Einbau

Der Betreiber meldete auf `/hobbyregister/muenzen/` semantisch falsche Überschriften: „Passt Münzen zu dir?“ und „Wo und wann kannst du Münzen ausüben?“. Die aktuelle HD-007-Version **1.2.16** erzeugt 862 Hobbyartikel mit acht Abschnitten; der zentrale Textvertrag verwendete blind `[Hobby]` statt einer grammatisch geeigneten Tätigkeitsform.

**Geprüfter Bestand:** 862/862 kanonische Hobbys und Kurzprofile aus der vorhandenen Hobby-Klassifikation, unabhängig mit dem 862er Hobby-Bildplan identitätsgenau abgeglichen (0 fehlende/zusätzliche Namen). Erarbeitet wurden **862/862** fachlich benannte Tätigkeitsformulierungen und daraus die sprachlich korrekten Alternativen für F2 und F3, ohne auch nur einen Hobby-Namen umzubenennen. F1 sowie F4–F8 bleiben bis zur vollständigen fachlichen Endkontrolle unberührt. Die Sammelbegriffe wurden einzeln geprüft; Fehlschlüsse wie „Pilzsuche sammeln“ oder „Postcrossing sammeln“ wurden verworfen und korrigiert.

**Reproduzierbare vollständige Liste im GitHub-Campus:** `../../../WISSENSDATENBANK/HOBBYREGISTER_862_UEBERSCHRIFTEN_KORREKTUR_20261101.csv`, plus `HOBBYREGISTER_862_UEBERSCHRIFTEN_AUDIT_20261101.md` und verbindlicher Regeländerung in `HOBBYREGISTER_TEXTREGELN_V1.md`.

**Technischer Blocker, nicht als Ausrede für ungetesteten Code übergehen:** HD-007 1.2.16-Voll-ZIP ist in der bestehenden Bibliothek vorhanden, ließ sich aber bei mehrfachem Original-Rohdateiabruf nicht materialisieren. Die Bilder und Quellcodedateien des installierten Originalplugins konnten daher nicht 1:1 bearbeitet oder bytevergleichend getestet werden. **Keine falsche Behauptung, dass die WordPress-Live-Überschriften korrigiert oder eine neue HD-007-ZIP gebaut wurden.**

**Nächster Schritt:** die echte 1.2.16 vollständig als editierbare Original-ZIP beschaffen/öffnen, die zentrale Headline-Ausgabe für F2/F3 aus der korrigierten ID-Zuordnung speisen und die 862er Ausgabe sowie Daten-/Bildbytegleichheit positiv und negativ testen. Danach nur das vollständige Originalplugin als neue Version ausgeben – **kein separates Plugin**.
