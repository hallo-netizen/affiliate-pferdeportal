# HAB & BEWAHR – KATEGORIEN – CURRENT STATE
<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

## AKTUELLE OPERATIVE ANBINDUNG V9.9 – 15.10.2026 – KEIN WORDPRESS-WRITE
Dieses Kategorienbüro ist und bleibt **alleiniger WordPress-Strukturschreiber**. Der neue fachliche Plan liegt jetzt im **eigenen zentralen Kategorienbüro**:
`V9_9_ZENTRALES_ADD_DELTA_107_KNOTEN_81_KATEGORIEN_364_IDEEN_NICHT_IMPORTIEREN_20261015.json`.

**Exakt belegte rein konzeptionelle ADD-Struktur:** 4 neue Bereiche, 22 Unterbereiche, 81 Blattkategorien und 364 individuelle Artikelideen, keine vorhandene Kategorie umbenennen, verschieben, zusammenlegen, archivieren oder löschen. **546 bestehende Objekte und 285 CORE-Endkategorien geschützt.** Alle neuen Blattkategorien enthalten mindestens drei getrennte Artikelansätze; alle neuen Zwischenebenen haben mindestens drei Kinder. **1 positiver lokaler Datensatztest und 8 absichtlich defekte Negativszenarien korrekt PASS** (doppelte Artikel, zu wenige Artikel/Kinder, fehlende Parent-Referenz, doppelte ID, illegales UPDATE sowie Rename/Move am Bestand). Das ist nur eine Konzeptdaten-/Add-Only-Gate-Prüfung; es wurde **kein Plugin-Code ausgeführt** und nicht live in WordPress geschrieben.

**Letzter harter WP-Nachweis:** `portal-final-target-readback-20261013-185929-utc.json`: Plugin `1.14.8.19`, R3/V8-Struktur **546/546 UNCHANGED**, 0 Archivierungen. Im autorisierten Archiv `/Eigentumsschutz/Plugins/HD-001-Kategorie-Workflow` liegt nur das ältere Voll-ZIP `1.14.8.9` und frühere Versionen, im verbundenen GitHub weder Code noch Release `1.14.8.19`. Das alte ZIP darf **nicht** als aktuelle Installationsbasis benutzt werden.

**RELEASE BLOCKED:** Das **exakte installierte Pluginpaket 1.14.8.19 samt Quellcode** konnte aus verfügbaren Quellen nicht beschafft werden; zudem sechs genaue R2-Originaltitel und der endgültige semantische Owner-Abgleich offen. Kein nachgebautes oder zusätzliches Kategorienplugin, kein riskanter Versionsrückschritt, keine ZIP zum Installieren. Vorschlags-Node-IDs sind Platzhalter und dürfen nicht als echte WordPress-IDs/Slugs verstanden werden.

**GENAU EINE AKTUELLE NEXT ACTION (operativ):** Den derzeit installierten Original-Workflow **1.14.8.19** read-only als vollständigen Quell-/ZIP-Stand verfügbar machen; dann die in der V9.9-Akte geprüften 107 reinen ADD-Operationen **im bestehenden Plugin** mit Artikel-/Referenz-/SEO-Gate, lokalem Positiv-/Negativtest und WP-Dry-Run simulieren. Ausschließlich bei fehlerfreiem Schutz der 546 Altobjekte ein einziges vollständiges Installationsupdate paketieren. Bis dahin **nichts installieren**.


STAND: 2026-10-14
STATUS: **EIGENES ZENTRALES KATEGORIENBÜRO EINGERICHTET; R3/V8 WORDPRESS-STRUKTUR 546/546 LIVE PASS; PLUGINÜBERGREIFENDER NEUTRALER LAUFZEIT-ZUGRIFF / SPÄTERE CRUD-PFADE NOCH NICHT END-TO-END ABGENOMMEN**

