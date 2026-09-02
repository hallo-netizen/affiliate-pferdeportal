# AFFILIATE-ZENTRALE — VERBINDLICHES FEHLERREGISTER

Stand: 2026-09-02
Workstream: `AFFILIATE_ZENTRALE`
Branch: `affiliate-release-current`
Status: `MANDATORY_PRESTEP_GATE`

## Harte Ausführungsregel

Vor jedem Analyse-, Code-, GitHub-, Test-, Build-, Installations-, Live- oder Release-Schritt:

1. aktuellen Scope bestimmen,
2. passende Fehler-IDs dieses Registers prüfen,
3. Positiv-/Negativ-/Gesamtworkflowtests daraus binden,
4. bekannte Fehlwege nicht wiederholen,
5. keinen PASS ohne geforderte Evidence behaupten.

Bekannter Fehlweg im geplanten Schritt => `FAIL_CLOSED`, Plan zuerst korrigieren.

Jeder neue Fehler wird **vor dem Fix** hier eingetragen mit Symptom, Root Cause, gescheitertem Weg, Nicht-Wiederholungsregel, Positiv-/Negativ-/Regressionstest und Status. Nach dem Fix folgt der Register-Postcheck. Kein Fix ohne Registereintrag; keine Abnahme ohne Registerabgleich.

---

## AFF-ERR-001 — Vorzeitige Abnahme / PASS ohne vollständigen Nachweis

**Symptom/Root Cause:** Teiltest oder lokale Evidence wurde als Gesamtworkflow-/Release-PASS dargestellt.

**Nicht wiederholen:** `PASS`, `fertig`, `Release` oder `Abnahme` nur mit allen explizit gebundenen lokalen Positiv-/Negativ-/Gesamtworkflowtests und erforderlichen Live-Gates.

**Tests:** lokaler Gesamtworkflow + Gegenfälle + Regression; Live nur mit echter Live-Evidence.

**Status:** CLOSED / permanenter Hardlock.

## AFF-ERR-002 — Last-Known-Good vor Schlussprüfung verdrängt

**Symptom/Root Cause:** neuer DS24-Kandidat konnte publiziertes LKG vor vollständiger Revalidation/Persistenz überschreiben oder deaktivieren.

**Nicht wiederholen:** Draft vollständig materialisieren und revalidieren; LKG erst nach persistiertem neuen `published` ersetzen. Fehler => LKG unverändert.

**POSITIV:** valider Kandidat publiziert und ersetzt danach LKG.
**NEGATIV:** invalid/stale/Persistenzfehler lässt LKG live.
**Regression:** eBay/idealo/Awin unverändert.

**Status:** LIVE_PASS im 6.68.0-Livepfad; Regel dauerhaft bindend.

## AFF-ERR-003 — Aktion lief, Backend zeigte altes/kein Ergebnis

**Symptom/Root Cause:** ausgeführter DS24-Lauf war im Backend nicht eindeutig als neuer persistierter Endzustand ablesbar.

**Nicht wiederholen:** jeder Lauf zeigt auf derselben Fachseite Laufzeit, Zahlen und Schlussprüfung; kein Erfolg ohne Readback.

**POSITIV:** neuer Zeitstempel + Run-Zahlen + Schlussprüfung sichtbar.
**NEGATIV:** fehlender/staler Readback verhindert PASS.

**Status:** LIVE_PASS im 6.68.0-Livepfad; Regel dauerhaft bindend.

## AFF-ERR-004 — Unrealistische Testdaten erzeugen falschen lokalen PASS

**Symptom/Root Cause:** idealisierte Fixtures enthielten bereits die gewünschte Fachklassifikation statt echter Rohdaten, z. B. `Pferdetraining` statt realem `MKA Horsemanship Academy`.

**Nicht wiederholen:** problematische Live-Rohdaten realitätsnah reproduzieren; erwartetes Ergebnis nie in die Eingabe hineinschreiben.

