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

**Recherchequellen (verbindlich):** Vor dem Writer akzeptiert die *bestehende* Rechercheentscheidung nur freigegebene offizielle Behörden-, Hochschul-, Fachverbands- und Herstellerseiten sowie echte Wikipedia-Artikel. Private Webseiten, Blogs, Foren, fremde Affiliate-/Testseiten und eigene Portaldomains sind ausgeschlossen. Neue offizielle Domains werden erst nach Überprüfung in der zentralen Quellenfreigabe der bestehenden Recherche ergänzt; bloße Domainendung `.org` oder eine behauptete Quellenbezeichnung reichen nicht. Textstellen müssen weiterhin auf der echten Originalseite belegbar sein. Unzulässige Quellen gehen ohne zusätzliche Prüfstelle zum selben Rechercheverantwortlichen zurück; die nachgelagerten K0-Regeln bleiben unverändert.

Portalzuordnung automatisch.

Interne Links: exakt 3; `parent_category` und `semantic_related` liegen in zwei verschiedenen Haupttextblöcken, `further_information` ausschließlich im Block `further_information`. Intro, Fazit und Tabelle zählen nicht als Haupttext.

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
