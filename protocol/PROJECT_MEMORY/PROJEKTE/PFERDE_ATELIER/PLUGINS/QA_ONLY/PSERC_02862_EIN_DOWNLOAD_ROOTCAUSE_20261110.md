# PSERC 0.28.62 – Reparatur der unnötigen zweiten Exportfunktion, 10.11.2026

**QA ONLY – nicht auf Live installieren.** Archiviertes Plugin im Projektbüro: `/pferdeatelier/PLUGINS/QA/PSERC-0.28.62-KISS-EINE-UEBERGABE-NUR-WORDPRESS-TEST.zip`. Testprotokoll: `/pferdeatelier/PLUGINS/QA/PSERC_0.28.62_QUALITAETSPRUEFUNG_20261110.md`. ZIP SHA256 `3b4ae411d85cbeeeaab6945ddc702cb302f2d2c148c5c82eefb9256dbb410c25`.

## Sicher festgestellte Ursache
0.28.61 ergänzte neben dem weiterhin gültigen kompakten Fünf-Felder-Export einen zweiten Admin-Button für das K0-Quellenmanifest. Dieser zusätzliche Download prüfte **für jeden** bereitstehenden Artikel die vorher nicht für den Export erforderlichen Kriterien `intent_profile.status=PASS`, `ok`, `search_intent`, `profile_sha256` und die Artikelart. Fehlt eines, wirft der Code `PSERC_K0_OWNER_INTENT_PROOF_NOT_PASS`. **Der Nutzer erhielt genau diesen Code.** Welche der Teilbedingungen im tatsächlichen WordPress-Datensatz nicht zutrifft, ist ohne den echten Plan-Snapshot **noch nicht bewiesen**. Das war die überstrenge zusätzliche Exportprüfung und die überflüssige zweite Benutzeraktion.

## Behoben, ohne eine neue Redaktion oder ein zusätzliches System
- 0.28.62: **ein** sichtbarer Download **„Produktionsübergabe herunterladen“**. Alte POST-Aktion bleibt nur für bereits offene Browser-Tabs erreichbar.
- Eine einzige vorhandene Manifestdatei enthält weiterhin den **exakt unveränderten** Fünf-Felder-Batch und die original gespeicherten PSTE-Intentprofile. Wenn die Profile vollständig belegbar sind, wird sie mit `mit-suchintent-nachweis` benannt. Bei fehlendem/fehlerhaftem Herkunftsnachweis bleibt das originale Manifest **als Diagnose** mit `ohne-suchintent-nachweis` downloadbar. Diese Dateien dürfen **nicht** als SEO-Freigabe behandelt werden; der getrennte K0-Provenienzwächter verweigert sie. Falls das Manifest selbst nicht verifiziert materialisiert werden kann, greift **nur** der bisherige geprüfte Fünf-Felder-Export als ausdrücklich unbewiesener Altfall.
- Sichtbar: Anzahl freigegebener Artikel, Artikelliste, ein Button. Statistik/Gründe und technische Hash-/Vertragsdaten bleiben eingeklappt. Importbereich ebenfalls eingeklappt. Keine zusätzliche Anzeige und keine automatische Neuberechnung.
- **Gezielte UI-only-Snapshot-Kompatibilität 0.28.61→0.28.62**: nur bei exakt vorangegangenem bekannten .61-Plugin/Package-Hash, **unveränderten** Kategorie-/SEO-/Inventar-/Struktur-/Produktionsdaten und bestandener vollständiger Paket-Selbstintegrität. Sonst weiterhin bisheriger Frische-Block. Normale neue Compiler-Versionen erhalten keinen generellen Bypass.
- PSTE, DataForSEO, PSERC-Kompilierung/Fachentscheide, 5-Felder-Vertrag und WordPress-/K0-Textproduktion **nicht verändert**.

## Eigene Tests, nicht als echten WordPress-Live-Lauf ausgeben
- Der vom Nutzer gemeldete Fehler wurde mit einer zuvor bereiten 3-Artikel-Projektion ohne `intent_profile` **an 0.28.61 wörtlich reproduziert**.
- 0.28.62: 3 simulierte READY-Artikel mit freigegebenen Profilen: voller Manifestdownload **PASS**, ursprünglicher Fünf-Felder-Batch **unverändert**, getesteter isolierter K0-Quellwächter **PASS**.
- Simulierte READY-Artikel mit fehlendem, ungültigem, manipuliertem oder teilweise vorhandenem Profil: **Diagnose-Datei wird ausgegeben**, K0-Quellwächter **lehnt die unbewiesene Entscheidung weiter ab**. Kein stilles Downgrade zu freigegebenem SEO-Profil.
- Reale Codefunktion WordPress-Admin-Oberfläche mit WP-Funktionsmocks gerendert: **exakt ein** Downloadformular, bisherige zwei Beschriftungen weg, weitere Informationen eingeklappt.
- UI-only-Upgrade: **1 positive und 7 negative** Daten-/Vertrags-/Hash-Proben PASS, zusätzlich echte Paketselbstprüfung PASS.
- PHP-Syntax **43/43 PASS**, Paketselbstintegrität **61/61 PASS**, ZIP-CRC PASS. Vergleich Original .61→.62: **nur 4 von 63 Dateien geändert**: Admin, streng begrenzte Snapshot-Kompatibilität, Versionskopf, Paketvertrag; **59 Dateien byteidentisch**. SHA256 verifiziert.
- **Echter WordPress-Testserver und tatsächlicher aktueller Plan-Snapshot wurden NICHT ausgelesen oder verändert.** Keine Produktion, kein WordPress-Schreiben, keine DataForSEO-Abfrage. Deshalb kein Freigabeversprechen für K0 beim echten Export ohne dessen Quellenbeleg.

## Nächste Benutzeraktion (nur TEST)
QA-Plugin installieren → SEO-Redaktionsplan öffnen → EINMAL `Produktionsübergabe herunterladen` → JSON hier hochladen. Bei `ohne-suchintent-nachweis` kann die Originalprofil-Lücke dann **an echten WP-Daten** präzise analysiert werden, statt blind einen Neuaufbau zu erzwingen.

**STATUS: QA_PACKAGE_VERIFIED; OLD_ERROR_REPRODUCED; ONE_DOWNLOAD_VERIFIED; WP_REAL_SNAPSHOT_NOT_TESTED; ACTIVE_K0_UNCHANGED.**
