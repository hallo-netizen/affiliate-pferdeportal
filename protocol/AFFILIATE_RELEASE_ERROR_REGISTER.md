# AFFILIATE-ZENTRALE — VERBINDLICHES FEHLERREGISTER

Stand: 2026-09-18
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

**POSITIV:** sichtbarer Pfad `WordPress-Dashboard → Affiliate-Zentrale → Partner & Einnahmen` delegiert direkt an `PPAR_Partner_Analytics_Admin::render_page()` und verwendet ausschließlich ingestierte Original-Providerreports; lokale WordPress-Klickwerte sind ausdrücklich ausgeschlossen.
**NEGATIV:** fehlende Providerdaten bleiben `nicht verfügbar`, niemals geschätzt.
**Regression:** Provideradapter, Ausspielung, Tracking unverändert.

**Evidence:** `release/affiliate-zentrale/evidence/current_scope_manual_import_partner_visibility_20260902.txt` — ausschließlich der darin enthaltene Analytics-/KISS-Nachweis bleibt verwendbar; der manuelle Runtime-Importteil ist durch AFF-ERR-015 verworfen.

**Status:** CANONICAL_ROOTFIX_BOUND / WordPress-Liveprüfung mit 6.72.72 noch offen.

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

**Status:** ROOT_CAUSE_PROVEN / FIX_PENDING — Feed fachlich falsch, False Positive vollständig erklärt; Produktionscode noch unverändert.

## AFF-ERR-025 — CURRENT-/Hobbyraum-Drift nach neuem OTTO-Livebefund

**Datum / Nachholprüfung:** 09.09.2026.

**Symptom:** Der aktuelle Master enthält gleichzeitig einen neuen NEXT ACTION zum falschen 298-Zeilen-Feed/FeedScope-False-Positive und weiter unten noch die alte Anweisung, 6.72.8 erst zu installieren und nur den Cleanup-Readback abzulesen. Zusätzlich nennt der Master als Live-Stand noch 6.72.7, obwohl 6.72.8 installiert und live geprüft wurde. `AFFILIATE_HOBBYRAUM/TASK.current.json` ist ebenfalls noch auf den bereits abgeschlossenen Cleanup-Provenienz-Test gebunden. Der ältere DS24-Scope-Lock bezeichnet sich weiterhin als aktuelle Nutzerautorität, obwohl die spätere ausdrückliche OTTO-Priorisierung vom 07.09.2026 den aktiven Scope geändert hat.

**Root Cause:** Nach Live-/Fachstandsänderungen wurden Governance und oberer Masterteil aktualisiert, aber nicht alle CURRENT-/Task-/Scope-Wahrheiten atomar nachgezogen.

**Nicht wiederholen:** Nach jeder Änderung des belastbaren Live-Standes oder NEXT ACTION müssen Master, Governance, Hobbyraum-Task und aktive Scope-Kennzeichnung in demselben Abschlussblock gegengeprüft werden. Historische Scope-Dateien dürfen nicht weiter als aktuell markiert bleiben. Keine konkurrierende zweite NEXT ACTION.

**POSITIV:** Master, Governance und TASK nennen denselben aktuellen OTTO-Schritt; Live-Stand ist 6.72.8; alter Cleanup-Installationsschritt ist nicht mehr aktuell; DS24-Scope-Datei ist sichtbar superseded.

**NEGATIV:** Suche nach aktiven Aussagen `live installierter Stand: 6.72.7`, `Installieren: Affiliate-Zentrale_6.72.8_TEST.zip` oder Cleanup-Provenienz als aktuelle TASK darf keine zweite aktuelle Wahrheit mehr ergeben.

**Tests / Postcheck:** strukturelle Gegenprüfung der vier autoritativen CURRENT-/Scope-/Task-Quellen plus Branch-Head; keine Source-/Pluginänderung, daher keine PHP-/Runtime-Regression durch diesen Nachholfix erforderlich.

**Status:** CLOSED / NACHGEHOLT — Master, Governance, Scope-Kennzeichnung und Hobbyraum-TASK wurden auf denselben 09.09.-Stand gezogen; struktureller Postcheck PASS.

---

## AFF-ERR-026 — Backend-Statistik darf keine eigene Erhebung als Partnerwahrheit verwenden

**Datum / Statusänderung:** 18.09.2026 / Nutzerentscheidung nach kanonischem Delta-Precheck.

**Symptom/Root Cause:** Die kanonische Partner-/Einnahmen-Seite verwendet eigene lokale Klickzähler zusätzlich zu Providerreports. Der Nutzer hat diese Mischform ausdrücklich verworfen: Die Backend-Statistik soll die Originaldaten der jeweiligen Partner/Provider abrufen und keine eigene Erhebung verwenden.

**Nicht wiederholen:** Für die Backend-Statistik ausschließlich verifizierte Original-Report-/API-Daten des jeweiligen Providers/Partners verwenden. Lokale Klick-, Bestell-, Umsatz- oder Provisionserhebung dort weder anzeigen noch addieren noch als Ersatz für fehlende Providerdaten einsetzen. Fehlender Providerreport = `nicht verfügbar`, nicht Null. Währungen getrennt behandeln; keine Bestpartner-Aussage aus unvollständiger oder nicht vergleichbarer Datenbasis.

**POSITIV:** Providerreport liefert Klicks/Bestellungen/Umsatz/Provision + Datenquelle/Datenstand; exakt diese Originalwerte werden angezeigt.

**NEGATIV:** Ohne Providerreport erscheinen keine lokalen Ersatzklicks und keine erfundenen Nullwerte. Eigene WordPress-Klickzähler verändern die Statistik nicht.

**Status:** FIXED_SOURCE / LIVE_GATE_OPEN — der kanonische 6.72.72-Testkandidat liest für `Partner & Einnahmen` ausschließlich gebundene Original-Providerreports; fehlende Daten bleiben `nicht verfügbar`. WordPress-Live-Readback ist noch offen.

## AFF-ERR-027 — Lokale 6.72.60–6.72.65-Testlinie darf keine zweite Pluginwahrheit werden

**Datum / Arbeitsschritt:** 18.09.2026 / Abschluss- und Übergabeprüfung.

**Symptom/Root Cause:** Im Chat entstanden mehrere höhere lokale Testpakete, während die autoritative GitHub-Source und das Pluginbüro weiter 6.72.19 führen. Einzelne lokale Stände haben Teil-/LIVE-Befunde, aber keinen gemeinsamen kanonischen Release-Gesamtgate.

**Nicht wiederholen:** Lokale 6.72.60–6.72.65 ausschließlich als Test-/Fehleroracle behandeln. Kein `CURRENT.zip`-Nachzug, kein Release-PASS und keine weitere Versionskaskade daraus. Nächster Schritt ist read-only kanonischer Delta-Precheck; danach genau ein Rootfix-Kandidat und vollständiger Gateblock.

**Status:** CLOSED / PROZESS-HARDLOCK ERFÜLLT — die alte 6.72.60–6.72.71-Linie bleibt ausschließlich Oracle/Historie; genau ein kanonischer 6.72.72-Testkandidat ist gebunden. Kein Pluginbüro-CURRENT-Nachzug vor Live-/Release-Abnahme.


# Routinghinweis — keine CURRENT-Wahrheit

Dieses Fehlerregister enthält Fehlerregeln, Status und Nachweise. Es führt **keinen aktuellen Branch-/Head-/Blocker-/NEXT-ACTION-Stand**.

Aktueller Arbeitsstatus und genau eine NEXT ACTION stehen ausschließlich in:
`control/release-governance/CURRENT_RELEASE.json`.

Der Einstieg bleibt:
`release/affiliate-zentrale/AGENTS.md -> CURRENT_RELEASE.json -> Frischecheck -> NEXT ACTION`.

## AFF-ERR-028 — Release-Guard-Vertragswerte in objective_control abgeschwächt

**Datum / Befund:** 18.09.2026 / Rootfix-Start.

**Symptom:** `CURRENT_RELEASE.json` enthielt für `microfix_policy`, `new_version_policy` und `investigation_policy` Lifecycle-spezifische Ersatztexte. Der unveränderliche `release_guard.py` akzeptiert jedoch nur seine exakten Vertragswerte und würde fail-closed mit `OBJECTIVE_CONTROL_WEAKENED:*` abbrechen.

**Nicht wiederholen:** Unveränderliche Guard-Vertragswerte niemals für Meilenstein-/Scope-Texte umbenennen. Fachlicher Status gehört in `current_milestone`, `user_scope_lock`, `execution_state` und Scope-Dokumente.

**Status:** CLOSED_SOURCE_CONTRACT — `objective_control` entspricht wieder den unveränderlichen Werten aus `release_guard.py`. Ein zusätzlicher neuer Runtime-Guard-PASS wird hier nicht behauptet.


## AFF-ERR-029 — Current-NEXT-ACTION widerspricht unveränderlichem Release-Guard

**Datum / Abschlussprüfung:** 18.09.2026.

**Symptom:** `control/release-governance/CURRENT_RELEASE.json` führt nach Erstellung des 6.72.72-Testkandidaten `INSTALL_67272_TEST_CANDIDATE_AND_VERIFY_START_CATEGORY_PAGE_AND_PROVIDER_STATS` als `execution_state.authorized_next_action`.

**Root Cause:** Der konkrete Livetest-Schritt wurde fälschlich direkt als technische NEXT-ACTION-Konstante in die Current geschrieben. Der unveränderliche `release_guard.py` akzeptiert an dieser Stelle ausschließlich `COMMIT_EXACT_V6638_21_FILE_SOURCE_TO_CANONICAL_ROOT`, `RUN_BOUND_RELEASE_GATES` oder `FINALIZE_RELEASE`. Damit wäre `governance-check` fail-closed.

**Nicht wiederholen:** Konkrete Testschritte gehören in die gebundene Gate-/Scope-Beschreibung. `authorized_next_action` muss immer exakt eine vom unveränderlichen Guard erlaubte Zustandsaktion tragen. Keine neue freie NEXT-ACTION-Konstante erfinden.

**Zusatzbefund:** `execution_state.hobbyroom_current` bezeichnet den bereits zurückgegebenen Rootfix weiter als `ACTIVE` und enthält eine alte eigene `next_action`. Hobbyraum darf keine zweite aktuelle NEXT-ACTION-Wahrheit bilden.

**POSITIV:** Current verwendet guard-konform `RUN_BOUND_RELEASE_GATES`; der konkrete erste Gate-Schritt bleibt eindeutig der eine 6.72.72-WordPress-Live-Readback.

**NEGATIV:** Suche nach aktivem `INSTALL_67272_TEST_CANDIDATE_AND_VERIFY_START_CATEGORY_PAGE_AND_PROVIDER_STATS` als `authorized_next_action` oder Hobbyraum-`next_action` darf keine zweite Current-Wahrheit ergeben.

**Status:** CLOSED / NACHGEHOLT — `CURRENT_RELEASE.json` Generation 67 verwendet wieder guard-konform genau `RUN_BOUND_RELEASE_GATES`; der konkrete erste Gate-Schritt ist dort gebunden. Hobbyraum ist als `COMPLETED_RETURNED_TO_CURRENT` markiert und führt keine eigene NEXT ACTION mehr.

## AFF-ERR-030 — Awin-Programmliste: falscher 6.72.105-Transport lieferte erneut Nicht-JSON

**Datum / Live-Befund:** 19.09.2026.

**Symptom:** 6.72.105 meldete live erneut `Awin lieferte keine gültige JSON-Programmliste; Last-Known-Good bleibt erhalten.`

**Tatsächliche Ursache:** Der 6.72.103/105-Weg wurde auf `includeHidden=true&accessToken=...` umgestellt und wich damit vom bereits funktionierenden Awin-Verbindungstest ab. Die aktuelle Awin-Authentifizierungsdokumentation bindet OAuth2 Bearer; der Programme-Endpunkt erlaubt `relationship=joined`. `includeHidden` ist laut Endpoint-Dokumentation nur ohne `relationship` wirksam. Der funktionierende KISS-Weg ist deshalb ein einziger gemeinsamer Requestpfad: `GET /publishers/{publisherId}/programmes?relationship=joined` + `Authorization: Bearer <token>`.

**Rootfix:** 6.72.106 vereinheitlicht Verbindungstest und Programmlisten-Refresh auf genau diesen Request. Kein zweiter Fallbacktransport. HTTP-/JSON-Fehler bleiben fail-closed; Last-Known-Good wird nicht überschrieben.

**POSITIV lokal:** 21/21 PASS inkl. `relationship=joined`, Bearer, gültige JSON-Liste und LKG-Write erst nach gültigem JSON.

**NEGATIV lokal:** HTTP 200 Nicht-JSON und HTTP 401 => WP_Error, exakt ein Request, kein Fallback, kein Programme-Write, LKG bleibt erhalten.

**LIVE:** Nutzer-Screenshot 19.09.2026: `Awin-Programmliste aktualisiert: 7 verbundene Programme`.

**Nicht wiederholen:** Nicht aus einer einzelnen Parameterbeschreibung einen neuen Auth-Transport ableiten. Verbindungstest und Refresh müssen denselben real bewiesenen Requestpfad verwenden.

**Status:** LIVE_PASS_6_72_106 / PRESERVED_IN_6_72_108.

## AFF-ERR-031 — Awin-Produkt erscheint in Banner-&-Werbemittel-Ansicht

**Datum / Live-Befund:** 19.09.2026.

**Symptom:** In `Affiliate-Zentrale → Banner & Werbemittel` mit Providerfilter Awin erscheint ein historischer OTTO-Produktdatensatz als Karte.

**Root Cause:** Die Creative-Library-Abfrage filterte providerseitig, trennte bei Awin aber `creative_type=product` nicht von der Banneransicht.

**Nicht wiederholen:** Die Awin-Banneransicht darf ausschließlich `creative_type=banner` liefern. Historische OTTO-Produkte werden nicht gelöscht und bleiben im Produktpfad.

**POSITIV:** Awin-Banner bleiben sichtbar.
**NEGATIV:** Awin-Produktzeile ist in der Banneransicht unsichtbar, Bestand bleibt erhalten.
**Regression:** Nicht-Awin-Providerquery unverändert; Ausspielung unverändert.

**Evidence lokal 6.72.103:** Runtime-SQL-Test PASS; Nicht-Awin-Gegenfall PASS; Bannerfilter-Mutation ROT; Fresh-Unpack PASS.

**Evidence:** `release/affiliate-zentrale/evidence/awin_672103_local_rootfix_20260919.txt`.

**Status:** FIXED_CANONICAL_6_72_105 / LOCAL_GATES_PASS / LIVE_GATE_OPEN.

## AFF-ERR-032 — Breadcrumb/Hero-First-Paint war fälschlich im Affiliate-Plugin repariert worden

**Datum / Live-Befund:** 19.09.2026.

**Symptom:** Pferde-Journal sprang beim Laden; der 6.72.102-Affiliate-Abstands-Guard löste das real nicht.

**Abschluss:** Der Lade-/Breadcrumb-Fix wurde aus der Affiliate-Linie wieder entfernt und in den allgemeinen Designpfad verlagert. Nutzer meldete danach die Ladezeit als okay. Die Affiliate-Linie 6.72.104ff enthält den gescheiterten 6.72.102-Breadcrumb-Spacer nicht mehr.

**Nicht wiederholen:** First-Paint/Breadcrumb-Geometrie ist Designverantwortung. Keine globalen Designspacer mehr als Affiliate-Nebenfix einbauen.

**Status:** CLOSED_OUTSIDE_AFFILIATE / AFFILIATE_GUARD_REMOVED / DESIGN_OWNERSHIP.

## AFF-ERR-033 — Drittes Produkt in Kategorieübersichten fällt auf fachfremden Fallback

**Datum / Live-Befund:** 19.09.2026.

**Korrektur der Fehlerbeschreibung:** Es war nicht der dritte Artikel, sondern der **dritte Produktplatz**. Beispiel: Kategorie Reitstiefel zeigte an Platz 3 ein Gerten-Produkt; Nutzer meldete dasselbe Muster in weiteren Kategorien.

**Root Cause:** `category_product_1..3` nahm mechanisch Kandidat 1/2/3 aus einer kombinierten Rangliste. Wenn nur zwei starke kategorierelevante Produkte vorhanden waren, konnte ein schwächerer Parent-/Fallback-Kandidat Platz 3 füllen.

**Rootfix 6.72.104:** Die drei Kategorie-Produktplätze bleiben innerhalb der stärksten Relevanzstufe. Reichen dort die Kandidaten nicht, bleibt der restliche Platz leer statt fachfremd aufzufüllen.

**Lokal:** Positiv 3 gleich relevante Produkte => 3 Plätze; Negativ 2 relevante + fremder Fallback => Platz 3 leer; Journal-Produktlogik unverändert. Der vollständige 6.72.108-Regressionslauf erhält diesen Block byte-/verhaltensgebunden.

**LIVE:** Für diesen Einzelpunkt wurde in diesem Chat kein separater, eindeutig isolierter Live-Readback protokolliert.

**Status:** FIXED_LOCAL_6_72_104 / PRESERVED_6_72_108 / SEPARATE_LIVE_RECHECK_NOT_DOCUMENTED.

## AFF-ERR-034 — 6.72.94ff beschädigte bestehende Banner-/Journal-Ausgaben

**Datum / Verlauf:** 19.09.2026.

**Symptom:** Nach der 6.72.94ff-Linie verschwanden Banner in Glossar, Pferderassen und Journal-Unterkategorien; Journal-Root war zeitweise ungleich geteilt; Glossar-Single wurde im Layout verschoben.

