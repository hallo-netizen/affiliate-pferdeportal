# AFFILIATE-ZENTRALE — VERBINDLICHES FEHLERREGISTER

Stand: 2026-09-02
Workstream: `AFFILIATE_ZENTRALE`
Branch: `affiliate-release-current`
Status: `MANDATORY_PRESTEP_GATE`

## Zweck

Dieses Register ist für **jeden Arbeitsschritt** der Affiliate-Zentrale verbindlich. Sein Zweck ist nicht nur Dokumentation, sondern die technische Pflicht, bekannte Fehler **nicht zu wiederholen**.

## Harte Ausführungsregel

Vor **jedem** Analyse-, Code-, GitHub-, Codex-, Test-, Build-, Installations-, Live- oder Release-Schritt muss dieses Register gelesen und gegen den geplanten Schritt geprüft werden.

Ein Schritt darf nur beginnen, wenn:

1. der aktuelle Scope genannt ist,
2. alle dazu passenden Fehler-IDs aus diesem Register berücksichtigt wurden,
3. für jede passende Fehler-ID die dort hinterlegte Gegenmaßnahme/Testpflicht eingeplant ist,
4. kein bereits als falsch dokumentierter Lösungsweg wiederholt wird,
5. kein PASS behauptet wird, solange die dafür geforderte Evidence fehlt.

Wenn ein geplanter Schritt einen bekannten Fehlerweg wiederholt, gilt **FAIL_CLOSED**: Schritt nicht ausführen, zuerst Ursache/Plan korrigieren.

## Pflicht bei jedem neuen Fehler

Jeder neue Fehler wird **vor dem nächsten Fix** hier eingetragen mit:

- Fehler-ID
- Datum / Arbeitsschritt
- sichtbares Symptom
- belegte Root Cause
- falscher/gescheiterter Lösungsweg
- betroffene Systembereiche
- verbindliche Nicht-Wiederholungsregel
- erforderlicher POSITIV-Test
- erforderlicher NEGATIV-Test
- erforderlicher Gesamtworkflow-/Regressionstest
- Evidence/Commit/Hash soweit vorhanden
- Status: OPEN / FIXED_LOCAL / LIVE_PASS / CLOSED

**Kein Fix ohne vorherigen Registereintrag. Keine Abnahme ohne Registerabgleich.**

## Pflicht je Arbeitsschritt

Jeder technische Arbeitsauftrag muss einen Abschnitt `ERROR-REGISTER PRECHECK` enthalten:

- geprüfte Fehler-IDs,
- warum sie relevant oder nicht relevant sind,
- welche Positiv-/Negativ-/Regressionstests daraus folgen.

Nach Abschluss muss ein `ERROR-REGISTER POSTCHECK` dokumentieren:

- neue Fehler: ja/nein,
- bekannte Fehler wiederholt: ja/nein,
- falls ja: Gate = FAIL,
- Evidence des Gegenbeweises.

---

# Bekannte Fehler und verbindliche Gegenregeln

## AFF-ERR-001 — Vorzeitige Abnahme / PASS ohne vollständigen Nachweis

**Symptom:** Lokaler Teiltest wurde als praktisch fertig dargestellt, obwohl Live-/End-to-End-Nachweis fehlte.

**Root Cause:** Teil-Evidence wurde mit Gesamtworkflow-Abnahme verwechselt.

**Nicht wiederholen:** `PASS`, `fertig`, `Release` oder `Abnahme` nur, wenn die explizit gebundenen lokalen POSITIV-/NEGATIV-/Gesamtworkflow-Tests und erforderlichen Live-Gates tatsächlich belegt sind.

**Pflichttests:** lokaler Gesamtworkflow + Gegenfälle + Regression; Live nur wenn Live-Gate gebunden.

**Status:** CLOSED / dauerhaftes Hardlock.

## AFF-ERR-002 — Last-Known-Good vor Schlussprüfung verdrängt

