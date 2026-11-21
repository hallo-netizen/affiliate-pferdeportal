# K0 START

## Befehl

`K0:start`

## Sichtbares Chatverhalten — HARDLOCK

Bei gültigem angehängtem K0-Handoff + `K0:start`:

**NICHT ANTWORTEN. SOFORT INTERN PRODUZIEREN.**

Verboten:
- Vorrede;
- Statusmeldung;
- Prüfankündigung;
- Prozessbeschreibung;
- Routing-Erklärung;
- Verweis auf andere Wege oder Konzepte;
- Bitte um `weiter`;
- Zwischenmeldung irgendeiner Art.

Die erste sichtbare Antwort ist ausschließlich:

1. die **fertige verifizierte WordPress-Datei**, oder
2. ein **echter terminaler Blocker**, der intern nicht lösbar ist.

## Produktionsweg

`Upload -> K0:start -> Recherche -> Writer -> vollständige Regeln -> LanguageTool 6.8 -> finale Regeln -> SYSTEM4_WORDPRESS_HANDOFF_V1 -> Verifikation -> Datei`

**Fazit-Überschrift (verbindlich):** Der bestehende K0-Writer muss im Schlussabschnitt (`data-block="conclusion"`) exakt die sichtbare Überschrift `<h2>Fazit</h2>` ausgeben. Beim Fehlen oder einer abweichenden Überschrift wird derselbe unveränderte Writer-Auftrag über `WRITER_REWRITE_REQUEST.json` zur Reparatur zurückgegeben. Keine zusätzliche Prüfstelle; die 81 übrigen Artikelregeln, PPM und der WordPress-Vertrag bleiben unverändert.

**Recherchequellen (verbindlich):** Vor dem Writer akzeptiert die *bestehende* Rechercheentscheidung nur freigegebene offizielle Behörden-, Hochschul-, Fachverbands- und Herstellerseiten sowie echte Wikipedia-Artikel. Private Webseiten, Blogs, Foren, fremde Affiliate-/Testseiten und eigene Portaldomains sind ausgeschlossen. Neue offizielle Domains werden erst nach Überprüfung in der zentralen Quellenfreigabe der bestehenden Recherche ergänzt; bloße Domainendung `.org` oder eine behauptete Quellenbezeichnung reichen nicht. Textstellen müssen weiterhin auf der echten Originalseite belegbar sein. Unzulässige Quellen gehen ohne zusätzliche Prüfstelle zum selben Rechercheverantwortlichen zurück; die nachgelagerten K0-Regeln bleiben unverändert.

Portalzuordnung automatisch.

Interne Links: **1 bis 3 sinnvolle Links**, ausschließlich auf bestehende WordPress-Kategorien oder veröffentlichte WordPress-Seiten, **niemals einzelne Beiträge/Artikel**. Die eine vorhandene Linkentscheidung vor dem Writer prüft die echte Seitenbeschreibung bzw. den Seiteninhalt, bevorzugt konkrete Themenziele und lässt unpassende optionale Links automatisch weg. Die übergeordnete Kategorie (`parent_category`) bleibt Pflicht; `semantic_related` und `further_information` sind nur bei nachgewiesenem Bezug erlaubt. Haupttextlinks stehen in verschiedenen Abschnitten; ein `further_information`-Link steht ausschließlich im Abschnitt `further_information`. Kein Ersatzlink auf die allgemeine Magazin-Startseite, keine zusätzliche Prüfstation.

Repository: `hallo-netizen/affiliate-pferdeportal`

Branch: `konzept0-portal-neutral-20261002`

Current: `K0_CURRENT_STATE.json`

`publish_allowed=false`

Keine Alternativroute.


## Ein Eingang für das bestehende WordPress-Paket – verbindlich auch für neue Chats