**Root Cause / Wiederherstellung:** Die globale Poollogik konnte bestehende Kampagnen deaktivieren und nachgelagerte Reparaturen arbeiteten zunächst auf der beschädigten Linie weiter. Der belastbare Wiederherstellungsweg war Rückkehr auf den letzten funktionierenden Vor-6.72.94-Verhaltensstand plus gezielte Wiederherstellung der echten Design-/Ausgabepfade.

**Live-Status:** Nutzer bestätigt nach 6.72.100:
- Pferde-Journal Root mittig/pari PASS;
- Pferde-Journal Unterkategorien PASS;
- Glossar Einzelbeitrag PASS;
- Glossar Kategorien PASS;
- Pferderassen inkl. Unterkategorien PASS.

**Nicht wiederholen:** Diese bestätigten Pfade ab jetzt nicht mehr nebenbei anfassen. Jede spätere Änderung muss sie als Regression-Hardlock behandeln.

**Status:** LIVE_PASS_6_72_100 / PERMANENTER NICHT-ANFASSEN-HARDLOCK.

## AFF-ERR-035 — Operative Live-/Testlinie ist nicht in der kanonischen Repository-Source gebunden

**Datum / Frischecheck:** 19.09.2026, Abschlussprüfung.

**Aktueller Befund:** Die direkte kanonische Repository-Source auf `affiliate-release-current` steht auf 6.72.105 / Manifest `ab1f4f54a7b0743e00ccbde5e1c11aa278a790ca47e5f72348bd125be9eabf29`. Der tatsächlich getestete und live verwendete Stand ist 6.72.108, ZIP-SHA-256 `d8aeb69bd67a18072996da9ca8101923e6ff6765a40c5d0d6a6f74bde3be5bb3`, lokaler Source-Manifest-SHA `d7771d6f2d7816217b0ccd576580bf722a22a40f5d1e19b333e29b5775719b8e`.

**Delta:** 6.72.108 gegen kanonische 6.72.105: 14/26 Dateien unterschiedlich. Das ist erneut ein echter Source-Drift und muss vor weiterer Pluginentwicklung geschlossen werden.

**Nicht wiederholen:** 6.72.108 nicht blind über die kanonische Source kopieren und 6.72.105 nicht als aktuellen Live-Stand ausgeben. Exakten 6.72.108-Tree gegen 6.72.105/6.72.104-Provenienz binden; danach Governance-/Positiv-/Negativ-/Regression-/Fresh-Unpack-Gates.

**Status:** REOPENED / CURRENT_FIRST_BLOCKER / 6_72_108_CANONICAL_RECONCILIATION_REQUIRED.



### Historischer Teilstand zu AFF-ERR-035 – abgelöst

**Historischer Frischecheck:** 19.09.2026, früherer Zwischenstand vor 6.72.108.

Damals lief WordPress laut Nutzer-Livetest auf 6.72.102; lokal existierte 6.72.103 und die kanonische Source stand auf 6.72.73. Dieser Drift wurde anschließend bis 6.72.105 reconciliiert. Der damalige Abschluss ist **nur Historie** und überschreibt den oben stehenden aktuellen REOPENED-Status nicht.

**Historische Evidence:** `release/affiliate-zentrale/evidence/awin_672103_local_rootfix_20260919.txt`.

**Historischer Abschluss:** CANONICAL_RECONCILED_6_72_105 / LOCAL_GATES_PASS. Danach entstand durch den getesteten/live verwendeten 6.72.108-Stand erneut Source-Drift; maßgeblich ist ausschließlich der aktuelle AFF-ERR-035-Abschnitt oben und für Status/NEXT ACTION ausschließlich `control/release-governance/CURRENT_RELEASE.json`.



## AFF-ERR-036 — 6.72.105 baute Awin-Fix auf falscher Altbasis und entfernte siteweit Anzeigen

**Datum / Live-Befund:** 19.09.2026.

**Symptom:** Nach Installation 6.72.105 waren Anzeigen siteweit verschwunden, einschließlich Journal, Glossar und Pferderassen; Journal-Platzierung/Zentrierung war damit erneut verletzt.

**Root Cause:** 6.72.105 wurde aus der älteren kanonischen 6.72.73-Linie abgeleitet, obwohl der funktionierende operative Stand bereits 6.72.104 enthielt. Vergleich 6.72.105 ↔ 6.72.104 zeigte 14 abweichende Dateien; damit wurden geschützte Ausgabeänderungen zurückgedreht.

**Rootfix:** 6.72.106 wurde exakt auf der funktionierenden 6.72.104-Basis gebaut und änderte nur den Awin-Programmlisten-Transport plus Versions-/Readme-Metadaten.

**Lokal:** kompletter Schutz-/Regressionstest auf der 6.72.104-Basis PASS. **LIVE:** Nutzer meldete nach 6.72.106 ausdrücklich `wieder ok`.

**Nicht wiederholen:** Jeder neue Affiliate-Kandidat muss gegen den letzten real funktionierenden Live-Basestand vollständig byte-/verhaltensgebunden regressionsgeprüft werden. Kein Fachfix auf einer älteren kanonischen Linie, wenn dadurch spätere Live-PASS-Deltas verloren gehen.

**Status:** CLOSED_LIVE_6_72_106 / PERMANENTE REGRESSIONSPFLICHT.

## AFF-ERR-037 — Synchronisierte Awin-Partner waren in Banner & Werbemittel nicht korrekt auswählbar

**Datum / Live-Befund:** 19.09.2026.

**Symptom 1:** Nach erfolgreichem Programme-Refresh erschienen die sieben Awin-Partner nicht in der Partnerauswahl der Bannerseite. Ursache: die UI las nur Partneraufnahme-Snapshots; Cleos war deshalb sichtbar, frisch synchronisierte Programme nicht.

**6.72.107:** führt Partneraufnahme-Snapshots und aktuell synchronisierte joined-Awin-Programme für die Auswahl zusammen; bestehende Snapshots wie Cleos haben Vorrang. Live zeigte sich danach noch ein UI-Restfehler: Partner-ID und Name waren bereits vorausgefüllt, das Dropdown blieb aber sichtbar auf `Manuell eingeben`.

**6.72.108 Rootfix:** bindet den tatsächlich vorausgefüllten Partner auch als `selected` im Dropdown.

**Lokal auf exakter 6.72.108-ZIP:** Partner/Cleos/Awin 25/25 PASS; voller Regressionstest 82/82 PASS; PHP 21/21 PASS; Fresh-Unpack 26/26 byteidentisch.

**LIVE:** Nutzer-Screenshot zeigt `Awin · Ahipos Horses DE · 120341` korrekt ausgewählt.

**Status:** LIVE_PASS_6_72_108.

## AFF-ERR-038 — Awin-Bannerinventar hat noch keine bewiesene automatische reale Quelle

**Datum / Abschlussprüfung:** 19.09.2026.

**Zielabweichung:** Programme und Partner sind jetzt synchronisiert, aber die echten Awin-Banner/Werbemittel der Partner werden noch nicht automatisch in den vorhandenen Creative-Lifecycle eingelesen.

**Bestehender Systemteil:** Creative-Library, Sammelimport, technische Bildprüfung, Matching, Ausspielung, Revalidierung und Re-Evaluation sind vorhanden. Der Awin-Automationspfad besitzt bereits eine statische-Creative-Eingangsnaht, aber keine gebundene reale Quelle.

**Cleos-Befund:** Cleos ist historisch als funktionierender Awin-Partner/Bannerbestand belegt. Der konkrete damalige Quellweg (Sammeldatei versus gesammelte Codes versus andere belastbare Quelle) konnte in der Abschlussprüfung jedoch noch nicht autoritativ bewiesen werden. Ein WordPress-Backup vom 29.08. nennt die Tabelle `slfo_ppar_creative_library`, der DB-Backup-Lauf brach jedoch mit Timeouts ab und liefert keinen verlässlichen Cleos-`source_kind`.

**Awin-Dokumentation:** Der dokumentierte Publisher-API-Katalog enthält Programme, Offers, Feeds, Reports usw.; ein vollständiger Publisher-`My Creative`-Inventarendpoint wurde in der aktuellen offiziellen API-Dokumentation nicht gefunden. Die `My Creative`-Dokumentation beschreibt Creative-Verwaltung auf Plattformebene, aber das ist kein Beweis für einen Publisher-Bulk-API-Abruf.

**Verbindliche Nutzerregel:** Kein normales Verfahren mit einzelnem `Code kopieren` je Creative. Keine Entwicklertools-/private Endpoint-Ermittlung als geratenes Produktionsverfahren.

**NEXT nach Source-Reconciliation:** Zuerst den historischen Cleos-Bulk-Importweg aus belastbarer Quelle beweisen. Falls dort keine wiederverwendbare Quelle existiert, nur einen dokumentierten/vertraglich belastbaren maschinenlesbaren Awin-Weg anbinden. Erst danach Implementierung.

**Status:** OPEN / CURRENT_AWIN_FUNCTIONAL_BLOCKER_AFTER_AFF_ERR_035.


## AFF-ERR-039 — Nichtkanonische 6.72.109–117 haben persistente Livezustände verändert; Downgrade stellt 6.72.108 nicht wieder her

**Datum / aktueller Live-Befund:** 20.09.2026.

**Symptomfolge:**
- Reithelme-Banner blieb trotz mehrerer Fixversuche fachlich falsch.
- Kategorie-Produktdarstellung fiel zunächst auf eine Produktkachel; anschließend meldete der Nutzer denselben Einbruch für alle Kategorien.
- eBay verschwand aus der sichtbaren Produktmischung; idealo blieb sichtbar.
- Nach 6.72.115 meldete der Nutzer, dass die sichtbare Artikel-/Produktausgabe vollständig verschwunden sei. Eine physische Löschung von WordPress-Beiträgen ist nicht belegt.
- 6.72.116 stellte den Zustand nicht wieder her.
- 6.72.117 zeigte generische Produktplatzhalter und einen beanstandeten Direktwerbeplatz-Platzhalter.
- Auch die erneute Installation einer älteren 6.72.111 beseitigte die Fehler laut Nutzer nicht.

**Belegte technische Ursache der Recovery-Blockade:** Die Linie 6.72.109–117 änderte nicht nur PHP-Code, sondern persistente WordPress-Zustände. Belegt sind unter anderem:
- 6.72.109: neue persistente Bannerplatzplanung `ppar_banner_placement_plan_v2`;
- 6.72.110 ff.: Analytics-v2-Cache/Bootstrap und geplante Refresh-Ereignisse;
- 6.72.114: persistierte Awin-Creative-Destination-Zustände (`_destination_*` / `destination_url`);
- 6.72.115: `ppar_network_idealo_v1.output_mode=automatic`, `idealo_sync_campaign_activation()`, Marker `ppar_multiprovider_category_repair_v672115`, globale Artikelplan-Revisionserhöhung;
- 6.72.116: Änderung von Artikelplan-Revision, Rebuild-State, Log und Cron im Recoveryversuch;
- 6.72.117: `output_mode=idealo_only` unter dem 6.72.115-Nachweis, erneute Aktivierungssynchronisation und Artikelplan-Rebuild auf aktueller Revision.

Ein bloßes Downgrade des Plugin-Codes kann diese persistierten Zustände nicht zuverlässig auf den Vorzustand zurücksetzen.

**Zusätzlicher Blocker 6.72.118:** Es existieren zwei unterschiedliche lokale Artefakte mit derselben Versionsnummer 6.72.118:
- `AFFILIATE_ZENTRALE_V6.72.118_EXACT_672108_STATE_RESTORE_POSNEG.zip` — SHA-256 `544ff072f3ec893fb3eb6244c8b22fce73ec18e540bd22fb54829ec96c66bbd4`;
- `AFFILIATE_ZENTRALE_V6.72.118_EXACT108_PRODUCT_STATE_RECOVERY_POSNEG.zip` — SHA-256 `3923edf87d90bac2dd1eb20723e17553310664c4105666b6cbea9d765a3fc10f`.
Sie enthalten unterschiedliche Recovery-Logik. Für keines ist ein Nutzer-LIVE-PASS belegt. **Beide sind gesperrt.**

**Was nicht mehr behauptet werden darf:**
- keine aktuell installierte Live-Version aus Erinnerung ableiten;
- keine physische Datenlöschung behaupten;
- keine Recovery als PASS aus lokalen Mock-/POSNEG-Tests ableiten;
- keinen alten ZIP-Downgrade als Zustandswiederherstellung behandeln.

**Autoritative Incident-Evidence:** `release/affiliate-zentrale/evidence/incident_672109_118_persistent_state_regression_20260920.txt`.

**Recovery-Zielvertrag:** `protocol/AFFILIATE_RELEASE_EMERGENCY_RECOVERY_672108_STATE_TARGET_20260920.md`.

**Genau eine NEXT ACTION:** Keine weitere Plugininstallation. Zuerst rein lesenden Live-Readback der im Recovery-Zielvertrag gebundenen Optionen/Postmeta/Creative-Library-/Cron-Zustände erstellen, aktuellen installierten Pluginstand bestimmen und den exakten persistenten Delta gegen 6.72.108 belegen. Erst danach einen minimalen Recoveryweg bauen oder einen exakt passenden Backupzustand gezielt wiederherstellen.

**Status:** OPEN / CURRENT_FIRST_BLOCKER / EMERGENCY_LIVE_RECOVERY_REQUIRED.


### AFF-ERR-039 – Recovery-Nachtrag 20.09.2026

**Korrektur des Arbeitswegs:** Der Nutzer hat ausdrücklich klargestellt, dass für diese Wiederherstellung kein direkter Live-Datenbankzugang erforderlich ist. Die vorhandenen 6.72.108–6.72.118-Artefakte, das Affiliate-Büro und das Plugin-Updateprotokoll wurden vollständig gegengeprüft.

**Belegte Ursache, warum die letzte 6.72.118 nichts bewirken konnte:**
- 6.72.118-A löscht die 115-/117-Marker.
- 6.72.118-B verlangt genau diese beiden Marker und kann danach fail-closed `not_applicable` werden.
- 6.72.118-B stellt nur `idealo_only -> automatic` zurück und nicht die komplette Persistenzkette.
- Bei bereits laufendem Status wird der nächste Batch nicht auf normalen Requests vorangetrieben.
- 6.72.118-A kann einen vollständigen Artikelplan-Rebuild mit Grund `v672118_restore_exact_672108_runtime` hinterlassen.

**Minimaler Recovery-Kandidat:** 6.72.119 auf exakter 6.72.108-Fachbasis, nur Hauptdatei + Readme abweichend. Keine neue Fachlogik, keine Inventarlöschung, kein globaler Revisionssprung, kein neuer Voll-Rebuild, keine Banneränderung. Nur Incident-Erkennung, 6.72.114-Destination-Rückführung, gezielte Provider-Aktivierung und Produktteil-Reparatur bestehender gespeicherter Artikelpläne.

**Artefakt:** `AFFILIATE_ZENTRALE_V6.72.119_KISS_EMERGENCY_RESTORE_POSNEG.zip`

**SHA-256:** `eb51dcbd19c62dae1a3958d209676926aa02793cb13a8fe64292ed53c3bcea74`

**Evidence:** `release/affiliate-zentrale/evidence/affiliate_672119_kiss_recovery_local_20260920.txt`

**Lokale Abnahme:** 12/12 Originalfehler-Nachweis; 55/55 statisch; 30/30 Runtime; Mutation/Sabotage fail-closed; PHP 21/21; Fresh-Unpack 26/26 byteidentisch.

**Status:** OPEN / LOCAL_RECOVERY_CANDIDATE_PASS / LIVE_RESTORE_TEST_OPEN.

**Genau eine NEXT ACTION:** exakt obigen SHA einmal installieren und anschließend die zuvor beschädigten realen Produkt-/Artikelausgaben sowie die geschützten Ausgabepfade prüfen. Kein weiterer Fachumbau und keine der alten 6.72.118-Versionen installieren.


### AFF-ERR-039 – kritischer Live-Nachtrag nach 6.72.119–6.72.123 – 20.09.2026

**Neuer belastbarer Live-Befund:**
- 6.72.119: Installation bewirkte laut Nutzer **keine sichtbare Wiederherstellung** der Kategorie-Produktkarten.
- 6.72.120: lokaler Kandidat, **kein belastbarer LIVE-PASS**; nicht als Wiederherstellung werten.
- 6.72.121: nach Installation blieben die drei generischen `Produktvorschau`-Karten sichtbar; **LIVE FAIL**.
- 6.72.122: nach Installation gleicher sichtbarer Fehler; **LIVE FAIL**.
- 6.72.123: nach Installation/Activation **kritischer LIVE FAIL: Frontend Timeout, WordPress-Backend nicht erreichbar**.

**Fehlerklasse / Ursache:**
- Für die ursprüngliche Wiederherstellungsblockade ist belegt: Code und persistenter WordPress-Zustand wurden in der 6.72.109–117-Linie gemeinsam verändert; ein Code-Downgrade allein stellt den früheren Zustand nicht wieder her.
- Für den neuen 6.72.123-Timeout ist nur die unmittelbare zeitliche/operative Kausalität zur Installation belastbar. Der exakte interne Timeout-Mechanismus ist **noch nicht bewiesen** und darf nicht geraten werden.
- Prozessfehler 119–123: lokale E2E-Harnesses starteten aus rekonstruierten/simulierten Schadenszuständen und konnten deshalb grün sein, obwohl der echte Livezustand davon abwich. Solche PASS dürfen nicht mehr als System-PASS gelten.

**Verbindliche Hard Rule ab jetzt:**
- Beide Teile gemeinsam prüfen: **Plugin-Code + real erfasster persistenter WordPress-Zustand**.
- Gesamtworkflow binden: persistenter Zustand → Provider/Kampagne → Zielbindung → `category_product_1..3` → eBay/idealo-Auswahl → Renderer → finales HTML → Template-`is_real` → sichtbare Kategorie.
- Positiv + Negativ + fail-closed gegen den kompletten Workflow.
- Kein weiterer Minifix, kein weiterer Installer, solange der erste echte Fehler offen ist.