**Symptom:** Neuer DS24-Kandidat konnte eine bereits veröffentlichte Last-Known-Good-Ausgabe vor vollständiger Schlussprüfung überschreiben/deaktivieren.

**Root Cause:** Aktivierung/Supersede war nicht strikt zweiphasig.

**Nicht wiederholen:** Draft zuerst vollständig materialisieren und revalidieren; bestehende LKG erst **nach** persistiertem neuen `published`-Zustand ablösen. Fehler = Rollback auf LKG.

**POSITIV:** neuer valider Kandidat wird veröffentlicht und ersetzt danach LKG.
**NEGATIV:** invalid/stale/Persistenzfehler lässt LKG unverändert live.
**Regression:** eBay/idealo/Awin-Ausgaben bleiben unverändert.

**Status:** LIVE_PASS im 6.68.0-Livepfad; Regel bleibt dauerhaft bindend.

## AFF-ERR-003 — Aktion lief, Backend zeigte altes/kein Ergebnis

**Symptom:** DS24-Aktion wurde ausgeführt, Backend-Readback zeigte aber den alten Status bzw. verschluckte das Ergebnis.

**Root Cause:** End-to-End-Readback war nicht Bestandteil des gleichen Abschlussvertrags.

**Nicht wiederholen:** Jeder manuell oder automatisch gestartete Lauf muss seinen persistierten Endzustand auf derselben Fachseite eindeutig anzeigen; keine Erfolgsmeldung ohne Readback.

**POSITIV:** neuer Laufzeitstempel + Run-Zahlen + Schlussprüfung sichtbar.
**NEGATIV:** fehlender/staler Readback verhindert PASS.

**Status:** LIVE_PASS im 6.68.0-Livepfad; Regel bleibt dauerhaft bindend.

## AFF-ERR-004 — Unrealistische Testdaten erzeugen falschen lokalen PASS

**Symptom:** Lokaler Zieltest nutzte bereits den fachlich idealisierten Begriff `Pferdetraining`, während Live `MKA Horsemanship Academy` vorlag; lokal PASS, live Review.

**Root Cause:** Testfixture enthielt die gewünschte Lösung statt den echten Live-Eingang.

**Nicht wiederholen:** Problemfälle werden mit echten/realitätsnahen Rohdaten reproduziert. Kein Test darf ein erwartetes Klassifikationsergebnis bereits in die Eingabedaten schreiben.

**POSITIV:** echter Rohname/echte Zielstruktur führt zum richtigen Ergebnis.
**NEGATIV:** generische/mehrdeutige Namen führen nicht zu erfundenen engen Treffern.
**Regression:** vollständiger realer Portalbaum wird mitgetestet.

**Status:** CLOSED / dauerhaftes Hardlock.

## AFF-ERR-005 — Zielklassifizierer bevorzugt generische Wörter/tiefe Unterpfade

**Symptom:** 3 DS24-Ausgaben geplant, aber 0 Entwürfe / Review statt sinnvoller automatischer Verteilung.

**Root Cause:** Allgemeine Signale wie `Pferd`/`Training` und tiefe Pfade wurden zu stark gewichtet; reale semantische Nähe wurde verzerrt.

**Nicht wiederholen:** Spezifische Fachsignale vor generischen Portalwörtern; Tiefe allein ist kein Qualitätsmerkmal; komplette reale Zielmenge prüfen; bei breiter Pferde-Relevanz darf ein fachlich breiter Pferde-Fallback genutzt werden.

**POSITIV:** spezifisches Ziel gewinnt bei echtem spezifischem Match.
**NEGATIV:** beliebige tiefe Kategorie gewinnt nicht nur wegen Pfadlänge/generischem Pferdewort.
**Gesamtworkflow:** Seiten + Kategorien + Beiträge + reales Zielinventar.

**Status:** LIVE_PASS 6.68.0; Regel bleibt dauerhaft bindend.