**POSITIV:** echter Rohname führt zum richtigen Ergebnis.
**NEGATIV:** generische/mehrdeutige Namen erzeugen keinen erfundenen engen Treffer.
**Regression:** kompletter realer Portalbaum.

**Status:** CLOSED / permanenter Hardlock.

## AFF-ERR-005 — Zielklassifizierer bevorzugt generische Wörter/tiefe Unterpfade

**Symptom/Root Cause:** allgemeine Signale wie `Pferd`/`Training` und Pfadtiefe verzerrten die Zielwahl; 3 DS24-Ausgaben geplant, aber 0 Entwürfe/Review.

**Nicht wiederholen:** spezifische Fachsignale vor generischen Portalwörtern; Tiefe allein kein Qualitätsmerkmal; vollständige reale Zielmenge; fachlich breiter Pferde-Fallback nur bei tatsächlich breiter Pferderelevanz.

**POSITIV:** spezifischer echter Match gewinnt.
**NEGATIV:** tiefer Pfad gewinnt nicht allein wegen Tiefe/generischem Wort.
**Gesamtworkflow:** Seiten + Kategorien + Beiträge.

**Status:** LIVE_PASS 6.68.0; Regel dauerhaft bindend.

## AFF-ERR-006 — Mini-Fix-/Versionskaskade statt Root-Cause-Fix

**Symptom/Root Cause:** viele Pluginstände behandelten jeweils nur das nächste sichtbare Symptom.

**Nicht wiederholen:** ein Fehler => Root Cause => gebündelter Fix => kompletter Positiv-/Negativ-/Gesamtworkflowtest. Keine neue Version für kosmetische/nachgelagerte Einzelerscheinungen derselben offenen Ursache.

**Pflicht:** vor Pluginbuild belegen, warum Codeänderung notwendig ist und welche gemeinsame Ursache sie schließt.

**Status:** OPEN als permanente Prozesssperre.

## AFF-ERR-007 — Unvollständige Backend-Pfade

**Symptom:** Nutzer musste nachfragen, wo eine Aktion im WordPress-Backend liegt.

**Nicht wiederholen:** jede Nutzerhandlung mit vollständigem Pfad ab `WordPress-Dashboard`.

**Status:** CLOSED / permanente Kommunikationsregel.

## AFF-ERR-008 — DS24-Einzelpflege als Dauerlösung

**Symptom/Root Cause:** jede DS24-Quelle müsste einzeln mit Produkt-ID/Promolink/Werbemittelseite gepflegt werden.

**Nicht wiederholen:** Ziel bleibt eine automatische Bulk-Synchronisation der real genehmigten Partnerschaften. Einzelpflege ist höchstens Notfall-Fallback. Ein CSV-/Dateiimport darf nicht als Runtime-Autorität an die Stelle der automatischen Partnerschafts-Discovery treten.

**POSITIV:** mehrere bestätigte Partner werden automatisch in einem Lauf aus einer unterstützten read-only Affiliate-seitigen Quelle gewonnen.
**NEGATIV:** nicht genehmigte/fremde/ungültige Datensätze werden nicht freigegeben; Testoracle-Dateien erzeugen keine Runtime-Autorität.

**Status:** OPEN — automatische Bulk-Discovery weiterhin ungelöst; frühere manuelle Runtime-Lösung durch AFF-ERR-015 ausdrücklich verworfen.

## AFF-ERR-009 — Bannerformat oder Position hart im Providercode verdrahtet

**Risiko:** neue Formate/Designpositionen würden Providerumbau erzwingen.

**Nicht wiederholen:** Quelle, Format und Slot sind getrennte Verträge. Banner speichert echte Maße/Ratio; zentrale Slotdefinition liefert Fähigkeiten; Provider kennt keine feste Position/Pflichtgröße; Runtime-Matching Banner↔Slot; responsive ohne Verzerrung; unpassendes Format bleibt verfügbar und kann später neu bewertet werden.

**POSITIV:** neue Slotgröße nur über Slotdefinition, ohne Providercode.
**NEGATIV:** kein erzwungenes Verzerren/Abschneiden.
**Regression:** bestehende Slots/Banner unverändert.