**Failed artifact 6.72.123:**
- `AFFILIATE_ZENTRALE_V6.72.123_CATEGORY_PRODUCT_STRUCTURE_RESTORE_FULLSYSTEM_HARDTEST.zip`
- SHA-256 `c71d8fb8fc03751b0377b525e7d2b7c791ee424d7b219c3d042a41b20de7aa44`
- Status: **FORBIDDEN / DO NOT REINSTALL / DO NOT PROMOTE**.

**Incident-/Handoff-Protokoll:**
`protocol/AFFILIATE_RELEASE_TIMEOUT_672123_HANDOFF_20260920.md`

**Genau eine NEXT ACTION:** Außerhalb von WordPress-Admin den aktiven Pluginordner `affiliate-portal-router` deaktivieren/umbenennen, damit WordPress ohne 6.72.123 bootet. Kein anderes Affiliate-ZIP installieren/aktivieren. Abschlussbedingung: `/wp-admin/` und eine öffentliche Seite laden wieder. Erst danach read-only Live-State erfassen; vor diesem Readback kein weiterer Recovery-Build.

**Status:** OPEN / CURRENT_FIRST_BLOCKER / CRITICAL_SITE_UNREACHABLE_AFTER_6_72_123.


### AFF-ERR-039 – Nachtrag 21.09.2026: 6.72.125–6.72.130 und GitHub-Gesamtworkflow

**Live-Nachholung:**
- 6.72.125 stellte die sichtbaren Produktkarten wieder her, aber die Produktzuordnungen blieben falsch.
- 6.72.126–6.72.129 stellten den geforderten Livezustand nicht wieder her.
- 6.72.130 ist **LIVE FAIL**: weiterhin falsche Produkte; eBay weiterhin nicht in den sichtbaren Produktkarten.
- Keines der Pakete 6.72.125–6.72.130 ist dadurch ein neuer belastbarer Gesamt-LIVE-PASS oder ein freigegebener Release-Stand.

**Harte Arbeitsregel des Nutzers:** Die Paket-/GitHub-Historie ist vollständig gegen den kompletten Workflow zu prüfen. Der **erste** exakte produkt-/eBay-wirksame Delta ist zu beweisen und anschließend ausschließlich dieser Delta zurückzunehmen. Produktkacheln, Renderer, CSS und JS sind dabei gesperrt.

**GitHub-E2E-Nachweis:** Auf der ausschließlich temporären Evidence-Ausführungsbranch `affiliate-e2e-repro-20260920` wurde ein echter WordPress-7.1-/MariaDB-10.11-Workflow mit dem exakten 6.72.130-ZIP und einem hashgebundenen, aus dem realen WordPress-Export 15.09.2026 abgeleiteten Kampagnenzustand ausgeführt. Run `35536312242` ist absichtlich **FAIL**, nicht PASS.

Belegt im E2E:
- 2012 reale historische Produktkampagnen: eBay 922, idealo 1090;
- eBay-Public-Checkpoint: 428 aktive IDs;
- Reithelme: 69 exakte eBay- und 26 exakte idealo-Kandidaten;
- eBay passiert Complete/Current/Program/Seller/Slot/Rank sowie Source/Checkpoint/Image;
- erster belegter eBay-Ausfall ist der **Control-Gate** mit `control_provider_access_disabled`;
- danach bleiben nur idealo-Kandidaten;
- ein separater Versuch, die offensichtlichen eBay-Control-Optionen im Testzustand zu öffnen, reicht noch nicht: eBay bleibt im gerenderten Frontend abwesend. Die verbleibende konkrete Control-/Compliance-Unterbedingung ist deshalb **noch offen und darf nicht geraten werden**;
- das Entfernen exakter Reithelme-Ziele reproduziert fachfremde Produktlecks;
- nur ein exakter Stallhalfter-Kandidat reproduziert genau eine sichtbare Kachel.

**Noch nicht erledigt:** Die exakten Pakete 6.72.108–6.72.111 sind im GitHub-E2E gebunden. Die vollständige sequenzielle 6.72.112→6.72.117-Gesamtworkflow-Ausführung ist noch offen. Damit ist der erste exakte Paket-Delta noch **nicht vollständig bewiesen** und es ist noch kein Rückbau autorisiert.

**Display-Hardlock:** kein Displayfix im E2E; `assets/frontend.css` SHA-256 `305f7954047fbde080a52cff57f286ca817757efacf1a9738612403fb60e7f7c`, `assets/frontend.js` SHA-256 `203acdc463075c90d307c6bc7798d4ce56c5d0c4ab9d2a090c7197dcc4b50ae6`.

**Current-Frischecheck:** Der vorgeschriebene Guard gegen `affiliate-release-current` HEAD `924df488db3a6c0ad1fc4f0200de5f78bfec0bc2` wurde in GitHub Actions ausgeführt und blockiert generation 85 mit `AFFILIATE_RELEASE_GUARD_BLOCKED:OBJECTIVE_CONTROL_WEAKENED:microfix_policy`. Die Current-Bindung muss deshalb auf den unveränderlichen Governance-Vertrag zurückgeführt werden.

**Evidence:** `release/affiliate-zentrale/evidence/aff039_github_full_e2e_status_20260921.txt`.

**Autoritätshinweis:** Alle in älteren AFF-ERR-039-Nachträgen enthaltenen damaligen „NEXT ACTION“-Zeilen sind ausschließlich historische Momentaufnahmen. Die **einzige aktuelle** Status-/Blocker-/NEXT-ACTION-Wahrheit ist `control/release-governance/CURRENT_RELEASE.json`.

**Status:** OPEN / FULL_HISTORY_E2E_FIRST_REGRESSION_NOT_YET_PROVEN.


## AFF-ERR-040 — Awin-Programmlisten-Transportregression in 6.72.141

**Datum / Live-Befund:** 21.09.2026.

**Symptom:** 6.72.141 meldete live: `Awin-Programmliste konnte nicht aktualisiert werden; Last-Known-Good bleibt erhalten.`

**Belegte Ursache:** 6.72.141 wich erneut vom zuvor live bewiesenen 6.72.108-Awin-Transport ab, indem zusätzlich `includeHidden` und `accessToken` in den Programmlistenaufruf aufgenommen wurden. Der frühere live bewiesene KISS-Pfad ist `relationship=joined` plus OAuth2-Bearer.

**Rootfix:** 6.72.142 stellt ausschließlich den bewiesenen Awin-Programmlisten-Transport wieder her. Der Nutzer bestätigte danach für diesen Punkt ausdrücklich PASS.

**Nicht wiederholen:** Kein neuer Awin-Auth-/Parameterweg aus Dokumentationsfragmenten ableiten, solange der bereits live bewiesene Transport funktioniert. Verbindungstest und Programme-Refresh müssen denselben real bewiesenen Requestpfad verwenden.

**Status:** LIVE_PASS_6_72_142 / KEIN GESAMT-RELEASE-PASS.

## AFF-ERR-041 — Kategorie-Banner nutzt Ziel-/Deeplink-Evidenz für exakte Themenrelevanz noch nicht belastbar

**Datum / Arbeitsbindung:** 21.09.2026.

**Referenzseite:** `https://pferde-atelier.de/ausruestung/ausruestung-reiterbedarf/reithelme/`

**Zielabweichung:** Für die Reithelm-Kategorien soll ein technisch passender Banner, dessen reale Ziel-/Deeplink-Zielseite die Shop-Kategorie Reithelme ist, als fachlich exakter Kandidat vor einem allgemeinen Pferde-/Shop-Banner gewinnen. Die bestehende Office-Regel erlaubt und verlangt genau diese Zielseiten-Evidenz. Der tatsächliche aktuelle Auswahlverlust ist noch nicht read-only bis zur ersten exakten Selektionsstufe bewiesen.

**HARD RULE:** Keine neue Pluginversion und kein State-Write, bevor für die Referenzseite der aktuelle Banner, alle technisch geeigneten Kandidaten, deren reale Ziel-/Deeplinks und die erste konkrete Auswahl-/Rankingstufe erfasst sind, an der ein exakter Reithelm-Kandidat gegen einen breiteren Fallback verliert.

**POSITIV-Ziel:** technisch gültiger Reithelm-Zielbanner wird als Exact-Topic erkannt und darf einen allgemeinen Banner fachlich überstimmen.

**NEGATIV-Ziel:** unklare, widersprüchliche oder fachfremde Zielseite erzeugt keinen Exact-Match und fällt auf eine breitere Relevanzstufe zurück.

**Evidence / Arbeitsbindung:** `release/affiliate-zentrale/evidence/awin_672142_live_pass_banner_targeturl_next_20260921.txt`.

**Status:** OPEN / READ_ONLY_ROOTCAUSE_PROOF_REQUIRED.

## AFF-ERR-042 — Bannerkette nur teilgeprüft: Zielwahl korrekt, reale Hub-Ausgabe trotzdem fehlend

**Datum / Arbeitsbindung:** 02.10.2026.

**Symptom:** Der reale Schabrackendesigner-Banner blieb trotz zunächst grünem Zielklassifikationstest unsichtbar.

**Belegte Root Cause:** Die frühe Prüfung deckte nur einen Teil der realen Kette ab. In 6.72.174 war die Realziel-Evidenz bei mehreren verwandten Zielen noch zu eng. 6.72.175 reparierte Zielwahl, Zielkontext und Slotableitung; danach zeigte die vollständige WordPress/MariaDB-Simulation den nächsten echten Restfehler: der fachlich korrekt gewählte `hub_after_cards`-Querbanner hatte auf designverwalteten Hub-1/Hub-2-Seiten keinen realen serverseitigen Mount-Punkt.

**Nicht wiederholen:** Banneränderungen nie aus Klassifikation/Planung allein abnehmen. Verbindlicher Positivpfad ist: reales Creative → reale Zielmenge → Zielwahl → Zielkontext → Slotwahl → aktive Kampagne → realer serverseitiger Mount/Renderer → finales HTML. Negativfälle: Mehrdeutigkeit, Veto, inaktiv, falsches Format, leerer Slot und Duplikat müssen fail-closed bleiben.

**Rootfix 6.72.176:** Genau `hub_after_cards` wird auf Hub-1/Hub-2 serverseitig einmal nach dem fertigen Hub-Inhalt gemountet; Start-, Kategorie- und Grid-Pfade bleiben unverändert.

**Evidence:** `release/affiliate-zentrale/evidence/affiliate_router_v672174_af077_full_gate_20261002.md`; `release/affiliate-zentrale/evidence/affiliate_router_v672175_automatic_banner_full_gate_20261002.md`; `release/affiliate-zentrale/evidence/affiliate_router_v672176_hub_mount_ebay_payload_full_gate_20261002.md`. Targeted 6.72.176 WordPress/MariaDB simulation run `36997037385`; full gate run `36997283155`.

**Status:** FIXED_SOURCE_RELEASED_6_72_176 / REAL_WORDPRESS_LIVE_READBACK_OPEN.

## AFF-ERR-043 — eBay-BUSINESS-Produktkarten lieferten später verworfene Langbeschreibung im initialen HTML aus

**Datum / Arbeitsbindung:** 02.10.2026.

**Symptom:** Beim Laden einzelner eBay-Produktkarten war zunächst langer Beschreibungstext sichtbar; nach Abschluss des Design-Runtime-Aufbaus verschwand er wieder.

**Belegte Root Cause:** Die Affiliate-Zentrale renderte bei eBay-BUSINESS-Produkten in `category_product_1..3` / `hub_product_1..3` die Kampagnenbeschreibung vollständig in das initiale Karten-HTML. Das Portal-Design baut diese Produktkarten nach DOMContentLoaded aus Bild, Titel, Preis, Verkäufer und CTA neu auf und verwirft den Beschreibungstext. Damit wurde unnötiger HTML-/DOM-Payload ausgeliefert.

**Nicht wiederholen:** Datenquelle und Frontend-Payload trennen. Vollständige eBay-Quelldaten und PRIVATE-Detailbeschreibung bleiben erhalten; nur bei eBay-BUSINESS-Produktkarten in Hub-/Kategorie-Produktrastern darf die später verworfene Beschreibung bereits serverseitig aus dem Karten-HTML entfallen. Nicht-eBay-Karten bleiben unverändert.

**Positiv/Negativ:** 12k synthetische Langbeschreibung reduziert den getesteten Karten-Payload um ca. 12.074 Byte; Titel/Bild/Preis/Verkäufer/CTA bleiben erhalten. Nicht-eBay-Beschreibung bleibt erhalten. PRIVATE-eBay-Detailbeschreibung bleibt erhalten.

**Evidence:** `release/affiliate-zentrale/evidence/affiliate_router_v672176_hub_mount_ebay_payload_full_gate_20261002.md`; targeted WordPress/MariaDB simulation run `36997037385`; full gate run `36997283155`.

**Status:** FIXED_SOURCE_RELEASED_6_72_176 / REAL_WORDPRESS_LIVE_FLASH_PAYLOAD_READBACK_OPEN.



### AFF-ERR-042 – Live-Nachtrag 02.10.2026: 6.72.176 Schabracke weiterhin FAIL

**Live-Befund:** Nach Installation/Readback von 6.72.176 bleibt der Schabrackendesigner auf der realen Schabracken-Seite unsichtbar. Damit ist AFF-ERR-042 nicht geschlossen.

**Nachgeholter Testfehler:** Der grüne 6.72.175/176-Schabracken-Test verwendete ein synthetisches Designfixture, das den Slug `schabracken` fest als `hub2` klassifizierte. Das echte Designplugin klassifiziert aus der WordPress-Seitenhierarchie. `Ausrüstung -> Sattel -> Schabracken` ist strukturell `category`, nicht `hub2`.

**Realer Slotvertrag:** `hub1/hub2 -> hub_after_cards`; `category/leaf -> product_after_category_tiles`. Der echte Kategorie-Renderer besitzt den `product_after_category_tiles`-Mount bereits. Der 6.72.176-Hub-Mount ist damit für echte Hubseiten nicht widerlegt; falsch war die Schabracken-Abnahme auf einem künstlich erzwungenen Hubtyp.

**6.72.177 Kandidat:** ausschließlich ein admin-only, einmaliger, exakt auf `page:schabracken` begrenzter Replan bereits veröffentlichter Altmaterialisierung `hub_after_cards`, und nur wenn das echte Design den verknüpften realen Seitentyp als `category` oder `leaf` zurückliefert. Replan erfolgt ausschließlich über den bestehenden autoritativen `output_plan_creative()`-Pfad und gilt nur als erfolgreich, wenn danach ein veröffentlichter `product_after_category_tiles`-Output existiert.

**Performance-Hardlock:** eBay-`render_banner()` und alle geschützten Performance-/Runtime-Traits bleiben gegenüber 6.72.176 unverändert. Der vom Nutzer beobachtete Größenwechsel der eBay-Kachel ist kein aktueller Fixauftrag, solange keine messbare Performanceverschlechterung belegt ist.

**Evidence:** `release/affiliate-zentrale/evidence/affiliate_router_v672177_schabracken_real_hierarchy_rootfix_20261002.md`

**Status:** LIVE_FAIL_6_72_176 / TEST_FIXTURE_CONTEXT_MISMATCH_PROVEN / 6_72_177_LOCAL_CANDIDATE_PASS / EXACT_WORDPRESS_MARIADB_FULL_GATE_OPEN.


## AFF-ERR-044 — Relevanzreihenfolge konnte exakte Zielkante hinter breiterem Runtime-Treffer verlieren

**Datum / Arbeitsbindung:** 04.10.2026.

**Symptom:** Die verbindliche Bannerreihenfolge `exakt -> weiterer Themenkreis -> allgemeiner/technisch gültiger Fallback` war im zentralen Runtime-Ranking nicht durchgehend garantiert. Ein früher zurückgegebener URL-/Runtime-Thementreffer konnte eine später vorhandene exakte gespeicherte Zielkante abschneiden. Gleichzeitig waren einzelne Banner-Slot-Aliase, insbesondere `category_recommendation`, im zentralen Creative-Type-Gate nicht als Banner typisiert; dadurch war der letzte themenfreie Pflicht-Fallback nicht auf jeder Ebene gleich abgesichert.

**Root Cause:** Mehrere Relevanzquellen wurden in einer Reihenfolge mit frühen Returns ausgewertet, statt die bereits materialisierte exakte Zielkante zuerst als harte Themenstufe zu behandeln. Die technische Banner-Slotliste und die Banner-Distributionsliste waren außerdem nicht vollständig deckungsgleich.

**Nutzerentscheidung 04.10.2026:** Seiten, Kategorien, Beiträge und Glossar verwenden einheitlich: 1) exaktes Thema, 2) weiterer Themenkreis, 3) danach Thema egal, sofern Banner aktiv und technisch/slotseitig gültig ist. Für Pferderassen gilt kein künstlicher Themenzwang; technisch gültige Rassenbanner werden in einer gemeinsamen Relevanzstufe durch die bereits vorhandene stabile Partner-/Creative-Verteilung verteilt.

**Nicht wiederholen:** Keine neue Sonderlogik pro Seite/Kategorie/Provider. Eine zentrale Bannerreihenfolge; technisch ungültige Banner bleiben ausgeschlossen. Rassen nutzen die bestehende stabile Verteilung, keine zweite Verteilungsmaschine. 6.72.171-Performancepfade, Request-Caches, Providerlogik, eBay/Idealo/GTIN/Housekeeping und Renderer bleiben unverändert.

