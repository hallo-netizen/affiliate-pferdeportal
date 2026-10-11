# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-11
STATUS: **RULE 2.7 / 2357 ZIELOBJEKTE LIVE-PASS / KATEGORIE-ZENTRALE EINGERICHTET / HD-004 LOCAL PASS / HD-001-DEAKTIVIERUNG LIVE ZU PRÜFEN**

## Autoritative Bindung

Zielvertrag:
`ZIELVERTRAG_HD001_AUTOMATISCHE_SEO_HIERARCHIE_20261003.md` – Fassung 2.7.

Zentrale Kategorie-Unterzentrale:
`KATEGORIE_ZENTRALE/START_HERE.md`

Technische Plugin-Wahrheiten:
- Bearbeiten/Sync: `../PLUGINS/PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`
- schlanker Runtime-Kern: `../PLUGINS/PLUGIN_AKTEN/HD-004-KATEGORIE-KERN/CURRENT.md`

Finale Live-Evidence:
`HD001_FINAL_LIVE_ACCEPTANCE_20261009.md`.

## Produktiver Kategorien-Endstand

Unverändert:
- Live-Profilrevision `HD-TARGET-3P-RULE27-CATEGORY-GAPFIX-HOBBYFINDER-20261009+0f4dbf59238a7d83`;
- 2371 logische Knoten;
- 2366 aktive Nodes;
- 2357 aktive physische Zielobjekte;
- 2357/2357 Readback;
- Runner COMPLETE / `TARGET_TREE_SYNC_AND_READBACK_PASS`;
- Frontend valid=true;
- 8 Welten;
- 330/330 terminale CORE-Seiten im Kategorie-Gate;
- 1920 aktive CORE-Content-Kategorien.

## Kategorie-Zentrale

Neu zentral gebunden:
`KATEGORIE_ZENTRALE/REGISTER.md`

Dort sind festgelegt:
- stabile Node-IDs;
- Taxonomie-/Objekttypen;
- Parent-Zuordnung;
- Live-Revision;
- Runtime-Snapshot;
- neutrales Plugin-Zugriffs-API;
- exaktes HD-001-Wiederherstellungsartefakt.

Zentrale Datenkopien:
- Zielprofil:
  `/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGET_PROFILE_RULE27_20261009.json`
- finaler Live-Readback:
  `/hobby rausch/KATEGORIE_ZENTRALE/hobby-depot-final-target-readback-20261009-170623-utc.json`
- HD-001 1.14.8:
  `/hobby rausch/KATEGORIE_ZENTRALE/HD001_V1.14.8_RULE27_FINAL_VERIFIED_E2E_20261009.zip`

## Harte Deaktivierungsprüfung HD-001

Exakter 1.14.8-Quellstand geprüft.

Befund:
- Deaktivierung löscht den produktiven Kategorienbestand nicht.
- kein `uninstall.php`;
- kein `register_uninstall_hook`;
- kein Deaktivierungs-Cleanup;
- aktive Snapshot-Optionen bleiben bestehen.
- DataForSEO ist kein separates dauerhaft notwendiges Strukturplugin.
- ABER: HD-001 registriert bisher `journal_cat` und stellt seine eigenen Snapshot-Klassen bereit.

Deshalb darf HD-001 nicht einfach ohne Ersatz deaktiviert werden.

## HD-004 Kategorie-Kern

Lokaler Kandidat:
`HOBBY_DEPOT_KATEGORIE_KERN_HD004_V1.0.0_READONLY_LOCALPASS.zip`

SHA-256:
`f3be1e10b093a24f41981c9386ce8ca208294bb0583b6bcc4a1f5295fb5c0bfb`

Aufgabe:
- `journal_cat` registrieren;
- bestehenden aktiven Snapshot read-only bereitstellen;
- neutrale API für andere Plugins;
- keine DataForSEO-Logik;
- keine Strukturwrites;
- keine zweite Datenhaltung.

Lokal:
PHP / ZIP / Runtime-API / Mapping / Taxonomie / Read-only-Audit PASS.

## Wichtig für spätere Änderungen

Add / Rename / Move / Merge / Archive bleiben jederzeit möglich.

Dafür:
HD-001 1.14.8 gezielt wieder aktivieren → Delta → lokale POS+NEG-Prüfung → Live-Dry-Run → genau ein Sync → 100%-Readback → wieder deaktivieren.

Keine Vollrekonstruktion.

## ERSTER OFFENER BLOCKER

**Nur noch der Live-Smoke-Test des schlanken Betriebs.**

## EXAKT EINE NEXT ACTION

**HD-004 1.0.0 installieren/aktivieren → HD-001 zunächst nur deaktivieren → Startseite + Magazin/journal_cat + eine CORE-Welt prüfen.**

Erst bei PASS ist das Löschen der HD-001-Plugin-Dateien freigegeben.
