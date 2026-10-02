# Übergabe – AFFILIATE_ZENTRALE – 2026-10-02

Rolle: kurzer Wegweiser. Diese Datei ist **keine Current-Autorität** und enthält keine eigene NEXT-ACTION-Wahrheit.

## Einstiegspunkt / Bürotür

`release/affiliate-zentrale/AGENTS.md`
→ `control/release-governance/CURRENT_RELEASE.json`
→ Governance-/Frischecheck
→ ausschließlich `execution_state` der Current-Autorität folgen.

Der temporäre `AFFILIATE_HOBBYRAUM` ist aktuell nicht aktiv und keine Statusquelle.

## Zuständige eine Current-Autorität

`control/release-governance/CURRENT_RELEASE.json`

Frisch geprüft am 2026-10-02:
- generation: 173
- workstream: `AFFILIATE_ZENTRALE`
- mode: `ENFORCED`
- active candidate: `6.72.176`
- candidate status: `RELEASED`
- release_allowed: `true`
- source manifest: `c01945cbd0e9aa4b107018260bfc833a8fc4f69aaee1f0e7a73f96391c2ffb4d`
- 27 Source-Dateien
- final installer SHA-256: `32f7bfd0cb316ebbb0e130d0ab310019d66cdbdebe0ce6085fa0ed2f1ec0b79b`

Die aktuell installierte reale WordPress-Version wurde in diesem Abschluss nicht autoritativ zurückgelesen. Nicht raten.

## Zielvertrag

Aktuelle gebundene Arbeitsabsicht aus Current:

- realen Hub-1/Hub-2-`hub_after_cards`-Mount reparieren;
- eBay-BUSINESS-Produktkarten dürfen später verworfene Langbeschreibungen nicht mehr im initialen Karten-HTML ausliefern;
- vollständige Quelldaten, PRIVATE-eBay-Detailbeschreibung und Nicht-eBay-Verhalten erhalten;
- Ziel-/Slotlogik aus 6.72.175 erhalten;
- alle früheren Performance-/Funktions-Hardlocks erhalten.

Übergeordnete verbindliche Verträge bleiben u. a.:
- `protocol/AFFILIATE_RELEASE_BANNER_AUTOMATION_TARGET_CONTRACT_20260901.md`
- `protocol/AFFILIATE_RELEASE_PERFORMANCE_OPTIMIZATION_TARGET_20260924.md`
- `protocol/AFFILIATE_RELEASE_PERFORMANCE_CLEANUP_TARGET_20260922.md`
- `protocol/AFFILIATE_RELEASE_EBAY_KISS_STORAGE_CLEANUP_TARGET_20260930.md`
- `protocol/AFFILIATE_RELEASE_ERROR_REGISTER.md`

## Was wurde gemacht

1. 6.72.173: historisch feste eBay-Katalog-Sollzahlen 329/1124 durch reale dynamische Katalogprüfung ersetzt.
2. 6.72.174: Realziel-Evidenz für Banner ergänzt.
3. 6.72.175: vollständige automatische Kette korrigiert:
   - mehrere verwandte Ziele korrekt ranken;
   - exakte Ziel-URL/Slug-Evidenz priorisieren;
   - Zielkontext → korrekten Slot ableiten;
   - alten Vollpool-Cursor beim Versionswechsel genau einmal verwerfen;
   - Alt-Veto-Migration auf richtige Control-Tabelle binden.
4. 6.72.176:
   - fehlenden realen Server-Mount für `hub_after_cards` auf Hub-1/Hub-2 ergänzt;
   - eBay-BUSINESS-Kartenbeschreibung ausschließlich in Hub-/Kategorie-Produktrastern aus dem ausgelieferten Karten-HTML entfernt, Quelldaten unverändert.
5. Targeted WordPress/MariaDB run `36997037385`: SUCCESS.
6. Full gate run `36997283155`: SUCCESS.
7. Fehlerregister nachgeholt:
   - AFF-ERR-042: Teilprüfung der Bannerkette / fehlender realer Hub-Mount.
   - AFF-ERR-043: eBay-Langbeschreibung als später verworfener HTML-/DOM-Payload.
8. Performance-Preservation-Recheck:
   `release/affiliate-zentrale/evidence/affiliate_router_v672176_performance_preservation_recheck_20261002.md`

## Performance-Hardlock – NICHT ANFASSEN

Direkter Vergleich released 6.72.175 → current 6.72.176:

- exakt 27 Plugin-Dateien auf beiden Ständen;
- nur zwei Plugin-Dateien geändert:
  - `pferdeportal-affiliate-router.php`
  - `readme.txt`
- byteidentisch geblieben:
  - `includes/trait-ppar-automation-suite.php`
  - `includes/trait-ppar-output-objects.php`
  - `includes/trait-ppar-ebay.php`
  - `includes/trait-ppar-idealo.php`
  - `includes/trait-ppar-housekeeping.php`