**POSITIV:** exakte gespeicherte Zielkante gewinnt auf Seite/Kategorie/Beitrag/Glossar vor breiterem URL-/Runtime-Thementreffer; breiter Themenkreis gewinnt vor themenfreiem Fallback; ohne Themenmatch bleibt ein technisch gültiger aktiver Banner lieferbar; `category_recommendation` und äquivalente Banner-Slots erhalten dieselbe Banner-Fallbacklogik.

**NEGATIV:** Produkt-Slots erhalten keinen Banner-Pflichtfallback; technisch falsches Format/Veto/inaktiv bleibt ausgeschlossen; Rassen-Themenbegriffe erzeugen keinen künstlichen Vorrang.

**PERFORMANCE:** keine Provider-/DB-/Remote-Abfrage im neuen Rassenweg; vorhandene request-lokale Ranking-/Kandidaten-Caches bleiben unangetastet.

**Status:** ROOTFIX_6_72_182_SOURCE_AND_INSTALLER_FULL_E2E_PASS / LIVE_READBACK_OPEN.


### 04.10.2026 – Vollständiger E2E-Nachweis / 6.72.181 superseded

Die frühere 6.72.181-Methodensimulation war als Abnahme unzureichend, weil Vorfilter vor dem Ranking nicht vollständig erfasst waren. Der vollständige WordPress+MariaDB-End-to-End-Gate reproduzierte zwei echte Root Causes: reale Slot-Aliase konnten den technischen Fallback vor dem Ranking verlieren; ein direkt passendes Banner-Placement konnte den technischen Formatvertrag umgehen.

6.72.182 führt den Bannerpfad auf dasselbe KISS-Prinzip wie den funktionierenden eBay/Idealo-Produktpfad zurück: Kandidaten -> technische Gültigkeit -> Relevanz -> Auswahl -> Renderer. Source-Gate Run 37216563071: 21/21 PASS. Installiertes ZIP-Gate Run 37216941150: 21/21 PASS, 27/27 Manifestidentität, Performance-Hardlock PASS. 6.72.181 ist damit superseded und darf nicht mehr als aktueller Installationskandidat verwendet werden.


## AFF-ERR-045 — Banner-Zielzuordnung hatte keine zentrale dauerhafte Ziel-URL-Wahrheit

**Datum:** 04.10.2026.

**Symptom:** Trotz lokaler Ranking-/Slot-Fixes änderte sich live sichtbar nichts zuverlässig. Die Tests konnten grün sein, obwohl reale Providerbanner ihre Zielzuordnung nicht dauerhaft aus einer einzigen Quelle erhielten.

**Root Cause:** Die Creative-Library besaß bereits `destination_url` und `topic_targets`, war aber nicht die alleinige Autorität. `topic_targets` konnte bei Assetprüfung wieder geleert werden; die Domain der Ziel-URL wurde in der Semantik nicht berücksichtigt; Tracking-Fallback konnte wie eine echte Zielseite behandelt werden; materialisierte Banner wurden im Frontend erneut aus URL/Text/Partnerdaten interpretiert.

**KISS-Fix 6.72.183:** Keine neue Tabelle. Die bestehende Creative-Library speichert einmal Ziel-URL-Provenienz, Portal-Zielkante und technisch kompatible Slots. Echte/decodierte Ziel-URL wird inklusive Domain einmal klassifiziert. Ohne eindeutiges Ziel entsteht ein allgemeiner technisch gültiger Fallback ohne Fake-Thema. Geänderte Ziel-URL leert die alte Kante und erzwingt Neuplanung. Output-Object-Banner lesen im Frontend nur noch die gespeicherte Kante; keine erneute URL-/Textklassifikation.

**Beweis Source:** Run 37219933282 = SUCCESS; alter Vollpfad 21/21 PASS; neue Library-Kette 26/26 PASS; Performance-Hardlock PASS.

**Beweis installiertes ZIP:** Run 37220236448 = SUCCESS; ZIP 27/27 manifestidentisch; alter Vollpfad 21/21 PASS; Library-Kette 26/26 PASS; Frontend 1000 Rank-Aufrufe mit 0 zusätzlichen DB-Queries und 0 HTTP.

**Installer:** `AFFILIATE_ZENTRALE_6.72.183.zip`, SHA-256 `3f689f076efc4318ed1188b86e51e66410f193d5256de7ddc54a91dc4aab6895`.

**Status:** SOURCE_AND_INSTALLED_ZIP_FULL_E2E_PASS / PERFORMANCE_PASS / LIVE_PRODUCTION_READBACK_OPEN.


## AFF-ERR-046 — Legacy-Automatik blieb parallel zur neuen Banner-Sammelstelle auslieferbar

**Datum:** 04.10.2026.

**Symptom:** Auf der realen Schabracken-Seite blieb unter 6.72.183 ein fachlich falscher SanoVet-Fütterungsbanner sichtbar, obwohl die neue Creative-Library-Zielzuordnung lokal grün getestet war.

**Root Cause:** 6.72.183 machte die Creative-Library nur für neu bzw. neu materialisierte Banner zur gespeicherten Ziel-URL-Wahrheit. Historische automatische Bannerkampagnen durften weiterhin parallel am Frontend-Ranking teilnehmen. Gleichzeitig fehlte ein gezielter Upgrade-Lauf, der den bereits vorhandenen aktiven Bannerbestand einmalig durch die neue Sammelstelle führt. Ein generischer Versions-Nachlauf hätte unnötig den gesamten Creative-Pool inklusive Produktzeilen erneut verarbeitet.

**KISS-Fix 6.72.184:** Für automatische Banner ist nur noch Creative-Library -> output_object_v4 autoritativ. Historische automatische Banner werden aus dem automatischen Pool ausgeschlossen; bestehende manuelle FIXED-Zuweisungen bleiben über ihren bisherigen Sonderpfad erhalten. Ein Banner-only-Migrationsworker verarbeitet ausschließlich aktive Banner aus der Creative-Library. Der generische Vollpool-Rescan wird für 6.72.184 nicht gestartet. eBay-/Idealo-/Produktkampagnen werden nicht neu geplant.

**Nicht wiederholen:** Nie zwei automatische Bannerquellen parallel zulassen. Neue Zuordnungsarchitektur muss auch den bestehenden Live-Bestand migrieren oder explizit sperren. Banner-only-Reparaturen dürfen keinen generischen Produkt-/Creative-Vollscan auslösen. Keine neue Frontend-DB-/HTTP-/URL-Neuklassifikation; Performance-Hotpaths bleiben geschützt.

**Beweis Source-Upgrade:** Run 37223477984 = SUCCESS; 6.72.183-Fehler reproduziert, Upgrade 6.72.184, Legacy-Automatik ausgeschlossen, Banner-only-Migration, korrekter Schabracken-Banner sichtbar, SanoVet nicht sichtbar, manuelle FIXED-Ausnahme erhalten, eBay/Idealo bytegleich, keine Remoteaufrufe; 20/20 PASS.

**Beweis installiertes ZIP:** Run 37223792210 = SUCCESS; Upgrade-Kette 20/20 PASS, frischer Library-Bannerpfad 21/21 PASS, Ziel-URL-Sammelstelle 26/26 PASS, ZIP 27/27 Manifest-Byteidentität, Performance-Hardlock PASS.

**Installer:** `AFFILIATE_ZENTRALE_6.72.184.zip`, SHA-256 `bc101bd7dc06aa3ecbf085165914440e28e0b7aaefe6786d1e7db33fc7f8fe06`.

**Status:** SOURCE_AND_INSTALLED_ZIP_FULL_E2E_PASS / LIVE_PRODUCTION_READBACK_OPEN. Noch kein Live-PASS für 6.72.184.


## AFF-ERR-047 — Gespeicherte falsche Creative-Library-Kante wurde bei Banner-Migration blind wiederverwendet

**Datum:** 04.10.2026.

**Live-Befund:** Nach dem ersten 6.72.184-Liveversuch blieb auf Schabracken der SanoVet-Fütterungsbanner sichtbar. Damit war der bisherige 6.72.184-Nachweis unvollständig und der alte Installer nicht abnahmefähig.

**Fehlender Gegenfall im alten Test:** Der frühere Upgrade-Test kannte einen Legacy-Banner außerhalb der Creative-Library und einen unmaterialisierten korrekten Library-Banner. Er enthielt aber keinen Banner, dessen echte Ziel-URL bereits auf Fütterung zeigt, während in der Creative-Library noch eine alte falsche Zielkante auf Schabracken gespeichert ist.

**Bewiesene Root Cause:** `output_banner_destination_classification()` verwendet eine vorhandene gespeicherte Library-Kante vor der erneuten Ziel-URL-Auswertung. Der 6.72.184-Banner-Migrationsworker rief deshalb den normalen Planner auf, ohne die alte automatische Kante vorher zu verwerfen. Eine falsche alte Kante konnte sich damit selbst bestätigen.

**NEGATIV-Beweis vor Fix:** WordPress 7.1.2 + MariaDB, Source-Run `37227361318` und ZIP-Run `37227361328`: echte Ziel-URL `/fuetterung-upgrade-e2e/`, gespeicherte Kante `Schabracken Upgrade E2E`. Der identische Upgrade-Gate wird gezielt ROT bei `POST_UPGRADE_stale_edge_recomputed_from_real_destination`. Performance-Hardlock bleibt PASS.

**KISS-Fix:** Nur im einmaligen Banner-only-Migrationsworker werden vor der bestehenden Planung die abgeleiteten automatischen Felder `topic_targets`, `topic_score` und `classified_at` für den jeweiligen aktiven Banner zurückgesetzt. Danach läuft unverändert der bestehende Ziel-URL-Klassifizierer und speichert die neue Kante. Manuelle Control-/FIXED-Entscheidungen liegen separat und bleiben erhalten. Keine Änderung am Frontend-Ranking, Renderer oder Performance-Hotpath.

**POSITIV-Beweis nach Fix:** Source-Run `37227561289` = SUCCESS, exakt derselbe vorher rote Zustand wird korrigiert: gespeicherte Kante wechselt von Schabracken auf Fütterung; 20/20 PASS; eBay und Idealo unverändert; FIXED-Ausnahme erhalten; 0 Remoteaufrufe. ZIP-Run `37227561276` = SUCCESS; 20/20 Upgrade, 21/21 kompletter Bannerpfad, 26/26 Ziel-URL-Sammelstelle, 27/27 Manifest-Byteidentität, PHP 21/21, Performance-Hardlock PASS.

**Neuer getesteter Installer:** `AFFILIATE_ZENTRALE_6.72.184.zip`, SHA-256 `46bcc02b2284fbbb0830b9f254d178f15ad0be072cbb3b40ee7fd658d4e1e437`, 793009 Bytes. Der frühere 6.72.184-Installer mit SHA `bc101bd7dc06aa3ecbf085165914440e28e0b7aaefe6786d1e7db33fc7f8fe06` ist superseded und darf nicht mehr installiert werden.

**Nicht wiederholen:** Eine Migrationsprüfung muss auch einen bereits falsch gespeicherten zentralen Zustand enthalten. Eine gespeicherte automatische Kante darf bei einer ausdrücklich angeordneten Re-Evaluation nicht ihre eigene Eingabe sein. Kein Frontend-Reklassifizieren als Ersatz.

**Status:** NEGATIVE_REPRODUCTION_PASS / FIXED_SOURCE_AND_ZIP_FULL_E2E_PASS / REAL_WORDPRESS_READBACK_OPEN.


## AFF-ERR-048 — Korrigierter Build trug dieselbe Versionsnummer 6.72.184

**Datum:** 05.10.2026.

**Fehler:** Nach dem stale-edge-Fix wurde zunächst erneut ein Installer mit Versionsnummer 6.72.184 erzeugt. Das ist für WordPress und für den einmaligen Migrationszustand nicht sauber unterscheidbar, wenn bereits eine andere 6.72.184 installiert wurde.

**Risiko:** Der alte 6.72.184-Migrationsstatus konnte bereits `done` sein. Ein korrigierter Build mit derselben Version und denselben State-/Hook-Schlüsseln wäre damit nicht zuverlässig als neuer Reparaturlauf erkennbar.

**Korrektur:** Eigene Version 6.72.185 plus eigene 6.72.185-Migrations-State-, Cursor-, Hook- und Result-Schlüssel. Die Fachlogik des bewiesenen stale-edge-Fixes bleibt unverändert.

**Negativ-/Positiv-Beweis:** Ausgangsbasis ist exakt der fehlerhafte erste 6.72.184-Installer SHA `bc101bd7dc06aa3ecbf085165914440e28e0b7aaefe6786d1e7db33fc7f8fe06`. Der Test setzt die alte 6.72.184-Migration bereits auf `done`, reproduziert den falschen SanoVet-Library-Banner auf Schabracken und führt anschließend das Upgrade auf 6.72.185 aus. Source-Run `37278423032`: 23/23 PASS. ZIP-Run `37278423041`: 23/23 Upgrade PASS, 21/21 Fresh-Banner PASS, 26/26 Ziel-URL-Library PASS, 27/27 Paketidentität, PHP 21/21, Performance-Hardlock PASS.

**Installer:** `AFFILIATE_ZENTRALE_6.72.185.zip`, SHA-256 `13fff3d67507d152e5368da9d7fc99028f8d26ad6d19338bb0cad1f44463fa28`, 793173 Bytes.

**Nicht wiederholen:** Zwei unterschiedliche installierbare Builds dürfen niemals dieselbe Versionsnummer tragen. Ein korrigierter einmaliger Migrationslauf benötigt eine neue Versions-/State-Generation.

**Status:** FIXED_SOURCE_AND_ZIP_FULL_E2E_PASS / REAL_WORDPRESS_READBACK_OPEN.


## AFF-ERR-049 — Bannerrotation durfte aus der besten Fachstufe in schwächere Fallbackstufen fallen

**Datum:** 05.10.2026.

**Realer Anlass:** Reithelme und Schabracken zeigten live wechselnde, fachlich falsche Banner. Ein früherer Einzel-Crawl war als Live-Oracle unzuverlässig; frische Read-only-Abrufe zeigten ebenfalls wechselnde reale Ausgaben. Entscheidend war deshalb der reproduzierbare Auswahlvertrag gegen den exakten bisherigen Installer.

**Bewiesener Kernfehler 6.72.185:** Bei einem exakten Banner plus mehreren allgemeinen Bannern war Position 1 exact, Position 2 fiel jedoch auf general. Die Rangliste hielt schwächere Relevanzstufen nach der Sortierung weiterhin ausgabefähig, und die zweite Positionsauswahl verlangte einen anderen Banner. Bei nur einem exact wurde daher unzulässig general/technical gewählt.

**Zusatzfehler Pferderassen:** Die historische themenneutrale Rassenregel lag vor der Auswertung einer bereits gespeicherten exakten Zielkante und konnte exact schon an Position 1 neutralisieren.

**NEGATIV-Beweis:** Exakter 6.72.185-Installer SHA `13fff3d67507d152e5368da9d7fc99028f8d26ad6d19338bb0cad1f44463fa28`. Fokussierter Run `37293474957`: Position 1 exact PASS, Position 2 general FAIL, 0 Frontend-HTTP. All-Context-Run `37293850326`: derselbe lower-tier escape auf Startseite, Hub, Kategorie/Produktseite, Kategoriearchiv, klassischen Beiträgen, Journal, Anzeigenmarkt/HivePress, Glossar und Rassen-Übersichten; Rassen-Einzelartikel zusätzlich mit exact-precedence-Fehler.

**KISS-Fix 6.72.186:** Nach dem bestehenden Ranking wird für Banner ausschließlich die beste vorhandene Relevanzstufe im Speicher behalten. Ein einzelner bester Banner bleibt fix; mehrere gleich beste Banner rotieren nur untereinander. Exakte gespeicherte Zielkanten werden bei Pferderassen vor der neutralen Rassenfallbackregel geprüft.

**Performance:** Keine neue DB-Abfrage, kein HTTP, keine Frontend-Ziel-URL-Auswertung. Geschützte Performancefunktionen einschließlich `banner_distribution_reorder_candidates`, `banner_distribution_stable_index` und `render_banner` bleiben gegenüber Baseline `a381aff4eb3f41754186f4bad86ce1a7e0823a29` körperidentisch.

**POSITIV Source:** Run `37295037827`: Universaltest 139/139 PASS, 0 Frontend-HTTP, alter Banner-Gesamttest 21/21 PASS, Ziel-URL-Library 26/26 PASS, Performance-Hardlock PASS.

**POSITIV exakte ZIP:** Run `37295977106`: exakte 6.72.185 zunächst ROT, dieselbe WordPress-Installation nach Upgrade auf gebaute 6.72.186 GRÜN; strict-tier 139/139 PASS; Fresh-ZIP 21/21 + 26/26 PASS; 27/27 Manifest-Byteidentität; PHP 21/21; Performance-Hardlock PASS.

**Installer:** `AFFILIATE_ZENTRALE_6.72.186.zip`, SHA-256 `1ca526ce92f339c678f2dc6e8775eae31355414668b8e06ed4afd561d5c15cae`, 793558 Bytes.

**Nicht wiederholen:** Rotation darf niemals eine schwächere Relevanzstufe betreten, solange mindestens ein Kandidat der besseren Stufe vorhanden ist. Ein einzelner best-tier-Banner bleibt fix. Eine Sonderregel für einen Contenttyp darf keine vorhandene exakte gespeicherte Zielkante neutralisieren.

**Status:** NEGATIVE_6_72_185_PROVEN / 6_72_186_SOURCE_AND_EXACT_ZIP_RED_GREEN_PASS / REAL_WORDPRESS_READBACK_OPEN.


## AFF-ERR-050 — 6.72.186 Best-Tier-Regel lokal grün, realer Live-Kandidatenbestand liefert trotzdem Guardian

