# PSERC 0.28.2 – Root Cause und Deltascope

Bindende Basis: STARTMASTER0053 + harter Prüfvertrag. Bestehender Workflow und Textmaschine sind tabu; Journal darf nur additiv über die signierte/versionierte Extension-Schnittstelle angebunden werden.

## RC-1 – Core-Release durch Journal-Extension global verschärft
Vor Journal konnten FAQ, Beratung, Vergleich und Pflege über den signierten `NORMAL_DRAFT_RELEASE_SCOPE_V1` produktionsfähig werden. Mit der Journal-Erweiterung wurde zusätzlich `globallyReady` auch für Core-Typen verlangt. Identischer 69-Assertion-Vorher/Nachher-Test: 0.26.0 = FAQ/Beratung/Vergleich/Pflege/Journal; 0.28.0 = nur Journal; 0.28.2 = FAQ/Beratung/Vergleich/Pflege/Journal.

Reparatur: Core-Release und Extension-Release werden allgemein getrennt. Core behält den bestehenden signierten Freigabepfad. Extension-Typen benötigen weiterhin zusätzlich das signierte Extension-/Certification-Gate. Keine Artikel-, Titel-, ID-, UUID-, Kategorie- oder Pilot-Sonderfälle.

## RC-2 – persistenter Plan-Snapshot nicht an produktionsrelevante Capability gebunden
Ein produktiv erzeugter persistenter 0.28.0-`0 READY`-Snapshot wurde nach Upgrade weiter als aktuell akzeptiert. Im getrennten Mehrprozess-Vorher/Nachher-Test wird dies vor 0.28.2 reproduziert. 0.28.2 bindet ausschließlich die technische Plan-Snapshot-Gültigkeit an Compiler-Build + verifizierte Production-/Article-Type-Capability. Topic-/Structure-Projektion wird komponentengenau wiederverwendet. Derselbe reale 562er Pfad endet nach 0.28.2 mit 12 eligible / 5 READY.

## Regel 1 / geschützter Scope
Nicht verändert: DataForSEO, Longtails, Themenauswahl, Kategorie, Artikeltypentscheidung, Titel, Titelvariation, H2, Textmaschine, Prompt, Recherche/Fact-Pack, Qualität, SEO, Links, Affiliate, HTML, Design und Artikelumfang.

0.28.1 -> 0.28.2 verändert ausschließlich `README.md`, `contracts/compiler-package-binding-v1.json`, `includes/class-pserc-plan-dependency-fingerprint.php`, `portal-seo-editorial-plan-compiler.php`; neu ist nur `CHANGELOG_0.28.2.md`. Der Production Reader aus 0.28.1 bleibt byteidentisch. One-Click, Production Trigger, Workflow Supervisor, Production Package, Extension Registry/Planning Gate und signiertes Manifest aus 0.28.0 bleiben byteidentisch.
