# Pferdeatelier eBay – verbindlicher Abschlussvertrag statt weiterer Einzelreparaturen
**11.11.2026 | Grundlage: realer QA12-Stand 6.72.323, Screenshots, CSV-Ablehnungen, QA2–QA12, QA12-Leistungsdiagnose.** Nur isolierter QA-Zweig, kein Live-/CURRENT-Eingriff.

## Was schon fertig ist und nicht wieder neu gebaut werden darf
Ein kanonischer eBay-Worker, gespeicherte Recherche und Kandidaten-Reuse, Mehrfachfamilien, Suchvarianten, begrenzte Nachsuche, 26 Nicht-Waren ausgeschlossen, ausschließlich eBay Deutschland/Business, getrennte Frühveröffentlichung und eigenständige Verfügbarkeitsprüfung, 6h-Frischegrenze, Stop/Fortsetzen mit Cursor, QA11 Einzelquellenfehlerisolation, QA12 kompaktes Backend und historische CSV/JSON-Protokollexporte. **Alle bisher nur simuliert/PHP-lokal erprobten Funktionen sind als noch nicht real abgenommen zu kennzeichnen, nicht als bereits betriebssicher.**

## Die drei offenen, tatsächlich belegten Abschlussprobleme
1. **Leistung:** QA12-Self-Drive dispatcht die nächste Runde sofort ohne Verzögerung; QA12-Audit liest und schreibt bei jedem gespeicherten Progress umfassende Options-Snapshots/100er-Chunks. Auf echter Seite sind Backend UND Frontend sehr langsam. Eine gemessene Kausalaufteilung fehlt.
2. **Öffentliche Produktausgabe:** Gespeicherte Freigaben (zuletzt 489) sind nicht gleich sichtbare, verfügbare eBay-Kacheln. 0/298 während eines neuen, noch nicht public-verifizierten Runs bedeutet „noch kein neuer Gesamtnachweis“, nicht Nullbestand. Richtige Seite und öffentliche Frischeprüfung müssen real nachgewiesen werden.
3. **Realtest:** Keiner der vielen lokalen PHP-/Mock-Tests ersetzt einen vollständigen echten WordPress-/MariaDB-/eBay-Lauf einschließlich sicherer Pause/Fortsetzung, Fehlerprotokoll und Seitenantwortzeiten.

## Nur diese Reihenfolge – kein weiterer Nebenumbau
**A. BESTAND SICHERN und LAST URSÄCHLICH EINGRENZEN.** Im laufenden Run nur vorhandenen Knopf „sicher anhalten“ nutzen, Cursor/Freigaben/Quelle/Runstatus bewahren. Backend- und Frontend-Antwortzeit mit angehaltenem vs. aktivem eBay-Hintergrundlauf real vergleichen; keine neue Recherche/Reset. Wenn Pause Last nicht erklärt, vor Pluginänderung Server-/WP-Profil prüfen.

**B. EIN zusammenhängender KISS-Performance-Fix.** Vorhandenen einzigen Self-Drive-Worker vernünftig takten (kein unmittelbares endloses Selbstaufrufen, kein zweiter Worker); bestehende 2h-Verfügbarkeitsprüfung in kleinen Paketen weiter unabhängig und ohne Konkurrenzlast; keine Vollsnapshots/Options-Chunk-Schreibvorgänge bei jedem bloßen Tick, sondern Phasen-/Fehler-/Publikationsereignisse sofort und Fortschritt sinnvoll gebündelt; lesende, schlanke Adminseite, keine teure Tabelle beim Aufruf. **Protokollierung darf nicht entfallen.** Keine zusätzlichen Tabellen, Menüs oder Suchcontroller. Bestehender Cursor darf nicht springen.

**C. Ausspielung mit vorhandenen Angeboten schließen.** Bereits geprüften Bestand nutzen; nur fachlich richtige, vom deutschen eBay-Marktplatz stammende, aktuelle, verfügbare Angebote auf korrekter Produktfamilie/Seite zeigen. Nachweislich nicht mehr verfügbare entfernen, bei bloßen temporären API-Fehlern keine Produktdaten löschen; 6h öffentlicher Datenfrische-Vertrag weiter einhalten. Offen gebliebene Familien **nach gespeicherten Gründen** (keine Treffer in begrenzter Suche / bewusster EBAY_DE-Filter / technischer Fehler / fachlich unpassend) deklarieren; nach begrenzter Nachsuche **keine Endlosschleifen**. Versicherungen/Beratung/Nicht-Waren bleiben ausgeschlossen; keine 298/298-Erfolgspflicht erfinden.

**D. EIN realer Gesamt-Abnahmelauf auf getrennter WordPress-Testinstanz mit gesicherter, repräsentativer Datenkopie**, nicht wieder zahlreiche einzelne ZIPs. Prüfbedingungen:
- Beim Anhalten und Fortsetzen **gleiche Run-ID und gleicher Cursor**, keine erneute 298er-Suche.
- Einzelnes fehlerhaftes eBay-Angebot blockiert nicht andere; Auth-/DB-Fehler bleiben harte Sperren.
- Protokoll CSV/JSON zeigt Runwechsel, Zeitpunkte, Fehlercodes/Post-IDs, Bestandserhalt; frühere Run-Logs bleiben abrufbar.
- Während laufendem Worker bleiben normale Backend- und Frontend-Seiten benutzbar; echte Zeiten vor/nach Performance-Fix festhalten. **Keine Behauptung ohne Messwert.**
- Je eine bekannte Kategorie- und Beitragsseite zeigt passende eBay-Kacheln mit funktionierenden eBay-Links; abgelaufenes/beendetes Angebot verschwindet entsprechend vorhandenen Regeln.
- Nach begrenztem Lauf nachvollziehbare Endbilanz: **abgedeckte Familien + bewusst offen gelassene Familien mit gespeicherten Gründen**. Keine künstliche 298/298-Pflicht.
- Alle alten recherchierten Angebote, Produkt-IDs, Zuordnungen, public Checkpoints und andere Provider bleiben erhalten.

**E. EINMALIGE Version/Releaseentscheidung:** Nur wenn Punkt D vollständig real bestanden ist, eine sauber versionierte produktive Fassung freigeben, mit GitHub-Diff, ehrlichem Testprotokoll und Download im Pluginbüro. Sonst **kein Erfolgssiegel und keine weiteren Schein-Release-ZIPs**: zuerst exakt den in D misslungenen realen Pfad korrigieren.

## Nicht mehr tun
Keine erneute Synonym-/Versicherungs-/Deutschland-Filter-Grundsatzdebatte, keine doppelten Suchcontroller oder Feedbackauswertungen, kein erneuter Start zur Diagnose, keine neue Tabelle, kein Wechsel/Backup-Löschen, kein automatisches Portieren in Hobbydepot oder Hab & Bewahr. Fortschreibung ausschließlich in bestehendem QA-PR #748 und im zentralen Transferregister PR #751. Dieses Dokument ist eine Priorisierung und kein bereits implementierter Leistungsfix.
