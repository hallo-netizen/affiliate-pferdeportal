# PRODUKTVERGLEICH – PROTOKOLL-NACHHOLUNG / FORTSETZUNG TEIL 2 – 2026-09-11

## ROLLE

Chronologische Fortsetzung von `PROTOKOLL_NACHHOLUNG_20260911.md`.
Diese Datei ist **keine** CURRENT_STATE-, Ziel- oder Fehlerquelle.

Aktuelle Standwahrheit: `CURRENT_STATE.md`.
Aktuelle Arbeit/NEXT ACTION: `HOBBYRAUM.md`.
Einzige detaillierte Fehlerquelle: `FEHLERQUELLEN.md`.
Verbindliches Ziel: `ZIELVERTRAG_V2.md`.

## AKTE 86

`AKTENSCHRANK/86_PROFILE_FACT_MATRIX_HUFSCHLAGRAEUMER_REITPLATZBEWAESSERUNG_MOBIL_WEIDEPFLEGEGERAETE_20260911.md`

Source-bound, nicht materialisiert:
- `hufschlagraeumer`;
- `reitplatzbewaesserung-mobil`;
- `weidepflegegeraete`.

Wesentliche Negativ-/Fail-closed-Grenzen:
- Hufschlagräumer: Handgerät, batteriegetriebenes Standalone-Gerät und Planer-Anbaugerät sind getrennte Subtypen; vorhandene Evidence erzeugt noch kein künstliches Cross-Brand-Paar über Subtypgrenzen hinweg;
- mobile Reitplatzbewässerung p170 bleibt strikt getrennt von fester Beregnung p163; Cross-Family-Pairing nur bei belastbar gebundener Hersteller-/OEM-Identität;
- Weidepflegegeräte p171 erste V1-Klasse = mechanischer 3-m-Grünlandstriegel ohne montiertes Sägerät; Nachsaat p172 und passive Weideschleppen p173 bleiben separat.

Keine technische Materialisierung. Kein Plugin-PASS daraus abgeleitet.

## AKTE 87

`AKTENSCHRANK/87_PROFILE_FACT_MATRIX_NACHSAAT_PFERDEWEIDEN_WEIDESCHLEPPEN_UNKRAUTSTECHER_20260911.md`

Source-bound, nicht materialisiert:
- `nachsaat-fuer-pferdeweiden`;
- `weideschleppen`;
- `unkrautstecher`.

Commit der Aktenanlage / Branch-HEAD vor der Abschlussnachholung:
`97daffebb527c08e4611ed66b1a5b47c780d6029`.

Wesentliche Negativ-/Fail-closed-Grenzen:
- p172 = physische Saatgutmischung für die Nachsaat bestehender Pferdeweiden; Saatgut wird niemals mit Nachsaatmaschine/Striegelkonfiguration gepaart;
- Saatmengen nur bei identischer Aussaatform vergleichen; Nachsaat/Durchsaat != Übersaat;
- p173 = passive Gussstern-/Netz-Grünlandegge/Wiesenschleppe; nicht mit Federzinken-Grünlandstriegel p171 vermischen;
- p174 erste V1-Klasse = langstieliger Ampfer-/Pfahlwurzelstecher für Grünland/Weide; allgemeine Garten-Löwenzahnstecher bleiben außerhalb dieser ersten Weideklasse;
- finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin aus aktuellem Product Knowledge.

Keine technische Materialisierung. Kein Plugin-PASS daraus abgeleitet.

## ABSCHLUSS-/NACHHOLPRÜFUNG NACH AKTE 87

Frisch aus den autoritativen Quellen gelesen:
- Branch `hobbyroom/productvergleich-workflow-v070-20260908`;
- realer Head vor der Nachholung `97daffebb527c08e4611ed66b1a5b47c780d6029`;
- `CURRENT_STATE.md`;
- `HOBBYRAUM.md`;
- `FEHLERQUELLEN.md`;
- `ZIELVERTRAG_V2.md`;
- zentrales `protocol/PROJECT_MEMORY/FEHLERREGISTER.md`;
- finale V1-Disposition Akte 59/60;
- Registry `affiliate-portal-router/assets/portal-structure-v279.json` für p175–p179.

### Neuer Governance-Befund