**Datum:** 05.10.2026.

**Realer Live-Befund:** Nach Installation des exakt getesteten 6.72.186-Installers zeigt die reale Schabracken-Seite weiterhin einen fachlich falschen Banner, jetzt Guardian Horse. Frischer öffentlicher Read-only-Readback nach Installation liefert auf Reithelme und Schabracken jeweils Promo `185797`, mehrfach normal und mit Cache-Bust identisch.

**Live-Evidence:** Benutzer-Screenshot 05.10.2026 13:32 lokal; Probe-Commit `6d54e1fa622771a9effa9e106eef97af6407e9cb`; Run `37304066825`.

**Was dadurch widerlegt ist:** Der 6.72.186-Universaltest 139/139 beweist die Best-Tier-Auswahl nur für den kontrollierten Kandidaten-/Zielkantenbestand des Test-Fixtures. Er beweist NICHT, dass der reale WordPress-/Creative-Library-Bestand für Seite 186 Reithelme und Seite 193 Schabracken den fachlich richtigen Kandidaten mit der richtigen gespeicherten Zielkante überhaupt in die höchste Relevanzstufe einspeist.

**Noch nicht bewiesene Root Cause:** Es ist noch offen, ob der fachlich genaue Banner real fehlt/inaktiv/technisch ungeeignet ist, eine falsche bzw. fehlende `automation_target_keys`-Kante besitzt, durch Assignment/Placement/Control vor dem Ranking ausscheidet oder ob Promo `185797` im realen Bestand selbst fälschlich eine zu hohe Specificity erhält. NICHT RATEN.

**Verbindliche Diagnose vor jedem Fix:** Reale Kandidatenliste für Seite 186 und 193 read-only erfassen, einschließlich Campaign/Creative/Promo-ID, `active`, `source`, `assignment_mode`, `automation_target_keys`, `destination_url` samt Provenienz, `placements`, technische Slot-Eignung, `specificity`, Ranking-`reason` und tatsächlich ausgewählte Position. Reithelm-Creative `322674` ausdrücklich gegen den realen Bestand prüfen; ebenso jeden real vorhandenen Schabracken-spezifischen Banner.

**Performance-Hardlock:** Keine neue Frontend-DB-Abfrage, kein Frontend-HTTP, keine URL-Neuklassifikation beim Seitenaufruf, kein Vollscan im Hotpath. Diagnose read-only/außerhalb des öffentlichen Hotpaths. Geschützte Performancepfade bleiben unangetastet.

**Evidence:** `release/affiliate-zentrale/evidence/affiliate_router_v672186_live_fail_guardian_rootcause_open_20261005.md`

**Status:** LIVE_6_72_186_FAIL / ROOT_CAUSE_OPEN / NO_NEW_FIX_BEFORE_REAL_POOL_AND_RANK_DIAGNOSIS.

### AFF-ERR-050 – Nachtrag 05.10.2026: Root Cause bewiesen, 6.72.189 Source-Fix gebunden

**Nachweis:** Der reale Read-only-Kandidatenexport zeigte für Reithelme 186 und Schabracken 193 keine feste Assignment-Ursache. Der ADCELL-Banner 322674 war nur als allgemeiner Fallback materialisiert, weil zwar `promotionCategoryId=14727`, aber kein Kategoriename vorhanden war. Der zuerst angenommene API-Weg `getPromoCategories` wurde live widerlegt (HTTP 405, `undefined method`). Der reale ADCELL-Endpunkt `/affiliate/promotion/getPromotionCategories` wurde live erkannt; der exakte Validierungsfehler lautete `parameter "programId" is required`.

**Gebundener Source-Fix 6.72.189:** ausschließlich ADCELL-Kategorienvertrag auf `GET /affiliate/promotion/getPromotionCategories` mit skalarem `programId` korrigiert; eigener versionsspezifischer ADCELL-Themen-Resync, damit alte `done`-States den korrigierten Import nicht unterdrücken. Keine Ranking-, Frontend-Hotpath-, AWIN-, eBay-, Digistore24- oder Idealo-Änderung.

**Evidence:** `release/affiliate-zentrale/evidence/affiliate_router_v672189_adcell_category_contract_rootfix_20261005.md`.

**Autoritätshinweis:** Aktueller Status, erster Blocker und einzige NEXT ACTION stehen ausschließlich in `control/release-governance/CURRENT_RELEASE.json`. Dieser Nachtrag ist Fehlerhistorie/Nachweis, keine zweite Current-Wahrheit.

**Historischer Status ersetzt durch:** ROOT_CAUSE_PROVEN / 6_72_189_SOURCE_MANIFEST_AND_GOVERNANCE_GUARD_PASS / EXTERNAL_SUCCESS_RESPONSE_AND_RELEASE_GATES_OPEN.


### AFF-ERR-050 – Nachtrag 06.10.2026: 6.72.190 HARD-KISS-Zielkarte vollständig bewiesen

**Entscheidung:** Die Zwischenwege 6.72.189 mit Provider-Thema/Kategorienmetadaten wurden als unnötig verworfen. Verbindliche Regel für automatische Banner ist jetzt ausschließlich:

`Import -> Ziel-URL -> einmalige Zuordnung zu festen Portalzielen -> speichern`

Runtime liest nur noch die gespeicherte Zielkarte. Ohne gespeicherte Zielkarte keine Ausspielung. Provider-Themen-Vorrang und allgemeiner Banner-Fallback sind für diesen Weg verboten.

**Rootfix 6.72.190:** Zielkarten werden nach dem Importbatch einmalig aus der realen Ziel-URL erzeugt und in der bestehenden Creative-Library gespeichert. Keine neue Tabelle, keine neue Spalte, keine URL-Historie, kein Frontend-HTTP, keine neue Frontend-DB-Abfrage.

**POSITIV:** WordPress/MariaDB Run `37443761578` PASS; Final-R2 Run `37444152532` PASS. Reithelme und Schabracken werden als feste Ziele gespeichert; fehlende Zielkarte fail-closed; Wiederholung erzeugt weder zusätzliche Zielrecords noch Creative-Zeilen.

**Finaler Installer:** `AFFILIATE_ZENTRALE_6.72.190.zip`, SHA-256 `1a4939c91f60a7f526bc713f63719cb1cd3da88d575b7b2ec79cf063f530c1e3`.

**Evidence:** `release/affiliate-zentrale/evidence/affiliate_router_v672190_hard_kiss_banner_target_map_20261006.md`.

**Status:** SOURCE/WORDPRESS_MARIADB/FINAL_ZIP PASS / MANUAL_WORDPRESS_INSTALL OPEN. Aktueller Status und NEXT ACTION ausschließlich in `control/release-governance/CURRENT_RELEASE.json`.

### AFF-ERR-029 – Wiederholung 06.10.2026: freie NEXT-ACTION-Konstante erneut eingetragen und nachgeholt

**Befund:** Current Generation 221 verwendete `MANUAL_WORDPRESS_INSTALL_6_72_190` als `execution_state.authorized_next_action`.

**Negativbeweis:** Run `37444424717`, Schritt `Affiliate governance check`, brach mit `AFFILIATE_RELEASE_GUARD_BLOCKED:AUTHORIZED_NEXT_ACTION_INVALID` ab.

**Fix:** Current Generation 222 verwendet wieder guard-konform `RUN_BOUND_RELEASE_GATES`. Der konkrete eine Arbeitsschritt bleibt ausschließlich in `bound_user_scope_action`: exakten 6.72.190-Installer manuell in WordPress installieren und den einmaligen versionsgebundenen Zielkarten-Nachlauf zulassen.

**Nicht wiederholen:** Keine freie Fachaktion in `authorized_next_action` eintragen. Konkrete Fachaktion ausschließlich unter dem guard-konformen Zustandswert binden.

**POSITIV:** Run `37445573248`, Schritt `Affiliate governance check`: PASS auf Current Generation 222. Der spätere Workflow-Fail entsteht erst beim fremden PSTE-0.57.6-Artefakt und ist kein Affiliate-Governance-Fail.

**Status:** CLOSED / NACHGEHOLT / GOVERNANCE PASS.


## AFF-ERR-051 — Tarifcheck zunächst gegen erfundenen Kosten-Root statt realen Kategoriebaum gedacht

**Datum:** 06.10.2026.

**Fehler:** Der erste 6.72.191-Ansatz behandelte „Kosten“ sinngemäß wie einen gemeinsamen Kategorieast. Die reale Portalstruktur besitzt jedoch keinen solchen Kosten-Root. Kosten sind verteilte Blattkategorien unter mehreren Hauptbereichen.

**Harter Baum-Nachweis:** `ebay-portal-catalog-v2.json` enthält 67 konfigurierte Kosten-Einträge mit 67 Slugs und 66 eindeutigen Pfaden. Die Blätter liegen unter Ausrüstung, Fütterung, Stall, Transport, Weide und Wissen. Ein Weidezaungeräte-Pfad ist im Katalog doppelt mit zwei Slugs vorhanden.

**Rootfix:** Tarifcheck-Kredit wird nach eindeutiger Ziel-URL-Prüfung auf die gesamte real vorhandene Kosten-Zielmenge gebunden. Ein echtes Kostenblatt muss `Kosten …` heißen und einen `…-kosten`-Slug besitzen. Es wird eine Kampagne mit mehreren festen Zielschlüsseln gespeichert, keine Bannerkopie je Kategorie.

**Versicherung:** Analog ausschließlich alle 14 echten Blattkategorien im Ast `Wissen > Versicherungen & Recht`. Ein zusätzlicher realer Test deckte auf, dass WordPress den Pfad als `Versicherungen &amp; Recht` liefert; die Pfadprüfung dekodiert HTML-Entities vor der Entscheidung.

**POSITIV Source:** Run `37450657203` = SUCCESS. Kredit 66/66 eindeutige Kostenpfade PASS; Versicherung 14/14 PASS; Kreuzsperren PASS; URL schlägt irreführenden Titel PASS; unbekannt/gemischt fail-closed PASS; Runtime-Zielmengen 66 und 14 PASS; keine neue Tabelle.

**POSITIV exaktes ZIP:** Run `37450856670` = SUCCESS. Fresh-Unpack 27/27 Byteidentität, PHP 21/21, exaktes ZIP frisch in WordPress/MariaDB installiert, kompletter Tarifcheck Positiv-/Negativtest PASS.

**Finaler Installer:** `AFFILIATE_ZENTRALE_6.72.191.zip`, SHA-256 `0987dec5826be39b99fc05a993a64149acf017445ecde0577dc3f975a13f9f5e`, 800276 Byte.

**Evidence:** `release/affiliate-zentrale/evidence/affiliate_router_v672191_tarifcheck_direct_code_kiss_20261006.md`.

**Status:** ROOT_CAUSE_FIXED / SOURCE_AND_EXACT_ZIP_WORDPRESS_MARIADB_PASS / MANUAL_LIVE_INSTALL_OPEN.


## AFF-ERR-052 — Tarifcheck-HTML-Banner wurden in 6.72.191 vor der technischen Bildprüfung zugeordnet

**Datum:** 06.10.2026.

**Fehler:** 6.72.191 konnte nach dem manuellen HTML-Code-Import bereits eine feste Zielkarte speichern, obwohl die reale Bannerbildprüfung erst danach im vorhandenen Prüfbatch lief. Damit war die Reihenfolge nicht streng `prüfen -> zuordnen`.

**Rootfix 6.72.192:** Direkt-/Manuellbanner, insbesondere Tarifcheck, bleiben bis zur erfolgreichen realen Bildprüfung ohne Zielkarte. Der Import ermittelt die echte Ziel-URL, speichert den Banner zunächst pending und lädt die betroffenen Banner einmal gebündelt. Erst der bestehende technische Prüfer baut nach erfolgreicher Bildprüfung die feste Zielkarte. Bei Bildfehler wird eine eventuell vorhandene Zielkarte geleert und der Banner blockiert.

**Fachregel:** Kredit -> alle realen Kosten-Blätter; Versicherung -> alle 14 realen Versicherungsblätter; unbekannt/gemischt -> keine Zielkarte. URL schlägt Titel.

**POSITIV Source:** Run `37454893550` SUCCESS. Vor Prüfung 0 Ziele, danach Kredit 66/66 und Versicherung 14/14; kaputtes Bild bleibt ohne Ziel; unbekannt/gemischt fail-closed; keine neue Tabelle.

**POSITIV exaktes ZIP:** Run `37455039161` SUCCESS. Fresh-Unpack 27/27, PHP 21/21, frische WordPress/MariaDB-Installation, kompletter Verify-Before-Assign-Test PASS.

**Finaler Installer:** `AFFILIATE_ZENTRALE_6.72.192.zip`, SHA-256 `49add47f6876e78737704b3ca067bf5d931ee68a5f7448f99d8227ee57fc60d9`, 801146 Byte.

**Status:** FIXED / SOURCE_AND_EXACT_ZIP_WORDPRESS_MARIADB_PASS / MANUAL_LIVE_INSTALL_OPEN.


## AFF-ERR-053 — 6.72.193 live: Schabracken weiter falsch + Tarifcheck nicht auswählbar

**Datum:** 06.10.2026.

**Live-Befund:** Nutzer hat 6.72.193 real installiert. Schabracken ist weiterhin fachlich falsch. Zusätzlich ist Tarifcheck im Werbemittel-Sammelimport unter **„Aufgenommener Partner“** nicht auswählbar.

**Bewiesene UI-Ursache Tarifcheck:** `creative_library_snapshots_for_select()` enthielt keinen Tarifcheck-Snapshot. Der vorhandene Hinweis, Provider „Direktpartner“ und Partnername „Tarifcheck“ händisch einzutragen, war nur ein Workaround und keine fertige Integration.

**Bewiesene Persistenzlücken für den Schabracken-Fehler:**
1. Der 6.72.190-Resync baut bestehende lokale Banner-Zielkarten nicht direkt neu; er startet nur die ADCELL-Programmsynchronisierung.
2. Der vorhandene Kampagnen-Finder suchte nur nach dem alten Metakey `ppar_library_identity_hash`, während aktuelle Output-Object-Kampagnen `_ppar_creative_identity_hash` speichern. Damit konnten aktuelle alte Auto-Kampagnen vom Bereinigungsweg übersehen werden.
3. Der frühere direkte Banner-Migrationsweg aus 6.72.185 war versionshart auf 6.72.185 begrenzt und läuft unter 6.72.193 nicht.

**Rootfix 6.72.194:**
- Tarifcheck als echter auswählbarer Directpartner-Preset;
- aktueller + Legacy-Campaign-Metakey werden erkannt;
- einmaliger admin-/background-only lokaler Neuaufbau aller aktiven Banner-Zielkarten aus der bereits gespeicherten `destination_url`;
- alte automatische `output_object_v4`-Kampagnen vor Neubindung fail-closed deaktivieren;
- ohne sichere neue Zielkarte keine Reaktivierung;
- manuelle/FIXED Kampagnen bleiben unangetastet;
- keine Provider-HTTP-Aufrufe, kein Frontend-Scan, keine neue Tabelle/Spalte, kein Produktpool-Rebuild.

**POSITIV Source:** Run `37480297999` SUCCESS. Exakt reproduzierter stale-edge Fall Fütterung -> Schabracken wird korrigiert; unbekannte URL bleibt ohne aktive Auto-Kampagne; manuelle Kampagne bleibt aktiv; Tarifcheck-Preset vorhanden.

**POSITIV exaktes ZIP:** Run `37480911019` SUCCESS. Fresh-Unpack 28/28, PHP 22/22, exaktes ZIP in WordPress/MariaDB, stale-edge-Test PASS, Tarifcheck-Preset PASS, 6.72.193 Tarifrechner-Regression PASS, 6.72.192 Tarifcheck-Bannervertrag PASS.

**Finaler Installer:** `AFFILIATE_ZENTRALE_6.72.194.zip`, SHA-256 `36efb30086ece987cf9a55e3ab24cb85073343b67b5f6b1b761055a0fab08d04`, 807040 Byte.

**Status:** SOURCE_AND_EXACT_ZIP_FIXED / LIVE_INSTALL_AND_SCHABRACKEN_READBACK_OPEN.

**Evidence:** `release/affiliate-zentrale/evidence/affiliate_router_v672194_live_schabracken_tarifcheck_preset_20261006.md`.


### AFF-ERR-050 – Nachtrag 06.10.2026: 6.72.195 deterministischer Reconcile + Tarifcheck-Gruppen, exakter Installer PASS

**Ausgangslage:** 6.72.194 blieb live bei Schabracken falsch. Zusätzlich waren manuell importierte Tarifcheck-Banner ohne ausdrücklich gespeicherte Fachgruppe bei Tracking-only-Links nicht sicher Kategorien zuordenbar.

**Struktureller Fix 6.72.195:** Alle aktiven automatisch erzeugten `output_object_v4`-Banner mit `auto_verified` werden vor dem Neuaufbau global deaktiviert, ohne Abhängigkeit von historischen Creative-Metakeys. Danach werden automatische Banner ausschließlich aus den aktuellen Creative-Library-`topic_targets` neu materialisiert. Manuelle/FIXED Banner und Produktkampagnen bleiben erhalten.

**Tarifcheck:** Bestehende oder neue Tarifcheck-Banner können ausdrücklich als `Versicherungen` oder `Kreditvergleich / Kosten` gruppiert werden. Diese bewusste Gruppe wird gespeichert und ist autoritativ. Ohne explizite Gruppe und ohne sicher erkennbare reale Ziel-URL bleibt der Banner fail-closed unsichtbar.

**Source WordPress/MariaDB:** Run `37489630643` PASS.

