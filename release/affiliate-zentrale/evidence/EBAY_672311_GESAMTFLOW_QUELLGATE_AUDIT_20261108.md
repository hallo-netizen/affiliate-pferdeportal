# Pferdeatelier / eBay 6.72.311 – nachgeprüftes Gesamtflow-Quellgate (08.11.2026)

**Entscheidung: RELEASE BLOCKIERT. Kein installierbares ZIP, keine Live-Änderung.**
Zielvertrag: ausschließlich gewerbliche eBay-Produkte (BUSINESS); keine privaten eBay-Abrufe/Veröffentlichungen, keine eBay-generierten HivePress-Listings. Normale unabhängige HivePress-Anzeigen und die übrigen Affiliate-Provider bleiben unberührt. Kein neuer Worker, keine neue Tabelle, keine Frontend-API, kein zweiter Workflow.

## Harte Quellbindung statt Vermutung

**Korrektur der missverständlichen Zugriffsformulierung:** Das Original 6.72.308 ist nachweislich hochgeladen und am 08.11.2026 tatsächlich geöffnet und vollständig geprüft worden. Eine momentane fehlende Byte-Lesemöglichkeit in dieser Chat-Sitzung oder in einem einzelnen GitHub-Branch beweist weder Dateiverlust noch fehlende Nutzerbereitstellung. Der Campus führt für Binärdateien einen separaten Plugin-Schrank; Details siehe `release/affiliate-zentrale/AGENTS.md` (Chatwechsel-Hardlock).
1. Im tatsächlich abgefragten GitHub-Tree `affiliate-release-current` ist der kanonische vollständige Pluginquellstand **6.72.211**, direkt im PHP-Pluginheader und in `control/release-governance/CURRENT_RELEASE.json` belegt, nicht 6.72.308.
2. Der untersuchte Git-Tree des Release-Branches (550 Einträge, nicht abgeschnitten) enthält **keine direkt abrufbare originale 6.72.308-ZIP**. Das ist eine Aussage nur über diesen Tree, nicht über den separaten Campus-Plugin-Schrank, andere Uploads oder die Existenz der Originaldatei. Der belegte Original-Upload von 08.11.2026: `AFFILIATE_ZENTRALE_6.72.308_URSACHENFIX_GESAMTTEST_NUR_TEST.zip`, SHA256 `b4d8547fd2aa134f7f82f568db3a81df54bb7d2131fd0752e76e3f0ca2251fe0`, 5.345.251 Bytes, 66 Dateien. Beleg: `evidence/AFFILIATE_ZENTRALE_6.72.308_ORIGINALZIP_UPLOADBELEG_20261108.md`. Der frühere Chat-Upload ist **kein** physisch verfügbarer GitHub-Quellstand.
3. `EBAY_672308_TO_672311_BUSINESS_ONLY_GESAMTURSACHENPATCH_NUR_TEST.patch` ist physisch vorhanden: 5 geänderte Dateiabschnitte, 40 Hunks, davon 12 BUSINESS-only-Hardlocks. **Der vollständige Patch wurde nicht gegen das originale ZIP angewendet.**
4. Der GitHub-Actions-Lauf [42489448439](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42489448439) meldet 17/17 PASS – ausschließlich für die 12 PRIVATE-Sperrhunks, auf **älterem Referenzquellcode**. Das ist **kein Gesamtflow-/WordPress-/Live-PASS**.

