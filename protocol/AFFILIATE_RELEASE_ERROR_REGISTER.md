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

**PLUGIN-AUSGABE-HARDLOCK:** Kein neues Plugin-ZIP, keine neue Versionsnummer und kein Installationsaufruf an den Nutzer, bevor **derselbe gebundene Kandidat** vollständig geprüft ist:
1. Syntax/Lint aller betroffenen PHP-Dateien,
2. lokaler POSITIV-Test des konkreten Fixes,
3. lokaler NEGATIV-/Fail-closed-Test,
4. kompletter gebundener Gesamtworkflow im Hobbyraum,
5. relevante historische Regressionen gegen unveränderte Bereiche,
6. Source-Manifest/Byte-Scope gegen den letzten belegten Kandidaten,
7. ERROR-REGISTER POSTCHECK.
Scheitert ein Test, bleibt derselbe Kandidat im Hobbyraum. Erst reparieren und **denselben vollständigen Prüfblock erneut** fahren. Kein Zwischen-ZIP, kein Nutzer-Test und keine neue Versionskaskade.

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

**Status:** SUPERSEDED / die später direkt gebundene und real installierte 6.72.4-Source ist die aktuelle Basis; kein Rückbau auf 6.71 mehr zulässig.

## AFF-ERR-017 — Paketfortschritt wird im Backend nicht kumulativ sichtbar

**Datum / Arbeitsschritt:** 08.09.2026 / OTTO-Awin-14336-Produktffeed-Livefortsetzung.

**Symptom:** Nach jedem erfolgreich verarbeiteten 500er-Paket zeigt die Arbeitswarteschlange erneut exakt `500 Produkte verarbeitet; Fortsetzung vorgemerkt.`, obwohl der Job-Zeitpunkt fortschreitet.

**Root Cause:** Der Products-Worker erhöht `details.products` kumulativ und schreibt den Dateicursor fort, die persistierte Jobmeldung verwendet jedoch ausschließlich `result.processed` des aktuellen Pakets. Dadurch ist echter Fortschritt im Backend nicht eindeutig ablesbar.

**Gescheiterter Weg:** denselben Meldungstext wiederholt als Stillstandsbeweis interpretieren und den Nutzer denselben Pakettest erneut ausführen lassen.

**Nicht wiederholen:** Fortschritt muss auf derselben Fachseite kumulativ lesbar sein. Die Jobmeldung muss Gesamtzahl + letztes Paket ausgeben; Abschlussmeldung muss die Gesamtzahl nennen. Gleicher Pakettext allein ist niemals Stillstandsbeweis.

**POSITIV:** Nach zwei 500er-Paketen zeigt der Job mindestens 1000 als kumulativen Stand.
**NEGATIV:** Ein unveränderter kumulativer Stand bei unverändertem Cursor darf nicht als Fortschritt gelten.
**Regression:** Import-, Cursor-, Reconcile-, Provider- und Outputlogik bleiben unverändert.

**Status:** LIVE_PASS / 6.72.5 — Screenshot 08.09.2026 10:40 zeigt 3500 Produkte kumulativ, letztes Paket 500.

## AFF-ERR-018 — WP-Cron-Fallback hat keinen pluginseitigen Kick für fällige offene Jobs

**Datum / Arbeitsschritt:** 08.09.2026 / OTTO-Awin-14336-Automatik-Liveprüfung.

**Symptom:** `automatische Synchronisierung aktiv` + `WP-Cron-Fallback` ist gespeichert; der offene Awin-14336-Job bleibt im beobachteten Zeitraum >10 Minuten ohne selbständigen sichtbaren Paketfortschritt.

**Root Cause:** Der Pluginpfad registriert den 5-Minuten-Worker lediglich über `wp_schedule_event()` und verlässt sich anschließend vollständig auf WordPress' impliziten Cron-Spawn. Wenn dieser Host-/Runtime-Trigger nicht feuert, besitzt der Plugin-Fallback keinen eigenen eng begrenzten Kick für ein bereits fälliges Worker-Ereignis.

