# UNIVERSAL GLOSSARY ENGINE – TESTPROTOKOLL 0.2.7

STAND: 2026-09-13
STATUS: TECHNISCHER KANDIDAT PASS / KEIN PFERDE-LIVE-PASS

## Grund für 0.2.7

0.2.6 wurde im Entwicklungsverlauf mehrfach als Kandidatenkennung verwendet. Damit war die Versionsnummer nicht mehr eindeutig genug für eine Übergabe.

Regel ab jetzt:
- unterschiedliche Paketbytes = unterschiedliche Pluginversion;
- kein erneutes Ausgeben eines geänderten Pakets unter derselben Version;
- nur das nach Fresh + Upgrade + Positiv/Negativ + Hashprüfung erzeugte Paket darf übergeben werden.

0.2.6 bleibt Entwicklungs-/Testhistorie. Übergabekandidat ist erstmals eindeutig `0.2.7`.

## Kandidatenbindung

Branch:
`hobbyroom/glossar-027-release-hardtest-20260913`

Getesteter Commit:
`7191f15358cc73a78231652e9479f3a9fb5a9c37`

Autoritativer Run:
`34749231699`

Plugin:
`Universal Glossary Engine 0.2.7`

Rewrite-Schema:
`5`

Innerer Plugin-ZIP SHA-256:
`e9c32fc64db3c64c3b85e0d2692ff200e8f6d60e5827d7ab514657adff2ae831`

Actions-Artefakt-ID:
`10315142446`

Äußerer Actions-Artefakt-Hash:
`975cc771cc109b62b56abafddc9e05334a4fd6f8b26535655c3fee4d3e8ed174`

## Fresh-Install

Job `103702569466` → PASS.

Positiv/negativ geprüft:
- WordPress + MySQL + Astra Boot;
- Version 0.2.7;
- Rewrite-Schema 5;
- Policy-/Seed-Matrix;
- alle Glossar-Kartenlinks;
- echte Einzelbegriffsseite mit Artikelmarkup/Inhalt, nicht nur HTTP 200;
- A–Z;
- Draft nicht öffentlich;
- unbekannter Begriff 404;
- Preview;
- Duplikatsperre;
- AJAX gültig/ungültiger Nonce;
- Kategorie-/Begriffskollision;
- normale WordPress-Beiträge unverändert;
- Hero-Abstand;
- responsive Hero-Darstellung;
- Breadcrumb-Achse.

## Echter Updateweg 0.2.5 → 0.2.7

Job `103702569602` → PASS.

Negativer Vorzustand:
- aktives 0.2.5;
- Einzelbegriff-Rewrite-Regel gezielt entfernt;
- bekannter Begriff danach 404;
- gespeichertes Schema bleibt 4.

Update:
- WordPress-eigener Plugin-Updater überschreibt 0.2.5 mit 0.2.7;
- installierte Dateien zeigen Version 0.2.7 und Rewrite-Schema 5;
- DB steht unmittelbar nach Dateiaustausch noch auf Schema 4;
- ein sofortiger Apache-Request darf wegen OPcache noch alten Bytecode sehen und wird deshalb sichtbar protokolliert, nicht als PASS versteckt;
- nach der normalen OPcache-Timestamp-Revalidierung muss der neue Code aktiv sein;
- danach wird Schema 4 → 5 zwingend nachgewiesen;
- Einzelbegriff-Rewrite-Regel ist wieder vorhanden;
- bekannter Begriff liefert 200 + echtes Glossar-Artikelmarkup + erwarteten Inhalt.

Danach erneut PASS:
- alle Kartenlinks;
- unbekannter Begriff 404;
- Draft 404;
- Legacy 301;
- Kategorie/gleichnamiger Begriff getrennt;
- ungültiger AJAX-Nonce negativ;
- normaler WordPress-Beitrag unverändert;
- Daten/Konfiguration erhalten;
- Deaktivieren/Reaktivieren ohne Routingverlust;
- komplette alte Frontend-/Regression-/Acceptance-Matrix erneut PASS.

## Gated Package

Job `103702749853` → PASS.

Der Paketjob lief erst nach Fresh-Install PASS und Upgrade PASS.

Erzeugtes inneres Plugin-ZIP:
`universal-glossary-engine-0.2.7.zip`

SHA-256:
`e9c32fc64db3c64c3b85e0d2692ff200e8f6d60e5827d7ab514657adff2ae831`

## Lokale Kontrolle des exakt erzeugten Artefakts

Das Actions-Artefakt wurde nach dem Run erneut heruntergeladen und lokal geprüft.

PASS:
- äußerer Artifact-Hash exakt `975cc771cc109b62b56abafddc9e05334a4fd6f8b26535655c3fee4d3e8ed174`;
- innerer Plugin-ZIP-Hash exakt `e9c32fc64db3c64c3b85e0d2692ff200e8f6d60e5827d7ab514657adff2ae831`;
- `SHA256.txt` stimmt mit dem lokal berechneten inneren ZIP-Hash überein;
- ZIP-Struktur fehlerfrei;
- Pluginheader `Version: 0.2.7`;
- `UGE_VERSION = 0.2.7`;
- Rewrite-Schema 5;
- negativ: `Version: 0.2.6` nicht im ausgelieferten Pluginheader vorhanden.

## Ergebnis

`0.2.7 TECHNISCHER KANDIDAT PASS`.

Nicht daraus ableiten:
- kein Pferde-Atelier-LIVE-PASS;
- keine reale Sichtabnahme der vier gemeldeten Frontendpunkte.

Nächster Schritt ist ausschließlich der reale Pferde-Atelier-Readback dieses exakt hashgebundenen 0.2.7-ZIPs.
