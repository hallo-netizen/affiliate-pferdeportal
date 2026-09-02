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

**Nicht wiederholen:** Bulk-Synchronisation/-Import bestätigter Partnerschaften; Einzelpflege höchstens Fallback.

**POSITIV:** mehrere bestätigte Partner in einem Lauf.
**NEGATIV:** nicht genehmigte/fremde/ungültige Datensätze werden nicht freigegeben.

**Status:** FIXED_LOCAL für den ausdrücklich autorisierten manuellen Ein-Feld-Bulkimport; automatische Discovery bleibt separat durch AFF-ERR-012 offen.

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

**Evidence:** `release/affiliate-zentrale/evidence/current_scope_manual_import_partner_visibility_20260902.txt`.

**Status:** FIXED_LOCAL / WordPress-Liveprüfung noch offen.

## AFF-ERR-012 — DS24 Affiliate-Partnerschaftsinventur mit falscher API-Autorität

**Symptom:** reale Menge 18 genehmigte Partnerschaften; 6.70 live 0/0, 6.71 live 1/1 mit alter lokaler Quelle 53213.

**Root Cause:** `listMarketplaceEntries` ist keine eigene Affiliate-Partnerschaftsinventur; `getAffiliateCommission(all)` wurde fälschlich als fremde Vendor-Inventur interpretiert; `validateAffiliate` kann nur bereits bekannte Produkt-IDs verifizieren.

**Gescheiterte Wege:** Marketplace als Vollinventur; synthetisches `getAffiliateCommission(all)`-Fixture; 53213 als Remote-Discovery-Erfolg.

**Nicht wiederholen:** diese drei Wege nicht als autoritative automatische Discovery verwenden. Der vom Nutzer ausdrücklich autorisierte manuelle CSV-Bulkimport ist ein separater Betriebsweg und darf niemals als Remote-Discovery-PASS ausgegeben werden.

**POSITIV automatische Discovery:** unterstützter read-only Affiliate-seitiger Kanal liefert ohne CSV/ID-Vorfütterung alle 18.
**POSITIV manueller Weg:** aktueller DS24-Partnerschaftsexport übernimmt vollständig, identitätsgebunden und reproduzierbar alle genehmigten Datensätze.
**NEGATIV:** 17/18 als Auto-Discovery, 53213-only, Marketplace-only, transaktions-only, falsche Identität, malformed/duplicate oder synthetische Antwort => fail closed; Importfehler => keine Publikationsmutation, LKG bleibt.
**Gesamtworkflow:** gültiger Eingang → Metadaten → Creative/Banner → Bild/Tracking → Targets/Slots → Draft → Revalidation → Persistenz → LKG → Readback → Reassignment; Partnerfehler isolieren; eBay/idealo/Awin regressionsprüfen.

**Evidence:** `protocol/AFFILIATE_RELEASE_DS24_DISCOVERY_CAPABILITY_AUDIT_20260902.md`; `protocol/AFFILIATE_RELEASE_MANUAL_IMPORT_CONTRACT_20260902.md`; `release/affiliate-zentrale/evidence/manual_import_authority_hardening_20260902.txt`.

**Status:** OPEN für automatische Discovery; manueller Bulkimport ausdrücklich zulässig.

## AFF-ERR-013 — Manueller Bestandsimport akzeptiert unvollständige oder widersprüchliche Autorität

**Symptom:** doppelte Produkt-ID konnte still überschrieben werden; GZIP >32 MiB konnte abgeschnitten als scheinbar vollständig behandelt werden.

**Root Cause:** Last-Write-Wins bei Produkt-ID und Sample-Reader als Vollreader ohne Overflow-Nachweis.

**Nicht wiederholen:** autoritative Bestandsdatei vor Mutation auf eindeutige Produkt-IDs und vollständigen GZIP-Inhalt prüfen; Parserfehler => null Mutation.