**Exakter Installer:** Run `37490868184` PASS:
- Fresh-Unpack / Source-Byteidentität 28/28;
- PHP-Lint 22/22;
- exaktes ZIP in frischem WordPress 7.1.2 + MariaDB 10.11 installiert;
- stale unverbundener Fütterungs-Auto-Banner deaktiviert;
- Schabracken korrekt neu materialisiert;
- Tarifcheck Kosten ausschließlich Kosten-Kategorien;
- Tarifcheck Versicherungen ausschließlich Versicherungs-Kategorien;
- unbekannter Tracking-only-Tarifcheck ohne Gruppe fail-closed;
- manuelle Banner und Produktkampagnen unverändert.

**Installer:** `AFFILIATE_ZENTRALE_6.72.195.zip`, SHA-256 `8594193622dd6e4af55128da3279e1c1623ae1188f43b1c4fa6ca4008c608ccf`, 809869 Byte.

**Status:** SOURCE_AND_EXACT_ZIP_PASS / LIVE_INSTALL_AND_READBACK_OPEN. AFF-ERR-050 bleibt offen, bis Schabracken sowie beide Tarifcheck-Gruppen real live bestätigt sind.

## AFF-ERR-054 — 6.72.195–6.72.198 reparierten nachgelagerte Bannerlogik, obwohl die ADCELL-Importbasis verlustbehaftet blieb

**Datum:** 07.10.2026.

**Realer Anlass / LIVE:** Nach der lokal vollständig grünen 6.72.198 wurde die Version real installiert; die WordPress-Pluginliste bestätigte `Affiliate-Zentrale (Portal-kompatibel) Version 6.72.198`. Der Nutzer meldete danach auf Schabracken weiterhin **kein Banner**. Damit ist der lokale 6.72.198-Fixture-PASS kein Live-PASS.

**Belegter Basisfehler im Sourcepfad vor 6.72.199:** `automation_adcell_banner_rows()` übernahm nur ausgewählte ADCELL-Felder und erzeugte bei fehlendem Providertitel selbst einen semantisch wirkenden Titel nach dem Muster `<Partner> Banner <ID> – <Kategorie>`. Beispiel aus dem untersuchten Pfad: `procavallo Banner 393923 – Ausrüstung`. Verschachtelte oder unbekannte Originalfelder des Provider-Bannerobjekts wurden nicht vollständig bis in die Creative Library konserviert. Damit arbeitete jede nachgelagerte Klassifikation auf einer potenziell beschnittenen und teilweise synthetischen Datenbasis.

**Warum die vorherigen Versuche nicht als Basislösung gelten:**
- **6.72.195:** globaler deterministischer Reconcile beseitigte stale Auto-Kampagnen und baute aus vorhandenen Zielkarten neu auf; er reparierte nicht die Qualität/Vollständigkeit der importierten Providerbasis.
- **6.72.196:** Tarifcheck wurde im Dropdown hart gebunden; das betrifft UI/Erreichbarkeit, nicht den ADCELL-Banner-Rohdatenvertrag.
- **6.72.197:** manuelle FIXED-Zielzuordnung wurde robust gemacht. Der Nutzer lehnte dies zu Recht als Systemlösung für automatische Banner ab; es ist nur ein manueller Ausnahmeweg.
- **6.72.198:** allgemeine Klassifikation wurde verbessert und Run `37501160643` bestand WordPress/MariaDB, Fresh-Unpack, Tarifcheck-Dropdown sowie positive/negative Banner-Fixtures. Diese Tests erzeugten jedoch kontrollierte Testdaten und bewiesen nicht, dass der reale ADCELL-Import alle tatsächlich verfügbaren Providerinformationen verlustfrei in dieselbe Entscheidungsbasis einspeist.

**Weitere Fehlversuche / falsche Diagnoserichtungen in diesem Chat:**
- Die Existenz einer historischen Root-Kopie der Affiliate-Zentrale wurde zunächst als mögliche Live-Ursache überbewertet. Die reale WordPress-Pluginliste belegte anschließend Version 6.72.198 aktiv; diese Hypothese ist als Live-Ursache nicht belegt.
- PHP-OPcache/IONOS/Server wurde ohne belastbare Evidence als mögliche Erklärung genannt. Dieser Verdacht ist **nicht belegt** und darf nicht als Ursache weitergetragen werden.
- Der Nutzer wurde unnötig zum WordPress-Plugin-Datei-Editor geschickt, obwohl die betreffende Source selbst geprüft werden konnte.
- „Tarifrechner“/„Tarifcheck im Dropdown“ wurde zeitweise falsch als WordPress-Menüpunkt interpretiert. Diese Interpretation war falsch.
- Ein Read-only-Workflow wurde durch eine Änderung unter `.github/workflows/` zu triggern versucht. Die Änderung war für den gebundenen Affiliate-Arbeitsweg ein unzulässiger Nebenschritt; sie wurde am 07.10.2026 wieder zurückgenommen. Die damaligen Läufe lieferten keinen verwendbaren Live-Nachweis.

**Gebundene Zielkorrektur:** `protocol/AFFILIATE_RELEASE_BANNER_IMPORT_BASIS_TARGET_20261007.md`. Erst vollständige, integritätsgebundene Provider-Rohdatenbasis beweisen; danach Zuordnungslogik. Ziel-URL bleibt belastbare Evidenz, aber nicht exklusiv. Runtime bleibt gespeicherte-Zielkarte-only.

**Aktueller Source-Delta 6.72.199 — NO PASS:** Im kanonischen Tree ist bereits ein 6.72.199-Arbeitsstand committed:
- vollständiges ADCELL-Bannerobjekt als kanonisches JSON + SHA-256 mitführen/speichern;
- `promotionCategoryId` über den belegten `getPromotionCategories(programId)`-Weg zum Kategorienamen auflösen;
- nur echte Provider-Titelfelder verwenden; fehlender Titel bleibt als `provider_missing` gekennzeichnet;
- Altbestand erst durch frischen echten ADCELL-Import ersetzen und erst danach reconciliieren;
- neue Basis-/Upgrade-Tests liegen unter `release/affiliate-zentrale/evidence/worktests/`.

**HARD STATUS:** Diese 6.72.199-Testdateien sind committed, aber am aktuellen Head existiert **kein ausgeführter Check-Run/PASS-Nachweis**. `CURRENT_SOURCE_SHA256.txt` und `CURRENT_RELEASE.json` waren beim Frischecheck noch auf 6.72.198 gebunden. Deshalb: **6.72.199 = WORKING / NICHT ABGENOMMEN / KEIN INSTALLER / NICHT LIVE INSTALLIEREN.**

**Nicht wiederholen:** Kein weiterer Ranking-, Target-, Reconcile-, UI-, Server- oder Einzelbanner-Fix, bevor die Importbasis sourcegebunden und im echten WordPress/MariaDB-Basis-E2E positiv und negativ bestanden ist.

**Status:** OPEN / FIRST_BLOCKER_SOURCE_BINDING_AND_BASIS_GATE.


### AFF-ERR-029 – Wiederholung 07.10.2026: freie NEXT-ACTION-Konstante in Current Generation 238 erneut verwendet

**Befund:** `control/release-governance/CURRENT_RELEASE.json` Generation 238 enthält als `execution_state.authorized_next_action` den freien Wert `MANUAL_INSTALL_6_72_198_THEN_OPEN_BACKEND_AND_READBACK_MULTIPLE_REAL_BANNERS`.

**Belegter Governance-Vertrag:** `release_guard.py` akzeptiert dort ausschließlich `COMMIT_EXACT_V6638_21_FILE_SOURCE_TO_CANONICAL_ROOT`, `RUN_BOUND_RELEASE_GATES` oder `FINALIZE_RELEASE`. Der Fehler war bereits am 06.10. unter AFF-ERR-029 dokumentiert und wurde trotzdem wieder eingeführt.

**Korrekturregel:** Current muss für den offenen Arbeitsblock wieder `RUN_BOUND_RELEASE_GATES` verwenden. Die konkrete Fachaktion steht ausschließlich in `bound_user_scope_action`.

**Status:** REPEATED / CURRENT_CORRECTION_REQUIRED.

### AFF-ERR-054 – Nachholung 07.10.2026: Source-/Current-Bindung hergestellt, Basis-Gate bleibt offen

Der 6.72.199-Arbeitsstand wurde nach dem Frischecheck technisch nachgezogen:

- `CURRENT_SOURCE_SHA256.txt` für den exakten aktuellen 28-Dateien-Pluginbaum regeneriert;
- Manifest-SHA-256: `b39aa305d31aa4391e6c258e339504a9b4eb890c71c37299ba46c962ca90f550`;
- `CURRENT_RELEASE.json` auf Generation 240 / Active Candidate 6.72.199 / `release_allowed=false` aktualisiert;
- `authorized_next_action` wieder guard-konform auf `RUN_BOUND_RELEASE_GATES` gesetzt;
- die drei noch **nicht ausgeführten** 6.72.199-Basis-Worktests liegen im erlaubten Evidence-Worktest-Pfad;
- der unerlaubte temporäre Kommentar in `.github/workflows/tmp-affiliate-live-schabracken-readonly.yml` wurde zurückgenommen; gegenüber dem letzten gebundenen 6.72.198-Stand bleibt dort kein Delta.

**Noch offen:** Release-Guard tatsächlich ausführen; anschließend die drei 6.72.199-Basis-Worktests in WordPress/MariaDB. Bis dahin kein PASS, kein ZIP, keine Live-Installation.

**Status:** OPEN / SOURCE_MANIFEST_AND_CURRENT_SYNCED / GUARD_AND_BASIS_TESTS_OPEN.


### AFF-ERR-029 – Nachholung 07.10.2026

Current Generation 240 verwendet wieder den zulässigen Zustand `RUN_BOUND_RELEASE_GATES`. Die konkrete Fachaktion steht ausschließlich in `bound_user_scope_action`.

**Status:** CLOSED / NACHGEHOLT.



## AFF-ERR-055 — 6.72.199 Basis-Worktests vorhanden, aber kein zulässiger versionsneutraler WordPress/MariaDB-Ausführungsweg

**Datum:** 07.10.2026.

**Befund:** Der exakt gebundene 6.72.199-Source-Stand besteht die Release-Governance und Source-Bindung. Für die vier aktuellen Worktests existiert im Repository jedoch kein versionsneutraler Affiliate-Runner, der den aktuellen Source-Tree in WordPress/MariaDB installiert und Dateien aus `release/affiliate-zentrale/evidence/worktests/` ausführt.

**Belegte Guards am final gebundenen Stand:** Current Generation 243 / Manifest SHA-256 `0f1c3f467d43ef742795929e02f82d3c64aec05c483bdb13bd6127b6179dbbff`.
- Run `37595536094`: Schritt `Affiliate governance check` PASS. Dieser Schritt führt `governance-check` und `start --branch affiliate-release-current` aus; `start` enthält erneut Source-Check.
- Run `37595536117`: `source-check` gibt `AFFILIATE_RELEASE_SOURCE_PASS` aus. Der Workflow stoppt erst anschließend an seiner historischen festen Prüfung `Version: 6.72.170`.
- Run `37595536101`: vorhandener Gesamt-Release-Workflow ist ebenfalls historisch auf 6.72.171 gebunden und stoppt vor seinen WordPress/MariaDB-Schritten.

**Vollständige Runner-Prüfung:** Die vorhandenen Affiliate-Workflows auf `affiliate-release-current` wurden gegen ihre Trigger und ersten Ausführungsschritte geprüft. Die WordPress/MariaDB-Läufe sind versionsspezifisch auf historische Kandidaten 6.72.170–6.72.198 gebunden. Auf `main` existiert kein zusätzlicher generischer Affiliate-Worktest-Runner. Es existiert auch kein Issue-/PR-/repository_dispatch- oder workflow_call-Weg, der die vier aktuellen Worktests versionsneutral übernimmt.

**Warum kein Workaround gebaut wird:** Eine Änderung unter `.github/workflows/**` ist im aktuell gebundenen Affiliate-Arbeitsweg ausdrücklich verboten. Genau ein solcher Trigger-Nebenschritt wurde bereits als Fehler dokumentiert und zurückgenommen. Alte Versionsprüfungen durch Fake-Kommentare, Versionsstrings oder andere Umgehungen zu täuschen wäre kein belastbarer Test und ist verboten.

**Offene vier Pflicht-Worktests:**
- `release/affiliate-zentrale/evidence/worktests/test_adcell_banner_import_basis_v672199.php`
- `release/affiliate-zentrale/evidence/worktests/test_adcell_banner_import_basis_e2e_v672199.php`
- `release/affiliate-zentrale/evidence/worktests/test_adcell_banner_basis_upgrade_v672199_e2e.php`
- `release/affiliate-zentrale/evidence/worktests/test_direct_partner_manual_banner_v672199_e2e.php`

**Status:** FIRST_REAL_BLOCKER / GUARDS_PASS / WORDPRESS_MARIADB_EXECUTION_PATH_MISSING / NO_ZIP / NO_RELEASE.


### AFF-ERR-055 – Nachtrag 07.10.2026: versionsneutraler Worktest-Runner jetzt vorhanden

**Korrektur des Blockers:** Der Teil „kein zulässiger versionsneutraler Runner vorhanden“ ist nach weiterer Arbeit nicht mehr aktuell. Unter dem erlaubten Worktest-Bereich existiert jetzt:

`release/affiliate-zentrale/evidence/worktests/run_banner_import_basis_v672199.sh`

Der Runner:
- verlangt exakt Branch `affiliate-release-current`;
- führt `governance-check`, `source-check` und `start` aus;
- lintet alle vier 6.72.199-Pflichttests;
- führt den statischen Basisvertrag aus;
- prüft im WordPress-Harness die aktive Pluginversion 6.72.199;
- vergleicht den installierten Pluginbaum bytegenau mit allen 28 Manifestdateien;
- führt anschließend die drei WordPress/MariaDB-E2E-Tests nacheinander aus und stoppt beim ersten Fehler.

Der Directpartner-Test wurde zugleich gehärtet: CHECK24 wird nicht mehr nur als Dropdown-/Speicherfall geprüft. Er beweist nun denselben Verify-before-Assign-Vertrag wie Tarifcheck: vor technischer Bildprüfung 0 Ziele; nach erfolgreicher Prüfung 66 reale Kostenpfade bzw. 14 echte Versicherungsblätter; kaputtes Bild bleibt fail-closed ohne Ziel; Runtime liest ausschließlich die gespeicherten CHECK24-Zielkarten.

Der statische ADCELL-Basistest bindet zusätzlich den Frontend-Hardlock: neuer Basisnachlauf admin-/workergebunden; Output-Runtime ohne direkten Provider-HTTP; Ziel-URL-Auflösung nur in Import-/Background-Kontexten.

**Verbleibender erster Blocker:** Es fehlt weiterhin der reale Lauf dieses Runners in einer WordPress/MariaDB-Umgebung. Der aktuell verfügbare lokale Ausführungscontainer besitzt weder MariaDB/Docker noch WordPress/WP-CLI und hat keinen GitHub-Netzzugriff; die bestehenden GitHub-Actions bleiben versionshart historisch gebunden. Daher weiterhin **kein PASS**, kein ZIP und keine Live-Installation.

**Status:** RUNNER_PREPARED / TEST_CONTRACT_HARDENED / REAL_WORDPRESS_MARIADB_EXECUTION_HOST_OPEN / NO_RELEASE.


### AFF-ERR-054 – Nachtrag 07.10.2026: Verify-before-Assign-Reihenfolge war in 6.72.199 noch nicht global

**Frischer Quellbefund:** Trotz vollständigerer Providerbasis war die im neuen Zielvertrag festgelegte Reihenfolge noch nicht überall umgesetzt. Drei reale Pfade konnten eine feste Banner-Zielkarte erzeugen, bevor die technische Bildprüfung abgeschlossen war:

1. `automation_import_rows()` konnte nach dem automatischen Providerimport sofort `output_assign_banner_targets_from_destination_once()` aufrufen.
2. `run_v672195_banner_reconcile()`, der vom 6.72.199-Basisnachlauf wiederverwendet wird, baute die Zielkarte vor der Prüfung von `_dimension_state`, Breite und Höhe.
3. Die manuelle Tarifcheck/CHECK24-Gruppenaktion konnte nach Setzen von Kosten/Versicherung ebenfalls sofort Zielkarten erzeugen.

Damit war der Zielvertrag **„Providerbasis → Ziel-URL-Provenienz → technische Assetprüfung → erst danach Zielzuordnung“** noch nicht vollständig erfüllt.

**6.72.199-Korrektur:**
- `creative_library_verify_before_assign_banner()` gilt jetzt für **jeden Banner**, nicht nur Direkt-/Manuellbanner.
- Automatikimport erzeugt für pending/unverifizierte Banner keine Zielkarte; verifiziert bedeutet Zustand `verified|mismatch` **und** reale Breite/Höhe > 0.
- Der globale Reconcile prüft die Asset-Evidence vor jeder Zielzuordnung.
- Der 6.72.199-Upgradezustand besitzt jetzt `waiting_assets -> ready_reconcile -> reconciling` und wartet nach dem frischen Providerlauf auf die technische Assetprüfung.
- Manuelle Tarifcheck/CHECK24-Familienwahl speichert die Familie, erzeugt aber bei pending Asset noch keine Zielkarte.
- Terminal fehlgeschlagene Bilder werden aus den Pending-Schleifen ausgeschlossen und bleiben fail-closed.