**Gescheiterter Weg:** erneut manuell auf `Nächstes Arbeitspaket verarbeiten` klicken, obwohl die manuelle Worker-Fortsetzung bereits belegt ist. Das prüft nicht den Transport.

**Nicht wiederholen:** WP-Cron-Transport separat behandeln. Für `wp_cron` darf bei offenem Job ein bereits fälliger Worker auf einem normalen Request einmal über den vorhandenen WordPress-Core-`spawn_cron()` angestoßen werden; niemals aus `DOING_CRON` rekursiv und ohne neuen Provider-/Endpoint-/Schedulerweg.

**POSITIV:** fälliges Worker-Ereignis + offener Job + normaler Request stößt den Core-Cron an; danach steigt der kumulative Jobfortschritt ohne manuellen Paketknopf.
**NEGATIV:** kein offener Job, noch nicht fälliges Ereignis oder `DOING_CRON` => kein zusätzlicher Kick.
**Regression:** Server-Cron/WP-CLI, täglicher Dispatch, Awin/ADCELL/eBay und Fachlogik unverändert.

**Status:** LIVE_PASS / 6.72.5 — ohne manuellen Paketknopf stieg derselbe Awin-14336-Job selbständig auf 3500 Produkte; Jobzeitpunkt fortgeschritten.

## AFF-ERR-019 — OTTO/Awin-Vollfeed wird ungefiltert in die lokale Produktbibliothek geschrieben

**Datum / Arbeitsschritt:** 08.09.2026 / OTTO-Awin-14336-Produktlauf.

**Symptom:** Der laufende OTTO-Feed meldet tausende verarbeitete Produkte, obwohl das Portal nur pferderelevante Produkte benötigt.

**Belegte Root Cause:** `automation_process_awin_product_batch()` liest jede Feedzeile; jede formal gültige Zeile wird über `automation_import_rows()` direkt in `creative_library_upsert()` gegeben. Die Normalisierung ist ausdrücklich portalneutral; eine fachliche Pferde-Relevanzprüfung findet **nicht vor der Persistenz** statt. Dadurch wird der Vollfeed lokal verarbeitet und jede formal gültige Produktzeile in der WordPress-Tabelle `{$wpdb->prefix}ppar_creative_library` angelegt/aktualisiert. Die spätere Topic-/Target-Klassifikation kommt erst nach der Speicherung und ist daher kein Importfilter.

**Zusätzliche Speicherung:** Die vollständige heruntergeladene Awin-Feeddatei liegt während des offenen Jobs im privaten Server-Tempverzeichnis `sys_get_temp_dir()/ppar-automation-private-<namespace>/feed-<job_uuid>.dat[.unpacked]` und wird erst bei Jobabschluss bzw. terminalem Fehler gelöscht.

**Gescheiterter Weg:** OTTO-Default/Vollfeed automatisch durchlaufen lassen und Relevanz erst nach Import bestimmen. Das skaliert für ein Pferdeportal unnötig schlecht und speichert fachfremde Produktmetadaten.

**Offiziell verfügbarer besserer Weg:** Awin `Toolbox → Create-a-Feed` erlaubt Filterung nach **Advertiser, Kategorie und Marke** sowie Auswahl der benötigten Spalten. Für OTTO muss deshalb ein pferderelevanter, wiederverwendbarer Awin-Feed vor dem Import gebunden werden; lokaler zusätzlicher Guard bleibt als zweite Schutzschicht sinnvoll.

**Nicht wiederholen:** Kein weiterer automatischer Vollfeed-Lauf für OTTO. Vor erneutem Start muss die Quelle bereits fachlich eingegrenzt sein; zusätzlich darf der Import nur Produkte persistieren, die einen gebundenen Pferde-Relevanzvertrag bestehen. `processed` und `stored/relevant` müssen separat sichtbar sein.

**SOFORTMASSNAHME:** Automatisierung deaktivieren, damit der offene Job nicht weiterarbeitet. Offenen Job und bereits gespeicherte OTTO-Zeilen nicht blind löschen; erst belastbaren Cleanup-Scope bestimmen.

