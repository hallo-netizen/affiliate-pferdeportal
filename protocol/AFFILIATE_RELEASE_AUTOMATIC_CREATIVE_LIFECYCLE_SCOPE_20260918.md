# AFFILIATE-ZENTRALE — Vollautomatischer Creative-Lifecycle + KISS-Bedienung

Stand: 2026-09-18
Status: `BOUND_ROOTFIX / NO_RELEASE_PASS`

## Ziel

Ausgehend ausschließlich von der kanonischen Source `release/affiliate-zentrale/current/affiliate-portal-router/` den Affiliate-Betrieb auf einen vollautomatischen, providerneutralen Normalbetrieb mit jederzeit möglichem manuellem Eingriff an entscheidenden Stellen überführen. Kein neuer Pluginbuild, bevor der gebundene Technikblock als ein Kandidat vollständig lokal geprüft ist und ein konkreter WordPress-Livetest erforderlich wird.

Fachquellen außerhalb des Repositories:
- `/Pferde-Atelier/Aktenschraenke/Affiliate/WERBEPLATZ_REGISTER.md`
- `/Pferde-Atelier/Aktenschraenke/Affiliate/KONZEPT_AUTOMATIK_LIFECYCLE_20260918.md`

## Verbindlicher KISS-Vertrag

1. Normalbetrieb vollautomatisch: neue valide Partner/Creatives nach Provider-Sync ohne Pflichtklick in gemeinsamen Bestand und Neubewertung.
2. Manuelle Eingriffe bleiben stärker als die Automatik: `Aus Automatik entfernen`, Sperren/Veto, bewusst fixieren/bevorzugen, `Zur Automatik zurück`.
3. Keine technischen Zwischenzustände als normaler Bedienweg.
4. Keine Provider-Sonderlogik im Matching-/Werbeplatzkern.

## Creative-Deduplizierung

1. Nur eindeutig identische Creative-Varianten automatisch zusammenfassen.
2. Gleiches Grundbild mit anderem Text, CTA, Rabatt oder Angebot bleibt eine eigene Variante.
3. Pro identischer Variante und Formatfamilie bleibt nur die größte Originalversion produktiv.
4. Quadrat/Quer/Sidebar usw. bleiben getrennte Formatfamilien.
5. Bei Unsicherheit getrennt behalten; keine riskante KI-Zwangsentscheidung.
6. Kleinere eindeutige Duplikate nur als schlanke Alias-/Auditreferenz, nicht als vollwertige aktive Creatives.

## Lifecycle / Hintergrundprüfung

1. zentraler Bestands-/Partner-/Creative-Sync im Plugin: Startintervall alle 2 Wochen;
2. tiefer Integritätslauf: Startintervall alle 3 Wochen;
3. manueller `Jetzt prüfen`-Weg bleibt;
4. späterer externer Cron darf denselben zentralen Job triggern, ohne zweite Fachlogik;
5. neue Partner/Creatives aufnehmen, geänderte aktualisieren, nicht mehr verfügbare deaktivieren;
6. nach relevantem Bestandswechsel nur betroffene Ziele/Slots neu bewerten;
7. fällt ein Creative weg, nächstbesten gültigen Treffer automatisch nachrücken lassen.

## Aktions-/Rabattbanner

- Providerstatus und belegte Start-/Enddaten sind Autorität.
- Nicht mehr gelieferte/deaktivierte/abgelaufene Creatives werden aus der aktiven Eignungsmenge entfernt.
- Fehlen belastbare Laufzeitdaten, muss der Provider das Creative beim regulären Sync erneut bestätigen.
- Keine Ablaufdatums-Erfindung aus Bildtext/OCR.

## Technische Eignung

- reale Maße/Ratio + zentrale Slotregeln entscheiden; Provider-Formatlabels sind nicht maßgeblich;
- proportional, kein Crop, keine Verzerrung;
- Downscale ohne pauschale Prozent-Untergrenze, sofern Erkennbarkeitsgate PASS;
- Upscale maximal +10 %;
- Backendfilter, Matcher und Frontend verwenden dieselbe Regelquelle.

## Partner & Einnahmen

