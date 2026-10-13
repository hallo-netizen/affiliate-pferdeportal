# Hab & Bewahr – R3 Struktur-/Redaktions-Abnahme (lokale Vorschlagsprüfung)
Stand: 2026-10-13. **NICHT als WordPress- oder SEO-Freigabe verstehen.**

## Autoritative Ausgangsdaten
- WordPress-R2-Readback: `APKW_FINAL_TARGET_DRY_RUN_V1`, Plugin 1.14.8.17; `sync_state.status=COMPLETE` auf Revision `HB-SECURITY-CATEGORY-OWNER-CORRECTIONS-20261012-R2+655852190d183cc9`; Runner readback_checked=354, frontend_readback.valid=true und 0 Fehler. Dies ist die **bestehende R2-Livebasis**, nicht R3.
- R2-Quelldatei (Beleg, keine zweite Current-Autorität): SHA256 `bd1594d7012ae36f787cf9ca2039e657d922e2954f3e097cc3f2b40482d42055`.
- R3 wurde nicht importiert. Keine WordPress-Schreibvorgänge, keine neuen DataForSEO-Provideraufrufe.

## Positiver Struktur-Test (voller Portalbaum)
- Schutzbereiche: 6 Gefahrenwelten, 31 bestehende Bereiche, 93 Unterbereiche (45 R2 +48 Vorschläge), 285 Blattkategorien (141 R2 +144 Vorschläge).
- 31/31 CORE-Bereiche: 3–10 unmittelbare Unterbereiche.
- 93/93 CORE-Unterbereiche: 3–10 unmittelbare Blattkategorien.
- CORE-Einstieg: 6 direkte Gefahrenwelten. Keine bestehenden IDs, Slugs, WordPress-Zuordnungen oder 704 redaktionellen Quelltitel verändert.
- MAGAZIN (EDITORIAL): 13 bestehende Zwischenknoten; direkte Kindzahl 3–10; **PASS ohne Änderung**.
- DIENSTLEISTER (DIRECTORY): 10 bestehende Zwischenknoten; direkte Kindzahl 3–9; **PASS ohne Änderung**.

## Redaktioneller Vorschlagstest
- 144 neue Kategoriekandidaten, je 3 ausgearbeitete redaktionelle Artikelvorschläge = 432 neue Titel.
- Nach 9 Textkorrekturen: 432/432 exakt verschiedene neue Titel, 0 exakte Titelduplikate gegen 704 originale R2-Themen.
- 17 lexikalisch ähnliche neue Titel einer konkreten fachlichen Erstprüfung zugeführt, 6 davon ausdrücklich SERP-Intent-Review offen. Ein Lexiktest ist **keine semantische Freigabe**.
- 21/21 alte R2-Owner-Reviews mit vorläufigem fachlichen Scope versehen; 17 konkrete alte Titel zur **Umhängung, nicht Kopie** vorgeschlagen; 1 Keyword-Duplikat nur als Alias vorgesehen.
- Nach allen 17 theoretischen Umhängungen haben alle beteiligten bisherigen Quellkategorien noch mindestens 3 vorhandene Titel. Original-704 bleiben im R2-Datenbestand unverändert.

## Negativ-Tests (alle erwartungsgemäß REJECT)
1. Ein-Kind-Bereich
2. Zwei-Kind-Bereich
3. Unterbereich mit zwei Blattkategorien
4. Doppelter neuer Artikeltext
5. Neue Kategorie ohne eindeutigen SEO-Owner / fehlender Keyword-Owner
6. Ursprüngliche Kategorie mit nur noch zwei Artikeln nach Verschiebung
7. Als WordPress-Profil ausgegebener nicht freigegebener R3-Entwurf
8. Nicht existierender Eltern-Unterbereich

## Echte verbleibende Schranke
**Kein grüner SEO- oder Live-Status:** Weder Titel-Eindeutigkeit noch Seitenstruktur beweisen, dass alle 144 neuen Kategorien eigenständige organische Suchintents besitzen. Keyword-Nachfrage und organische SERP-/Owner-Überschneidung sind noch nicht vollständig nachgewiesen. Historische 282er DataForSEO-Auswertung meldete 128 Treffer und 154 fehlende Keywords (nicht als 0 zu interpretieren); die 20 SERP-Felder waren nur punktuell und 4 davon nicht vollständig gemessen. Keine automatischen zusätzlichen bezahlten Anfragen.

**Vorgabe:** R3 nicht installieren/importieren, keine IDs/Slugs umhängen und keine neuen indexierten leeren Seiten anlegen, bevor dieser inhaltliche Nachweis geführt und die Gesamtstruktur erneut bestätigt wurde.
