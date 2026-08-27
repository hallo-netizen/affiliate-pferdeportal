# Fehlerkatalog – V6.56 BUSINESS Safe-Gap Churn Revalidation Rootfix – 27.08.2026

## E1 – Live-Gesamtlauf stoppt nach 662 Paketen mit `business_safe_gap_new_missing_family`
Live belegt am realen Pferde-Atelier-System: Run `50dec1a2-799`, Phase `coverage_verify`, 7/311 BUSINESS-Familien gedeckt, 304 fehlend, Fehler `business_safe_gap_new_missing_family`, sicherer Frontend-Checkpoint unverändert aktiv.

## E2 – Ursache
Der V6.50-Sicherheitsvertrag erlaubte exakt einen kanonischen Gap-Fill-Snapshot. Wird während eines mehrstündigen/-tägigen realen eBay-Laufs eine zuvor gedeckte Familie neu fehlend, liegt sie außerhalb dieses alten Ziel-Snapshots. Der unveränderte Hard-Guard klassifiziert das als `business_safe_gap_new_missing_family` und beendet den Gesamtlauf. Das ist bei einem dynamischen Marktplatz kein hinreichender Beweis für einen Systemfehler.

## E3 – Rootfix
Der Hard-Guard selbst bleibt unverändert. Vor seiner Anwendung erkennt `coverage_verify` und `public_verify` neu fehlende Familien. Der kanonische Beweisumfang wird monoton erweitert; Discovery läuft nur für die neu hinzugekommenen Familien, danach wird die bestehende BUSINESS-Auswahl über den vollständigen Beweisumfang erneut ausgeführt. Erst danach darf der unveränderte Safe-Gap-/Public-Vertrag entscheiden.

## E4 – Sicherheitsgrenzen
`business_gapfill_public_invariant_failed`, unbekannte Familien, inkonsistente Coverage, Storage-/Checkpoint-/Runtime-/CAS-Fehler bleiben hart fail-closed. Es gibt keine direkte Freigabe, keine künstliche Public-Ausgabe und kein Überspringen des kanonischen Selectors.

## E5 – Endlosschleifenschutz
Der Beweisumfang ist monoton und auf das autoritative 311-Familien-Manifest begrenzt. Eine Familie kann pro Run nur einmal neu in den Beweisumfang aufgenommen werden. Discovery arbeitet ausschließlich auf dem Delta; die Auswahl bleibt bounded.