**Status:** OPEN / permanenter Architektur-Hardlock.

## AFF-ERR-010 — Organisch wachsendes Portal nur einmalig zugeordnet

**Risiko:** neue/geänderte Kategorien, Seiten, Beiträge oder Banner würden nicht neu bewertet.

**Nicht wiederholen:** Zuordnung re-entrant; neue/geänderte Ziele/Banner lösen Recheck aus; zusätzlich zentraler periodischer Recheck; keine Provider-Cron-Inseln.

**POSITIV:** neuer passender Beitrag erhält Bannerchance.
**NEGATIV:** fremder Themenbereich erhält keine automatische Pferdeportal-Zuordnung.

**Status:** OPEN / permanenter Workflow-Hardlock.

## AFF-ERR-011 — Partner-&-Einnahmen-Übersicht blendet aktive Produktquellen aus

**Symptom/Root Cause:** sichtbare KISS-Seite nutzte nur `banner_networks()`, obwohl zentrale Analytics eBay/idealo und weitere Produktquellen bereits providerübergreifend kannte.

**Nicht wiederholen:** `Partner & Einnahmen` muss direkt die zentrale providerübergreifende Analytics verwenden. Keine zweite Statistik-Wahrheit und keine künstliche Banner-/Produktquellentrennung in der Einnahmenansicht.

**POSITIV:** sichtbarer Pfad `WordPress-Dashboard → Affiliate-Zentrale → Partner & Einnahmen` delegiert direkt an `PPAR_Partner_Analytics_Admin::render_page()` und enthält mindestens eBay, idealo, Awin, ADCELL, Digistore24, Direktpartner sowie lokale Klicks.
**NEGATIV:** fehlende Providerdaten bleiben `nicht verfügbar`, niemals geschätzt.
**Regression:** Provideradapter, Ausspielung, Tracking unverändert.

**Evidence:** `release/affiliate-zentrale/evidence/current_scope_manual_import_partner_visibility_20260902.txt` — ausschließlich der darin enthaltene Analytics-/KISS-Nachweis bleibt verwendbar; der manuelle Runtime-Importteil ist durch AFF-ERR-015 verworfen.

**Status:** FIXED_LOCAL / WordPress-Liveprüfung noch offen.

## AFF-ERR-012 — DS24 Affiliate-Partnerschaftsinventur mit falscher API-Autorität

**Symptom:** reale Menge 18 genehmigte Partnerschaften; 6.70 live 0/0, 6.71 live 1/1 mit alter lokaler Quelle 53213.

**Root Cause:** `listMarketplaceEntries` ist keine eigene Affiliate-Partnerschaftsinventur; `getAffiliateCommission(all)` wurde fälschlich als fremde Vendor-Inventur interpretiert; `validateAffiliate` kann nur bereits bekannte Produkt-IDs verifizieren.

**Gescheiterte Wege:** Marketplace als Vollinventur; synthetisches `getAffiliateCommission(all)`-Fixture; 53213 als Remote-Discovery-Erfolg; CSV-/Dateiimport als Ersatz für die automatische Discovery.

**Nicht wiederholen:** `listMarketplaceEntries`, `getAffiliateCommission(all)` und `validateAffiliate` nicht ohne neuen realen Gegenbeweis als autoritative automatische Discovery verwenden. CSV/Kontrollliste bleibt ausschließlich Testoracle und darf niemals Runtime-Autorität oder Runtime-Partnerschaftsbestand erzeugen.

**POSITIV automatische Discovery:** unterstützter read-only Affiliate-seitiger Kanal liefert ohne CSV/ID-Vorfütterung alle 18.
**NEGATIV:** 17/18 als Auto-Discovery, 53213-only, Marketplace-only, transaktions-only, falsche Identität, malformed/duplicate, synthetische Antwort oder testoracle-basierter Runtimebestand => fail closed.
**Gesamtworkflow:** gültiger automatischer Eingang → Metadaten → Creative/Banner → Bild/Tracking → Targets/Slots → Draft → Revalidation → Persistenz → LKG → Readback → Reassignment; Partnerfehler isolieren; eBay/idealo/Awin regressionsprüfen.