**Testhärtung:**
- ADCELL-Basis-E2E: reales Schabracken-Ziel vorhanden, trotzdem **0 Ziele vor Bildprüfung**; nach erfolgreicher Bildprüfung erst exaktes Schabracken-Ziel aus Provider-Kategorie.
- Upgrade-E2E: frischer Providerjob -> `waiting_assets` -> reale Bildbytes/Assetprüfung -> erst danach Reconcile/`done`.
- CHECK24-E2E: 0 Ziele vor Prüfung; danach 66 Kostenpfade bzw. 14 Versicherungsblätter; kaputtes Bild ohne Ziel.
- Statischer Basisvertrag sperrt alle drei Umgehungswege und Frontend-Provider-HTTP.
- Provider-Rohdatenprüfung wurde auf vollständige Wert-/Typgleichheit inklusive unbekannter verschachtelter Felder gehärtet.

**Noch kein PASS:** Die korrigierte Source muss nach neuer Manifestbindung erneut durch Governance/Source/Start und danach durch den realen WordPress/MariaDB-Runner. Kein Installer vorher.

**Status:** ROOT_CAUSE_DEEPENED / VERIFY_BEFORE_ASSIGN_SOURCE_FIXED / MANIFEST_REBOUND / GUARDS_AND_REAL_DB_GATE_OPEN.


### AFF-ERR-054 – Nachtrag 07.10.2026: Fixture-Beweis reicht nicht, echter ADCELL-Gate gebunden

**Zielvertragsprüfung:** Der Basisvertrag verbietet ausdrücklich, eine lokale Fixture-Abnahme als Beweis für reale Providerdaten zu verwenden. Die bisherigen 6.72.199-E2E-Fixtures beweisen Mechanik, Fail-closed-Verhalten und WordPress/MariaDB-Persistenz, aber nicht, dass ein tatsächlich von ADCELL gelieferter Banner vollständig durch denselben Weg läuft.

**Korrektur:** Neuer Pflichtgate:
`release/affiliate-zentrale/evidence/worktests/test_adcell_banner_import_basis_real_provider_v672199.php`

Er ist absichtlich nur für einen isolierten WordPress/MariaDB-Testhost bestimmt und:
- verweigert die Ausführung auf `pferde-atelier.de`;
- benötigt explizit `PPAR_REAL_PROVIDER_GATE=1`;
- nimmt ADCELL-Benutzer/Passwort und Programm-IDs ausschließlich aus Umgebungsvariablen;
- ruft den echten ADCELL-Programm-/Bannerweg ohne HTTP-Fixture auf;
- vergleicht das vom API-Adapter gelieferte reale Bannerobjekt wert- und typgleich mit dem als Roh-JSON gebundenen Objekt plus SHA-256;
- importiert genau diesen echten Banner über den normalen Creative-Library-Weg;
- prüft Kategorie-ID/-Name, echte Titelherkunft, Tracking-/Ziel-URL-Provenienz und 0 Zielkarten vor Assetprüfung;
- lädt die reale Bildquelle und prüft echte Maße, Bildbytes und SHA;
- kapselt Testdaten und Zugangsdaten in einer DB-Transaktion und rollt sie zurück.

Der versionsneutrale Sammelrunner verlangt diesen realen Provider-Gate jetzt zwingend als **5. Test**. Ohne echte Credentials/Programm-IDs gibt es absichtlich kein Gesamt-PASS.

**Zusatzkorrektur Retry:** Ein innerhalb eines Laufs fehlgeschlagenes Bild bleibt terminal fail-closed. Ein späterer echter Provider-Reimport desselben unveränderten Banners setzt ausschließlich die technische Asset-Evidence erneut auf `pending`, damit ein temporärer Bildfehler nicht dauerhaft festgeschrieben wird. Erfolgreich verifizierte identische Assets werden weiterhin wiederverwendet.

**Status:** REAL_PROVIDER_GATE_REQUIRED / FIXTURE_ONLY_PASS_FORBIDDEN / FAILED_ASSET_REIMPORT_RETRY_FIXED / GUARDS_OPEN.


### AFF-ERR-055 – Abschlussnachtrag 07.10.2026: Ausführungsweg geschlossen

Der frühere Runner-/WordPress-/MariaDB-Blocker ist **geschlossen**.

Beleg:
- Run `37606358698` hat auf dem manifestgebundenen 6.72.199-Source die internen Gates erfolgreich ausgeführt.
- Frische WordPress-/MariaDB-Installation: PASS.
- installierter Pluginbaum: 28/28 byteidentisch zum Source-Manifest.
- statischer Basisvertrag, mocked ADCELL E2E, Upgrade-E2E, Tarifcheck/CHECK24/manueller Banner-E2E: PASS.
- bestehende Bannerregression: PASS.
- Candidate-Installer gebaut, Fresh-Unpack/Byteidentität: PASS.
- Evidence: `release/affiliate-zentrale/evidence/affiliate_router_v672199_internal_candidate_gate_20261007.md`.

**Status:** CLOSED_AS_EXECUTION_BLOCKER / INTERNAL_GATES_PASS.

### AFF-ERR-054 – Aktueller Abschlussstand 07.10.2026: nur echter ADCELL-Provider-Gate offen

Der technische 6.72.199-Fix ist intern durch die gebundenen WordPress/MariaDB-Gates belegt. Der Candidate-Installer
`AFFILIATE_ZENTRALE_6.72.199.zip` wurde aus exakt diesem Source gebaut und byteidentisch geprüft.

**Noch offen ist ausschließlich der externe Real-Provider-Nachweis:** Der Test
`release/affiliate-zentrale/evidence/worktests/test_adcell_banner_import_basis_real_provider_v672199.php`
muss mit echten ADCELL-Zugangsdaten und Programm-IDs auf einem isolierten Testhost laufen.

Im erfolgreichen Candidate-Lauf `37606358698` wurde dieser Gate ausdrücklich nicht ausgeführt, weil
`PPAR_ADCELL_USERNAME`, `PPAR_ADCELL_PASSWORD` und `PPAR_ADCELL_PROGRAM_IDS` nicht vorhanden waren.

**KISS-Hardlock für den nächsten Chat:**
- Bereits grüne, hash-identisch gebundene Tests **nicht wiederholen**.
- Keine neuen Tests „zur Sicherheit“ erfinden.
- Keine neue Banner-, Ranking-, Target- oder Performancearchitektur bauen.
- Nur den echten ADCELL-Provider-Gate ausführen.
- Bei FAIL nur den ersten konkret belegten Fehler beheben.
- Bei PASS den vorhandenen Candidate-Installer als final binden und `release-check` ausführen.

**Status:** INTERNAL_PASS / CANDIDATE_INSTALLER_READY / REAL_ADCELL_PROVIDER_GATE_ONLY_OPEN / NO_RELEASE_YET.


## AFF-ERR-056 – 07.10.2026: Live-Kernfehler trotz 6.72.199-Candidate – bestehende Banner bleiben ohne korrekte Kategorie / Tarifcheck-Filter unzuverlässig

**Auslöser:** Nutzer-Live-Screenshot nach Installation des bisherigen 6.72.199-Candidate. Der Kernfehler war weiterhin sichtbar:
- Banner wie Schabracken zeigten keine belastbare korrekte Kategorie-/Portalziel-Zuordnung.
- Tarifcheck war als Filter vorhanden, lieferte aber nicht zuverlässig nur die Tarifcheck-Banner.

**Wichtig:** Damit ist der frühere interne Candidate-PASS von Run `37606358698` für den aktuellen Rootfix-Source **stale**. Er bleibt Historie/Evidence für den alten Manifeststand, ist aber kein PASS für den neuen Source.

### Frischer Delta-Befund – konkret belegter Sourcefehler

Der vorhandene Reconcile-Runner `run_v672195_banner_reconcile()` erlaubte Version `6.72.199`.

Sein automatischer Admin-Einstieg `maybe_reconcile_banner_state_v672195()` erlaubte dagegen nur:
`6.72.195`, `6.72.196`, `6.72.197`, `6.72.198`.

Damit konnte der allgemeine einmalige Bestands-Reconcile in 6.72.199 **nicht über seinen normalen Admin-Einstieg starten**. Bereits vorhandene/verifizierte Live-Banner konnten dadurch mit alten/leeren `topic_targets` stehenbleiben, obwohl der neuere Zuordnungscode vorhanden war.

Das ist ein konkreter Sourcefehler und kein Hoster-/Cache-/Frontendproblem.

### Rootfix im aktuellen Source

Betroffene Source-Dateien:

- `release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-automation-suite.php`
- `release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-creative-library.php`

Änderungen:

1. 6.72.199 erhält nach abgeschlossenem ADCELL-Basislauf genau **einen** frischen Bestands-Reconcile über den bereits vorhandenen Runner.
2. Keine neue Reconcile-Architektur, kein neuer Dauerworker.
3. Tarifcheck/CHECK24-Filter wird an der Partneridentität festgemacht und kann damit auch historische Direkt-/Manuellimporte erfassen; dieser Teil ist **noch nicht live bewiesen**.
4. Kartenoberfläche zeigt nun explizit:
   - Provider-Kategorie;
   - tatsächlich gespeichertes Portalziel.
   Dadurch ist sofort sichtbar, ob Importbasis oder Zielzuordnung fehlt.

### Analyse der bisherigen Lösungswege – was nicht erneut gemacht werden darf

1. **6.72.198 lokaler PASS war kein Live-Beweis.**
   Der Nutzer meldete weiterhin keinen Schabracken-Banner. Lokale Fixtures hatten den realen bestehenden Live-Bestand nicht ausreichend abgebildet.

2. **Provider-Rohdaten/Kategorie-Erhalt allein war notwendig, aber nicht ausreichend.**
   6.72.199 konnte neue Providerdaten sauberer speichern, aber das löst alte Live-Zeilen nicht, wenn der Bestands-Reconcile gar nicht läuft.

3. **Verify-before-Assign war ein gültiger Sicherheitsfix, aber nicht der Live-Kernfix.**
   Er verhindert falsche Zielkarten vor Bildprüfung; er erzeugt aber keine Kategorie für Bestandsbanner, wenn der Reconcile-Einstieg nicht ausgeführt wird.

4. **Banner-vor-Produkte in der Bildprüfung war ein Performance-/Wartezeitfix, nicht der Kategorie-Rootfix.**
   Diese Änderung darf nicht wieder als Lösung für fehlende fachliche Zielzuordnung behandelt werden.

5. **Real-ADCELL-Gate wurde zu früh als einziger verbleibender Blocker behandelt.**
   Der spätere Live-Screenshot hat bewiesen, dass bereits vor diesem Gate ein sichtbarer Funktionsfehler im aktuellen Bestand offen war.

6. **Dropdown vorhanden != Filter funktioniert.**
   Das bloße Vorhandensein von „Tarifcheck“ im UI beweist keine korrekte Datenfilterung. Der neue partnerbasierte Filter ist Source-seitig umgesetzt, aber noch nicht live belegt.

7. **Keine weitere Prüforgie.**
   Kein neuer Workflow, kein neues Testgerüst, keine neue Ranking-/Target-Architektur, solange der nächste Schritt lediglich das gebundene Rootfix-ZIP ist.

### Performance-Hardlock

Unverändert:
- maximal 5 technische Assetprüfungen pro Lauf;
- Banner zuerst;
- nur freie PrüfsLOTS mit Produkten auffüllen;
- kein Frontend-HTTP;
- keine neue Ranking-/Target-Schicht;
- keine Änderung der festen Banner-/Produktplätze.

### Aktueller Status

- Current: Generation 258.
- Source-Manifest-SHA-256: `a51ef1236e8caa530493b65cc0c0e7c9c553f147a55745f4924f643b1b6ee844`.
- Rootfix-Source: gebunden.
- Neues Rootfix-ZIP: **noch nicht gebaut**.
- Neuer Rootfix-PASS: **nicht vorhanden**.
- Live-Beweis für Rootfix: **nicht vorhanden**.

**Erster offener Schritt:** exakt ein installierbares ZIP aus diesem manifestgebundenen Rootfix-Source bauen.

**Status:** LIVE_FAILURE_CONFIRMED / ROOTFIX_SOURCE_BOUND / PLUGIN_NOT_BUILT / NO_PASS / BUILD_ROOTFIX_PLUGIN_NEXT.

### AFF-ERR-056 – Nachtrag 07.10.2026: struktureller Runtime-Fallback als weiterer Root Cause bewiesen und KISS geschlossen

**Belegter Widerspruch:** Der aktuelle Zielvertrag verlangte bereits `STORED_FIXED_TARGET_MAP_ONLY`, `NO_STORED_FIXED_TARGET_NO_BANNER` und keinen themenlosen Pflichtfallback. Trotzdem lieferte `campaign_match_rank()` automatische Creative-Library-/`output_object_v4`-Banner bei einer **nicht passenden gespeicherten Zielkante** weiterhin als allgemeinen bzw. technischen Fallback aus. Bei Pferderassen lag zusätzlich die themenneutrale Regel vor diesem Fail-Closed-Gate.

Damit konnte ein durch Reconcile korrekt von Schabracken auf Fütterung zurückgesetzter Altbanner anschließend auf Schabracken **weiterhin als technischer Fallback Kandidat bleiben**. Das erklärt, warum mehrere lokale Zuordnungs-/Reconcile-Fixes das sichtbare Gesamtproblem nicht zuverlässig beenden konnten.

**KISS-Rootfix:** Für automatische `output_object_v4`-Banner gilt jetzt im Frontend ausschließlich:
- gespeicherte Zielkante passt -> Kandidat;
- gespeicherte Zielkante passt nicht oder fehlt -> `null` / kein Kandidat;
- erst danach arbeitet die vorhandene Verteilung.

Manuelle/FIXED-Ausnahmen bleiben im vorhandenen Vorrangpfad unangetastet.

**Performance-Hardlock geprüft:** Keine neue DB-Abfrage, kein Frontend-HTTP, keine URL-/Text-Neuklassifikation. `banner_distribution_reorder_candidates()`, `banner_distribution_stable_index()`, `ranked_campaigns_for_slot()` und `render_banner()` sind gegenüber dem unmittelbar vorherigen Rootfix-Source bytegleich.

**Regression:** Der bestehende 6.72.199-Basisvertrag enthält jetzt ausdrücklich den Guard, dass Creative-Library-Banner ohne passenden gespeicherten Target-Match nicht über allgemeinen/technischen Fallback wieder in den Pool gelangen und dass dieses Gate vor der historischen neutralen Rassenregel liegt.

**Source-Bindung:** Manifest SHA-256 `31fb24c02b38d5d91b7a59a5b2d5bc50047edb7e0e6459e9a381f7861974ed8c`, 28 Plugin-Dateien. Current Generation 259.

**Governance-Nachholung:** Der vorherige Current-Wert `BUILD_ROOTFIX_PLUGIN` war laut `release_guard.py` kein zulässiger `authorized_next_action`. Current verwendet wieder `RUN_BOUND_RELEASE_GATES`; die konkrete Fachaktion steht in `bound_user_scope_action`.

**Status:** ROOT_CAUSE_PROVEN / STORED_TARGET_ELIGIBILITY_KISS_FIXED / PERFORMANCE_FAST_PATHS_PRESERVED / SOURCE_MANIFEST_BOUND / CURRENT_GATES_OPEN / NO_ZIP_YET.

### AFF-ERR-056 – Nachtrag 07.10.2026: 6.72.201 verursachte Backend-Timeout; 6.72.202 korrigiert Performance- und Kostenregel

**Live-Fehler 6.72.201:** Der 6.72.201-KISS-Reconcile wurde über `admin_init` nicht nur gestartet, sondern verarbeitete Banner synchron im Backend-Request. Mit bis zu 50 Bannern und einem mehrsekündigen Laufzeitfenster konnte dadurch das WordPress-Backend massiv verlangsamt werden und in einen Gateway-Timeout laufen. Das widerspricht dem Performance-/Datenbankvertrag.

**Root Cause im Source:** `maybe_rebuild_banner_kiss_v672201()` führte den Reconcile direkt im Admin-Request aus. Der Hintergrundworker existierte, wurde aber nicht als alleiniger Ausführungsweg benutzt.

**6.72.202-Korrektur:**
- Admin-Request markiert den Reconcile nur noch als laufend und plant einen einzelnen Hintergrundevent.
- Keine Bannerverarbeitung mehr synchron im Backend.
- Hintergrundworker verarbeitet maximal 5 aktive Banner pro Lauf.
- Harter Laufzeitdeckel: 3 Sekunden; danach Fortsetzung im nächsten kleinen Hintergrundlauf.
- Kein zusätzlicher Frontend-HTTP-Pfad und keine neue Frontend-DB-Abfrage.

**Zweiter belegter Fehler – Kostenregel:** Die frühere Tarifcheck/CHECK24-Kostenprüfung verlangte gleichzeitig ein Namensmuster `Kosten ...` und einen `...-kosten`-Slug. Das war fachlich zu eng und entsprach nicht der Nutzerregel „Kreditrechner auf alle realen Kosten-Kategorien“.

**6.72.202-Korrektur:** Für Kredit/Kosten gilt jetzt ausschließlich:
- Ziel ist eine reale `leaf_category`;
- `kosten` kommt irgendwo im realen Kategorienpfad oder im Slug vor.
Damit gibt es keinen künstlichen Prefix+Suffix-Doppelzwang mehr.

**Unverändert gebunden:**
- tiefstes belastbares Bannerziel + Elternpfad;
- Ziel-Evidenz: Ziel-URL -> Provider-Kategorie -> echter Bannertext;
- Formatprüfung vor Auswahl/Verteilung;
- Glossar Desktop 0,50–1,50 / min. 310 px; Mobil 2,50–12,00 / min. 300 px;
- stabile Verteilung innerhalb des zulässigen Fallback-Pools;
- regelmäßiger Providerabgleich; erster Fehllauf Quarantäne, zweiter Fehllauf `inactive_missing` + automatische Kampagne aus;
- Versicherung -> alle realen Versicherungs-Blattkategorien.

