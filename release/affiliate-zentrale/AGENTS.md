# Affiliate-Zentrale – externe Release-Kontrollinstanz

Diese Datei steuert **ausschließlich** den Workstream `AFFILIATE_ZENTRALE` einschließlich eBay.

WICHTIG: Für diesen Workstream gilt **nicht** die STARTMASTER-/`.pferde-capsule`-Eingangstür aus dem Root-Workflow.

## Verbindlicher Start

1. `control/release-governance/CURRENT_RELEASE.json` lesen. Diese Datei ist die einzige maschinenlesbare Entscheidungsinstanz für Ziel, Zustand, Arbeitsbranch und Release-Gates.
2. `python3 control/release-governance/release_guard.py governance-check` ausführen.
3. Auf `affiliate-release-current` zusätzlich `python3 control/release-governance/release_guard.py start --branch "$(git branch --show-current)"` ausführen.
4. Einzige aktuelle Quelle ist `release/affiliate-zentrale/current/affiliate-portal-router/` plus `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt`.

## KISS-Ausführungszyklus

Es gibt nur diesen Zyklus:

`GESAMTTEST -> ERSTER_ECHTER_FEHLER -> GENAU_DIESEN_FEHLER_FIXEN -> GESAMTTEST`

Wenn der Gesamttest vollständig PASS ist:

`GESAMTTEST -> RELEASE_CHECK -> RELEASE`

Regeln:
- Maximal **ein** Arbeitsstrang.
- Bei einem FAIL nur den **ersten belegten Fehler** bearbeiten.
- Keine neue Architektur, keine neue Version und keine Nebenuntersuchung, solange derselbe Fehler offen ist.
- Für einen belegten Fehler dürfen ausschließlich die direkt betroffenen Dateien im kanonischen Source-Tree geändert werden.
- Danach Source-Manifest aktualisieren und alle Evidence, deren Source-Manifest-Bindung dadurch veraltet ist, als stale behandeln.
- Anschließend wieder **ein einziger Gesamt-Gate-Zyklus**, nicht elf manuelle Einzelprojekte.
- Bereits hash-identisch gültige PASS-Evidence wird wiederverwendet.

## Release-Gates

Die einzelnen Pflichtgates in `CURRENT_RELEASE.json` bleiben als Nachweis-Matrix bestehen. Sie sind **keine separaten Arbeitsstränge**. Ein Gesamtlauf darf mehrere Gates gleichzeitig schließen.

Pflichtlogik:
1. alter Fehlerzustand belegt FAIL,
2. aktueller Stand belegt denselben Fall PASS,
3. relevante Gegen-/Fehlerzustände fail-closed,
4. Gesamtworkflow/WordPress/MariaDB soweit gebunden,
5. Installer/Fresh-Unpack/Byteidentität/Final-SHA erst am Ende.

## Verbote

- Keine Base64-, GZIP-, Chunk-, Patch-, ZIP- oder Historien-Rekonstruktion der aktuellen Quelle.
- Keine Versions-, Staging-, Probe- oder Nebenbranches für Release-Arbeit.
- Keine STARTMASTER-Navigation.
- Keine Änderung fremder Workstreams.
- Keine Release-ZIP vor dem finalen Gate.

## PASS und Release

Jeder PASS benötigt Evidence unter `release/affiliate-zentrale/evidence/` mit Evidence-SHA und Bindung an den aktuellen Source-Manifest-SHA.

Vor Freigabe muss `python3 control/release-governance/release_guard.py release-check` PASS liefern.

Wenn ein Gate FAIL ist, lautet der Zustand **FIX_FIRST_FAILED_GATE**. Wenn alle Pflichtgates PASS sind, lautet der nächste Schritt **RELEASE_CHECK**.

## Fach-Evidence-Hardlock für Feed-/Providerdaten