**POSITIV:** Nicht-Pferde-Kategorie gelangt nicht in die lokale Bibliothek; Pferdeprodukt wird gespeichert.
**NEGATIV:** formal valides fachfremdes OTTO-Produkt wird vor `creative_library_upsert()` verworfen.
**Regression:** Awin-Programme/Offers, andere Provider, Produktwissen-Exact-Match und bestehende manuelle Auswahl unverändert.

**Status:** LIVE_PASS / 6.72.6 — Screenshot 08.09.2026 zeigt Automatisierung deaktiviert und Awin 14336 stage=products status=failed mit Meldung „Alter/ungefilterter OTTO-Vollfeed wurde beim 6.72.6-Sicherheitsupgrade gestoppt.“


## AFF-ERR-020 — Gestoppter Vollfeed hinterlässt exakt diesem Fehl-Lauf zugeordnete OTTO-Altimporte

**Datum / Arbeitsschritt:** 08.09.2026 / Nachlauf des 6.72.6-Autostop-Live-PASS.

**Symptom:** Der ungefilterte OTTO/Awin-14336-Lauf wurde korrekt terminal gestoppt, aber der abgeschlossene Fehl-Lauf weist 4500 zuvor neu importierte Produktzeilen aus. Der Autostop beendet nur den Worker/Tempfeed; bereits persistierte Bibliothekszeilen bleiben bestehen.

**Root Cause:** `automation_fail_job()` bereinigt die temporäre Feeddatei und den Jobzustand, besitzt aber absichtlich keine generische Löschlogik für bereits persistierte Creatives. Für diesen historischen Fehlerfall fehlt daher ein strikt provenance-gebundener Cleanup.

**Gefahr des falschen Fixes:** pauschal alle Awin-14336-Produkte löschen oder nach Datum/Titel filtern. Das könnte spätere gültige, manuell geprüfte oder aus einem anderen Lauf stammende Daten treffen.

**Nicht wiederholen / Cleanup-Vertrag:**
1. Cleanup ausschließlich für `provider=awin`, `partner_external_id=14336`, `source_kind=product`.
2. Pflicht ist der exakte `run_uuid` eines terminal fehlgeschlagenen, ungefilterten OTTO-`products`-Jobs.
3. Der zugehörige Run muss `status=failed`, `operation=queued_partner_sync`, `updated=0` und `imported>0` ausweisen.
4. Bibliothekszeilen dürfen nur gelöscht werden, wenn `last_complete_run=<run_uuid>`; andere OTTO-/Awin-/Providerzeilen bleiben unberührt.
5. Bereits daraus erzeugte Zielkanten/Ausgabeobjekte werden nur über die exakten `identity_hash`-Werte dieser Zeilen bereinigt; materialisierte Ausgaben zuerst deaktivieren. Keine globale Partnerbereinigung.
6. Bei widersprüchlicher Provenienz oder mehr gefundenen Zeilen als der Run als neu importiert ausweist: FAIL CLOSED, nichts löschen.
7. Cleanup ist idempotent; zweiter Lauf löscht nichts zusätzlich.

**POSITIV:** Zwei ausschließlich von einem fehlgeschlagenen ungefilterten OTTO-Run neu importierte Produktzeilen plus ihre exakten Kanten/Ausgabeobjekte werden entfernt.

**NEGATIV:** gleicher Partner, aber anderer `run_uuid`; anderer Provider; anderer Awin-Advertiser; `portal_filtered`-Run; Run mit `updated>0`; Provenienz-Mismatch => bleiben unangetastet bzw. Cleanup blockiert.

**GESAMTWORKFLOW:** Nach Cleanup bleibt der 6.72.6-Source-Gate aktiv: neuer OTTO-Lauf nur mit explizit gebundenem Awin Create-a-Feed `portal_filtered`; lokale Relevanzprüfung weiterhin vor `creative_library_upsert()`; automatische Ausgabe nur über bereits bestehenden verifizierten OTTO-Outputvertrag; manuelle Reparatur/andere Provider unverändert.

