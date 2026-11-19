# Texterstellung – 0.4.5-Arbeitsstand, keine Plugin-Auslieferung

**Status: Gesamtzielvertrag NICHT BESTANDEN, NICHT INSTALLIEREN.** Stand 14.11.2026.

## Tatsächlicher Befund am ausgelieferten 0.4.4-Code
Der tägliche Cron rief die Originalkategorieentscheidung erneut für alle offenen historischen FREI auf. Das verletzt die klare Trennung: **einmaliges Fachurteil** gegen **spätere technische Kategorieüberwachung**. Alte 61 echte Aufträge sind laut WordPress-Diagnose noch nicht bereit (61 METADATEN_OFFEN). Kein neuer Echtlauf liegt vor.

## Kleinstmögliche technische WIP-Korrektur
1. Eindeutige Kategorieentscheidung **höchstens einmal pro historischem Auftrag**; Beleg `category_owner_visited` wird im bestehenden Auftrag `texterstellung_orders_v1` gespeichert, keine zusätzliche Tabelle oder Prüfqueue. Nur echte technische Ausführungsfehler bleiben wiederanlaufbar.
2. Täglicher Lauf ruft ausschließlich `loadLegacyApprovals(false)` auf. Er liest gespeicherte Original-PSTE-Quellen und übernimmt neue **bereits bestätigte** Felder, trifft aber keinerlei neue Fach-, Titel- oder Artikelartentscheidung.
3. Der tägliche Leser zählt gemeinsam mit dem bestehenden Originalquellenzugriff lediglich **bereits gespeicherte** fehlende Kategorie-Vorschläge (`PSTE_CATEGORY_GAP_ANALYSIS_V2`), ohne einen zweiten WordPress-Kategorielauf. Fehlt das genaue Originalangebot, bleibt es `unresolved`, ohne Ratezuordnung.
4. K0 fünf Felder, Titelprozess, Import sowie die bestehende Entwurfssperre unverändert. Keine automatischen WordPress-Kategorien angelegt oder Original-FREI überschrieben.

## Harte Prüfergebnisse
- 117/117 PHP-Syntax, ZIP Integrität und bytegleicher Neuaufbau PASS.
- **89/89 lokale Prüfaussagen**: 11 „einmaliger Owner“ mit realen 61 Auftragskennungen und nachgebildeter WP-Datenbank; 7 „separate technische Kategorienüberwachung“ mit **synthetischen** Gap-Quellzeilen; 27 originaler 20er-Workflow mit nachgebildeten WordPress-Funktionen; 12/12 bisherige Kategorienbindung; 5/5 Zeitplan; 10/10 ursprüngliche Owner-Automatik-Mockfälle; **17/17 echte 61 Diagnose-Auftragswerte ohne künstliche Metadaten**, bei denen **0** den K0-Export erreichen. Das beweist korrekte Sicherheitsgrenzen, **keine** echte erfolgreiche Produktion.
- Exakter Datei- und Zeilenvergleich gegen 0.4.4: **170/173 Dateien unverändert**, geändert nur Hauptdatei, Originalquellenleser und README; **0 weitere Original-PSTE/PSERC-Dateien** geändert. **Wichtig:** 0.4.4 hatte bereits gegenüber 0.4.3 eine ursprüngliche PSTE-Admin-Datei angepasst; deshalb keine unbelegte Behauptung „vollständig originale Automatik übernommen“.

## Verbleibende harte Zielvertragslücken
- Die aktuelle reale PSTE-Tabelle mit den 61 vollständigen Payloads liegt nicht vor; die früheren 52 offenen Kategorie-Büro-Fälle lassen sich nicht ohne weitere nachgewiesene Originalstruktur verbindlich zuordnen.
- Die getrennte Überwachung meldet Kategoriebedarf, aber **erstellt fehlende Kategorien nicht automatisch und bindet neue Kategorien noch nicht vollständig an wartende Aufträge**. Hieraus folgt ausdrücklich **KEIN fertiger Kategorie-KISS-Gesamtworkflow**.
- Automatische originale Google-Fragen/PAA-/DataForSEO-Funktionsgleichheit, echte externe K0-Texterstellung mit 81 Regeln sowie echter WordPress-Entwurf inklusive Wiederanlauf nicht im selben realen System abgenommen.
- Die Aussage „89/89 bestanden“ ist **keine Release-Freigabe**, sondern nur lokaler Test der begrenzten technischen Änderung. Nach Regeln 14, 21 und 23 ist **keine Installation** erlaubt.

## Ergebnis
Die wiederholte Kategorieentscheidung ist technisch entfernt und geprüft. Der vollständige Zielvertrag bleibt **OFFEN**; keine neue installierbare ZIP, keine Änderung an Live-WordPress, kein neues Plugin. Der vorherige freigegebene Teststand wird nicht überschrieben.
