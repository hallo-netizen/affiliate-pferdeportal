# Hab & Bewahr: Offline-Simulation mit vorhandenen 118 Keywords (20.11.2026)

**Verbindlich:** Die breite DataForSEO-Suche bleibt unverändert. Nachgelagerte fachliche Prüfung ist zu eng. Kein Rückbau, keine zweite Sachentscheidung, keine neue bezahlte Anbieterabfrage.

## Datenbasis (ausschließlich bestehende drei Diagnose-Dateien)
- Abholbox: 9 Sandbox-RAW-Keywords, 0 brauchbare: Pizza, Phone, SEO -> 9/9 sachfremd
- Abluftanlagen & Unterdruck: 9 Sandbox-RAW-Keywords, 0 brauchbare -> 9/9 sachfremd
- Alarm & Kamera ohne Netz: Häufige Fragen: 100 echte gespeicherte RAW-Keywords (99 Aliasgruppen), 98 persistierte Kandidaten, original 0 PASS. Original-Filter: 99/99 NO_MATCH wegen fehlender Pflichtwörter und fehlendem Subject Head; originale Normalpfad-Entscheidung: 98/98 BLOCKED/SANDBOX_REQUIRED.

## Unveränderter Originalcode als Ursachenbeleg
- `class-pste-runner.php`: FAMILY_REVIEW und NO_MATCH bleiben in Rohdaten erhalten, aber `PSTE_Normal_Metadata_Path::applyToPayload` entscheidet am Ende über den Kandidaten.
- `class-pste-portal-relevance-gate.php::evaluateBeforeAssignment`: Portalrelevanz wird zunächst aus strengem Familienabgleich hergeleitet; falls keine Familie passt, verlangt die Stelle weitere Nachweise. Keine positive Portalfreigabe trotz möglicher relevanter anderer Sicherheitsrubriken.
- `class-pste-family-identity-v2.php`: `SUBJECT_HEAD_MISSING` und `REQUIRED_DISCRIMINATOR_MISSING` machen 99 Aliasgruppen zum NO_MATCH der engen Ursprungsfamilie. Genau diesen Zwang nicht mit der Portalrelevanz gleichsetzen. Auch eine lockere Beurteilung darf keine sachfremden Suchwörter automatisch akzeptieren.

## Simulationsauswertung
Kamera: **5 themennahe Fragen**, **29 mögliche Sicherheitskategorie (anderer Zweig)**, **17 Kontext unklar**, **49 sachfremd** = 100 RAW-Begriffe.
Alt-Sandbox-Läufe: **18 sachfremd von 18**.
Es wurden alle 118 gespeicherten RAW-Begriffe **einmalig manuell fachlich** einer Klasse zugeordnet und maschinell ausgezählt. Die Zahl 34 (5+29) ist eine mögliche **Weiterverwendung als Themenkandidat**, kein Produktions-PASS, kein verifizierter WordPress-Zielzweig und kein fertiger Artikel. Technische Zusicherungen zu WLAN/Internet/Cloud/SIM sind aus dem Suchwort allein nicht ableitbar.
- Beispiel themennahe Frage: `ip kamera ohne cloud`, `tapo-kamera auf nas speichern`, `gsm kamera mit sim karte`.
- Andere Sicherheitsrubrik: `kamera mit bewegungsmelder`, `ip kamera outdoor`, `kamera für türspion`.
- Sachfremd: `obs virtuelle kamera`, `gta 5 kamera fixieren`, `nistkasten kamera`.

## KISS-Ziel für gebündelte spätere Reparatur
**Breite Recherche -> genau eine fachliche Entscheidung aus vorhandenem Normalpfad**: passende Ursprungskategorie; andere existierende Sicherheitskategorie; nur bei unklarer Relevanz Review; sachfremd aussortieren. Ein fehlender Wortbestandteil aus C23 (etwa »Häufige Fragen«) ist **kein** Beweis gegen Portalrelevanz. Die eigentliche fertige Artikelzulassung bleibt aber an den Original-K0-/Titel-/Kategorievertrag gebunden.

## Grenzen
Nur Offline-Simulation auf gespeicherten Rohkeywords; keine Änderung am WP-Plugin, keine Datenbankmutation, kein bezahlter DataForSEO-Aufruf. Die Kategorieeignung wurde nicht durch echte WordPress-Kategoriensnapshots überprüft, keine automatische 34/34 Freigabe behauptet.

CSV-/JSON-Ergebnisdatei im Hab-Büro unter `/hab-und-bewahr/TEXTERSTELLUNG/SIMULATION_BREITE_SUCHBEGRIFFE_20261120/` (separat zu archivieren).
