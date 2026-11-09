# Pferdeatelier – ECHTER PSTE v0.57.144.25 Export 09.11.2026 / einmalige externe SEO-Fachentscheidung

**Aktueller IST-STAND (09.11.2026).** Nach tatsächlicher Testseiteninstallation von PSTE **0.57.144.25** hat der Betreiber `pferdeatelier-mini-ergebnisse-20261109-074817.json` geliefert. **Technischer Datenbestand erstmals vollständig freigabefähig und exakt nachgerechnet; externe SEO-Ergebnisdatei für 87 JA-Themen aus diesem Bestand jetzt erstellt und mit dem *tatsächlichen PSTE-v25-Importvertrag* lokal geprüft.** **Noch nicht in WordPress importiert; keine Artikel-/K0-Übergabe, kein Live-/Git-Merge.**

## 1. Echte, nun geprüfte WordPress-Quelle

Originaldatei privat in Library `/pferdeatelier/SEO-PRUEFUNG/pferdeatelier-mini-ergebnisse-20261109-074817.json`, **SHA256 `a02cb27a74bbba1365b88c7d8de1252cf916c1120132a88264336bd6d188c5d6`**, `created_utc=2026-11-09T07:48:16+00:00`. 100 MINI-Stichwörter: 87 JA, 9 VIELLEICHT, 4 NEIN; 87 eindeutige `seo_subjects`, 97 vorgeschlagene Artikeltitel (10 zweite Titelideen).

`parkhaus_complete=true`, `parkhaus_snapshot.complete=true`, `reason=""`, **Snapshot-SHA256 `b9755a7aacb86657bfa2b64804e47eb1e4994eccb5d12a3eabd971fc3b8f9ff9`**. Die Prüfsumme wurde **unabhängig mit Python und PHP aus den unverändert exportierten `sources` + `items` gemäß Original-v25-Quellcode neu berechnet, beide identisch**. Alle **1.179** Zeilen: `WORDPRESS` 1.024, `PSTE_PLAN` 1, `EDITORIAL_PLAN` 9, `PSERC_ACTIVE_PLAN` 1, `PPM679_EXISTING_EDITORIAL_RUNTIME` 144, `MINI_RESERVED` 0.

**Die bisherige echte Ursachenklasse ist auf dem Server jetzt unterscheidbar und korrekt abgegrenzt:**
- `EDITORIAL_PLAN` hat `source_origin=OPTION`, `option_item_count=9`, `filter_item_count=0`, `source_conflict=false`; alle neun sind gespeicherte **LEGACY_EMPTY_PLACEHOLDER**, `unresolved_count=0`, semantische Artikelbelegung `NONE`. Sie sind nicht stillschweigend gelöscht.
- `PPM679` enthält **144 eindeutige und weiterhin belegte Plan-Slots**, davon 141 lesbare WordPress-Beiträge und drei ausdrücklich als `HISTORICAL_ORPHAN_RESERVATION` markierte historische nicht mehr auffindbare Post-IDs **972356/972414/972560**. Diese drei Plätze bleiben weiterhin technisch BELEGT/reserviert und dürfen nicht neu vergeben werden.
- WP Canonical-Metadaten-Kollision `article:cf3b0b8f487bf47c0bbbc3f9` zwischen WP-IDs **16029** („Können Pferde schwimmen?“) und **972638** („Warum sagt man eigentlich ‚alte Schabracke‘?“) bleibt exakt im Export sichtbar; nur der zweite Post hat den eindeutigen PPM679-Plan-Slot. **Fehlerhafte Original-Metadaten nicht überschrieben oder entfernt.**

## 2. Einmalige externe SEO-Entscheidung – tatsächliches Ergebnis

**Genau EIN semantischer externer Entscheider pro 87 JA-Rohfragen, jeweils anhand des ERSTEN vorhandenen Titels**, der konkreten Bestands-Artikel und -Überschriften, bereits geplanter PSTE/PSERC-Themen, sowie Prüfung von Überschneidungen innerhalb desselben 87er-Stapels:

- **FREI: 61** – eindeutig abgegrenzte erste Titel, kein offenkundig deckungsgleicher aktiver Bestandsartikel/Plan aus der vorhandenen Metadatenübersicht; jeder hat eigenen, gegen alle 144 Bestands-Slots abgeglichenen 64-stelligen Intent-Slot.
- **BELEGT: 20** – jeweils direkter konkreter Quellbezug wie `WORDPRESS:9108` (Regendecken-Auswahl), `WORDPRESS:15617` (Regendecken reparieren), `WORDPRESS:972631` (Frieren Pferde unter Regendecken?), `WORDPRESS:17126` (Heuraufen-Auswahl), `WORDPRESS:10669` (2er-Pferdeanhänger) oder `PSTE_PLAN:867f1986-c220-408c-b71c-6449a9249cbb` (bereits eingeplante Anhängerkamera). Kein erneut geplanter Artikel hierfür.
- **KLÄRUNG: 6** – die Rohfragen `regendecken` (unklarer allgemeiner Überblick), `pferd` (zu breit/multiple Absichten), `strahlfäule pferd` (inhaltliche Abgrenzung gegen Glossar nicht aus Überschriften belegbar), `pferd decken` (Bedeckung vs. Pferdedecken), `regendecke pferd ungefüttert` (gleicher Intent wie schon im Batch freigegebene 0-g-Decke), `pferde regendecken günstig` (gleicher Intent wie bereits im Batch freigegebene günstige Regendecken). **Kein stiller SEO-FREI-Wert bei diesen Grenzfällen.**

