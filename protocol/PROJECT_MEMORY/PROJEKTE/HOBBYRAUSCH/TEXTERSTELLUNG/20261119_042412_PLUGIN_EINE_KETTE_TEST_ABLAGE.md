# Hobbydepot Texterstellung 0.4.24.12 – Original-Workflow-Test / Stand 19.11.2026

## Genau eine installationsfähige WordPress-ZIP
`Texterstellung_Hobbydepot_0.4.24.12_GESPEICHERTE_RECHERCHE_MINI_K0.zip`
in der persönlichen Bibliothek `/Hobby Depot/Plugin-Büro/`, zusätzlich `Texterstellung_0.4.24.12_PRUEFNACHWEISE.json` und erneuerter `Texterstellung-CURRENT.md`.

Dateigröße 512306 Bytes; SHA256 `48a3650138af209d76cd6bdfb48ff2f7e72df352b01bda942ead98cee501f965`; Root `texterstellung-hobbydepot/` ersetzt 0.4.24.11.
Nur drei der ursprünglichen 87 Dateien verändert (84 byte-identisch):
1. `texterstellung.php` Version, Start und admin-gebundene, begrenzte Fortsetzung der originalen providerfreien Queue;
2. `contracts/k0-article-type-capabilities-v1.json` K0-Originalartikelarten aus Pferdeatelier;
3. `original/pste/includes/class-pste-portal-relevance-gate.php` einmalige Portalrelevanz nutzt aktuelle WP-Themenfamilie nur mit eng umgrenzter redaktioneller Absicht (Regeln, Parcours etc.).

Original `PSTE_Breadth_Research_Queue::startExistingOnly(...)` verwendet `provider_fallback_allowed=false`. WICHTIG: PSTE Research Driver hat `EXISTING_ONLY_AUTOREPLAY_DISABLED`, daher startet die UI nicht blind diesen Treiber, sondern setzt dieselbe Originalqueue via auth. AJAX `PSTE_Breadth_Research_Queue::advance` fort. Bei pausiertem/geblocktem Lauf STOP, kein neuer Anbieteraufruf. Nutzer hält die WP-Recherche-Seite offen.

## Quell- und Nachweistests
- Original-PHP 6/6 Themenbeispiele PASS, negativ: Ortsfremdkontext, Modellpark, nicht verbundene WP-Kategorie -> gesperrt.
- Original-K0-Artikelartensnapshot 5/5 PASS.
- 78/78 PHP-Lint, 87/87 ZIP-CRC+exakte Dateibytes, 84/87 Originaldateien unverändert.
- Keine neue DataForSEO-Recherche; 223 Rohbegriffe aus der Nutzerdiagnose bleiben in WordPress erhalten.
- K0 Originalbranch `konzept0-portal-neutral-20261002` erweitert auf bereits validiertes `WP_K0_SOURCE_RECEIPT_V1.site_host` mit festem Hostregister und unverändertem alten Kategoriefallback. CI `K0 portal-neutral selftest` Run 44545937102 PASS, `K0 Hobby Discgolf acceptance` Run 44545937080 PASS; inkl. 6 neuer Host/Receipt-Manipulationstests.

## Offen / ausdrücklich kein erfundener Gesamt-PASS
Es liegt noch kein **echter neuer Hobbydepot-MINI-Export, Original-K0-Writer- und LanguageTool-Abschluss** der 223 aktuellen Live-Keywords vor; Simulation kann das nicht belegen. Installation als technischer Test auf bestätigter WP-Site ist freigegeben, keine automatische Publikation. Keine neue kostenpflichtige Recherche starten.

## Nutzerklickweg
Backup -> Plugins -> ZIP 0.4.24.12 hochladen, bestehendes Plugin ersetzen -> Texterstellung / Recherche / 'Gespeicherte Keywords kostenfrei nachpruefen' -> Seite offen lassen -> danach Mini-Gesamtauftrag, danach K0 und K0-Rückimport prüfen.