## AFF-ERR-006 — Mini-Fix-/Versionskaskade statt Root-Cause-Fix

**Symptom:** Mehrere aufeinanderfolgende Pluginstände behandelten jeweils nur das nächste sichtbare Symptom.

**Root Cause:** Zu enger Testscope und Fix vor vollständiger Ursachen-/Gesamtworkflowanalyse.

**Nicht wiederholen:** Ein Fehler → Root Cause → gebündelter Fix → kompletter POSITIV/NEGATIV/Gesamtworkflow-Test. Keine neue Version für bloße kosmetische oder nachgelagerte Einzelerscheinung, wenn dieselbe Ursache offen ist.

**Pflicht:** Vor neuem Pluginbuild belegen, warum eine Codeänderung notwendig ist und welche gemeinsame Ursache damit geschlossen wird.

**Status:** OPEN als permanente Prozesssperre.

## AFF-ERR-007 — Unvollständige Backend-Pfade

**Symptom:** Nutzer musste nachfragen, wo eine Aktion im WordPress-Backend zu finden ist.

**Root Cause:** UI-Anweisung nannte nur Zielseite/Button statt vollständiger Navigation.

**Nicht wiederholen:** Jede Nutzerhandlung im Backend mit vollständigem Pfad ab `WordPress-Dashboard` nennen.

**Status:** CLOSED / permanente Kommunikationsregel.

## AFF-ERR-008 — DS24-Einzelpflege als Dauerlösung

**Symptom:** Jede freigegebene Digistore24-Bannerquelle müsste einzeln mit Produkt-ID/Promolink/Werbemittelseite eingetragen werden.

**Root Cause:** Technischer Einzelimport wurde als Betriebsmodell stehen gelassen.

**Nicht wiederholen:** Ziel ist Bulk-Synchronisation der bereits passenden/bestätigten Partnerschaften und danach automatische Bannererfassung/-pflege. Einzelpflege bleibt höchstens Fallback, nicht Hauptworkflow.

**POSITIV:** mehrere bestätigte Partner in einem Lauf importier-/synchronisierbar.
**NEGATIV:** unbestätigte/fremde/nicht-pferderelevante Partner werden nicht automatisch freigegeben.

**Status:** OPEN — Bestandteil des aktuellen Zielvertrags.

## AFF-ERR-009 — Bannerformat oder Position hart im Providercode verdrahtet

**Risiko/Symptom:** Neue Bannerformate oder spätere Designänderungen würden einen Umbau der Provider-/Zuordnungslogik erzwingen.

**Root Cause, die verboten ist:** feste Pixelmaße, feste Seitentyp-Positionen oder DS24-spezifische Slotregeln direkt im Provideradapter.

**Nicht wiederholen / Architektur-Hardlock:** Bannerquelle, Bannerformat und Ausgabeslot müssen getrennte Verträge sein.

Verbindlich:

- Banner speichert reale Breite, Höhe, Seitenverhältnis und technische Eigenschaften als Metadaten.
- Design-/Slotdefinitionen liefern verfügbare Slottypen und deren aktuelle Fähigkeiten/Positionen über eine zentrale konfigurierbare Schnittstelle.
- Providerlogik kennt **keine** fest verdrahtete Position und **keine** einzelne Pflichtgröße.
- Matching entscheidet zur Laufzeit Banner ↔ Slot.
- Ein Slot darf mehrere zulässige Formatklassen akzeptieren.
- Größenänderung/Positionsänderung im Design darf nur Slotdefinition/Konfiguration ändern, nicht Provideradapter oder gesamte Zuordnungsarchitektur.
- Responsive Skalierung verzerrt nie das Seitenverhältnis.
- Wenn ein neues Format nicht passt, bleibt es verfügbar und wird bei später passenden Slots automatisch neu bewertet.