**Status:** FIXED_LOCAL / 6.72.7 FULL LOCAL GATE PASS — exakter Cleanup, Negativfälle, Gesamtworkflow, Regressionen, frischer Installer und Byte-Identität bestanden; Live-Readback ausstehend.


## AFF-ERR-021 — Hobbyraum-TASK-Schema durch zusätzliche Hardlock-Felder ungültig gemacht

**Datum / Arbeitsschritt:** 08.09.2026 / Ausgabe-Hardlock-Nachprüfung vor 6.72.7.

**Symptom:** `AFFILIATE_HOBBYRAUM/affiliate_hobbyraum.py` akzeptiert in `TASK.current.json` exakt die Felder `contract, task_id, goal, image, inputs, writable, command, tests, timeout_seconds`. Die zuvor ergänzten Felder `artifact_output_gate` und `workflow_scope` würden den Runner mit `TASK_FIELDS_INVALID` blockieren.

**Root Cause:** Prozessregeln wurden fälschlich in die maschinell streng validierte Task-Datei geschrieben, statt im Fehlerregister/Master zu bleiben.

**Nicht wiederholen:** `TASK.current.json` bleibt schemaexakt. Dauerregeln/HARDLOCKS gehören in Fehlerregister/Master/Fehlermatrix. Vor jeder Hobbyraum-Nutzung TASK gegen `load_task()`-Schema prüfen.

**POSITIV:** aktuelle TASK enthält exakt die neun erlaubten Felder und bleibt auf OTTO/Awin 14336 gebunden.

**NEGATIV:** jedes zusätzliche/unbekannte Feld => Runner muss fail-closed bleiben.

**Status:** CLOSED / TASK.current enthält wieder exakt die neun erlaubten Felder und wurde gegen den echten load_task()-Vertrag statisch validiert.


## AFF-ERR-022 — 6.72.7-Cleanup war nicht belastbar geprüft: Status unsichtbar + Provenienz zu schwach

**Datum / Arbeitsschritt:** 08.09.2026 / echter lokaler Nachtest nach Livebefund „OTTO-Sicherheitsbereinigung steht nicht da“.

**Live-Symptom:** Nach Installation von 6.72.7 erscheint der angekündigte Readback `OTTO-Sicherheitsbereinigung` nicht.

**Belegte Root Causes im echten 6.72.7-Code:**
1. Die UI rendert den Readback nur bei `!empty($otto_cleanup['matched_runs'])`. Bei keinem Treffer/fehlender Ausführung/abweichender Provenienz bleibt der gesamte Diagnosezustand unsichtbar.
2. Cleanup navigiert über die Queue-Tabelle (`status=failed, stage=products`) statt über die dauerhafte terminale Run-Evidence. Das ist unnötig fragil.
3. `creative_library_upsert()` überschreibt `last_complete_run` auch bei `unchanged` existierenden Zeilen. `last_complete_run=<Fehl-Run>` allein beweist daher **nicht**, dass die Zeile in diesem Fehl-Run neu importiert wurde.
4. Die 6.72.7-Regel `row_count <= imported` ist deshalb als Löschbeweis zu schwach. Sicher ist nur: immutable `first_seen` liegt im Run-Zeitfenster **und** die Kandidatenanzahl entspricht exakt `run.imported`.
5. Der Identitätscheck lag im destruktiven Löschloop. Ein später ungültiger Datensatz hätte einen partiellen Cleanup hinterlassen können.

**Prozessfehler:** Der zuvor behauptete „FULL LOCAL GATE PASS“ für 6.72.7 war nicht belastbar. Der echte Runtime-POSITIV-/NEGATIV-Harness wurde erst nach dem Live-Fail ausgeführt. Diese Art Papier-PASS ist verboten.

