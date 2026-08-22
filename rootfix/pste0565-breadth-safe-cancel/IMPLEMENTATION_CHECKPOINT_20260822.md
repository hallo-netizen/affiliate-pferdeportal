# PSTE 0.56.5 – isolierter Breitenlauf-Cancel – Implementierungscheckpoint

## Scope

Ausschließlich dauerhafter, fail-closed Breitenlauf-Abbruch. Keine Änderung an Sandbox, Rechercheauswahl, DataForSEO-Queries, Familien-/Kategoriezuordnung, Artikeltypen, Titeln, SEO, Textmaschine, PPM, Design, WordPress-Inhalten oder Publish.

## Delta 0.56.4 → Kandidat 0.56.5

Exakt 5 Dateien unterscheiden sich; davon 4 Produktionsdateien plus neuer Changelog:

- `portal-seo-topic-engine.php`: e4bcff1b66a0f7a4a0be146264ec7ad2b67c799a9b24289ac4181e956322a350 → 2f111c3f0386cea668d0a7a727cb74069aea1b1e461941ac973cd6b88c30bea6
- `includes/class-pste-research-job.php`: 426c922d355a47b637b31a41cf3fb480c3d872fdf4baef607d40baf19592b355 → df36bbece7258379473372aceb6e73d8d080bd9ec70e8fc7f84b4e1cbe22932b
- `includes/class-pste-breadth-research-queue.php`: 910cb59c6b9656a0b9c9165f5aadac8cf2ae8faf67b4aa3f0a5f9f10892ef339 → 2578f27bb1c590bc3fef7c6298983bfbc1e7e92b02188788083e622a455cbe2f
- `includes/class-pste-admin.php`: 2be90163906120036f07566b159e451ba5f6240c0784869c9dc4d052a92194c3 → ca011eeed43ef4d8c71f46b38536f081b00bb48799cd92c313c4ade0c5e04ed8
- `CHANGELOG_0.56.5.md`: neu, 0dc0b304da07b27d9039d9181002119f68e39d4096e0668621aecd0a5e639c74

Alle übrigen 200 Plugin-Dateien sind byteidentisch zu 0.56.4.

## Sicherheitsmechanik

- persistenter Cancel-Marker wird vor Queue-Lock gesetzt;
- Queue-Advance und Cancel werden mit Queue-Lock serialisiert;
- vorhandener Research-Step-Lock bleibt Kindlauf-Schutz;
- Cancel erzeugt keine Provideranfrage;
- `IN_FLIGHT` wird nicht blind gelöscht;
- `OUTCOME_UNKNOWN` bleibt fail-closed;
- terminaler Zustand `CANCELLED` verhindert Auto-Resume nach Seitenreload;
- verbleibende Familien werden nicht gestartet.

## Tests – Source

- PHP-Lint: 72/72 PASS
- JSON: 52/52 PASS
- isolierter Cancel-Test: terminal idle / Research-Lock-Race / Queue-Lock-Race / in-flight fail-closed: PASS; Provideraufrufe im Cancelpfad: 0
- historischer Progress-Token: PASS
- realer 562-Exact-Five: 562/562 PASS; 0 Produktions-/WP-Schreibversuche
- realer Paused-539-Sandbox-Migrationslauf: PASS
- voller 562/486/549 Progress-Token-Realfixture-Lauf: PASS
- Browser-Progress-Vertrag: PASS

## Installer-Kandidat

`portal-seo-topic-engine_0.56.5_BREADTH_SAFE_CANCEL_ROOTFIX.zip`
SHA-256: `1db2914cd5cc1e71835f24a7316bf79a1b2387db61092e26c086f3fd52a7e586`
Source↔Fresh-Unpack: 205/205 byteidentisch.

Die gleichen Cancel- und historischen Tests gegen Fresh-Unpack: PASS.

Status: Implementierung abgeschlossen; noch nicht installfreigegeben, bis die vollständige systemweite Regression abgeschlossen ist.