**POSITIV:** neue Slotgröße/Position wird durch geänderte Slotdefinition übernommen, ohne DS24/Awin/Providercode zu ändern.
**NEGATIV:** unpassendes Seitenverhältnis wird nicht verzerrt/abgeschnitten erzwungen.
**Regression:** bestehende Slots/Banner funktionieren unverändert.

**Status:** OPEN — zwingender Bestandteil des aktuellen Banner-Automations-Zielvertrags.

## AFF-ERR-010 — Organisch wachsendes Portal nur einmalig zugeordnet

**Risiko/Symptom:** Neue Kategorien/Seiten/Beiträge würden keine bestehenden Banner erhalten; bessere spätere Zieltreffer würden nicht genutzt.

**Nicht wiederholen:** Zuordnung ist kontinuierlich/re-entrant. Neue oder geänderte Ziele und Banner lösen eine erneute Bewertung aus; zusätzlich periodischer zentraler Recheck. Keine Provider-eigenen Cron-Inseln.

**POSITIV:** neu hinzugefügter passender Beitrag erhält beim nächsten zentralen Lauf eine passende Bannerchance.
**NEGATIV:** fremder Themenbereich außerhalb des Pferde-Portals erhält keine automatische Bannerzuordnung.

**Status:** OPEN — Bestandteil des aktuellen Zielvertrags.

## AFF-ERR-011 — Partner-&-Einnahmen-Übersicht blendet aktive Produktquellen aus

**Symptom:** `idealo` und `eBay` sind technisch aktiv und in der zentralen Einnahmen-/Klickauswertung vorhanden, erscheinen aber nicht auf der sichtbaren KISS-Einstiegsseite `Partner & Einnahmen`.

**Root Cause:** Die KISS-Seite baut ihre sichtbaren Karten ausschließlich aus `banner_networks()` auf. Aktive monetarisierende Produkt-/Preisvergleichsquellen aus `product_sources()` werden dadurch fälschlich ausgeblendet, obwohl die bestehende Partner-Analytics sie bereits vollständig führt.

**Gescheiterter Weg:** Die sichtbare Partnerseite als reine Bannernetzwerk-Liste behandeln und Nutzer für Klickdaten zusätzlich auf eine zweite Unterseite schicken.

**Nicht wiederholen:** `Partner & Einnahmen` ist die zentrale monetarisierende Übersicht und muss die vorhandene providerübergreifende Partner-Analytics direkt verwenden. Keine künstliche Trennung nach Banner-/Produktquelle in der sichtbaren Einnahmenansicht.

**POSITIV:** `WordPress-Dashboard → Affiliate-Zentrale → Partner & Einnahmen` zeigt mindestens eBay, idealo, Awin, ADCELL, Digistore24 und Direktpartner sowie die vorhandenen lokalen Klicks; Provider-Klicks/Einnahmen erscheinen nur bei real gelieferten Daten.

**NEGATIV:** Fehlende Provider-Reports werden weiterhin als `nicht verfügbar`/`noch kein Report` angezeigt und niemals geschätzt; vorbereitete Quellen werden nicht als aktive Einnahmen erfunden.

**Regression:** Provideradapter, eBay-/idealo-Ausspielung, DS24-Bannerlogik und bestehendes Klicktracking bleiben unverändert; es wird ausschließlich die bereits vorhandene zentrale Auswertung sichtbar gemacht.

**Status:** OPEN — gemeinsamer UI-Ursachenfix im aktuellen Abschlussblock.

## AFF-ERR-012 — DS24 Affiliate-Partnerschaftsinventur mit falscher API-Autorität

**Datum / Arbeitsschritt:** 02.09.2026 / automatische Digistore24-Partnerschafts-Discovery.

**Symptom:** Reale Kontrollmenge = 18 genehmigte Affiliate-Partnerschaften. 6.70 live = 0/0; 6.71 live = 1/1, wobei die einzige Quelle die alte lokale 53213 und nicht eine der 18 Kontrollpartnerschaften war.

