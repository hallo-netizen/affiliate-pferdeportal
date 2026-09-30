# HD-002 – HOBBY DEPOT SEO THEMENENGINE – CURRENT

STAND: 2026-09-30
STATUS: V0.1.0 EIGENER HOBBY-DEPOT-STRANG / HARD LOCAL PASS / LIVE-INSTALLATION OFFEN

## Identität

Plugin:
`Hobby Depot SEO Themenengine`

Version:
`0.1.0`

Installer:
`HOBBY_DEPOT_SEO_THEMENENGINE_V0.1.0_HD002_HARD_LOCAL_PASS.zip`

Source:
`QUELLCODE_HDTE_V0.1.0_HD002_HARD_LOCAL_PASS.zip`

SHA-256:
`c6b24fdff3499c1e9a1039fae722d6ad8418df215e55a07e394408bbcac9f2a5`

## Harte Projekttrennung

- eigener PHP-Präfix: `HDTE_`;
- eigener Option-/Table-/Hook-Präfix: `hdte_`;
- eigene Projekt-ID: `hobby_depot`;
- keine Runtime-Abhängigkeit vom Pferdeatelier-PSTE;
- paralleler Boot mit PSTE geprüft;
- Aktivierungs-/Release-Guard blockiert Fremdprojekt-Quellreste;
- direkte DB-Schreibpfade sind auf eigene `wp_*hdte_*` Tabellen begrenzt;
- atomare Optionsbereinigung nur für eigene `hdte_`-Keys/Transients.

Pferdeatelier-PSTE wurde nur einmalig als Referenzbasis gelesen/kopiert und wird von HD-002 nicht verändert.

## Übernommene technische Basis

Referenz:
`PSTE-0.57.13-DATABASE_STORAGE_CLEANUP_PERFORMANCE_SAFE_HARD_PASS.zip`

Referenz-SHA:
`bb5f3cc84dc00fa85e2c0ddf48c8994a4788c2595c6d98f0d440780377060248`

Storage-/Performance-Abgleich:
- Research-Archive: normalisierte Parität PASS;
- Sandbox-Record-Store: normalisierte Parität PASS;
- Repository: nur projektbezogene Handoff-/FAQ-Anpassungen; Storage-/Cleanup-Mechanik erhalten;
- Storage-Maintenance: nur Rollback-UI-Wortlaut angepasst; Komprimierungs-/Restore-Mechanik erhalten;
- keine alte `.orig`-Datei übernommen.

## Hobby-Depot-Anpassung

- V1.9.1-Editorial-Ownership-Handoff wird read-only unterstützt;
- `owner_concept_id` + `semantic_intent_key` vor Artikelpromotion;
- neue eigenständige Intents sind erlaubt, wenn Owner gültig und semantischer Schlüssel einzigartig ist;
- answer-equivalente Varianten dürfen nicht zu einem anderen Owner springen;
- Frageform besitzt keine automatische FAQ-/Kategorie-Owner-Autorität;
- keine Kategorien- oder Artikelanlage durch diesen Gate-Schritt.

## Harte lokale Prüfung

Fresh Installer:
- PHP-Lint 80/80 PASS;
- Project Boundary PASS;
- Ownership 11/11 PASS;
- Frage≠FAQ 12/12 PASS;
- Family Identity 8/8 PASS;
- Frontend-Boot: 0 DB Reads/Writes, 0 Schedules, 0 Remote;
- Admin-Boot: 3 Reads, 0 Writes, 0 Schedules, 0 Remote;
- Koexistenz mit PSTE: PASS;
- Runtime Worktree↔Fresh-Unpack: 135/135 byte-identisch.

## Beleggrenze

Noch keine Live-WordPress-Installation.
Noch keine produktive Datenänderung.

## NEXT ACTION

Vor Live-Installation den aktuellen Nachbarchat-PSTE-Stand noch einmal nur als Referenzdelta prüfen, falls dort ein neuerer Storage-/Performance-Stand veröffentlicht wurde.

Wenn kein neuer Delta existiert:
HD-002 V0.1.0 auf Hobby Depot installieren und ausschließlich mit eigenen `hdte_` Daten initialisieren.
