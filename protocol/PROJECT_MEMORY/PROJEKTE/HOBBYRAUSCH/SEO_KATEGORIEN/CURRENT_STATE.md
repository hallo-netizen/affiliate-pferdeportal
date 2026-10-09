# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-09
STATUS: RULE 2.7 FAIL-CLOSED KANDIDAT LOKAL PASS / LIVE 2148-PLAN VERWORFEN / FINALER LIVE-DRY-RUN AUSSTEHEND

## Autoritative Bindung

Zielvertrag:
`ZIELVERTRAG_HD001_AUTOMATISCHE_SEO_HIERARCHIE_20261003.md` – Fassung 2.7.

Technische Plugin-Wahrheit:
`../PLUGINS/PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`.

Aktuelle Evidence:
`HD001_RULE27_FAILCLOSED_FINAL_LOCAL_ACCEPTANCE_20261009.md`.

## Aktueller Live-Stand

WordPress läuft wieder auf der 1.14.8-Codebasis.

Der aktuell sichtbare Screen `Kategorien → Finaler Zielbaum` zeigt einen PASS-Dry-Run des inzwischen verworfenen 2148er Rule-2.7-Profils:
- Zielobjekte 2148;
- CREATE 419;
- ADOPT 0;
- UPDATE 1729;
- UNCHANGED 0;
- ARCHIVE 6;
- EDITORIAL-DEMOTION 0;
- Provider 0;
- Strukturwrites 0.

Dieser Plan ist noch NICHT synchronisiert und darf NICHT synchronisiert werden.

## Warum der aktuelle 2148er Plan verworfen ist

Der Nachholcheck fand 46 optionale `Ausrüstung & Kosten`-Leafs, die nur aus generischen Template-Intents erzeugt worden waren.

Das ist für Zielvertrag 2.7 nicht ausreichend belegt.

Fail-closed wurden diese 46 Leafs aus dem neuen Kandidaten entfernt. Bestands-Leafs bleiben erhalten.

## Aktueller lokal freigegebener Kandidat

`HD001_V1.14.8_RULE27_FAILCLOSED_COMPLETE_ONE_SYNC_HARDPASS.zip`

SHA-256:
`0ae09fa5d75656416a0e4e7c1bb4fab74e01e776c2e36b13b8b6734a9efc5c0c`

Revision:
`HD-TARGET-3P-RULE27-FAILCLOSED-COMPLETE-20261009+bacb614f00854923`

Wesentliche Fachziele:
- 8 Hauptwelten bleiben Root;
- Mega-Menü max. 10 Kinder je Welt;
- Technik = 9 sichtbare Kinder über `RC & Modelltechnik`;
- Fertigen bleibt 10;
- 279 HOBBY_HUBs;
- bestehende sinnvolle Leafs bleiben;
- FAQ sichtbar an allen 279 Hubs;
- fehlende Einstiegsabdeckung ergänzt;
- keine künstliche Gesamtobergrenze auf der Content-Ebene;
- 12 Magazin-Kacheln nach 2.7;
- keine Kategorie unter Kategorie;
- keine Hard-Deletes;
- DataForSEO ist keine Strukturautorität.

Fail-closed Zielstand:
- 2102 aktive physische Zielobjekte;
- 1665 aktive CORE-Content-Kategorien;
- Hub-Verteilung 78×5 / 139×6 / 55×7 / 7×8.

## Frische lokale Abnahme

Gegen den realen 1.14.8-Live-Baseline-Stand frisch wiederholt:
- Dry-Run PASS: 373 CREATE / 0 ADOPT / 1729 UPDATE / 6 ARCHIVE / 0 DEMOTE;
- Full Sync COMPLETE: 2102/2102 Readback;
- Frontend-Readback PASS;
- 279/279 HOBBY_HUB-Gate PASS;
- Header PASS;
- zweiter Dry-Run: 2102 UNCHANGED / 0 Writes;
- PHP-Lint 33/33 PASS;
- ZIP-Integrität PASS.

Lokaler PASS ist ausdrücklich KEIN Live-PASS.

## ERSTER OFFENER BLOCKER

`HD001_RULE27_FAILCLOSED_LIVE_DRYRUN_PENDING`

Der aktuelle 2148er Live-Plan ist veraltet. Der 2102er fail-closed Kandidat ist noch nicht live geprüft.

## EXAKT EINE NEXT ACTION

Den aktuellen 2148er Plan NICHT synchronisieren.

Stattdessen exakt
`HD001_V1.14.8_RULE27_FAILCLOSED_COMPLETE_ONE_SYNC_HARDPASS.zip`
installieren/ersetzen und genau EINEN neuen read-only `Finalen Delta-Dry-Run` ausführen.

Erwartung ohne Drift:
`PASS / Zielobjekte 2102 / CREATE 373 / ADOPT 0 / UPDATE 1729 / UNCHANGED 0 / ARCHIVE 6 / DEMOTE 0 / Provider 0 / Writes 0`.

Danach JSON exportieren und prüfen. Vor dieser Prüfung KEIN Sync.

## NICHT ANFASSEN

- keine 1.14.9/1.14.10-Wiederbelebung;
- keine Keyword-Ideas-Tiefenrecherche;
- keine neue Architektur;
- keine Bestands-Leaf-Löschung;
- kein Sync des aktuell sichtbaren 2148er Plans;
- keine weitere 10er-/16er-Pilotdatei.