**Belegte Root Cause:** Die Discovery-Quelle wurde semantisch falsch gewählt. `listMarketplaceEntries` ist keine verlässliche Inventur der eigenen genehmigten Affiliate-Partnerschaften. `getAffiliateCommission(product_ids=all)` erlaubt zwar den Parameter `all`, wurde aber fälschlich als Affiliate-seitige Fremdvendor-Inventur interpretiert; der reale bekannte Fremdvendor-Fall 53213 hatte bereits keine verwertbare `data.commissions`-Antwort für diesen Zweck geliefert. `validateAffiliate` benötigt bekannte Produkt-IDs und kann daher nur verifizieren, nicht inventarisieren.

**Gescheiterte Wege:** Marketplace als vollständige Partnerschaftsinventur; `getAffiliateCommission(all)` aufgrund synthetischer lokaler Fixtures als autoritative Discovery; bestehende lokale Quelle 53213 als Remote-Discovery-Erfolg mitzählen.

**Betroffene Systembereiche:** ausschließlich DS24-Discovery-Eingang und dessen Reporting. Bestehende Bannerparser, Ziel-/Slotlogik, LKG, eBay, idealo, Awin und zentrale Analytics dürfen ohne Regression nicht neu gebaut werden.

**Nicht wiederholen:** Keiner der drei Wege `listMarketplaceEntries`, `getAffiliateCommission(all)`, `validateAffiliate` darf ohne neuen realen Gegenbeweis als autoritative **automatische** Affiliate-Partnerschafts-Discovery implementiert werden. Der vom Nutzer am 02.09.2026 ausdrücklich autorisierte, manuell gestartete CSV-Bulkimport ist davon ausgenommen: Er ist ein eigener Betriebsweg und darf niemals als Remote-Discovery-PASS ausgegeben werden. Kein Fixture darf eine gewünschte Remote-Antwort vorwegnehmen.

**POSITIV automatische Discovery:** Ein von Digistore24 unterstützter, read-only, maschinenlesbarer Affiliate-seitiger Discovery-Kanal liefert ohne CSV-/Produkt-ID-Vorfütterung alle 18 Kontroll-IDs.

**POSITIV manueller Betriebsweg:** Ein explizit hochgeladener aktueller Digistore24-Partnerschaftsexport übernimmt alle genehmigten Partnerschaften vollständig, identitätsgebunden und reproduzierbar; Reporting bezeichnet die Herkunft klar als manuellen Dateiimport.

**NEGATIV:** 17/18 als behauptete automatische Discovery, 53213-only, Marketplace-only, Transaktions-only, fremde Affiliate-Identität, malformed/duplicate Schema oder synthetisch angenommene API-Antwort bleiben für automatische Discovery FAIL_CLOSED. Ein manueller Importfehler führt zu null nachgelagerten Veröffentlichungsmutationen und lässt LKG unverändert.

**Gesamtworkflow / Regression:** Nach gültigem Partnerschaftseingang bestehende Verarbeitungskette unverändert weiterverwenden: Vendor-/Produktmetadaten → Werbemittelseite/Creative → Banner → Bild/Tracking → Seiten/Kategorien/Beiträge → flexible Slots → Draft → Revalidation → Persistenz → LKG → Backend-Readback → Reassignment; einzelne Partner-/Creative-/Persistenzfehler dürfen andere Partner nicht stoppen; eBay/idealo/Awin/Partner-&-Einnahmen/Klicktracking/Zeitraumfilter regressionsprüfen.

**Evidence:** `protocol/AFFILIATE_RELEASE_DS24_DISCOVERY_CAPABILITY_AUDIT_20260902.md`; `protocol/AFFILIATE_RELEASE_MANUAL_IMPORT_CONTRACT_20260902.md`.

**Status:** OPEN für automatische Discovery; der ausdrücklich autorisierte manuelle Bulkimport ist als separater Betriebsweg zulässig.