**Versionsfehler nachgezogen:** Ein inhaltlich neuer Installationsstand darf keine bereits verwendete Pluginversionsnummer wiederverwenden. Der aktuelle Kandidat ist deshalb fortlaufend **6.72.202**.

**Aktueller Prüfstatus:** Source und ZIP sind gebunden; ZIP-Integrität ist dokumentiert. 6.72.202 ist **nicht final freigegeben**. Live-Readback/gebundene Release-Gates sind offen und bleiben die einzige nächste operative Prüfung.

**Status:** ROOT_CAUSE_PROVEN / 6_72_202_SOURCE_AND_ZIP_BOUND / PERFORMANCE_KISS_FIXED / KOSTEN_RULE_FIXED / LIVE_READBACK_OPEN / NO_FINAL_RELEASE.

## AFF-ERR-057 — 07.10.2026: Vergleichsrechner mit korrekter ID wird im Beitrag nicht angezeigt

**Auslöser:** Nutzerkorrektur im laufenden 6.72.203-Arbeitsstrang. Der offene Fehler betrifft ausdrücklich **nicht Schabracken/Bannerzuordnung**, sondern einen Vergleichs-/Tarifrechner in einem Beitrag: Der Beitrag enthält nach Nutzerangabe die korrekte Rechner-ID, der Rechner wird im Artikel trotzdem nicht angezeigt.

### Frischer Quellenbefund

Der kanonische Source enthält weiterhin den seit 6.72.193 vorgesehenen KISS-Weg:
- Shortcode `affiliate_rechner` ist auf `shortcode_tariff_tool()` registriert.
- Die zentrale Rechnerliste liegt in der vorhandenen nicht-autoloadenden Option `ppar_tariff_tools_v1`.
- Der Renderer gibt nur dann HTML aus, wenn die bereinigte ID existiert, der Rechner aktiv ist und sein HTML-Code nicht leer ist.
- Der historische 6.72.193-Test `AFFILIATE_HOBBYRAUM/test_tariff_tools_kiss_v672193.php` beweist direkte `do_shortcode()`-Ausgabe für aktive bekannte IDs, einschließlich Script-/Iframe-Code.
- Dieser historische Test beweist **nicht** die heute gemeldete reale Kette eines klassischen Beitrags durch den vollständigen `the_content`-Renderpfad.

### Falscher Zwischenweg korrigiert

Die unmittelbar vor der Nutzerkorrektur vorgenommenen Änderungen
- `0c157ccff7f2eed197a56d1fcee5774f90cb1a25` – zusätzliche Banner-Slot-Weitergabe,
- `2821c521e1725f601451ef18760c3d49731e4c69` – Produktseiten-Banner auf redaktionelle Post-Kategorien,
- `b2ad9a4b1079429516251978b1d64414740cfef5` – `affiliate_rechner` blockiert normale Auto-Banner im Artikel,

adressieren die gemeldete Rechner-Nichtanzeige nicht belastbar. Insbesondere kann das bloße Unterdrücken eines Auto-Banners keinen fehlenden Rechner rendern.

Diese drei fachfremden Source-Deltas werden deshalb aus dem kanonischen Source zurückgenommen. Der 6.72.203-Banner-KISS-Stand vor dieser Fehlinterpretation bleibt erhalten.

### Erster echter Blocker

Die erste fehlerhafte Stufe der Rechner-Renderkette ist **noch nicht belegt**. Nicht raten.

Genau einmal zu prüfen:
`Shortcode registriert -> exakte ID vorhanden/aktiv/HTML nicht leer -> Shortcode-Callback liefert HTML -> finaler the_content-Artikel enthält Rechner`.

Erst am ersten belegten FAIL wird geändert. Banner-Zuordnung, Schabracken, Kategorie-Mapping und Ranking sind für diesen Fehler nicht automatisch beteiligt.

**Status:** CURRENT_RENDER_PATH_PASS / LIVE_SHORTCODE_AND_ID_PROVEN / LIVE_CENTRAL_CALCULATOR_RECORD_INVALID_PROVEN / EXACT_RECORD_SUBSTATE_READBACK_NEXT / NO_RELEASE.



### AFF-ERR-057 Nachholbefund 07.10.2026

Fokussierter WordPress/MariaDB-Rendernachweis: Run 37677771944 = PASS in allen vier Stufen.

Live-Readback: Run 37679085019.
- 16 veröffentlichte Finanzierungsbeiträge.
- Exakt `[affiliate_rechner id="kredit"]`: 16 Treffer.
- Falsche Kontroll-ID: 0 Treffer.
- Rechner fehlt im finalen Live-HTML.
- Live-Plugin: 6.72.202.
- Tarifrechner-Renderer 6.72.202 und 6.72.203: identisch.

Erster bewiesener Live-FAIL: zentraler Datensatz `kredit` erfüllt die Gültigkeitsbedingung nicht. Offen ist nur noch, ob er fehlt, inaktiv ist oder leeren HTML-/Widget-Code enthält.

Evidence: `release/affiliate-zentrale/evidence/affiliate_err_057_calculator_live_root_cause_20261007.md`.

NEXT ACTION: authentifizierter Readback von `ppar_tariff_tools_v1['kredit']`; genau den fehlenden Zustand korrigieren; danach denselben Live-Artikel erneut rendern. Kein Source-Fix.


## AFF-ERR-058 — 08.10.2026: Banner hatte zwei Zielwahrheiten

**Root Cause:** Automatische Banner-Ziele wurden in `topic_targets` gespeichert. Eine manuelle feste Themen-/Portalziel-Zuordnung wurde dagegen primär als separate Portalentscheidung mit eigenem `target_key` geführt. Dadurch konnten Automatik, manuelle Zuordnung und Runtime unterschiedliche Zielquellen benutzen.

**KISS-Fix:** Für Banner ist `topic_targets` die einzige fachliche Zielwahrheit. Automatische und manuelle Themenzuordnung schreiben in dieselbe Struktur. Der Runtime-Bannerpfad liest ausschließlich diese gespeicherte Zuordnung. Ein nicht als `mapped` gespeicherter Zustand ist keine automatische Bannerfreigabe.

**Bedienregel:** Jeder Banner kann im Backend direkt über „Thema / Portalziel fest zuordnen“ einem realen Portalziel zugeordnet werden. Eine Begründung ist dafür nicht Pflicht.

**Hardlock:** Keine zweite Banner-Zielquelle, keine Frontend-Neuklassifikation und kein fachfremder General-Fallback.

**Status:** SOURCE_FIXED / MANIFEST_BOUND / RELEASE_GATES_OPEN / NO_RELEASE_PASS.


### AFF-ERR-058 Nachtrag 08.10.2026 – lokale Positiv-/Negativsimulation

Bei der vollständigen lokalen KISS-Simulation wurde ein weiterer Umgehungspfad im späteren Campaign-Ranking gefunden: automatische Creative-Library-Banner (`source=output_object_v4`) konnten bei fehlendem Target-Match noch über `assignment_mode=fallback` sowie über den neutralen Pferderassen-Fallback ausgabefähig bleiben.

Rootfix: Commit `02799c180da3b95ad34341fbfa939db599891eb2`.
Für automatische Creative-Library-Banner gilt jetzt im Ranking ausschließlich:
`gespeicherte automation_target_keys passen -> Kandidat; sonst -> null`.

Danach:
- Source-/Logiksimulation: 14/14 PASS.
- unabhängiger lokaler PHP-Harness: 10/10 PASS.
- falsches Thema, fehlendes Thema, ungültiges Ziel, anderes Portal, alter `general`-Zustand, `fallback` und Rassen-Sonderfallback: jeweils fail-closed.
- Performance/DB: 0 neue Frontend-DB-Zugriffe, 0 neue Frontend-HTTP-Aufrufe, 0 neue Tabelle.

Evidence:
`release/affiliate-zentrale/evidence/affiliate_err_058_kiss_banner_single_target_local_sim_20261008.md`

**Status:** LOCAL_POSITIVE_NEGATIVE_SIM_PASS / PERFORMANCE_DB_HARDLOCK_PASS / WORDPRESS_MARIADB_RELEASE_GATES_OPEN / NO_RELEASE.


## AFF-ERR-059 — 08.10.2026: Manuelle FIXED-Bannerzuordnung durch Single-Truth-Umbau entwertet

**Symptom:** Die am 08.10.2026 eingeführte Banner-Single-Truth-Änderung schrieb eine manuelle feste Banner-Zuordnung zusätzlich in `topic_targets`, entfernte anschließend aber `target_key` / Zielkontext aus der separaten Portalentscheidung. Gleichzeitig wurde `portal_banner` in `output_classify_for_portal()` vor der bestehenden FIXED-Auswertung direkt auf die gespeicherte Banner-Zielkarte geroutet.

**Belegte Vertragsverletzung:** Der autoritative Zielvertrag verlangt ausdrücklich, dass manuelle FIXED-Entscheidungen getrennt erhalten bleiben. Die historische Fehlerregel AFF-ERR-047 bestätigt denselben Vertrag: automatische Kanten dürfen bei Re-Evaluation gelöscht werden, manuelle Control-/FIXED-Entscheidungen liegen separat und bleiben erhalten.

**Root Cause:** Die Regel „eine zentrale automatische Zielkarte“ wurde fälschlich auf manuelle FIXED-Entscheidungen ausgedehnt. Dabei wurde „eine Runtime-Reihenfolge“ mit „nur ein Speicherort“ verwechselt.

**Korrekte KISS-Reihenfolge:** technische/rechtliche Safety -> manuelles Veto/Review -> manuelles FIXED-Ziel (separat, Vorrang) -> automatische gespeicherte `topic_targets`-Ziel-/Pfadkarte -> Format -> spezifische Auswahl -> falls kein spezifischer Banner: ausdrücklich allgemeiner aktiver Fallbackbestand -> stabile bestehende Verteilung.

**Fixziel:** Für `portal_approve_fixed` Zielinformationen ausschließlich als separate Portalentscheidung erhalten; keine automatische Zielkarte überschreiben. In `output_classify_for_portal()` FIXED wieder vor der automatischen Banner-Zielkarte auswerten. UI „Thema / Portalziel fest zuordnen“ darf bleiben.

**POSITIV:** FIXED-Ziel gewinnt auch dann, wenn automatische `topic_targets` ein anderes Ziel enthalten.
**NEGATIV:** Rücknahme der manuellen Entscheidung gibt wieder die unveränderte automatische Zielkarte frei; Reconcile darf FIXED nicht löschen.
**Regression:** Automatische Bannerzuordnung, allgemeiner Fallback, Produktpfade, eBay/Idealo, Rechner und Performance unverändert.
**Performance:** keine neue Tabelle, kein Frontend-HTTP, keine neue Frontend-DB-Abfrage.

**Status:** OPEN / ROOT_CAUSE_PROVEN / SOURCE_FIX_NEXT.


## AFF-ERR-060 — 08.10.2026: Allgemeiner Banner-Fallback war im aktuellen Import/Reconcile nicht mehr erreichbar

**Symptom:** Der Source besitzt weiterhin Runtime-/Materialisierungsunterstützung für explizite allgemeine Banner (`state=general`, `assignment_mode=fallback`, `creative_library_general_fallback`). Der aktuelle automatische Zuordnungsweg `output_assign_banner_targets_from_destination_once()` erzeugt bei fehlendem eindeutigen Fachziel jedoch nur `topic_targets=[]`. `output_store_banner_library_assignment()`, das `state=general` schreiben könnte, hat im aktuellen Source keinen Aufrufer. Der 6.72.203-Reconcile deaktiviert Banner mit `mapped=0` anschließend aus der Automatik.

**Belegte Vertragsverletzung:** Zielvertrag Abschnitt 9.4 verlangt: Gibt es für ein Ziel keinen spezifisch passenden Banner, wird aus dem technisch und formatlich zulässigen allgemeinen aktiven Bannerbestand verteilt. AFF-ERR-045 bindet zusätzlich den KISS-Vertrag: Ohne eindeutiges Ziel entsteht ein allgemeiner technisch gültiger Fallback ohne Fake-Thema.

**Root Cause:** Beim Umbau auf die gespeicherte Ziel-/Pfadkarte wurde der spezifische Zuordnungsweg vollständig gemacht, der bereits definierte allgemeine Fallback-Erzeugungsweg aber nicht mehr an Import/Reconcile angebunden.

**Fixziel:** Nach bestandener Assetprüfung und nur wenn keine eindeutige spezifische Zuordnung existiert, darf ein fachlich nicht widersprüchlicher Banner als explizit `general` gespeichert werden. Kein erfundenes Thema, keine Frontend-Klassifikation. Der allgemeine Datensatz muss die vorhandene Slot-/Formatprüfung nutzen und danach über den bestehenden stabilen Fallback-Verteiler laufen.

**NEGATIV:** Mehrdeutige/widersprüchliche oder fachfremde Evidenz darf nicht automatisch zu `general` werden. Tarifcheck/CHECK24 mit unklarer Familie bleibt fail-closed. Unverifizierte Assets bleiben gesperrt.
**POSITIV:** Verifizierter themenneutraler Banner ohne spezifischen Zieltreffer wird als `general` gespeichert, technisch/formatlich geprüft und nur nach fehlendem spezifischen Treffer verwendet.
**Performance:** keine neue Tabelle, kein Frontend-HTTP, keine neue Frontend-DB-Abfrage; Erzeugung ausschließlich Import/Reconcile.

**Status:** OPEN / ROOT_CAUSE_PROVEN / SOURCE_FIX_NEXT.


## AFF-ERR-061 — 08.10.2026: Banner-Deduplizierung war nicht eindeutig identitätsgebunden

**Belegter Vertragsbruch:** Der Lifecycle-Zielvertrag erlaubt automatisches Zusammenfassen nur bei eindeutig identischen Creative-Varianten; unterschiedliche Motive, CTA, Rabatt oder Angebot müssen getrennt bleiben. Die aktuelle Runtime-Signatur verwendete jedoch nur Provider, Partner, Ziel, Titel und grobe Ratio-Familie. Zwei unterschiedliche Creatives mit denselben Metadaten konnten dadurch fälschlich als Auflösungsvariante zusammenfallen.

**Root Cause:** Die vorhandene kanonische Creative-Identität wurde nicht in die materialisierte Kampagne übernommen und deshalb im Dedupe-Hotpath nicht verwendet.

**KISS-Fixziel:** `creative_identity_hash` aus der Creative Library in die Kampagnendaten übernehmen. Runtime-Dedupe nur bei gültiger identischer 64-stelliger Creative-Identität plus Formatfamilie. Fehlt die Identität bei historischem Altbestand, nicht deduplizieren. Keine Bildanalyse, keine neue Tabelle, keine DB-/HTTP-Abfrage im Ranking.

**POSITIV:** dieselbe Creative-Identität in mehreren Auflösungen derselben Formatfamilie -> größte belegte Version bleibt.
**NEGATIV:** unterschiedliche Creative-Identitäten bei gleichem Partner/Ziel/Titel/Ratio -> beide bleiben Kandidaten.
**Status:** OPEN / ROOT_CAUSE_PROVEN / SOURCE_FIX_NEXT.


## AFF-ERR-062 — 08.10.2026: Sichtbare Blocküberschrift „Anzeige“ auf breiten Übersichts-Bannern unterdrückt

**Belegter Vertragsbruch:** Der Lifecycle-Zielvertrag verlangt ausdrücklich, dass die sichtbare Blocküberschrift `Anzeige` erhalten bleibt. Glossar- und Rassen-Einzelbanner rendern diese Überschrift bereits sichtbar. Für breite Übersichts-Banner wurde sie in der aktuellen Ausgabe dagegen absichtlich entfernt: der Renderer leert das Label und die CSS-Regel blendet `.ppar-affiliate-label` im Overview-Slot aus.

**Fixziel:** Breite Übersichts-Banner erhalten wieder sichtbar `Anzeige`. Keine Änderung an Bannerwahl, Ranking, Zielkarte, Format, Tracking oder Verteilung.

**Status:** OPEN / ROOT_CAUSE_PROVEN / SOURCE_FIX_NEXT.


### Autoritative Korrektur zu AFF-ERR-056 — 08.10.2026

Der ältere Hardlock `NO_STORED_FIXED_TARGET_NO_BANNER` darf nicht als Verbot des allgemeinen Banner-Fallbacks gelesen werden. Der spätere autoritative Zielvertrag `AFFILIATE_RELEASE_BANNER_IMPORT_BASIS_TARGET_20261007.md`, Abschnitt 9.4, bindet ausdrücklich:

- ein spezifisch zugeordneter Banner darf bei Nichttreffer nicht fachfremd ausweichen;
- gibt es für das aktuelle Ziel keinen spezifisch passenden Banner, darf ein **separat als allgemein geführter, aktiver, technisch und formatlich gültiger Bannerbestand** greifen;
- spezifisch -> allgemein -> stabile bestehende Verteilung;
- kein Frontend-Reclassify.

Damit ist der ältere pauschale „kein Ziel = kein Banner“-Teil von AFF-ERR-056 insoweit superseded.

### Autoritative Korrektur zu AFF-ERR-058 — 08.10.2026

Die frühere Formulierung „manuelle und automatische Themenzuordnung teilen ausschließlich dieselbe `topic_targets`-Wahrheit“ war zu weitgehend und widersprach dem Zielvertrag. Korrekt ist:

- automatische Banner-Ziel-/Pfadkarte: `topic_targets`;
- manuelle FIXED-Entscheidung: separat gespeichert und vorrangig;
- Runtime-Reihenfolge: Safety -> Veto/Review -> FIXED -> automatische Zielkarte -> Format -> spezifische Auswahl -> allgemeiner Fallback -> stabile Verteilung.

AFF-ERR-059 ist für diese Präzisierung die jüngere Root-Cause-Korrektur.
