# HOBBY DEPOT – BUCHBINDEN – TECHNISCHE INTENT-ABSICHERUNG

STAND: 2026-09-30
STATUS: IST-STAND GEPRÜFT / ARTIKEL-OWNERSHIP FÜR HOBBY DEPOT NOCH NICHT END-TO-END GEBUNDEN

## 1. Bezug

Fachliche Pilotmatrix:
`BUCHBINDEN_INTENT_OWNERSHIP_MATRIX_20260930.md`

Technischer Scope des Kategorie-Workflows bleibt separat:
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/CURRENT_STATE.md`

Redaktioneller Scope bleibt separat:
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/TEXT_REDAKTION/CURRENT_STATE.md`

Diese Datei ändert keinen Plugin-/Release-Status.

## 2. Was der vorhandene Kategorie-Workflow bereits belegt kann

Die verifizierte R10-/V1.8.x-Linie besitzt bereits allgemeine Mechanismen für:
- Search-Intent-Prüfung;
- Keyword-Ownership;
- Kannibalisierungsprüfung;
- Global-/Cluster-Coverage;
- Spezialisierungs-/Residual-Coverage;
- Research-Evidenz;
- stabile Strukturidentität über `concept_id`.

Damit existiert bereits ein allgemeiner technischer Unterbau für die Frage:
**Sind zwei Struktur-/Keyword-Kandidaten inhaltlich zu nah oder konkurrieren sie?**

## 3. Was V1.9.0 tatsächlich ergänzt

Autoritative Hobby-Depot-Pluginakte:
`PROJEKTE/HOBBYRAUSCH/PLUGINS/PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`

Dort exakt gebunden:
- Plugin: `Affiliate-Portal Kategorie-Workflow V1.9.0 Hobby Depot Stage Hardlock`;
- Installer: `AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.9.0_HOBBY_DEPOT_STAGE_HARDLOCK.zip`;
- Installer SHA-256: `79d914e6896c36c0022dbae25c7c3ec24923dc453eadc499ef6cd1b88fcd83a1`;
- Source: `QUELLCODE_KATEGORIE_WORKFLOW_V1.9.0_HOBBY_DEPOT_STAGE_HARDLOCK.zip`;
- Source SHA-256: `b63fbedaf4a474923ce6946cafec45faa5ebcea4de36cd534dd9c546d089c3c9`;
- lokale Prüfung: 241/241 PASS für Source und Fresh-Unpack-Installer.

Der V1.9.0-Fix betrifft den **Ablauf-/Stage-Hardlock**:
- veraltete spätere Aktionen blockieren;
- abhängige Downstream-Pakete bei neuem Upstream-Stand invalidieren;
- READ_ONLY_PREVIEW darf nicht in einen alten Deploymentpfad springen;
- aktives Deployment blockiert neuen Upstream-Import bis Rollback.

**V1.9.0 ist damit kein neuer FAQ-/Artikel-Ownership-Fix.**

## 4. Aktuelle Beweisgrenze V1.9.0

Die oben genannten Dateinamen, Hashes und Testergebnisse sind in der autoritativen Pluginakte gebunden.

Im aktuell geprüften Campus-Branch und im Branch `hobbydepot/category-workflow-v1-20260926` liegen die genannten V1.9.0-ZIP-Bytes jedoch nicht als direkt erneut prüfbare Dateien im Git-Baum.

Daher gilt:
- V1.9.0-Identität: **DOKUMENTIERT UND GEBUNDEN**;
- frühere 241/241-Prüfung: **DOKUMENTIERT**;
- frische erneute Byte-/Quellcodeprüfung in diesem Chat: **NICHT MÖGLICH, SOLANGE DIE EXAKTEN ZIP-BYTES NICHT GEBUNDEN VORLIEGEN**.

Keine Rekonstruktion aus älteren Versionen.

## 5. Was Hobby Depot heute noch nicht belegt erzwingt