## Festgestellte gemeinsame Fehlerkette und nicht geschlossene Gates
| Station | Nachweisstand | Offen für Gesamt-PASS |
| --- | --- | --- |
| Originalbestand | 6.72.308 ZIP wurde im vorigen Chat physisch geprüft, ist hier nicht vorhanden | Zugriff auf die bereits bewiesene Originalquelle aus dem zuständigen Binärschrank herstellen und Hash abgleichen; keine Rückportierung auf 6.72.211 |
| Discovery/Suche | Reale Diagnose 07./08.11.: `http_request_failed` / cURL28 (SSL timeout) -> `partial` -> `gapfill_partial_unresumable` | Auf Originalcode: Retry gleicher Cursor, Erfolg nach Timeout, dauerhafter Timeout, 429/5xx, 401/403, falsche nächste URL, vollständig unabhängige Profile |
| Produktprüfung | BUSINESS-only-Filter und 298 Warenfamilien im späteren Konzept dokumentiert | Originalkatalog + Fach-/Marktplatz-/Seller-Vetos, Duplikate, externe echte Warenlücken, keine Scheinabdeckung |
| Speicherung/Frische | 6.72.311-Patch enthält getItem-Vorprüfung und begrenzte Wiederholung | echte gespeicherte WP-Quelle, 6h-Grenze, Ablauf, kein verfrühtes Verbergen und keine erfundene Aktualität |
| Freigabe | PRIVATE-Checkpoint-Hardlock lokal geprüft; Rückhalten des vorherigen sicheren BUSINESS-Stands bei offenen Suchprofilen im Patch vorgesehen | vollständige Kontrollkette Auswahl -> aktueller Checkpoint -> Ausgabe, kein falscher grüner Abschluss |
| Normales WordPress/HivePress | Im alten PHP ist `the_posts`-Filter registriert; `ebay_private_public_post_allowed()` benutzt PRIVATE-Checkpoint-Gate; Patch sperrt dieses Gate. Bereits publizierte eBay-eigene `hp_listing`-Datensätze werden damit aber nicht nachweisbar **in WordPress selbst auf Entwurf gestellt** | native Single-/Listen-/Suche-/Sitemap-Wege und der Altbestand prüfen; eBay-eigene Altanzeigen vollständig aus der Veröffentlichung entfernen, ohne echte fremde HivePress-Inserate anzutasten |
| Abschluss / Frontend | 17 Ref-Tests; kein vollständiger echter Durchlauf und keine nachweislich gerenderten BUSINESS-Karten | gesamte 6.72.311-ZIP lokal/auf WP-Testseite, echte eBay-Browse/getItem-Daten, gerenderte Kategorie/Artikelkarten, Banner/K0 unverändert |

## Einheitliche Freigaberegel
Ein einziger Gesamtzyklus an der **tatsächlichen originalen 6.72.308-Quelle**: Original-FEHLER reproduzieren -> kumulativen BUSINESS-only-Ursachenpatch vollständig anwenden/bei Bedarf ursächlich korrigieren -> PHP-/WP-/DB- und reale eBay-End-to-End-PASS-/NEGATIVfälle -> WordPress Altbestand/Native HivePress und echte eBay-Karten prüfen -> ZIP-Identität/Release-Gate. Bis dahin **6.72.310 niemals installieren, 6.72.311 nur Test-Kandidat, `release_allowed=false`**.

Dieser Audit ändert weder Plugin noch WordPress, definiert keine zusätzliche Fachlogik und ersetzt keinen Gesamt-Test.

## Nachprüfung der nativen HivePress-Ausgabe (08.11.2026, 15:10 UTC)
Der vorhandene Referenztest wurde ohne neue Teststrecke auf die normale WordPress/HivePress-Ausgabe `the_posts` erweitert. Reale geänderte PHP-Referenz-Traits wurden ausgeführt. GitHub Actions [42493404467](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42493404467): **19/19 tatsächlich ausgeführte Referenzprüfungen PASS**; Logs zusätzlich gelesen, kein PHP-Syntaxfehler. Neu geprüfte POSITIV-/NEGATIV-Paare: (a) altes eBay-generiertes, veröffentlichtes `hp_listing` wird im normalen Archiv herausgefiltert; (b) unabhängiges natives HivePress-Listing bleibt sichtbar. Bestehender Quellfilter `the_posts` ist in der Referenzquelle registriert. **Grenzen bleiben:** 6.72.308-Original fehlt; weder direkte Live-Single-Seite noch WP-Sitemap, tatsächliche Bestandsposts, echte BUSINESS-Produktkarten oder vollständige 40-Hunk-Regression sind damit nachgewiesen. Der Referenztest ist kein Release-Gate-PASS.

Zusätzliche Quellensuche: persönliche Library verzeichnet `AFFILIATE_ZENTRALE_6.72.309_EBAY_TIMEOUT_KISS_GESAMTTEST_NUR_TEST.zip`, stellt jedoch keinen autorisierten Dateizugriff zum Öffnen/Hashen bereit; **nicht als geprüfte oder ersetzende Quelle verwendet**.