**Evidence:** `protocol/AFFILIATE_RELEASE_DS24_DISCOVERY_CAPABILITY_AUDIT_20260902.md`; `release/affiliate-zentrale/evidence/csv_oracle_only_and_ds24_public_api_exhaustion_20260902.txt`; reale 18er-Kontrollliste ausschließlich als Oracle.

**Zusätzlicher 02.09.-Nachweis:** Die aktuelle offizielle Digistore24-OpenAPI-Referenz führt im Affiliate-Bereich `getAffiliateCommission`, `getCustomerToAffiliateBuyerDetails`, `getReferringAffiliate`, `getAffiliateForEmail`, `setAffiliateForEmail`, `setReferringAffiliate`, `updateAffiliateCommission`, `validateAffiliate`; kein `listAffiliations`/Partnerschaftsinventar. `validateAffiliate` verlangt Produkt-IDs. `listProducts` listet Produkte des eigenen Digistore24-Kontos. `listMarketplaceEntries` listet Marketplace-Einträge. `on_affiliation` ist ein Vendor-seitiges Neupartnerschaftsereignis, kein Affiliate-Bestandsbackfill.

**Status:** OPEN — dokumentierte öffentliche API vollständig geprüft; kein unterstützter Affiliate-seitiger Bestandsendpoint gefunden. Nächste reale Evidence ist ausschließlich der authentifizierte Request hinter der 18er-Backoffice-Tabelle bzw. ihrem Export, danach Klassifikation supported API vs. private Session-Transport.

## AFF-ERR-013 — Manueller Bestandsimport akzeptierte unvollständige oder widersprüchliche Autorität

**Symptom:** doppelte Produkt-ID konnte still überschrieben werden; GZIP >32 MiB konnte abgeschnitten als scheinbar vollständig behandelt werden.

**Root Cause:** Last-Write-Wins bei Produkt-ID und Sample-Reader als Vollreader ohne Overflow-Nachweis.

**Nicht wiederholen:** Falls künftig ausdrücklich ein nicht-autoritativer Diagnose-/Testimport genutzt wird, muss er fail-closed bleiben. Er darf jedoch unabhängig von seiner technischen Härte niemals Runtime-Autorität für DS24-Partnerschaften erhalten.

**Evidence:** `release/affiliate-zentrale/evidence/manual_import_authority_hardening_20260902.txt` — technische Tests historisch vorhanden, aber keine Runtime-Autorisierung.

**Status:** SUPERSEDED_BY_AFF-ERR-015 — kein Runtime-Betriebsweg.

## AFF-ERR-014 — KISS-Navigation wiederholt bereits live gescheiterten `remove_submenu_page()`-Weg

**Datum / Arbeitsschritt:** 02.09.2026 / Gesamtregression vor Livekandidat.

**Symptom:** KISS-Source hatte für funktionale Legacy-/Providerseiten wieder `remove_submenu_page()` verwendet. Der dokumentierte 6.64.0-Livefehler war genau: KISS entfernte alte Unterseiten und verlinkte danach weiter auf diese Slugs; WordPress zeigte `Du bist leider nicht berechtigt, auf diese Seite zuzugreifen.` Der 6.64.1-Rootfix verlangte: funktionale Seiten registriert lassen, nur optisch ausblenden, kein `remove_submenu_page()` im KISS-Teil.

**Root Cause:** ein bereits live widerlegter Navigationsweg wurde beim späteren KISS-Source erneut eingeführt und bei den Importtests zunächst nicht gegen die historische Regression geprüft.

**Gescheiterter Weg:** funktionale Zielseiten mit `remove_submenu_page()` aus der Menüstruktur entfernen und sie anschließend weiterhin über KISS-Buttons direkt ansteuern.