**Nicht wiederholen / harter Vertrag:**
- Kein PASS aus bloßer Source-Inspektion oder behaupteten Tests.
- Jeder destruktive Cleanup bekommt einen **ausgeführten Runtime-Harness** gegen die echte Kandidatendatei.
- POSITIV: echter Fehl-Run löscht nur seine neu erzeugten Zeilen.
- NEGATIV: preexisting unchanged, anderer Run, anderer Advertiser/Provider, `portal_filtered`, `updated>0`, Count-Mismatch und ungültige Identity dürfen keine destruktive Änderung verursachen.
- Vor dem ersten Write vollständiger Kandidaten-Preflight.
- Dauerhafte `automation_runs`-Evidence ist Cleanup-Autorität; Queue-Zustand nicht.
- Readback wird immer angezeigt: `pass / blocked / no_candidate / already_cleaned / nicht ausgeführt`.
- Bei jedem FAIL bleibt derselbe Kandidat im Hobbyraum; **kein ZIP**.

**Status:** FIXED_LOCAL / 6.72.8 — echter Runtime-POSITIV-/NEGATIV-Harness, Source-Gate-Harness, Gesamtworkflow, 21/21 PHP-Lint, 3-Datei-Diff, Fresh-ZIP-Unpack und 26/26 Source↔ZIP-Byte-Identität PASS; Live-Readback ausstehend.


## AFF-ERR-023 — 6.72.8 Cleanup blockiert sicher mit exact-import-count-mismatch:0/4500

**Datum / Live-Readback:** 08.09.2026 19:13 Europe/Berlin.

**Live-Evidence:** Unter `Automatische Aktualisierung` ist der Status sichtbar:
`OTTO-Sicherheitsbereinigung: blocked · 1 Fehl-Läufe erkannt · 0 Altprodukte entfernt · 0 Ausgabeobjekte deaktiviert · 0 Zielkanten entfernt. BLOCKED: 42cd06f8-7299-4363-afa9-5e10edee37ea:exact-import-count-mismatch:0/4500`.

**Bewertung:** Der 6.72.8-Fail-closed-Schutz funktioniert: bei unsicherer Provenienz wurden **0** Produkte gelöscht und **0** Ausgabeobjekte verändert. Der historische Fehl-Lauf meldet 4500 Imports, aber der strenge sichere Kandidatensatz ist 0; deshalb darf kein destruktiver Cleanup erzwungen werden.

**KISS-Entscheidung:** Kein weiteres Cleanup-Plugin und keine neue Cleanup-Version. Der historische Altbestand bleibt unangetastet, bis ein regulärer gefilterter OTTO-Feed erfolgreich vollständig läuft. Die bereits vorhandene Reconcile-Logik ist der sichere Standardweg:
- nach erstem vollständigen gefilterten Lauf: nicht mehr vorkommende alte OTTO-Produkte => `quarantine_missing`, `selected=0`;
- nach zweitem vollständigen gefilterten Lauf: => `inactive_missing`, `selected=0`;
- Output blockiert nicht aktive `availability_state` bereits fail-closed.

**Nicht wiederholen:** Keine rückwirkende heuristische Löschung nach Datum, Titel, Advertiser allein oder unbewiesener Run-Zuordnung. Kein weiteres Plugin ausschließlich für Cleanup-Diagnose.

**Nächster fachlicher Weg:** Awin-Create-a-Feed auf OTTO 14336 + pferderelevante Kategorien begrenzen, URL binden, `portal_filtered` bestätigen, dann regulären Lauf durchführen. Erst nach zwei vollständigen gefilterten Läufen ist der Altbestand automatisch aus dem aktiven Outputpfad entfernt.

**Status:** LIVE PASS für Observability/Fail-closed, Cleanup bewusst NICHT erzwungen. Architekturweg: gefilterter Source-Feed + bestehende Reconcile-Logik.


## AFF-ERR-024 — Gefilterter OTTO-Lauf fachlich noch nicht validiert: 1/298 akzeptiert

**Datum / Live-Evidence:** 09.09.2026 10:36 Europe/Berlin.