- Backend-Statistik ausschließlich aus verifizierten Originaldaten des jeweiligen Partners/Providers über dessen Report-/API-Weg;
- keine eigene Klick-, Bestell-, Umsatz- oder Provisionserhebung in dieser Statistik anzeigen, addieren, ergänzen oder als Ersatzwert verwenden;
- lokale Klickzähler gehören nicht in die Backend-Statistik;
- fehlende Provider-Reportdaten nicht als `0 €` oder `0` ausgeben, sondern `nicht verfügbar`;
- Währungen nicht als Euro-Gesamtsumme vermischen;
- keine Rang-/Bestpartner-Aussage bei unvollständiger oder nicht vergleichbarer Datenbasis.

## UI/Disclosure

- zentraler Kurzsatz: `Werbelink: Bei Kauf erhalten wir ggf. eine Provision.`;
- kleine, zentrierte Darstellung;
- sichtbare Blocküberschrift `Anzeige` bleibt;
- Glossar-/Rassen-Werbeblock optisch einheitlich;
- Produktkachelgruppen müssen die reale verfügbare Inhaltsbreite füllen.

## Lokale Testlinie als Oracle — NICHT kanonisch

Nichtkanonische lokale Pakete 6.72.60–6.72.65 dürfen ausschließlich als Test-/Diagnoseoracle dienen.

- 6.72.60: Glossar-Design/Position/Zentrierung — Nutzer-LIVE-PASS.
- 6.72.61/62: Rassen-/Disclosure-/Kachelgeometrie — nicht vollständig abgenommen.
- Vor 6.72.63: Produktkachelbreite im Nutzer-Screenshot FAIL; Rassenseite fast PASS.
- 6.72.63: lokaler Struktur-/Fresh-Unpack-Nachweis vorhanden; LIVE-Retest offen.
- 6.72.64/65: Hintergrund-Lifecycle/Status bzw. Partner-Analytics-Wahrheitsfix; kein kanonischer Gesamtgate und kein LIVE-PASS.

Diese Pakete ersetzen weder die kanonische 6.72.19-Source noch `PPA-001/CURRENT.zip`.

## Zwingender Precheck vor Codeänderung

1. ERROR-REGISTER PRECHECK.
2. Kanonische 6.72.19-Source gegen diesen Vertrag lesen.
3. Lokale 6.72.60–6.72.65 nur als Delta-/Fehleroracle auswerten.
4. Exakten minimalen kanonischen Delta-Scope bestimmen.
5. Keine Versionswahl, kein ZIP, kein Installer.
6. Vor späterem Build: Positiv, Negativ/fail-closed, betroffener Gesamtworkflow, historische Regressionen, Fresh-Unpack/Source-Identität, Mutation/Sabotage, Error-Register-Postcheck.
7. Erst danach genau ein Testkandidat; LIVE-PASS separat durch realen WordPress-Readback.

## Nicht anfassen

- keine eBay-PRIVATE-/Checkpoint-Massenmutation;
- keine OTTO-Cleanup-Neuarchitektur;
- kein Designplugin für Affiliate-Fachlogik;
- keine zweite Provider-/Pixel-/Werbeplatz-Wahrheit;
- keine neue Pluginversion für Zwischenarbeit;
- keine Backendpfade raten.


## Awin-Bannerquelle – verbindliche Beschaffungsregel 19.09.2026

Diese Ergänzung präzisiert den bestehenden Vollautomatik-/KISS-Zielvertrag; sie ändert nicht dessen Grundziel.

- Awin-Programme und Partner dürfen automatisch synchronisiert werden.
- Der normale Bannerbestand muss ohne Pflichtarbeit `Code kopieren` pro einzelnes Creative in den vorhandenen Creative-Lifecycle gelangen.
- Zuerst vorhandenen bewiesenen Cleos-Bulkweg wiederverwenden, falls dessen reale Quelle belastbar nachgewiesen werden kann.
- Alternativ nur eine dokumentierte oder vertraglich belastbare maschinenlesbare Awin-Publisherquelle anbinden.
- Kein geratener/private UI-Endpoint, kein DevTools-Scraping als Produktionsvertrag, keine erfundene Creative-API.
- Nach der Beschaffung bleibt der vorhandene providerneutrale Ablauf zuständig: Import -> technische Prüfung -> fachliches Matching -> Ausspielung -> Revalidierung/Re-Evaluation.
- Frontend-, Journal-, Glossar-, Pferderassen-, Kategorie- und Design-PASS-Pfade sind dabei Nicht-Anfassen-Hardlocks.
