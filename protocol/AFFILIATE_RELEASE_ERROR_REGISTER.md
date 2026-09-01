# AFFILIATE-ZENTRALE — VERBINDLICHES FEHLERREGISTER

Stand: 2026-09-01
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

---

# Aktueller PRECHECK für den nächsten Banner-Automationsblock

Relevante Fehler-IDs zwingend: `AFF-ERR-001`, `002`, `003`, `004`, `005`, `006`, `008`, `009`, `010`.

Der nächste Implementierungsblock darf erst als lokal PASS gelten, wenn **Bulk-Partnerschaften + Bannerimport + flexible Slotdefinition + Seiten/Kategorien/Beiträge + Mehrfachnutzung + Pferde-Fallback + regelmäßige Neubewertung + Größen-/Responsive-Matching + LKG/Persistenz + Provider-Regression** gemeinsam positiv und negativ getestet sind.

Keine Abnahme aus Einzeltests.
