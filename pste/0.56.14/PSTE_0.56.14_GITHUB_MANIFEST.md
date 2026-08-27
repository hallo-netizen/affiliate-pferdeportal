# PSTE 0.56.14 – Batch Title Diversity Rootfix

Status: RELEASE VERIFICATION PASS
Date: 2026-08-27

Root cause: Beratungstitel wurden item-lokal erzeugt. Dadurch konnten Titel einzeln PASS sein, aber als Batch dasselbe Leitwort/Satzgerüst wiederholen. Einzelwort-Blacklists verschoben den Fehler nur.

Fix: batchweite generische Diversitätsauswahl über vollständige Titeloberflächen. Kein bevorzugtes oder speziell verbotenes Ersatzwort in der Diversitätslogik. Identische Satzgerüste und dominierende zusätzliche Inhaltswort-Stämme werden batchweit begrenzt; wenn keine zulässige natürliche Kombination existiert, fail-closed REVIEW_REQUIRED.

Hardlocks:
- Textmaschine unverändert
- Artikelinhalt unverändert
- Design/CSS/JS/Templates unverändert
- PSERC unverändert
- PPM 6.7.9 unverändert
- LanguageTool unverändert
- Kategorie, Artikeltyp, Target Keyword, Planplatz, canonical article identity unverändert
- kein Auto-Publish

Release installer SHA-256:
`e6bf6df33c94cbb6a0cf299a1092b91ed79e73736ed5290c7f99ff760db4b491`

Changed files vs verified PSTE 0.56.13:
- `portal-seo-topic-engine.php`
- `includes/class-pste-title-composer.php`
- `includes/class-pste-title-diversity.php` (new)
- `includes/class-pste-runner.php`
- `includes/class-pste-repository.php`
- `CHANGELOG_0.56.14.md` (new)

Verification:
- 73/73 PHP syntax PASS
- current four title compatibility cases: 4/4 full pipeline + batch audit PASS
- 10 real Beratung families: portfolio/full-pipeline regression PASS
- protected bindings byte-equal PASS
- blocked item unchanged PASS
- manual title unchanged PASS
- non-Beratung composer output parity vs 0.56.13 PASS
- existing title validator / German reviewer / editorial quality gate / title pipeline byte-identical vs 0.56.13 PASS
- added-line content/design write-surface scan PASS
- installer re-extraction byte-identical PASS

Next live step: install PSTE 0.56.14, open SEO Redaktionsplan, export a fresh pure metadata JSON. Article production is not claimed until that live snapshot proves READY items.
