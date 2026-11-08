# Pferdeatelier – tatsächlicher Stand nach Anwender-Export 08.11.2026 15:03:46 UTC

**Verbindlicher Übergabestatus: TESTSYSTEM, noch kein externer SEO-Entscheid, kein SEO-Rückimport, kein K0-Auftrag.** Weder die ältere 5.016er Gesamtdiagnose noch der alte 87-Titel-Reentry-Lauf sind die externe FREI/BELEGT/KLÄRUNG-Entscheidung.

## 1. Reale Dateien, zeitlich richtig eingeordnet

- **PSTE 0.57.144.22 und PSERC 0.28.55** sind laut Betreiber in WordPress-Testsystem installiert; Admin-Screenshots zeigen entsprechende Versionskennungen, PSERC-Snapshot wurde im Test-WordPress einmal aktualisiert. ZIP-Binärkopien jetzt unter `/pferdeatelier/PLUGINS/` (private Bibliothek), Bytegrößen/SHA in [Paar-Manifest](../INSTALLATIONS_PAKETE/TESTPAAR_20261108_ARCHIV/MANIFEST.md).
- **Gesamtdiagnose** von 2026-11-08: `EVIDENCE/pste-gesamtdiagnose-2026-11-08.json`, 5.016 Themen. Diese Datei ersetzt NICHT den Inhalts-/Planexport. Keine Neuanforderung.
- **Erster echter Nutzerexport** 14:45 UTC aus Test-WP: in privater Library `/pferdeatelier/pferdeatelier-mini-ergebnisse-20261108-144510(1).json`, 969627 Byte, SHA256 `ef1b6bd844de2dc839dfcf99be5c2249dc76e9f4e877f93da82fb997f89c1ba9`, `parkhaus_complete=false`, PSERC-Snapshot zu diesem Zeitpunkt unvollständig/veraltet.
- **Zweiter echter Nutzerexport nach erfolgreicher Snapshot-Aktualisierung** 15:03:46 UTC: privat in Library `/pferdeatelier/pferdeatelier-mini-ergebnisse-20261108-150347(1).json`, 1043468 Byte, SHA256 `f31e68a5de77be965e384e4b7517ec7a48a7cd1ca8ae6631b9fb5637dd93a2ba`. Diese zweite Datei ist der **maßgebliche aktuelle echte Export**. Nicht öffentlich nach GitHub kopieren, weil private Entwürfe/Planungsdaten.

## 2. Was wirklich geprüft wurde – und was NICHT

Direkt aus vollständiger lokaler JSON-Originaldatei und ZIP-Dateien, nicht aus Vermutungen:

- JSON erfolgreich vollständig gelesen; `contract=PSTE_MINI_RESULTS_FOR_EDITORIAL_V1`, `count=100`, 87 JA, 9 VIELLEICHT, 4 NEIN, 87 echte `seo_subjects`.
- `parkhaus_snapshot.complete=true`, `parkhaus_complete=true`, 64-stellige Prüfsumme, `status=PARKHAUS_FOR_SINGLE_EXTERNAL_SEO_OWNER_NOT_APPROVED`: Der Snapshot hat seine **technische Vollständigkeitsmarkierung**, aber der externe Fachentscheid ist **noch nicht erfolgt**.
- 1.179 Snapshot-Einträge aus **WORDPRESS 1.024**, **PSTE_PLAN 1**, **EDITORIAL_PLAN 9**, **PSERC_ACTIVE_PLAN 1**, **PPM679_EXISTING_EDITORIAL_RUNTIME 144**, **MINI_RESERVED 0**; Quelle PSERC `complete=true`, PPM679 `complete=true` und `PRESENT`.
- **Inhaltlicher Mangel 1:** 9/9 `EDITORIAL_PLAN`-Titel sind der literale String `Array`; gleichzeitig `EDITORIAL_PLAN.status=NOT_AVAILABLE`. Das boolesche `complete=true` bedeutet daher **nicht** nachgewiesene semantisch nutzbare Vollständigkeit.
- **Inhaltlicher Mangel 2:** 144/144 `PPM679_EXISTING_EDITORIAL_RUNTIME`-Einträge haben leeren Titel, Zielkeyword und Kategorie im exportierten Datensatz; 141/144 referenzieren `post_id` eines tatsächlich im selben WordPress-Snapshot enthaltenen Eintrags mit lesbarem Titel. 3/144 Post-Verweise konnten in diesem Snapshot nicht aufgelöst werden. Bereits vorhandene Planplätze werden in der Fachprüfung sonst möglicherweise falsch als unbelegt bewertet.
- Die Test-ZIPs wurden lokal erneut anhand der wirklichen Header, Größe, SHA256 und ZIP-CRC bestätigt. Das zusammengefasste Test-Paket enthält beide unverändert. Kein **aktueller** Codefix an PSTE/PSERC aus diesem Arbeitsschritt, keine neue installierbare Version, keine aktuelle PHP-End-to-End-WP-DB-Probe.
- Anwenderscreenshot: PSERC `METADATEN-VORSCHAU PASS` für gespeicherten Snapshot, aber `0 Position(en)` für Artikelübergabe. **Dieser PASS betrifft nur PSERC-Metadaten-Snapshot**, NICHT den SEO-Owner, NICHT die inhaltliche Vollständigkeit des externen Parkhauses und NICHT den gesamten End-to-End-Ablauf.