- **Deklarierter Quellen-/Feed-Scope ist niemals Fach-Evidence.** Werte wie `portal_filtered`, `FeedScope=Pferdebedarf`, Providerlabel oder manuelle Scope-Bestätigung dürfen den Transport/Source-Gate freigeben, aber niemals selbst beweisen, dass eine einzelne Produktzeile fachlich ins Pferdeportal gehört.
- Automatische Fachklassifikation muss auf realen Zeilenfakten beruhen: Produkttitel, reale Kategorie/Produkttyp-/Merkmalsdaten und andere tatsächlich vom Anbieter gelieferte Produktinformationen.
- Ein synthetischer Scope darf keine generische Produktphrase in einen Pferde-Treffer verwandeln. NEGATIV-Regressionen müssen diesen Gegenfall bei neuen Provider-/Feedwegen binden.


## CHATWECHSEL-HARDLOCK – ORIGINAL 6.72.308 (08.11.2026)

**Faktisch nachgewiesen:** Der Nutzer hat das originale, vollständige 6.72.308-Plugin als echte ZIP hochgeladen; es wurde geöffnet, gehasht und gegen vorherige Prüfbelege abgeglichen. Exakte Primärakte: `release/affiliate-zentrale/evidence/AFFILIATE_ZENTRALE_6.72.308_ORIGINALZIP_UPLOADBELEG_20261108.md`. Datei `AFFILIATE_ZENTRALE_6.72.308_URSACHENFIX_GESAMTTEST_NUR_TEST.zip`, SHA256 `b4d8547fd2aa134f7f82f568db3a81df54bb7d2131fd0752e76e3f0ca2251fe0`, 5.345.251 Bytes, 66 Dateien, 23 PHP, 3 JSON, CRC PASS, Pluginheader 6.72.308. Die gesamte 6.72.309-Testfassung wurde daraus erstellt und 66/66 gegen den Ursprungsstand verglichen (Prüfakte `evidence/EBAY_6.72.309_KISS_GESAMTQA_20261108.json`).

**WICHTIG – vorhandenes Original und gegenwärtiger Byte-Zugriff sind verschiedene Aussagen.** NIEMALS aus einem GitHub-404, fehlendem ZIP im `affiliate-release-current`-Tree, einem anderen Chat oder einer gerade nicht verbundenen Library folgern, der Nutzer habe das Original nicht bereitgestellt oder es existiere nicht. Der Campus-Vertrag `protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PLUGINS/SYNC_VERTRAG.md` unterscheidet GitHub-Steuerakten ausdrücklich von einem separaten persistenten `/Campus-Plugins/...`-Binärschrank. Ein Schrank-Verbindungsfehler sagt NICHTS über dessen tatsächlichen Bestand.

**Pflicht vor jeder Aussage über die Verfügbarkeit:** (1) diese Primärakten lesen; (2) tatsächlich autorisierte binäre Zugänge aus GitHub-Repository UND Release-Assets, verbundenem Campus-Plugins-Schrank, Library und aktuellen/älteren Conversation-Uploads prüfen; (3) nur dann zwischen `HISTORISCH_BEWIESEN`, `AKTUELL_BYTELESBAR` und `AKTUELLER_ZUGRIFF_NOCH_NICHT_GEKLÄRT` unterscheiden. Keine pauschalen Aussagen `Original fehlt`; keine erneute Uploadforderung allein wegen GitHub-404. 6.72.308 niemals aus 6.72.211 oder Textpatch als angeblich originales ZIP rekonstruieren.

**Installationsgate bleibt streng:** Bewiesener früherer Upload ist kein Ersatz für aktuellen Byte-Readback. Für Gesamt-PASS exakt dieselbe Originaldatei hashen und den vollständigen 6.72.311-BUSINESS-only-Patch gegen diese reale Quelle testen; bis dahin keine Freigabe. Die PRIVATE-Route und eBay-generierte HivePress-Anzeigen sind dauerhaft aus dem Zielbild gestrichen.
