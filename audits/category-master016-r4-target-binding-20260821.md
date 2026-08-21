# Kategorie-Workflow MASTER 016-R4 / V1.6.4 – Stage12 Target-Binding Rootfix

Datum: 2026-08-21
Branch: `category-master016-r4-target-binding-20260821`
Basis: `category-master016-r3-http402-rootfix-20260821`
Status: `LOCAL FULL ARTIFACT HARD PASS / LIVE TARGET-BINDING NOCH NICHT AUSGEFUEHRT`

## Realer Trigger
Der reale Gaumen-Atelier-Stage12-Read-only-Lauf ergab:
- Gesamtstatus `BLOCKED`
- Schemapruefung `PASS`
- DataForSEO-Evidenz `PASS_WITH_RESEARCH_EVIDENCE`
- Live-Bestandsvorschau `BLOCKED_PREVIEW`

Die verbliebenen echten Live-Blocker waren ausschliesslich Magazin-Knoten mit `TAXONOMY_UNAVAILABLE`, weil das im signierten Paket deklarierte logische Ziel `journal_cat` auf der konkreten WordPress-Installation nicht registriert ist. Content- und Marketplace-Ziele waren davon nicht betroffen.

## Root Cause
Das bisherige Paket band die Magazin-Saeule an `journal_cat`. Der Workflow durfte diese signierte Zieldefinition nicht nachtraeglich still veraendern und durfte ebenso wenig eine andere WordPress-Taxonomie erraten oder automatisch erzeugen. Daher war der fail-closed Stage12-Block korrekt, aber es fehlte eine sichere, explizite technische Zielbindung fuer die konkrete Installation.

## V1.6.4 Rootfix
V1.6.4 fuegt ausschliesslich im Read-only-/Final-Pfad eine serverseitig signierte `deployment_binding` hinzu:
- nur wenn Schema/Evidenz gueltig sind und die Live-Blocker ausschliesslich fehlende Ziel-Taxonomien betreffen;
- das urspruenglich signierte logische Ziel bleibt unveraendert erhalten;
- kein automatisches Mapping `journal_cat -> category` oder auf irgendeine andere Taxonomie;
- WordPress zeigt nur real registrierte, oeffentliche, hierarchische Taxonomien zur expliziten Auswahl;
- keine Vorauswahl;
- Bindung ist Site-, Scope-, Mapping-, User- und Zeit-gebunden und HMAC-signiert;
- wird das urspruengliche Ziel spaeter verfuegbar oder das Mapping manipuliert, gilt die Bindung fail-closed als ungueltig;
- Initial- und Global-Gap-Review-Hashes bleiben unveraendert; der finale Review-Scope bindet die Deployment-Bindung mit ein;
- nach gueltiger Bindung laufen Validator, DataForSEO-Evidenz und Live-Comparator erneut read-only;
- nur bei PASS wird ein neues gebundenes `READ_ONLY_PREVIEW` zum Download angeboten;
- keine Kategorie-, Taxonomie-, Beitrags-, HivePress- oder Menueschreibfunktion wird dadurch aktiviert.

## Geaenderte Produktions-/Vertragsdateien gegenueber V1.6.3
Exakt 6 relevante Produktions-/Schema-Dateien:
1. `affiliate-portal-kategorie-workflow.php`
2. `includes/class-apkw-admin.php`
3. `includes/class-apkw-comparator.php`
4. `includes/class-apkw-inventory.php`
5. `includes/class-apkw-validator.php`
6. `schema-category-v1.4.json`

Dokumentation/Tests wurden entsprechend erweitert.

## Neue verbindliche MASTER-Regeln
- R-131: fehlende Ziel-Taxonomie bleibt BLOCKED; kein Raten, Erzeugen oder stilles Remapping.
- R-132: explizite serverseitig signierte, installationsspezifische Deployment-Zielbindung.
- R-133: technische Zielbindung darf Inhalt, Hierarchie, Keywords, Longtails, Intents, Artikeltypen oder Produktionsentscheidungen nicht veraendern.
- R-134: Kategorie-/Menueimport ist ein separater Post-FINAL-Transaktionsblock; Kategorien zuerst, Navigation/Menue danach. Der Writer darf erst nach `PASS_FINAL_APPROVED` aktiviert werden.

Aktive Regeln: 134/134 `ACTIVE`. Workflow bleibt exakt 14/14 Hauptstufen. Contract-ID bleibt wegen der laufenden signierten Paketkette `ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_WORKFLOW_HARDLOCK`; Master-Revision ist `016-R4`.

## Post-FINAL WordPress-Importziel
Der MASTER dokumentiert den naechsten separaten Block fuer einen integrierten Import im selben Plugin-UI:
- nur `FINAL_APPROVED` als Quelle;
- Dry-Run vor Write;
- WordPress-/HivePress-/Journal-Kategorien hierarchisch und adaptergebunden;
- idempotent, keine automatischen Loeschungen oder Ueberschreibungen;
- Backup, Protokoll, Rollback;
- Kategorienhierarchie und Navigationsmenue bleiben getrennte Transaktionen;
- Menue erst nach erfolgreichem Kategorieimport;
- keine Freischaltung dieses Writers innerhalb der aktuellen Read-only-14-Stufen-Kette.

## Pruefungen
- aktive Source: 146/146 PASS
- Fresh Source ZIP: 146/146 PASS
- Fresh Installer ZIP: 146/146 PASS
- Fresh Master-Source: 146/146 PASS
- Fresh Master-Installer: 146/146 PASS
- Source <-> Installer: 0 Diff
- PHP-Lint: 10/10 PASS
- JSON-Parse: PASS
- Content-Write-Scan: 0 Treffer
- Produktionsendpunkte unveraendert: `user_data`, `keyword_ideas/live`, `keyword_overview/live`, `keyword_suggestions/live`
- aktiver Master-Conflict-Audit: PASS
- Workflow: 14/14
- aktive Regeln: 134/134 ACTIVE
- Master-SHA-Manifest: 455/455 PASS nach Fresh-Unpack
- externe und Master-eingebettete Source-/Installer-ZIPs byteidentisch
- Master-/Installer-/Source-ZIP-Integritaet PASS

## Artefakte
- Installer `AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.6.4_MASTER016_R4_TARGET_BINDING_ROOTFIX.zip`
  - SHA-256 `3fe90acda59a0ee2f55e26572fb7dba3d35ac1e8eba6fa86a1fd66310cca9805`
- Source `QUELLCODE_KATEGORIE_WORKFLOW_V1.6.4_MASTER016_R4_TARGET_BINDING_ROOTFIX.zip`
  - SHA-256 `92f2b84a1681c54c3a14ef9d5f7f343067cf696d6069708d920b52a60d035a58`
- Master `ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_R4_WORKFLOW_HARDLOCK.zip`
  - SHA-256 `69fc2a7fe569545cffe003669f0ed4bb35be53a49fd1d53991cd2ae5a6a13b9a`

## Codex
Ein Codex-Auditauftrag ist im MASTER dokumentiert. Codex war fuer diesen Rootfix nicht erforderlich, da Root Cause, Fix, negative/positive Regression, Fresh-Unpack und Artefaktparitaet lokal reproduzierbar PASS sind. Bei spaeterem Einsatz darf Codex nur den eingefrorenen V1.6.4-/MASTER016-R4-Stand pruefen und keine eigenmaechtigen Fach-, Struktur-, Content- oder Workflowaenderungen vornehmen.

## Abgrenzung
`main` bleibt unveraendert; kein Merge. Keine API-Keys, WordPress-Datenbank, Medien, Research-Rohpakete oder Secrets werden in GitHub gespeichert.