**Betroffene Bereiche:** ausschließlich KISS-Navigation/Backend-Erreichbarkeit. Providerlogik, Analytics, DS24, eBay, idealo, Awin, Output/LKG bleiben unverändert.

**Nicht wiederholen:** Legacy-/Providerseiten vollständig registriert und erreichbar lassen. Optische Reduktion ausschließlich über Darstellung/CSS; niemals funktionale Registrierung/Berechtigungsroute entfernen.

**POSITIV:** fünf KISS-Einstiege werden registriert; alle KISS-Button-Zielslugs bleiben durch ihre ursprünglichen Registrierungen erreichbar.
**NEGATIV:** kein `remove_submenu_page()` im KISS-Code; keine Page-Hook-Lücke.
**Regression:** direkte Partner-Analytics bleibt; Provider-/Outputbytes unverändert.

**Evidence:** historisches Liveprotokoll `AFFILIATE_ZENTRALE_GESAMTPROTOKOLL_ZIELVERTRAG_FEHLER_STATUS_2026-09-01.md`, Abschnitte 6.64.0/6.64.1; aktueller lokaler Gegenbeweis `release/affiliate-zentrale/evidence/current_scope_manual_import_partner_visibility_20260902.txt`.

**Status:** FIXED_LOCAL / WordPress-Liveprüfung der Navigation noch offen.

## AFF-ERR-015 — Testoracle wurde fälschlich zum manuellen Runtime-Betriebsweg gemacht

**Datum / Arbeitsschritt:** 02.09.2026 / Wiederabgleich mit verbindlicher Übergabe und Zielvertrag.

**Symptom:** Nach dem Discovery-Fail wurde ein universeller Ein-Feld-Importer samt DS24-Bestandsimport und Preserve-Guard in den kanonischen Source aufgenommen und im Fehlerregister zeitweise als zulässiger manueller Betriebsweg bezeichnet.

**Belegte Root Cause:** Die reale DS24-CSV/Kontrollliste wurde semantisch von ihrer einzigen erlaubten Rolle als Testoracle in eine Runtime-Autorität umgedeutet. Damit wurde der eigentliche Auftrag — automatische Partnerschafts-Discovery — umgangen statt gelöst.

**Gescheiterter Weg:** `export.csv` oder vergleichbare DS24-Partnerschaftsdatei zum Aufbau/Persistieren des Runtime-Partnerschaftsbestands verwenden; universellen Upload als Ersatz für die fehlende Remote-Discovery anbieten.

**Betroffene Bereiche:** `class-ppar-universal-import.php`, `class-ppar-manual-import-guard.php`, deren KISS-Einbindung sowie alle Protokoll-/Evidence-Aussagen, die den manuellen DS24-Dateiimport als Runtime-Betriebsweg autorisieren. Analytics-/KISS-Navigation selbst ist davon unabhängig.

**Nicht wiederholen:** DS24-Kontrollliste/CSV ausschließlich lesen, vergleichen und testen. Sie darf weder Partnerbestand noch Marketplace-Cache noch Creative-/Output-Pipeline autorisieren oder persistieren. Keine Ersatzarchitektur für eine fehlende automatische Discovery.

**POSITIV:** Source besitzt keinen DS24-Dateiweg, der Runtime-Partnerschaftsautorität aus der Kontrollliste erzeugt; automatische Discovery bleibt fail-closed offen, bis ein realer unterstützter Kanal belegt ist.
**NEGATIV:** Hochladen/Einlesen einer Kontroll-CSV kann keinen DS24-Runtimebestand erzeugen; fehlende automatische Discovery bleibt sichtbar FAIL und wird nicht durch Dateiimport kaschiert.
**Regression:** KISS-Navigation, Partner-&-Einnahmen, eBay, idealo, Awin, bestehende DS24-Validation-/Banner-/Output-/LKG-Kette bleiben unverändert.