**Relevante Eingabegrenze:** Der WordPress-Parkhausexport enthält vollständige URLs? **Nein:** Er enthält Titel, Typ, Status, Überschriften, Slugs und Prüfsummen des Artikelinhalts, aber **nicht den kompletten Volltext jedes Bestandsartikels**. Entscheidungen nutzen nur diesen nachweisbaren Bestand. Bei echten Grenzfällen bewusst KLÄRUNG statt vorgetäuschter Volltextabnahme. Die 10 weiteren, im MINI-Export vorhandenen Titelideen wurden vollständig im **privaten** Prüfbericht erhalten; der vorhandene PSTE-Import arbeitet derzeit pro JA-Rohfrage mit **`titles[0]`**, daher wurden sie ausdrücklich **nicht** als zusätzliche freigegebene Artikel erfunden.

## 3. Echte Importvertragsprüfung und Negativtests

Zwei lokale private Dateien:
- `/pferdeatelier/SEO-PRUEFUNG/pferdeatelier-seo-einmalentscheidung-20261109.json` – **der fertig importierbare Originalvertrag `PSTE_MINI_SEO_DECISIONS_V1`** mit `owner=EXTERNAL_SINGLE_SEO_EDITOR` und exakt der nachgerechneten Snapshot-SHA, **SHA256 `e50ae4eb934eddf7ec2d47feeaba5b6f30d0803756c1301d5ad545fec8dfb34c`**.
- `/pferdeatelier/SEO-PRUEFUNG/pferdeatelier-seo-einmalentscheidung-pruefbericht-20261109.json` – 87 Einzelfall-Begründungen/Bestands-Referenzen, alle 10 zusätzlich vorgeschlagenen Titelideen, **SHA256 `13578d7ae8c206e5efd01b61bd76fa141b46d2877e3bcb18078c69c82d87bc87`**.

Die **echte vorhandene PHP-Methode** `PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions` aus `PSTE-0.57.144.25-QUELLEN-IDENTITAET-KISS-NUR-TEST.zip` wurde mit den tatsächlich 100 MINI-Auswahlzeilen / 87 unveränderten `pool_key`-Bindungen, allen **1.179 echten Parkhaus-Einträgen** und der **echten 87er-Entscheidungs-JSON** direkt lokal ausgeführt: **159/159 Checks PASS**, darunter genau **61 FREI, 20 BELEGT, 6 KLÄRUNG** als vom Plugin tatsächlich akzeptierte Werte und alle 61 neuen, eindeutigen freien Slots außerhalb bereits reservierter Planplätze. Negative Tests: veränderter Snapshot verweigert, falscher Owner verweigert, doppelter Keyword-Quellschlüssel hält an, erfundener BELEGT-Beleg wird KLÄRUNG, doppelt beanspruchter Bestands-Slot wird KLÄRUNG. Ein PHP-Test-Runner und Prüf-Log liegen privat unter `/pferdeatelier/SEO-PRUEFUNG/QA/`. PHP-Syntaxcheck bestanden.

**Nicht getestet und NICHT behauptet:** Der echte `admin-post.php`-Upload oder seine atomare MySQL-Optionsspeicherung auf der WordPress-Testseite; ein echter Rückimport wurde **noch nicht** ausgelöst. Auch **kein** daraus folgender Titelplan-Reentry, kein PSERC-/K0-Artikelauftrag, keine neue Pluginversion und keine Änderung von K0, Live oder gespeicherten Original-WordPress-Werten. Der lokale Test gibt `eligible_for_article_handoff=false` zurück, wie vom bestehenden Vertrag gefordert.

## 4. Nächster konkreter Bedienungsschritt, ohne alte Diagnose

Die bereits fertige JSON `pferdeatelier-seo-einmalentscheidung-20261109.json` auf der **isolierten Testseite** in **SEO Themenengine → Themenprüfung → Externe SEO-Prüfung → „2. Extern geprüfte SEO-Ergebnisdatei“ → „Ergebnis importieren“** auswählen. Vorher **keinen neuen Parkhaus-Export**: der bestehende Snapshot-Fingerprint aus 07:48 UTC ist gebunden und bei geänderten Quellen absichtlich ungültig. Nach dem technischen Import ausschließlich die drei Statuszahlen im selben Formular prüfen (61/20/6) und die nicht vorgemerkten 10 zusätzlichen Titelideen nicht stillschweigend verlieren. **Noch nicht „an den Plan weitergeben“/K0 starten**, bevor eine echte WP-Speicher-/Readback-Abnahme bestätigt ist.

PR #682 bleibt auf dem isolierten QA-Branch `fix/pste-kisten-einmalige-pruefung-20261107` DRAFT, **nicht mergen**. Vollständige Original-SEO-Datei privat; GitHub enthält **nur Beweis, Hashes, Zahlen und Abnahmegrenzen**, keine Rohdaten.