Bei `K0:start` mit `contract: WP_K0_UPLOAD_PACKAGE_V1` enthält **die eine hochgeladene Datei bereits beides**:
- `k0_intake`: der ursprüngliche unveränderte Auftrag mit genau fünf Feldern je Artikel;
- `word_press_order_receipt`: die bereits in WordPress getroffene und gespeicherte Herkunfts-/Suchintententscheidung (`WP_K0_SOURCE_RECEIPT_V1`).

Die vorhandene Eingangs-Funktion `engine.k0_wp_upload.unpack` beziehungsweise `write_runs` legt je Artikel die vorhandenen Standarddateien an: `WORDPRESS_INTAKE.json` aus `k0_intake` und `PSERC_SOURCE_MANIFEST.json` **aus `word_press_order_receipt`**. Der Dateiname `PSERC_SOURCE_MANIFEST.json` ist nur der bestehende K0-Eingangsplatz, **keine Forderung nach einem zusätzlichen alten PSERC-Export**. Der vorhandene K0-Binder `engine.k0_seo_owner_binding.inspect` unterstützt ausdrücklich **beide** Verträge: Original-PSERC-Manifest oder WordPress-Auftragsbeleg.

**Niemals** einen `WP_K0_UPLOAD_PACKAGE_V1`-Upload wegen `K0_UPSTREAM_SEO_SOURCE_MANIFEST_MISSING` blockieren, wenn sein vorhandener `word_press_order_receipt` durch den bestehenden Binder akzeptiert wird. Ebenso **niemals** aus dem Dokument eine neue fachliche Entscheidung berechnen, neue SEO-Recherche vor MINI starten, zusätzliche Nutzerdateien anfordern oder eine andere K0-Route bauen. Bei ungültigem Beleg meldet der **bestehende** Binder den tatsächlichen Identitäts-/Intentfehler; keine Umgehung.

Dieser Eingang gilt für **alle** künftigen gültigen WordPress-Pakete mit beliebiger Artikelanzahl. MINI → WordPress-Regal, Writer, 81 Regeln, exakte C-Linktexte, LanguageTool 6.8, PPM und Import als Entwurf **unverändert**.


## K0-Tabellen – maßgeblich ab 21.11.2026 (nur Original-K0)

Keine Zwangstabelle bei FAQ, Beratung oder Pflege. Es gibt keine Tabellenquote. Die einzige bestehende Entscheidung vor dem Writer legt eine Tabelle nur bei **echtem, auf die Ziel-Suchfrage bezogenem Vergleichs- oder Entscheidungsnutzen** fest. Eine bloße 4×3-Matrix ohne eigenständigen Mehrwert ist ausdrücklich unzulässig; keine Füllzeilen, keine künstlichen Zahlen, keine bloße Wiederholung des Fließtextes. Für echte Artikel des Typs Vergleich bleibt eine fachlich sinnvolle Tabelle Pflicht.

`table_decision.k0_policy` ist `K0_TABLE_MEANINGFUL_ONLY_V1`. Bei INCLUDE verlangt die vorhandene Regelkontextprüfung: `reader_question` = Zielkeyword, `reader_benefit`, `why_not_prose`, `comparison_axes` (mindestens zwei) und `source_fact_ids` (mindestens zwei aus freigegebener Faktenrecherche, tatsächlich in der Tabelle verwendet). Das bisherige pauschale `INCLUDE_ADDED_VALUE` mit einer bloßen allgemeinen Begründung reicht **nicht** mehr. Bei OMIT genügt eine konkrete fachliche Begründung ohne vorgeschobenen Ausnahmegrund.

Negativbeispiel: „Wie alt ist das älteste Pferd in Deutschland?“ hat keinen sinnvoll belegten deutschlandbezogenen Vergleich. Eine Tabelle aus Old Billy, seinem Todesjahr und allgemeiner Pferdelebenserwartung ist keine passende Antwort; sie muss entfallen. Prüf- und Reparaturrücklauf bleiben im **gleichen bestehenden K0-Schritt**, kein zusätzliches Redaktionsgremium, keine Änderung anderer Beitrags- oder Linkregeln. Die getrennten historischen K10-Regeln werden nicht verändert.