Der neue Buchbinden-Vertrag lautet:

**Ein Beitrag = genau ein Intent-/Keyword-Owner.**

Zusätzlich:
**FAQ darf nur einen Intent besitzen, der nicht bereits Einstieg, Ausrüstung, Material, Techniken/Praxis oder Fragen/Probleme gehört.**

Dafür fehlt aktuell der End-to-End-Beweis im Hobby-Depot-Artikelweg.

Grund:
`HOBBYRAUSCH/TEXT_REDAKTION/CURRENT_STATE.md` steht weiterhin auf **NEU / LEER**.

Es ist deshalb nicht belegt, dass vor einer Hobby-Depot-Artikelerstellung technisch geprüft wird:
1. welcher Leaf den Intent besitzt;
2. ob derselbe Intent schon einem anderen Beitrag zugeordnet ist;
3. ob ein als FAQ geplanter Beitrag tatsächlich ein eigenständiger Restintent ist;
4. ob eine bloße Frageform fälschlich als FAQ-Eigenintent behandelt wird.

## 6. Vorhandene Referenz aus Pferde Atelier

Im Pferde-Atelier existieren bereits technische Mechanismen für:
- Pre-Title-Duplicate-Prüfung;
- Keyword-Ownership;
- Duplicate-/Cannibalization-Blockade;
- gebundene Search-Intent-Schlüssel.

Diese Mechanismen sind **Referenz**, aber nicht automatisch Hobby-Depot-Autorität.

Es darf daher nichts blind kopiert oder als bereits aktiv behauptet werden.

## 7. Minimaler technischer Bedarf aus dem Buchbinden-Pilot

Benötigt wird kein neues Fachsystem, sondern eine allgemeine Prüfung vor Artikelpromotion/-planung:

Eingabe je Artikelkandidat:
- primärer Intent;
- primäres Keyword/Keyword-Cluster;
- Owner-Leaf;
- eindeutige Artikelidentität.

Prüfung:
- gleicher/semantisch gleicher Intent bereits vergeben → BLOCKED oder bestehendem Owner zuordnen;
- FAQ-Kandidat kollidiert mit anderem Leaf-Owner → FAQ-Promotion BLOCKED;
- unklarer Owner → nicht freigeben;
- ein Owner vorhanden → Kandidat darf in genau diesem Leaf weiterlaufen.

Die konkrete technische Umsetzung darf erst nach frischer Bindung des exakten V1.9.0-Quellstands entschieden werden.

## 8. Exakter technischer nächster Schritt

**Keine Pluginänderung.**

Zuerst die exakten V1.9.0-Source-/Installer-Bytes wieder als autoritativ prüfbare Originale binden und gegen die dokumentierten SHA-256 prüfen.

Danach ausschließlich prüfen:
- ob der vorhandene Kategorie-Workflow die neue Cross-Leaf-Ownership bereits vollständig abbilden kann;
- ob der vorhandene Pferde-Atelier-Artikel-Gate allgemeingültig wiederverwendbar ist;
- welcher kleinste fehlende Mechanismus für Hobby Depot tatsächlich übrig bleibt.

Erst dann ist eine technische Änderung zulässig.

## 9. Konzept-Ergebnis

Für den Buchbinden-Pilot ist die fachliche Trennung jetzt definiert.

Offen bleiben zwei getrennte Beweise:
1. **FAQ-Tragfähigkeit:** DataForSEO-/SERP-Evidenz muss mindestens 3, bevorzugt 4+ eigenständige FAQ-Restintents zeigen; sonst nicht künstlich auffüllen.
2. **Technische Artikelsperre:** Hobby Depot muss vor Artikelproduktion dieselbe eindeutige Ownership-Regel technisch fail-closed erzwingen.

Der bestehende SEO-Kategorie-Workflow und der leere Text-Redaktionsscope dürfen dabei nicht miteinander verwechselt werden.
