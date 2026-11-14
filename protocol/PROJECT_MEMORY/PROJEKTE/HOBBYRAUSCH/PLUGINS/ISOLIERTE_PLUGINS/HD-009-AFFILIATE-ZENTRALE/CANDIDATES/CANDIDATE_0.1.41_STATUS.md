HD009 0.1.41 – **nur interner Gesamtstand, nicht zur Installation freigegeben**.

- Die einzige Themen-Entscheidung fällt beim vorhandenen Idealo-Import; direkte und belegte verwandte Ausrüstung werden gemeinsam erkannt.
- Die einzige Zielentscheidung benutzt die schon gespeicherten Zielschlüssel. Keine nachgelagerte Produktbewertung, keine neuen Tabellen oder Frontend-Abfragen.
- Gleicher Feed-Hash, neue Zuordnungsregel, Feedwechsel, 304 und automatischer Refresh im ursprünglichen Worker geprüft.
- DB-INSERT/UPDATE-Fehler werden am Speichervorgang erkannt; fehlgeschlagener SELECT stoppt die Kampagnenverarbeitung statt gültige Karten zu löschen.
- **End-to-End-Gesamtsimulation bestanden:** Original-PHP-Matcher mit echtem HD007-Register → synthetische CSV → Original-Import → Speicher → Kampagnen; passende Airbrushpistole und themenverwandter Kompressor als echte Testkarten, falsche Damenkleidung verworfen.
- Vollständiger Testlauf: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43612968772
- 41 Dateien im ZIP, 24 PHP-Dateien geprüft. Vollständiges Archiv im bisherigen Kandidatenordner: `HOBBY_DEPOT_HD009_0.1.41_KISS_NUR_INTERN.zip`.
- SHA256 `86cfca33840cdc6ab2bbb0037f6264a91582dfd4ea4802da16ed3140188811c1`.
- **Noch nicht bewiesen:** tatsächliche private Idealo-Feedabdeckung 2747/2901 und authentifizierter WordPress-Liveablauf. Daher keine Betreiberfreigabe, kein Downloadlink.
- Offizielles `CURRENT.zip` bleibt 0.1.37; WordPress und HD003-CURRENT unverändert. Fehler- und Entscheidungsverlauf ausschließlich im bisherigen Affiliate-Fehlerregister Stand 12.