## 3. Verbindlicher Ablauf (ein einziger semantischer Entscheider)

**Normalweg:** WP stellt aktuellen vollständigen Bestand/Artikelplätze einmal als Snapshot bereit → EIN externer SEO-Owner entscheidet je Original-Suchabsicht **FREI/BELEGT/KLÄRUNG**, inklusive Paketdubletten und konkreten Bestandsbelegen → bestehender WP-Rückimport prüft **nur technische Herkunft, Frische und atomare Belegung** (keine zweite fachliche Dublettenentscheidung) → bestehender Redaktions-/PSERC-Weg gibt technisch komplette fünf Metadaten an **K0 unverändert** weiter. NICHT automatisch neue Artikel aus 87 JA generieren. Kein zusätzlicher Owner, Datenbank oder Worker.

## 4. Benutzeroberfläche: festgehaltene Nutzerentscheidung, NICHT implementiert

Der Betreiber lehnt das alte umfangreiche PSERC-Vorschau-/Produktion-/Diagnose-Menü als regulären Normalweg ab. **Gewünschte Vereinfachung:** `Export` → `extern entscheiden` → `Ergebnis importieren` → `Status`; bestehende Spezialprüfungen allenfalls als Experten-/Diagnosefunktionen behalten, aber nicht als zweite SEO-Fachentscheidung. **Bisher weder UI-Code geändert noch ein UI-Test bestanden.** Nicht als bereits umgesetzt darstellen.

## 5. Konkreter offener Auftrag – in der richtigen Reihenfolge

1. PSTE-Export normalisiert die 9 `EDITORIAL_PLAN`-Objekte mit echten Titeln/IDs oder markiert diese Quelle eindeutig `KLÄRUNG`; `Array` ist nicht erlaubt. Keine Fakten erfinden.
2. PSTE-Export ergänzt die 144 PPM679-Plätze mit der **bereits vorhandenen** WP-Titelreferenz (141 sicher verknüpfte, 3 fehlende explizit klären); nur einmalige Quelllesung, **kein Keyword-Gesamtdurchlauf**. Prüfsumme/Vollständigkeitsvertrag muss unbrauchbare Titel erkennen.
3. Zwei Original-TEST-ZIPs getrennt/zusammen **im isolierten QA-Zweig** nach wirklicher Korrektur auf positive/negative Vollständigkeit und Rückweg testen; K0 und Originalplugins unverändert, ohne Freigabe des jetzigen ZIP-Paars.
4. Danach genau EINE echte externe FREI/BELEGT/KLÄRUNG-Bewertung am nachweisbar brauchbaren aktuellen Snapshot. **Vorher kein SEO-Ergebnis erfinden, kein Rückimport, kein Artikelauftrag.**
5. Den WordPress-Normalweg optisch und funktionell auf die vier notwendigen Handlungen reduzieren, erst nach eindeutiger Bestands-/Abhängigkeitsprüfung. Altes Menü nicht blind entfernen.

**Was der Betreiber jetzt tun muss: NICHTS.** Die bereits zweimal gelieferten Dateien reichen zum Festhalten der nachgewiesenen Fehler. Weitere Downloads/Screenshots/Durchläufe nicht erneut verlangen.

**GitHub-Status:** ausschließlich isolierter Draft-PR #682 / Branch `fix/pste-kisten-einmalige-pruefung-20261107`, kein Merge, kein Live, kein K0. ZIP-Pakete liegen in der privaten Bibliothek und sind im GitHub-Manifest inventarisiert, nicht in den Git-Baum hochgeladen.