## AFF-ERR-013 — Manueller Bestandsimport akzeptiert unvollständige oder widersprüchliche Autorität

**Datum / Arbeitsschritt:** 02.09.2026 / lokaler Negativtest des neuen Ein-Feld-Dateiimports.

**Symptom:** Zwei unabhängige Negativfälle wurden vom kanonischen Importer angenommen: dieselbe Produkt-ID konnte in zwei widersprüchlichen DS24-Zeilen vorkommen und die spätere Zeile überschrieb die frühere still; eine GZIP-Datei oberhalb des 32-MiB-Dekompressionslimits wurde beim Limit abgeschnitten und als scheinbar vollständiger Inhalt zurückgegeben.

**Belegte Root Cause:** Der neue autoritative manuelle Bestandsweg prüfte zwar Schema, Status, IDs und Vendor-/Werbemittel-Konflikte, aber noch nicht die Eindeutigkeit der Produkt-ID über die gesamte Datei und nicht die Vollständigkeit eines limitierten GZIP-Vollimports.

**Gescheiterter Weg:** Produkt-ID als Array-Key mit stillem Last-Write-Wins; Wiederverwendung des absichtlich begrenzten Sample-Readers als vollständiger GZIP-Reader ohne Overflow-Nachweis.

**Betroffene Systembereiche:** ausschließlich `class-ppar-universal-import.php` und dessen DS24-Dateieingang. Provideradapter, eBay, idealo, Awin, Output-/Slotlogik, LKG und Analytics bleiben unangetastet.

**Nicht wiederholen:** Autoritative Bestandsdateien dürfen vor jeder Mutation weder widersprüchliche doppelte Produkt-IDs noch abgeschnittene Vollinhalte akzeptieren. Vollimport-GZIP muss Überlauf explizit erkennen und fail-closed abbrechen. Parserfehler = null Importmutation.

**POSITIV:** reale 18er-Kontrollstruktur bleibt 18 Produktpartnerschaften / 10 Werbemittelquellen / 10 Vendoren; normale CSV und GZIP innerhalb des Limits werden vollständig gelesen.

**NEGATIV:** doppelte Produkt-ID, auch bei anderer Vendor-/Werbemittelzuordnung, wird vor Persistenz blockiert; GZIP >32 MiB dekomprimiert wird vor Parsing/Persistenz blockiert; pending/rejected/ungültige IDs bleiben blockiert.

**Gesamtworkflow / Regression:** Ein-Feld-Erkennung DS24/idealo/Awin/ADCELL/eBay, DS24-Identitätsbindung, Reimport/Idempotenz, Marketplace-Preserve-Guard, LKG-Erhalt und hash-identische Provider-/Outputpfade erneut prüfen.

**Evidence vor Fix:** lokaler Negativlauf 02.09.2026: beide neuen Gegenfälle FAIL.

**Status:** OPEN — nächster gebundener Ursachenfix.

---

# Aktueller PRECHECK für den manuellen Ein-Feld-Import

Relevante Fehler-IDs zwingend: `AFF-ERR-001`, `002`, `003`, `004`, `006`, `007`, `008`, `011`, `012`, `013`; für nachgelagerte Banner-/Ausspielungslogik zusätzlich `005`, `009`, `010`.

Der manuell gestartete CSV-Bulkimport ist aufgrund der ausdrücklichen Nutzerentscheidung zulässig und benötigt **keinen** vorherigen erfolgreichen automatischen 18er-Discovery-Nachweis. Er darf aber niemals als automatische Discovery bezeichnet werden. Der aktuelle erste belegte Fehler ist AFF-ERR-013; zuerst dessen Autoritäts-/Vollständigkeitsprüfung schließen, danach den vollständigen lokalen Positiv-/Negativ-/Regressionstest des Ein-Feld-Imports wiederholen.

Keine Abnahme aus Einzeltests.