# eBay – Faktenabgleich gegen alle bereits belegten Versuche (10.11.2026)

**Status:** HISTORIEN-/CODE-AUDIT, **keine neue Version**, **keine Datenänderung**. Quelle: reale hochgeladene CSV `Pferdeatelier_eBay_fehlende_Produktfamilien_3e9e9207-d82.csv` (Run `3e9e9207-d82f-4223-943b-5df8d0d6feb8`), echte Nutzerscreenshots, vollständig physisch vorhandene Plugins QA7 `6.72.320` und QA9 `6.72.321`, frühere Berichte QA2–QA9 sowie 07.11.-Referenz.

## A. Was bereits wirklich im aktuellen QA9-Quelltext vorhanden ist (NICHT NEU BAUEN)

| Bereits erledigt | Quelle / genauer Beleg | Realstatus |
|---|---|---|
| 06./07.11. Sammelpatch: begrenzte Produktabfrage und gebündelte Daten-/Quellprüfungen | `PFERDEATELIER_REFERENZ_UPSTREAM_20261107.md` in HD und HAB; 6.72.308 | Quellpatch, kein öffentlicher Live-Abnahmebeweis |
| Timeout/Retries/gespeicherter Cursor ohne fälschlichen Neustart | 311/312, im QA6-Bericht als bereits erledigt | Getestet, gespeicherte Live-Historie schützen |
| Gleiche Startberechtigung für Backend und echten Worker; `queued` ist nicht `complete` | 313/314 | Bereits umgesetzt |
| Die 0/298-Anzeige eines neuen Teilabschnitts nicht mit öffentlicher Gesamtabdeckung verwechseln | 315 | Bereits umgesetzt |
| Neben dem Original-Suchwort einmal **exakten Katalogtitel** abfragen; nicht immer „Pferd“ anhängen | bereits **316**, Methode `ebay_business_gap_query_variants` in QA9 vorhanden | Nicht als neuen Suchwort-Fix anbieten |
| Gleiche Artikel-ID bei mehreren sachlich geprüften Produktfamilien berücksichtigen | `business_processed_by_concept`, `ebay_business_add_verified_secondary` in QA9 | Bereits implementiert; reale Wirksamkeit nicht bewiesen |
| Vorhandene gespeicherte Quellen erneut verifizieren und innerhalb der einzigen kanonischen Auswahl verwerten | QA2/QA5: `ebay_selection_prepare_business_batch` ruft `ebay_business_reuse_stored_for_concept` bei `canonical_gapfill` ohne aktiven Gewinner auf; `ebay_selection_reuse_checkpoint_batch` als Bestandsprüfung eines bereits begonnenen Teilabschnitts | **Bereits implementiert**, keine zweite Engine anbieten |
| Einzelne Fehler isolieren, fachlich sichere letzte Freigaben erhalten, gezielte Nachsuche und Prune nur für betroffene Familien | QA2–QA5 | Bereits implementiert, in simulierter WP/PHP-Umgebung getestet |
| Nicht verwendete Methoden / redundante Speicherprüfung entfernen; Backendmenüs reduziert | QA5–QA7 | Teilweise KISS-Verschlankung schon erfolgt, vollständiges Backend weiterhin langsam |
| Manuelle Pause vom äußeren Heartbeat nicht als Fehler/Neustart behandeln | QA8 | In QA9 enthalten, kein zweiter Worker |
| Geeignete Produkte vor Abschluss der gesamten Recherche freigeben; unabhängige 2h-Verfügbarkeitsprüfung | QA9 6.72.321 | **Neuer Teststand**, 61 bestehende + 19 neue lokale PHP-Tests; echter WordPress-Gesamtnachweis fehlt |
| 6h-Quelle/Marketplace EBAY_DE/fachliche Qualität und öffentliche Kampagnen-Gates | `ebay_accept_item` und `ebay_run_public_business_coverage` | Bewusste Sicherheitsregeln, nicht ohne Evidenz lockern |

**Physischer Versionenvergleich:** `ebay_accept_item`, `ebay_build_search_request`, `ebay_business_reuse_stored_for_concept` und `ebay_business_gap_query_variants` sind **im ZIP QA7 6.72.320 und QA9 6.72.321 bytegleich**. QA9 repariert den Grund der nachfolgend aufgeführten Ablehnungen daher nicht.

## B. Neue tatsächliche CSV – nicht den alten 187er Bericht erneut als aktuellen Stand behaupten