`PV-GOV-20260911-003`:
- Akte 87 existierte real, aber CURRENT_STATE/HOBBYRAUM standen noch bei Akte 86 / 74 zusätzlichen source-bound Gruppen;
- FEHLERQUELLEN stand noch bei Akte 85 / 71 Gruppen und einem bereits abgearbeiteten NEXT ACTION;
- das bisherige Nachholprotokoll endete bei Akte 85.

Damit bestand eine dokumentarische, nicht technische, konkurrierende Standwahrheit.

### Nachholung

Nachgezogen:
- `CURRENT_STATE.md` auf Akten 62–87 / **77 zusätzliche source-bound Gruppen**;
- `HOBBYRAUM.md` auf Akte 87 / 77 Gruppen / echten nächsten Arbeitsblock;
- `FEHLERQUELLEN.md` um `PV-GOV-20260911-003`, Akten 62–87 und den echten offenen Block;
- dieses Teil-2-Protokoll für Akte 86, Akte 87 und die Abschlussprüfung.

Das zentrale `FEHLERREGISTER.md` bleibt korrekt ein reiner Wegweiser und verweist weiterhin nur auf `PROJEKTE/PFERDE_ATELIER/PRODUKTVERGLEICH/FEHLERQUELLEN.md`.

## ZIEL / WARUM / ARCHITEKTUR

`ZIELVERTRAG_V2.md` bleibt unverändert.

Keine neue Systemarchitektur in dieser Fortsetzung:
- Research/Product Knowledge liefert Fakten;
- SEO erst nach fachlich zulässigem Kandidatenuniversum;
- finale Paarentscheidung ausschließlich im Produktvergleichs-Plugin;
- source-bound Profilspecs sind Vorbereitung, keine technische Materialisierung;
- kein Writer/Draft/Publish aus diesem Büro.

Die neuen Trennregeln der Akten 86/87 sind gruppenspezifische fachliche WHAT/WHY-Grenzen und sind in den jeweiligen Akten dauerhaft gebunden; kein zusätzlicher allgemeiner Campus-Standard wurde daraus abgeleitet.

## TESTS / PASS-GRENZE

In dieser Fortsetzung tatsächlich ausgeführt:
- frischer Branch-/HEAD-Read;
- frischer Read der Stand-/Fehler-/Zielquellen;
- Registry-Folge p175 `weidewalzen`, p176 `solar-weidepumpen`, p177 `weidebrunnen`, p178 `wassertroege-fuer-weiden`, p179 `weidetimer` direkt gegengeprüft;
- p177 `weidebrunnen` gegen finale 25er V1-NOT-APPLICABLE-Disposition gegengeprüft;
- Akte 86 und Akte 87 als real vorhandene source-bound Specs gegengeprüft;
- negative Governance-Prüfung auf veraltete Standwahrheiten durchgeführt und repariert.

Nicht ausgeführt:
- kein UPC-Code geändert;
- keine technische Materialisierung der 77 zusätzlichen source-bound Specs;
- keine neue Plugin-Regression;
- kein neuer PHP-Lint;
- kein neuer Fresh-ZIP-Test;
- kein WordPress-Live-Test von UPC 0.8.6;
- kein Codex;
- kein Merge;
- kein Publish.

Historische UPC-0.8.6-PASS-Receipts bleiben vorhandene Belege, wurden hier nicht neu ausgeführt.

## NEXT ACTION

Autoritative Folge nach Akte 87:
1. `p175 weidewalzen`;
2. `p176 solar-weidepumpen`;
3. `p177 weidebrunnen` = V1-NOT-APPLICABLE, überspringen;
4. `p178 wassertroege-fuer-weiden`;
5. danach `p179 weidetimer`.

Nächster fachlich zulässiger Profilblock:
`weidewalzen` -> `solar-weidepumpen` -> `wassertroege-fuer-weiden`.

Arbeitsweg:
source-bound Faktenmatrix -> gleiche Nutzungsklasse/Subtypen hart normalisieren -> Positiv-/Negativgrenzen -> Produktgegenprüfung -> sinnvoll bündeln -> erst danach technische Materialisierung -> vollständiger Positiv-/Negativ-/Mutation-/Fresh-ZIP-Test.

Kein Codex, bis der Nutzer ihn ausdrücklich wieder freigibt.
Kein Merge.
Kein Publish.
