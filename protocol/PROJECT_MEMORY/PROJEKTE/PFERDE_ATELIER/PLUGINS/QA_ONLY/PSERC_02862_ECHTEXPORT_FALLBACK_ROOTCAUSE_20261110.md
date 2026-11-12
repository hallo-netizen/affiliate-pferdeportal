# PSERC 0.28.62 – echter Nutzer-Export: Fallback statt Quellenmanifest (10.11.2026)

**Nur Diagnose/QA. Keine Veränderung an WordPress, aktiver K0-Produktion, PSTE/PSERC oder gespeicherten Artikeln.**

## Echtes Nutzer-Artefakt
- Name: `seo-redaktionsplan-ohne-suchintent-nachweis-42619ca7b6e36a625e0c8ae4e562534a9ff1b115ac7772f598435a064d06f546.json`
- Größe: 1.393 Byte; unveränderter Datei-SHA256: `d943ebe3ab65ca53de04b54aca02321c1b2052b3e30e40ab6ff4d5a4cc9b22c9`.
- Inhalt exakt der früher bereits originalgeprüfte 3-Artikel-Fünf-Felder-Handoff. Kern-SHA256 selbst nachgerechnet = `42619ca7b6e36a625e0c8ae4e562534a9ff1b115ac7772f598435a064d06f546`.
- In der Datei kein `intent_profile`, `search_intent`, `profile_sha256` und kein `next_textmachine_metadata_batch`/Quellenmanifest.
- Gegen **physisch gelesene PSERC-0.28.62-Test-ZIP**, SHA256 `3b4ae411d85cbeeeaab6945ddc702cb302f2d2c148c5c82eefb9256dbb410c25`, mit Original PHP8.4-Klassen `PSERC_Stable_Json` und `PSERC_Metadata_Boundary` ausgeführt: `PSERC_METADATA_BOUNDARY_PASS` und `requireReadyBatchForExport = PASS`.

## Kausal geprüfter Exportpfad in 0.28.62
`PSERC_Admin::exportSingleHandoff()` legt **zuerst** den geprüften nackten Fünf-Felder-Batch als `$output` ab und setzt Standardnamen `ohne-suchintent-nachweis`.
Anschließend versucht die Methode `PSERC_Plan_Snapshot_Store::manifestForSelectedBatch($header,$batch)`.
Nur wenn `existingManifestEnvelopeIsValid($manifest,$batch)` **true** ist, wird `$output = $manifest`; ein zwar vorhandener, aber mangelhafter Intent führt dann zu einem **ausführlichen** Manifest mit Dateiname `ohne-suchintent-nachweis`.
Beim aktuellen echten Export ist `$output` **noch der nackte Batch**. Damit ist **bewiesen**: Die Erzeugung oder vollständige Validierung des Manifests kam NICHT erfolgreich durch; ein bloß fehlender Intent in einem anderweitig gültigen Manifest erklärt die nackte Dateiform nicht allein.
Der `catch(Throwable $proofReadFailure)` ist leer. Ein Fehlercode wird nicht erfasst/ausgegeben; daher **ist die konkrete Teilursache** (fehlender READY-Detailindex, Bindungsfehler, Detailstatus, Manifest-Abgleich oder eine andere Ausnahme) aus diesem Artefakt nicht bestimmbar.

## Abgrenzung
- Es ist NICHT nachgewiesen, ob das originale PSTE-Suchintentprofil in WP fehlt oder erhalten ist.
- Fünf-Felder-Vertrag und bisherige 3 Artikel sind **intakt**, aber kein vollständiger SEO-Herkunftsnachweis. K0-SEO-Herkunftswächter darf diesen nackten Batch nicht als PASS freigeben.
- Die WordPress-TEST-Installation wurde hier **nicht** direkt ausgelesen. Kein Neuaufbau von Recherche/Plan auslösen.

## Einziger zielgerichteter Anschluss
Zuerst **lesend und ohne Migration** für alle drei originalen `plan_slot`-Werte die bestehenden PSERC-READY-Indexzeilen und `final_item`-Daten sowie `intent_profile` überprüfen. Exakt prüfen, an welcher `manifestForSelectedBatch`-/Envelope-Bedingung der Übergang scheitert. Den vorhandenen Fehler im bisherigen `exportSingleHandoff` als geschützten, ausschließlich internen Diagnosehinweis sichtbar machen (statt still zu verschlucken) — kein zweiter Download, keine neue Fachentscheidung, keine Änderung an K0 oder 5-Felder-Batch.
Erst nach Originalprofil-Rücklesung über denselben Planplatz den existierenden Manifestweg herstellen, vollständigen Export verifizieren und auf getrenntem K0-QA-Zweig testen. **Keine Live- oder K0-Produktionsfreigabe.**