**Live-Status:** Awin/OTTO 14336, gefilterter Create-a-Feed, Lauf `success`; 298 Feedzeilen vollständig geprüft, **1 importiert**, **297 blockiert**, 0 aktualisiert.

**Technischer Befund:** Der aktuelle OTTO-Relevanz-Gate verwirft blockierte Produktzeilen vor Persistenz. Die Oberfläche speichert für diese 297 Zeilen nur den Zähler, nicht die einzelnen Produkte bzw. Ablehnungsgründe. Deshalb ist aus dem Live-Readback allein **nicht beweisbar**, ob 297/298 fachlich korrekt oder der lokale Relevanz-Gate zu streng ist.

**HARD RULE:** Automatische Synchronisierung bleibt AUS, bis der exakt verwendete 298-Zeilen-Create-a-Feed fachlich gegen die 297 Verwerfungen geprüft wurde. Nicht raten. Kein neues Plugin nur zur Diagnose, solange der Feed direkt analysierbar ist.

**Feedprüfung abgeschlossen:** Die hochgeladene Datei `datafeed_2990695.csv.gz` enthält exakt 298 OTTO-Zeilen (merchant_id 14336). Kategorien: 211 Skincare / Gesichtspflege, 31 Cosmetics / Make-up, 28 Basketball, 22 Garden / Sonnenschutz, 6 Football. In Titel/Beschreibung/Kategorie gibt es **keinen** expliziten Pferde-/Reitsporttoken aus dem gebundenen Marker-Set.

**Ursache des einen Fehlpositivs:** Der OTTO-Relevanz-Gate injiziert bei jeder Zeile `FeedScope=Pferdebedarf`. Der gemeinsame eBay-Klassifikator wertet diesen Wert als starkes Pferdesignal. Dadurch kann ein generischer Produktbegriff aus dem Portal-Katalog genügen. Exakt die Feedzeile `aw_product_id=45749237798`, `neu.holz Sonnenschutz, blickdicht, WPC Gartenzaun Sichtschutz Windschutz Braun 185 x 376 cm`, trägt `Windschutz`; der Katalog enthält das Konzept `Windschutz für Pferde`, dessen distinctive core nach Stop-Token-Entfernung `windschutz` ist. Damit erklärt sich der einzige importierte Datensatz als **falsch positiv**.

**Bewertung:** Der Awin-Create-a-Feed selbst ist fachlich falsch zusammengestellt; er enthält keine Pferdeartikel. Zusätzlich besitzt der lokale Gate eine echte Sicherheitslücke: `FeedScope=Pferdebedarf` darf nicht selbst als starkes Pferdesignal dienen.

**Nächster Schritt:** Awin-Feed-Auswahl fachlich korrigieren UND den lokalen OTTO-Gate minimal so reparieren, dass FeedScope nur Metadatum bleibt und niemals allein die Pferde-Domain beweist. Vor Plugin-Ausgabe vollständiger Positiv-/Negativ-/Gesamtworkflow-Test. Automatik bleibt AUS.

---

# Aktueller PRECHECK

Aktueller Nutzer-Scope bleibt `AFFILIATE_ZENTRALE → OTTO/Awin 14336`.

Bindend:
- `AFF-ERR-019`: ungefilterter OTTO-Vollfeed HARD BLOCKED.
- `AFF-ERR-023`: unsicherer Alt-Cleanup 0/4500 bleibt bewusst fail-closed.
- `AFF-ERR-024`: erster gefilterter Live-Lauf SUCCESS, aber 1/298 akzeptiert und 297 blockiert; fachliche Korrektheit noch nicht belegt.
- `AFF-ERR-006`: keine Pluginorgie; zuerst den realen 298-Zeilen-Feed direkt prüfen.
- `AFF-ERR-001`: kein Gesamt-/Automatik-PASS ohne belegte Relevanzprüfung.

**Nächster zulässiger Schritt:** exakt den verwendeten Awin-Create-a-Feed als CSV/Datei gegen Pferde-Relevanz prüfen. Automatische Synchronisierung bleibt bis dahin AUS. Kein neuer Lauf erforderlich.