**Evidence:** `release/affiliate-zentrale/evidence/csv_oracle_only_and_ds24_public_api_exhaustion_20260902.txt`. Git-Vergleich gegen den Stand vor Rootfix ändert nur Governance/Protokoll/Manifest/KISS und entfernt genau die beiden Runtime-Dateiimportklassen; keine Provider-/Output-/Analytics-Implementation geändert. Beide Dateiimportklassen sind im aktuellen Source 404/nicht vorhanden; KISS enthält keinen Uploadweg und behält nicht-destruktive Navigation sowie direkte Analytics-Delegation.

**Status:** FIXED_LOCAL — kein Runtime-Dateiimport mehr im kanonischen Source; CSV wieder ausschließlich Testoracle.

## AFF-ERR-016 — Kanonischer Repository-Source ist nicht der belegte Live-6.71-Source

**Datum / Arbeitsschritt:** 02.09.2026 / Livekandidaten-Vorprüfung.

**Symptom:** Der belegte aktuelle WordPress-Livekandidat ist `6.71.0` mit SHA-256 `f6e74cc06be8f5c450f4f7647aef8f419257e483d0be473bb2879cd81c5e71a9`. Das aktuelle Repository-Governanceobjekt führt dagegen weiterhin Kandidat `6.64.0`, während der kanonische Haupt-PHP-Header sogar noch `6.63.8` trägt. Die tatsächliche 6.71-ZIP ist weder im kanonischen GitHub-Source noch aktuell als zugreifbare Uploaddatei verfügbar.

**Root Cause:** Live-Weiterentwicklung 6.65–6.71 wurde nicht bytegenau zurück in die einzige Release-Autorität `release/affiliate-zentrale/current/affiliate-portal-router` gebunden. Dadurch kann der Repository-Source derzeit nicht als sichere Basis für ein Plugin dienen, das die live installierte 6.71 ersetzt.

**Gescheiterter Weg:** aus dem älteren kanonischen 6.64/6.63.8-Source einen neuen Installer bauen oder ihn als Fortsetzung von 6.71 behandeln. Das wäre ein nicht belegter Rückbau/Rekonstruktionspfad und verstößt gegen `no_reconstruction`.

**Nicht wiederholen:** Kein Pluginbuild, keine Versionsanhebung, kein Installationskandidat und kein Live-Replace, bevor die exakte 6.71-Quellbasis bytegenau verfügbar und in die Governance als direkte Source-Autorität gebunden ist. Keine Rekonstruktion aus Protokollen, Diffs oder älteren ZIPs.

**POSITIV:** exakte 6.71-ZIP/Source mit erwartetem SHA-256 wird direkt eingelesen; daraus gewonnener Source wird byteidentisch gebunden, bevor irgendein neuer Code darauf aufsetzt.
**NEGATIV:** fehlende/falsche ZIP, anderer SHA, rekonstruiertes 6.71 oder älterer Source => Build/Live-Replace fail closed.
**Regression:** Nach Source-Bind erst vollständiger Positiv-/Negativ-/Gesamtworkflowtest; kein Provider-/LKG-/KISS-/Analytics-Rückbau.

**Status:** OPEN / HARD BLOCK für jeden neuen Installer oder Live-Replace.

---

# Aktueller PRECHECK

`AFF-ERR-015` ist lokal geschlossen. Der aktuelle fachliche Root-Blocker ist wieder ausschließlich `AFF-ERR-012` automatische DS24-Partnerschafts-Discovery.

Öffentliche dokumentierte API-Wege sind erschöpft und als nicht ausreichend belegt. Nächster zulässiger Discovery-Schritt ist nur reale Read-only-Evidence des Requests hinter `Verkäufe & Partner → Partnerschaften mit Vendoren` bzw. dessen Export; keine Zugangsdaten/Cookies/Tokens übernehmen und keinen privaten Session-Endpunkt als supported Runtime-API ausgeben.

Parallel bleibt `AFF-ERR-016` HARD BLOCK für jeden Installer/Live-Replace, bis die exakte Live-6.71-Quellbasis vorliegt. Die 18er-CSV bleibt ausschließlich Testoracle. Keine Release-/Live-Abnahme aus lokalen Einzeltests.