# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-11
STATUS: AKTIV / 0.8.5 LIVE FAIL-CLOSED PASS / UPK 0.5.1 LOCAL HARD PASS / LIVE-MATERIALISIERUNG OFFEN

## AKTUELLER VERGLEICHSKANDIDAT

`universal-product-comparison-0.8.5-prototype.zip`

SHA-256:
`0174051e6584902142f5be5787642426b30aab6c7ba15ef0b07ccbdb4a5844fd`

0.8.5 nicht erneut reparieren.
Es hat live korrekt `PRODUCT_INVENTORY_MISSING` gezeigt und keinen Providerlauf gestartet.

## LIVE-BEFUND

Oben:
- `PAIRING_READY: 1`;
- `PROFILE_MISSING: 166`;
- `POLICY_MISSING: 0`;
- `PRODUCT_INVENTORY_MISSING: 6`;
- `GROUP_KEY_COLLISION: 2`.

Winterdecken:
- Recherchekatalog: 8 Kandidaten / 3 Hersteller;
- Research-Vollständigkeit `UNPROVEN`;
- echtes Inventar 0 Produkte / 0 Hersteller;
- 0 Cross-Family-Paare;
- korrekt fail-closed.

## ROOT CAUSE

Der Lokaltest 0.8.5 prüfte die vorhandenen Recherchekandidaten synthetisch gegen Profile/Policies.
Das war geeignet für Fach-/Paarlogik, aber kein Beweis der echten WordPress-Inventarmaterialisierung.

Keine 130 Live-Paare behaupten.
Die 130 sind nur katalogseitiges Potential **nach** erfolgreicher Live-Quellenprüfung und Materialisierung.

## KISS-KANDIDAT PRODUCT KNOWLEDGE 0.5.1

`universal-product-knowledge-0.5.1-prototype.zip`

SHA-256:
`17ba686ebbfeac774de5224a042e8ea5fcc472b91774c47271e6b585d74960a1`

0.5.1 automatisiert ausschließlich den vorhandenen kanonischen Product-Knowledge-Weg:
- vorhandene freigegebene Recherchegruppen;
- eine Gruppe pro AJAX-Request;
- `UPK_Research::run_product_group()` unverändert;
- echte Herstellerquellenprüfung;
- nur PASS-Produkte/Fakten werden mit dem bestehenden Import materialisiert;
- fachlich BLOCKED sichtbar;
- Security-/Transportfehler STOP;
- Markt-Vollständigkeit bleibt UNPROVEN.

## HARTER LOKAL-PASS

UPK 0.5.1:
- Positiv/Negativ PASS;
- Nonce/Capability PASS;
- sequenzieller Batch PASS;
- vorhandener Einzelgruppenweg erhalten;
- 4 Mutationen korrekt ROT;
- PHP-Lint 5/5;
- Source↔ZIP 8/8;
- Report-Hashes 7/7;
- kein SEO/UPC/Writer/Publish-Eigentum.

Gesamtworkflow-Gegenprüfung:
UPC 0.8.5 gegen exakt finale UPK-0.5.1-ZIP = **35/35 PASS**.

## NEXT ACTION WORDPRESS

1. ausschließlich **Universal Product Knowledge 0.5.1** installieren/ersetzen;
2. Product Comparison 0.8.5 unverändert lassen;
3. WordPress → `Produktvergleich` → `Produktwissen` öffnen;
4. **noch keinen Batch starten**;
5. Screenshot schicken;
6. dort prüfen wir nur:
   - Version 0.5.1;
   - bestehender Einzelgruppenweg erhalten;
   - neuer Button `Alle freigegebenen Recherchegruppen nacheinander prüfen/importieren` sichtbar;
   - keine falsche Vollständigkeitsbehauptung;
7. erst danach genau einen Batch starten;
8. nach Batchende Summary-Screenshot;
9. danach UPC Winterdecken nur read-only neu prüfen.

## LIVE-ERWARTUNG NACH SPÄTEREM BATCH

Keine feste Produkt-/Paarzahl vorhersagen.
Die Herstellerseiten werden live neu geprüft; veraltete/fehlende Quellen dürfen Produkte blockieren.

Erlaubte Aussage danach ausschließlich aus echtem Ergebnis:
- welche Gruppen PASS/PARTIAL/BLOCKED;
- wie viele Produkte tatsächlich materialisiert;
- wie viele echte Herstellerfamilien;
- welche Gruppen danach `PAIRING_READY` werden;
- reales Paaruniversum daraus.

## BLOCK-GRENZE

BLOCK bei:
- UPK-Version falsch;
- Batch umgeht `run_product_group()`;
- Parallel-/Monsterrequest statt Sequenz;
- fehlendem Nonce/Capability;
- falschem COMPLETE-/Markt-vollständig-Status;
- Product Comparison Providerlauf vor Materialisierung;
- Writer/Draft/Publish-Aktivierung.

Kein SEO/TEXT-/ACM-Umbau.
Kein Publish.
