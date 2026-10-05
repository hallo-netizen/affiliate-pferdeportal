# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-05
STATUS: V1.9.9 PFERDEATELIER-TAXONOMIE LOKAL HARD PASS / LIVE-INSTALLATION UND REALER FRONTEND-READBACK OFFEN

## Live-Wahrheit

Livebestand wurde während der lokalen Prüfung nicht verändert.

Real zuletzt beobachtet:
- `Buchbinden` ist sichtbar;
- die Content-Kategorien waren im bisherigen Live-Stand auf der Seite nicht sichtbar.

V1.9.7 und V1.9.8 sind verworfen und dürfen nicht installiert werden.

## Harte Root Cause

Der funktionierende Pferdeatelier-Aufbau wurde erneut gegen die reale Portalstruktur und das reale Template-Kit geprüft.

Bewährtes Muster:
- Level 1–3 = echte WordPress-Seiten über `post_parent`;
- Level 4 = echte WordPress-`category`-Terme mit `parent=0`;
- keine technischen Bridge-Terme;
- Kategorien besitzen kontextuell eindeutige Namen/Slugs, z. B. `FAQ Trensen` / `trensen-faq`;
- die Ebene-3-Seite ermittelt die zugehörigen Kategorien über den fachlichen Produkt-/Seitenkontext und rendert sie sichtbar.

V1.9.8 hatte dieses Muster falsch mit technischen Bridge-Termen nachgebaut.

## V1.9.9 – korrigierter lokaler Kandidat

V1.9.9 übernimmt das Pferdeatelier-Prinzip ohne Verbindung zum Pferdeportal:

- Page-Hierarchie 1–3 nativ;
- Content-Leafs bleiben echte Root-`category`-Terme;
- kein Bridge-Term;
- stabile logische Bindung über `_apkw_parent_concept_id`;
- technischer Speichername wird kontextuell eindeutig, z. B. `Einstieg Buchbinden`;
- technischer Slug bleibt kontextuell, z. B. `buchbinden-einstieg`;
- sichtbares Frontend-Label bleibt kurz: `Einstieg`;
- bestehende Buchbinden-Term-IDs bleiben erhalten;
- Magazin bleibt eigene `journal_cat`;
- HivePress bleibt eigene `hp_listing_category`;
- keine automatische Löschung;
- Sparse-/Delta-Erweiterung bleibt erhalten.

## Harte lokale Prüfung

Wichtiger Recheck:
Der frühere einzelne Test `full-e2e-positive.php` war standalone nicht belastbar und fiel bereits in der unveränderten alten V1.9.8-Quelle an der DataForSEO-Evidenzbindung durch.
Dieser Scheintest wurde verworfen/korrigiert; der tatsächliche vollständige Positivlauf ist jetzt standalone grün.

Frischer V1.9.9-Stand:
- Regression: 270/270 PASS;
- Full Builder Flex: PASS;
- echter Buchbinden-Altbestand: PASS;
- kompletter Positiv-E2E: PASS;
- kompletter Negativ-E2E: PASS;
- Fresh-Source nach ZIP-Entpacken: erneut alles PASS;
- Runtime Source↔Installer: 19/19 byteidentisch;
- Installer PHP-Lint: 19/19 PASS.

Realer Buchbinden-Altbestand:
- bestehende V1.9.4-Bindungen werden direkt erkannt;
- Einstieg / Ausrüstung / Material / Techniken & Praxis werden ohne Bridge sichtbar;
- bestehende vier Term-IDs bleiben erhalten;
- kontextuelle Umbenennung kann kontrolliert auf denselben IDs erfolgen;
- Magazin/HivePress leaken nicht in Content.

## Negativabdeckung

BLOCKED bei:
- unbekanntem Parent;
- unbelegtem DataForSEO-Keyword;
- doppeltem Leaf unter demselben Hobby;
- fehlendem Marketplace-Pillar;
- stillem Entfernen bestehender Knoten;
- manipuliertem `_apkw_parent_concept_id`;
- Page-Parent-Drift;
- neuer Kategorie ohne neue Research-Evidenz;
- Mutation nach Approval.

## Artefakte

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.9.9_PFERDEATELIER_TAXONOMY_E2E_HARD_PASS.zip`

SHA-256:
`601a7c7e8a796a12cb9f27388899cdd82264e460314284e29f5ef0018c33e05a`

Source:
`QUELLCODE_KATEGORIE_WORKFLOW_V1.9.9_PFERDEATELIER_TAXONOMY_E2E_HARD_PASS.zip`

SHA-256:
`6ace7bb651025729da6a80d055076c689ee5ff3ba619ec783c1bebb07cda25e9`

## ERSTER OFFENER BLOCKER

`HD001_V199_LIVE_INSTALL_AND_FRONTEND_READBACK_OPEN`

## NEXT ACTION

Exakt V1.9.9 installieren.
Kein Reset, keine neue Research-Runde.

Danach den vorhandenen Buchbinden-Stand einmal durch den vorgesehenen Publish/Republish-Weg laufen lassen und das echte Frontend prüfen.

PASS erst, wenn die Seite `Buchbinden` die vier Content-Kategorien sichtbar zeigt.