## Verbindliche Nutzerentscheidung – 14.10.2026
- **Zentral, nicht pro Plugin:** Alle Kategorien/Seitenknoten/Taxonomien für CORE, Magazin und Dienstleister gehören zu einer gemeinsamen, unabhängig von Design, Affiliate, SEO, Magazin, Text- oder Bildplugin geführten WordPress-Kategorienverwaltung.
- **Separates Fachbüro:** Dieses Büro ist die *einzige* Current-Autorität für aktuelle operative Kategorie-Bindung, Änderungsweg und konsumierende Schnittstellen. Das Konzeptbüro bleibt zuständig für die *fachliche* Entscheidung über Themen, Duplikate und SEO-Owner. Keine zweite Current-Wahrheit.
- **Änderbar ohne Plugin-Umbau:** Zukünftige Plugins dürfen keine eingefrorenen Kategorie-IDs/Slugs, eigene Kategorie-Master oder eigene Hierarchie-Writes voraussetzen; sie müssen immer die aktuell gültige zentrale Zuordnung lesen. Erweiterungen, Umbenennungen, Verschiebungen, Zusammenführungen, Archivierung und kontrollierte Entfernung sollen Datenoperationen sein, keine neuen Pluginarchitekturen.
- **Keine freie destruktive Änderung:** Bestehende stabile logische Node-IDs erhalten; WordPress-Objekt-IDs/Slugs/URLs soweit möglich schützen. Bei Umzug/Umbenennung abhängige Artikel, Links, Breadcrumbs und SEO/Redirect-Folgen berücksichtigen; bei Löschung mit Referenzen kontrolliert archivieren/zusammenführen statt blind vernichten.
- **Ein Schreiber, viele Leser:** Alle verändernden Operationen über den bestehenden zentralen Kategorien-Workflow mit Delta/Preflight/Dry-Run/einmaligem Sync/Live-Readback. Alle übrigen Plugins **read-only** über einen neutralen, versionsfähigen Lesevertrag. Keine zusätzliche Kategoriehaltung.
- **Keine bezahlten SEO-Provider-Anfragen als Pflicht**; keine neue Architektur und keine Plugin-Neuentwicklung allein zur Einrichtung des Büros.

## Fachliche Neuregelung 15.10.2026 – KEIN WP-UPDATE
Das KONZEPTBÜRO führt ab 15.10.2026 den aktualisierten Fachvertrag `../KONZEPT/ZIELVERTRAG_KATEGORIEN_MINDESTENS_3_OHNE_MAXIMUM_20261015.md`: mindestens 3 direkte Kinder je Zwischenebene, **keine maximale Kinderzahl**, jede Endkategorie mit Platz für mindestens drei bis fünf unterschiedliche Artikelthemen (auch mehr möglich). Die frühere 3–10-Regel gehört nur noch zur R3/V8-Historie. Der Kategorien-Workflow/aktive WordPress-Bestand bleibt bis zur fachlichen Neusichtung und einem eigenen geprüften Änderungsdelta **UNVERÄNDERT**. Das Megamenü darf unabhängig von der tatsächlichen Kinderzahl spaltenweise balancieren, nie fachlich abschneiden.

## Gesicherter WordPress-Stand
Autoritativer Abschlussbeleg aus der Nutzerdatei `portal-final-target-readback-20261013-185929-utc.json`, SHA-256 `e90d1e66c814f291e33c6dee3239924d760d493b8998b0bf5ea565f2080cbdae`.
- R3/V8 Profilrevision: `HB-R3-V8-20261013-039c80c8c16d9b4f+b1998ec09edd98d0`.
- Plugin: Hab & Bewahr Kategorie-Workflow `1.14.8.19`.
- 546 physische WordPress-Zielobjekte; 6 Welten, 31 Bereiche, 93 Unterbereiche, 285 CORE-Blattkategorien, ergänzt um Magazin-/Dienstleisterstruktur.
- 192 neu / 354 bestehende aktualisiert / 0 archiviert, 546/546 Post-Sync `UNCHANGED`, 0 Fehler, Frontend-Readback PASS.
- WordPress-Mapping `node_id → object_id / object_type / taxonomy` im Sync-Readback konsistent. Dies ist **keine** End-to-End-Abnahme einer neutralen pluginübergreifenden Runtime-API.

## Erster offener Nachweis
Die vorhandene WordPress-Struktur ist real bestätigt. **Nicht belegt** sind derzeit: ein auf Hab & Bewahr live nutzbarer stabiler neutraler Lesevertrag für *alle* Fremdplugins und sicher durchgetestete spätere Add/Rename/Move/Merge/Archive/Remove-Änderungsfälle einschließlich Auswirkungen auf bereits zugeordnete Beiträge und Links. Deshalb nicht behaupten, dass jedes noch zu entwickelnde Plugin heute bereits umbaufrei kompatibel ist.

## EXAKT EINE NEXT ACTION
**Bei der nächsten tatsächlichen Plugin-Anbindung den vorhandenen R3/V8-WordPress-Aktivstand read-only gegen den `SCHNITTSTELLENVERTRAG.md` prüfen und den einen neutralen Zugriffspunkt nachweisen.** Bei fehlendem Zugriffspunkt nur die kleinste notwendige Kompatibilitätsbindung am bestehenden System konzipieren und gesondert freigeben; keine Kategorienänderung, kein neuer Sync und keine Arbeiten am laufenden Designauftrag.