Im geänderten Hauptrouter textidentisch zu 6.72.175:
- request-local ranking/cache helpers;
- `select_category_product_campaign_fast_v672171()`;
- `ranked_campaign_candidate_pool()`;
- `ranked_campaigns_for_slot()`;
- `category_product_provider_mix_v672133()`.

Funktional geändert wurden dort nur:
- `render_banner()`
- `auto_inject_template_affiliate_slots()`
- Versionsmetadaten.

Kein Rückbau/Überschreiben der 6.72.170/171/172/173/174/175-Hardlocks zulässig.

## Exakter Status quo

Current-Zustand: `FINAL_RELEASE_BOUND`.

6.72.176 ist Source-/Gate-seitig released, aber der reale WordPress-Live-Readback ist noch offen.

Erster offener Blocker dieses aktuellen Scopes:
**Real WordPress install/readback 6.72.176 fehlt.**

Nicht autoritativ belegt und daher nicht behaupten:
- welche Affiliate-Version aktuell live installiert ist;
- ob der Schabrackendesigner live bereits sichtbar ist;
- ob der eBay-Langtext-Flash live bereits verschwunden ist.

## Exakt eine NEXT ACTION

Aus der Current-Bindung:

**6.72.176 einmal real installieren/verwenden und anschließend genau zwei Live-Readbacks prüfen:**
1. Schabrackendesigner erscheint als breiter `hub_after_cards`-Banner am richtigen Schabracken-Ziel.
2. eBay-BUSINESS-Produktkarten zeigen beim Laden keinen langen Beschreibungstext-Flash mehr und liefern den unnötigen Karten-Payload nicht mehr aus.

Kein neuer Pluginbuild vor diesem Readback.

## Danach, nur wenn der Live-Readback PASS ist

Current nennt anschließend:
- AF-078 eBay PRIVATE rootfix;
- AF-079 eBay BUSINESS Live-Diagnose/Rootcause;
- Dead-Code-Cleanup in kleinen getesteten Batches.

Diese Punkte sind **nicht** die aktuelle NEXT ACTION.

## Fehlerprotokoll – aktueller Arbeitsblock

### Behoben/source-gated
- eBay-Katalogvalidator mit historischen festen Sollzahlen → 6.72.173.
- Schabrackendesigner scheitert vor Realziel-Ranking → 6.72.174.
- verwandte Mehrziele/Slotkontext/Cursor/Alt-SQL → 6.72.175.
- korrekte Ziel-/Slotplanung ohne realen Hub-Mount → AFF-ERR-042 → 6.72.176.
- eBay-BUSINESS-Langbeschreibung wird später vom Design verworfen, aber initial ausgeliefert → AFF-ERR-043 → 6.72.176.

### Offen, aber nachgelagert
- AF-078: PRIVATE kann in HivePress gezählt, aber durch unvollständigen Candidate/Public-Checkpoint unsichtbar bleiben. Lokale Logiksimulation vorhanden; Source-Fix noch nicht ausgeführt.
- AF-079: eBay BUSINESS fehlend; exakter erster Live-Blocker noch nicht bewiesen. Keine Ursache raten.
- Plugin-Verschlankung: 44 starke Dead-Code-Kandidaten inventarisiert; noch nicht löschen. Nur kleine Batches nach Live-Readback und vollständigen Regressionen.

### Permanente Nicht-Wiederholungsregeln
- kein PASS aus Teiltest;
- kein Plugin-ZIP vor Positiv-, Negativ-, WordPress/MariaDB- und Gesamtgate;
- keine Versionskaskade;
- keine alten Performancepfade überschreiben;
- keine Provider-/Slot-/Veto-/PRIVATE-/BUSINESS-/Coverage-/Quality-/Health-/Tracking-Semantik nebenbei verändern;
- keine alte Source rekonstruieren oder als Basis verwenden.

## Plugin-Refs

Current final artifact:
`release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.176.zip`

SHA-256:
`32f7bfd0cb316ebbb0e130d0ab310019d66cdbdebe0ce6085fa0ed2f1ec0b79b`

Full-gate evidence:
`release/affiliate-zentrale/evidence/affiliate_router_v672176_hub_mount_ebay_payload_full_gate_20261002.md`

Performance preservation:
`release/affiliate-zentrale/evidence/affiliate_router_v672176_performance_preservation_recheck_20261002.md`

Fallback-/historische Dateien sind keine Current-Autorität.

## Neuer Chat – exakter Einstieg

1. `release/affiliate-zentrale/AGENTS.md` lesen.
2. `control/release-governance/CURRENT_RELEASE.json` lesen.
3. Frischecheck durchführen.
4. Wenn Current weiterhin 6.72.176 / `FINAL_RELEASE_BOUND` / gleicher Manifest-SHA ist: **keine Vollrekonstruktion**.
5. Direkt die eine Current-NEXT-ACTION ausführen: realen 6.72.176-WordPress-Readback.
6. Erst bei belegter Änderung nur das Delta untersuchen.
7. Diese Übergabe niemals als Current verwenden.