Gespeicherte CSV mit **138 fehlenden Familien**, alle aus Run `3e9e9207-d82f-4223-943b-5df8d0d6feb8`:
- **94**: eBay-Angebote im begrenzten Suchausschnitt vorhanden, aber nicht angenommen.
- **43**: keine Treffer im geprüften Suchausschnitt.
- **1**: technischer Fehler `http_request_failed`, **keine Markt-Nichtverfügbarkeit**.
- Insgesamt **258 Anfragen, 1.329 Angebotstreffer, 764 im Feld `blockiert`, 0 angenommen** für *diese offenen Familien*. **Nicht** gleichzusetzen mit 0 akzeptierten Angeboten der ganzen Website.
- Vorherrschende **Ablehnungsereignisse**, keine eindeutigen Einzelangebote: `ebay_marketplace_mismatch` **610** (bei **68 Familien**), `ebay_portal_topic_negative` **234** (bei 27), `ebay_business_concept_missing` **179** (bei 27), `ebay_portal_topic_missing` **96** (bei 22), `ebay_toy_item_blocked` **80** (bei 13). Ereignisgründe können sich bei einem Kandidaten/Profil überschneiden, deshalb nicht als disjunkte Produktsummen behandeln.
- Der **aktuellere Screenshot 17:48** hat **154/298** und **144 offen**. Die CSV ist ein anderer gespeicherter Exportzeitpunkt, mit **138 Zeilen**; Werte **nicht zusammenmischen**.

## C. Der wichtigste Ablehnungsgrund ist in früheren Audits bereits geklärt – KISS heißt: nicht blind entfernen

`ebay_accept_item` prüft `listingMarketplaceId`; nur genau `EBAY_DE` ist erlaubt, sonst `ebay_marketplace_mismatch`. Die bestehende Suche setzt zwar den Request-Header `X-EBAY-C-MARKETPLACE-ID: EBAY_DE`, filtert aber zusätzlich `deliveryCountry:DE`. **Lieferbarkeit nach Deutschland ist nicht dasselbe wie Herkunftsmarktplatz Deutschland.** Darauf wurde schon am **07.11.** in beiden Affiliate-Upstream-Referenzen ausdrücklich hingewiesen. Die 610 Ereignisse sind deshalb keine neue, bisher unerklärte technische Rätselzahl; sie sind **eine bekannte, bewusst strikte Filterentscheidung**. Aus dem Export allein folgt weder, dass 610 *gültige* deutsche Angebote fälschlich abgelehnt wurden, noch dass diese Regel verhandelbar ist. **Nicht** einfach von `EBAY_DE` auf „alle liefern nach DE“ umstellen.

Die fachlichen Negativ- und Zuordnungsgründe (234 + 179 Ereignisse) sind **ebenfalls gespeicherte Ablehnungen**; ohne einzelne eBay-Datensätze keine belegte Aussage „fälschlich abgelehnt“. Kein neues synonymes Gesamtsuchsystem / kein zweiter Quality-Classifier.

## D. Korrektur einer früheren irreführenden Aussage

Die zuletzt behauptete „neue Ursache: das Plugin durchsucht erst eBay, bevor es überhaupt vorhandene Kandidaten verwendet“ ist **zu pauschal**. Richtig ist: In `gapfill_discovery` erfolgt die erneute eBay-Suche tatsächlich **vor dem erneuten `gapfill_select` dieses Abschnitts**. Aber: **Der wiederverwendende Selektor und lokale Quellen-Reuse sind bereits seit QA2 implementiert und werden in diesem `gapfill_select` aufgerufen**. Die Ausgangsauswahl des Gesamtlaufs hat bereits Produkte verarbeitet (Screenshot: 299 aktiv/materialisiert), und QA9 kann diese früher freigeben. Einen weiteren „erst Speicher prüfen, dann suchen“-Pfad **als angeblich noch nie gemachte Innovation** vorzuschlagen, wäre Doppelarbeit. Eine komplette Neuordnung würde erneut Auswahlschleifen und Prune-Risiken schaffen.

**Warum 399 Pakete ohne neue 154/298-Abdeckung?** Der reale Screenshot 17:48 zeigt **`gapfill_discovery`**. In dieser Phase wird die öffentliche Abdeckung nach Code **nicht pro Artikel neu gezählt**; erst Auswahl/Checkpoint/öffentliche Prüfung können sie verändern. Das ist **kein Nachweis** eines festsitzenden Workers und kein Beweis von 144 Marktlücken.

## E. Grenze und zulässiger nächster Ursachenbeweis

**KEINE neue Plugin-ZIP**, kein Massenneustart, keine neue gesamte Recherche, keine zweite Controllersteuerung und keine Änderung der bewussten Marketplace-/Sicherheitsfilter. Der derzeit belegte Restkonflikt ist **welche der 94 Angebotsfamilien *zu Recht* ausgeschlossen sind und ob nach bereits vorhandener QA9-Auswahl/Veröffentlichung tatsächlich versorgbare Produkte hängen bleiben**. Für diese Feststellung den **vorhandenen** CSV-Grund und die **bereits vorhandenen** gespeicherten Auswahl-/Veröffentlichungsnachweise zusammenführen, nicht neue Ablehnungsgründe erstellen. Ohne Zugriff auf die produktiven gespeicherten Angebotsdetails kann keine konkrete Datenfehlklassifikation als repariert gelten.

**Bereits erledigte Bearbeitungen bleiben erledigt und werden nicht erneut angekündigt.** Für anderen Portalcode (HD-009 / HAB-004) nur Referenz; keine automatische Übernahme, kein Current-Wechsel, keine Datenänderung.
