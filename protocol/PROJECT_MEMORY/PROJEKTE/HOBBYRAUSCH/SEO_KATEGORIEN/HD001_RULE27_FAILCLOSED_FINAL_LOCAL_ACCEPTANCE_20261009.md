# HD-001 – RULE 2.7 FAIL-CLOSED FINAL LOCAL ACCEPTANCE

STAND: 2026-10-09
ROLLE: EVIDENCE / KEINE CURRENT-WAHRHEIT

## Ausgangslage live

Letzte sichtbare Live-Evidence vor dieser Korrektur:
- WordPress → Kategorien → Finaler Zielbaum;
- Plugin-Codebasis 1.14.8;
- aktueller Live-Dry-Run: PASS;
- Zielobjekte: 2148;
- CREATE 419;
- ADOPT 0;
- UPDATE 1729;
- UNCHANGED 0;
- ARCHIVE 6;
- EDITORIAL-DEMOTION 0;
- Provider-Aufrufe 0;
- Strukturwrites 0;
- der aktuelle Plan war noch NICHT synchronisiert.

Dieser 2148er Plan ist NICHT mehr freigegeben.

## Warum der 2148er Plan verworfen wurde

Im lokalen Nachholcheck wurden 46 neu erzeugte Leafs `Ausrüstung & Kosten` identifiziert, die nur aus generischen Template-Intents entstanden waren.

Damit war für diese 46 Leafs die Zielvertrag-2.7-Bedingung „mindestens 3 eigenständige sinnvolle Beitragsintentionen nach Ownership-Dedupe“ nicht belastbar belegt.

Fail-closed-Korrektur:
- alle 46 nicht belegten optionalen `Ausrüstung & Kosten`-Leafs entfernt;
- keine Bestands-Leafs gelöscht;
- FAQ-/Einstiegsabdeckung, Navigation und Magazinmodell beibehalten;
- keine neue technische Architektur;
- keine DataForSEO-Strukturautorität.

## Aktueller lokal freigegebener Kandidat

Artefakt:
`HD001_V1.14.8_RULE27_FAILCLOSED_COMPLETE_ONE_SYNC_HARDPASS.zip`

SHA-256:
`0ae09fa5d75656416a0e4e7c1bb4fab74e01e776c2e36b13b8b6734a9efc5c0c`

Technische Basis:
`Affiliate-Portal Kategorie-Workflow 1.14.8`

Revision:
`HD-TARGET-3P-RULE27-FAILCLOSED-COMPLETE-20261009+bacb614f00854923`

Delta gegenüber dem vorherigen 2148er Kandidaten:
- exakt eine Paketdatei geändert: `profiles/hobby-depot-v1.json`;
- 46 nicht belegte optionale `Ausrüstung & Kosten`-Leafs entfernt;
- PHP-Code unverändert.

## Zielstand des fail-closed Kandidaten

- 8 geschützte CORE-Welten bleiben Root;
- sichtbare Mega-Menü-Kinder:
  - Gestalten 7;
  - Fertigen 10;
  - Technik 9;
  - Forschen 5;
  - Pflanzen 9;
  - Tiere 7;
  - Bewegen 8;
  - Sammeln 8;
- Technik enthält den neuen gemeinsamen Zwischenbereich `RC & Modelltechnik`;
- 279 HOBBY_HUBs;
- 1665 aktive CORE-Content-Kategorien;
- FAQ sichtbar an allen 279 HOBBY_HUBs;
- fehlende Einstiegsabdeckung wurde ergänzt; bestehende sinnvolle Einstiegs-/Basics-Leafs bleiben Owner;
- keine künstliche 3–6-Gesamtobergrenze;
- HOBBY_HUB-Verteilung:
  - 78 × 5 Leafs;
  - 139 × 6 Leafs;
  - 55 × 7 Leafs;
  - 7 × 8 Leafs;
- 12 Magazin-Kacheln nach Zielvertrag 2.7;
- 0 Kategorie-unter-Kategorie-Kanten;
- 2102 aktive physische Zielobjekte.

## Frisch ausgeführte lokale Prüfung gegen den realen 1.14.8-Live-Baseline-Stand

Dry-Run:
- PASS;
- CREATE 373;
- ADOPT 0;
- UPDATE 1729;
- UNCHANGED 0;
- ARCHIVE 6;
- EDITORIAL-DEMOTION 0;
- errors = [].

Vollständiger Sync mit den echten Plugin-Klassen:
- status = COMPLETE;
- node_count = 2102;
- created = 373;
- updated = 1729;
- adopted = 0;
- archived = 6;
- readback_checked = 2102;
- error = leer;
- Frontend-Readback = PASS;
- HOBBY_HUB category failures = 0;
- Header-Navigation = PASS.

Idempotenz:
- zweiter Dry-Run = 2102 UNCHANGED;
- CREATE/ADOPT/UPDATE/ARCHIVE = 0.

Release-Prüfung:
- PHP-Lint 33/33 PASS;
- ZIP-Integrität PASS;
- SHA-256 erneut geprüft.

## Live-Status

Der fail-closed Kandidat ist NOCH NICHT live installiert und NOCH NICHT live synchronisiert.

Der aktuell im WordPress-Screen sichtbare 2148er Dry-Run darf NICHT synchronisiert werden.

## Nächster Live-Gate

Exakt den fail-closed Kandidaten installieren und genau EINEN neuen read-only Delta-Dry-Run ausführen.

Erwartung ohne Live-Drift:
- PASS;
- Zielobjekte 2102;
- CREATE 373;
- ADOPT 0;
- UPDATE 1729;
- UNCHANGED 0;
- ARCHIVE 6;
- EDITORIAL-DEMOTION 0;
- Provider 0;
- Strukturwrites 0.

Bei jeder Abweichung: NICHT synchronisieren; Ursache zuerst diagnostisch eingrenzen.