**POSITIV:** reale Kontrollstruktur 18 Partnerschaften / 10 Werbemittelquellen / 10 Vendoren; CSV/GZIP innerhalb Limit vollständig.
**NEGATIV:** doppelte Produkt-ID, >32-MiB-GZIP, pending/rejected/ungültige IDs fail closed.
**Regression:** Ein-Feld-Erkennung DS24/idealo/Awin/ADCELL/eBay, Identitätsbindung, Reimport, Preserve-Guard, LKG und Provider-/Outputgrenze.

**Evidence:** `release/affiliate-zentrale/evidence/manual_import_authority_hardening_20260902.txt` — 35/35 fokussierte Checks, 3/3 PHP-Lints, 7/7 reale Multipart-HTTP-Routen.

**Status:** FIXED_LOCAL / WordPress-Liveimport noch offen.

## AFF-ERR-014 — KISS-Navigation wiederholt bereits live gescheiterten `remove_submenu_page()`-Weg

**Datum / Arbeitsschritt:** 02.09.2026 / Gesamtregression vor Livekandidat.

**Symptom:** aktueller `class-ppar-admin-kiss.php` ruft für die funktionalen Legacy-/Providerseiten wieder `remove_submenu_page()` auf. Der dokumentierte 6.64.0-Livefehler war genau: KISS entfernte alte Unterseiten und verlinkte danach weiter auf diese Slugs; Nutzer erhielt `Du bist leider nicht berechtigt, auf diese Seite zuzugreifen.` Der 6.64.1-Rootfix verlangte ausdrücklich: funktionale Seiten registriert lassen, nur optisch ausblenden, **kein `remove_submenu_page()` im KISS-Teil**.

**Root Cause:** ein bereits live widerlegter Navigationsweg wurde beim späteren KISS-Source erneut eingeführt und bei den jüngsten Importtests nicht als historische Regression gegengeprüft.

**Gescheiterter Weg:** funktionale Zielseiten mit `remove_submenu_page()` aus der WordPress-Menüstruktur entfernen und sie anschließend weiterhin über KISS-Buttons direkt ansteuern.

**Betroffene Bereiche:** ausschließlich KISS-Navigation/Backend-Erreichbarkeit. Providerlogik, Importer, Analytics, DS24, eBay, idealo, Awin, Output/LKG dürfen nicht geändert werden.

**Nicht wiederholen:** Legacy-/Providerseiten bleiben vollständig registriert und erreichbar. Falls sie in der linken Navigation optisch reduziert werden sollen, ausschließlich Darstellung/CSS auf bereits registrierten Menüpunkten ändern; niemals die funktionale Registrierung/WordPress-Berechtigungsroute entfernen.

**POSITIV:** jeder KISS-Button-Zielslug bleibt nach KISS-Menüaufbau registriert/erreichbar; insbesondere Netzwerke, Sync, Awin, ADCELL, eBay, idealo, Digistore24, Outputs, Assignments, Preview, Control, Automation, Health und Deals.
**NEGATIV:** kein `remove_submenu_page()` für funktionale Zielseiten im KISS-Code; keine Berechtigungs-/Page-Hook-Lücke.
**Regression:** sichtbare fünf KISS-Einstiege bleiben; Ein-Feld-Upload und direkte Partner-Analytics bleiben; Provider-/Outputbytes unverändert.

**Evidence vor Fix:** historisches Liveprotokoll `AFFILIATE_ZENTRALE_GESAMTPROTOKOLL_ZIELVERTRAG_FEHLER_STATUS_2026-09-01.md`, Abschnitt 6.64.0/6.64.1; aktueller Source enthält den widerlegten Aufruf erneut.

**Status:** OPEN — aktueller erster belegter Fehler; vor weiterem Live-/Buildschritt schließen.

---

# Aktueller PRECHECK

Aktueller erster Fehler: `AFF-ERR-014`.

Gebundener nächster Zyklus:
`GESAMTTEST → AFF-ERR-014 Rootfix ausschließlich KISS-Navigation → GESAMTTEST`.

Dabei bleiben `AFF-ERR-011` und `AFF-ERR-013` lokal geschlossen; `AFF-ERR-012` automatische Discovery bleibt offen, blockiert aber den ausdrücklich autorisierten manuellen Bulkimport nicht. Keine Release-/Live-Abnahme aus lokalen Einzeltests.
