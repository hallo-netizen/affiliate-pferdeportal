## 14.11.2026 – RC44 GETESTET UND IM PLUGIN-BÜRO: ECHTE FRONTEND-FEHLER 14:52/14:54

**Live-Stand vor RC44 (nach RC43, Nutzerbeobachtung 14:52):** WordPress-Backend meldet 160/160 Banner aktiv/0 ohne Ziel. **Öffentliche Sichtprüfung widerspricht einer vollständigen Abnahme:** Auf `Tierkrankenversicherung` wird fälschlich ein `Hundehaftpflichtvers.`-Motiv ausgegeben, darunter ein abgesetzter dunkelgrüner `Mehr erfahren`-Button. Auf `Haus- und Grundbesitzerhaftpflichtversicherung`, `Haftpflicht & Rechtsschutz` und `Krankenversicherung & Vorsorge` meldet Nutzer keine sichtbare Banneranzeige. Diese drei fehlen noch als **tatsächlich live bestätigte Anzeige**, auch wenn RC44 das nachgewiesene Hub2-Slotproblem korrigiert.

**Drei im ORIGINAL-PHP nachgewiesene technische Ursachen und Korrekturen, KISS:**

1. **Fachlich falscher Hundebanner:** RC43 ordnete `deep=hundeversicherung` pauschal R2 `Haftpflicht & Rechtsschutz` zu und erweiterte automatisch auf alle Unterseiten, einschließlich fachfremder Tierkrankenversicherung. Die am echten Screenshot belegte Werbung lautet aber `Hundehaftpflichtvers.`. RC44 wählt für diese verifizierte Quellgruppe nur die vorhandene R3 `Hundehaftpflichtversicherung` (WordPress 786). `Tierkrankenversicherung` (815) **nicht** in den erlaubten Zielpfaden. Andere mehrdeutige fest zugeordnete R2-Angebote werden auf die passende R2-Seite selbst begrenzt und nicht blind in die fremden R3-Zweige vererbt. Echte ausdrücklich allgemeine R1-Versicherungsbanner weiterhin als Allgemeinbanner. Keine zweite Ausspielungsprüfung, nur der einzige bisherige Importentscheider.
2. **R2-Übersichtsseiten unsichtbar:** Der bisherige EINE `output_format_slot()` konnte bei R2 `hub2` fälschlich `product_after_category_tiles` priorisieren (Slot einer Unterseite) statt den real vorhandenen R2-Slot `hub_after_cards`. RC44 wählt bei einem bereits als Versicherungsziel bestätigten `hub2` direkt den **bereits passenden** echten `hub_after_cards`-Slot. Die bestehende manuelle Vorentscheidung bleibt vorrangig, andere Portale und R3 verwenden die vorherigen Regeln. Exakt der Original-PHP-Methodentest prüft `hub2→hub_after_cards`, `R3/category→product_after_category_tiles` und unveränderte non-Hab-Ausgabe.
3. **Doppelter Button mit falscher Farbe:** Im bisherigen Originalruntime-Renderpfad eines niedrigen Querbildbanners ist das **vollständige Originalbild selbst schon ein `<a href>`-Klickziel**, danach erzeugt das Plugin nochmal den identischen CTA `Mehr erfahren` inkl. grün/gelber CSS-Farbvorgabe. RC44 entfernt **nur die redundante CTA-Ausgabe und den damit überflüssigen alten HTML-Split** für diese bereits verlinkten Originalbildbanner. `Anzeige` bleibt, das Bild und sein Affiliate-Link bleiben, andere Produktkarten/Editor-Blocks bleiben unverändert. Keine CSS-/Designpluginänderung, keine Bildgrößenänderung.

**RC44 fertiges vollständiges Plugin 0.1.41-rc44**, gegen die **wirklich installierte RC43-Basis** gebaut, exakt 3 bisher vorhandene Plugin-Dateien geändert. Full PHP-QA SUCCESS https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43605029576: die 20 tatsächlichen `deep`-Produktgruppen × 8 Formate (160), kein Tierkranken-/Rechtsschutz-Leck, R2-Scope nur R2, echter Hub2-/R3-Slot, klickbares Bild ohne CTA, bisheriger privater Tarifcheck-JSON-Export/Zugriffsschutz, andere Anbieter unverändert, 25 PHP-Lints, 36 archivierte Dateien.

**RICHTIG IM OFFIZIELLEN PLUGINBÜRO ABGELEGT:** `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip` **und** `HAB_AFFILIATE_RC44_0.1.41-rc44.zip`, exakt dieselben originalen 36 ZIP-Dateien, jeweils **2.361.654 Bytes** und SHA256 `2a9701c465fdf4ac1830a6b02b9329f5613337587c65379f09be94c20b00e681`. Historische RC22-Baubasis und RC43-Version bleiben getrennt erhalten. Release: https://github.com/hallo-netizen/affiliate-pferdeportal/releases/tag/hab-affiliate-rc44-hub2-target-and-banner-only-20261114 .

**EINZIGER LIVE-ABNAHME-SCHRITT:** RC44 als Update des **bestehenden** HAB-004-Affiliate-Plugins in WordPress installieren, **Werbemittel & Ausspielung** drei Mal öffnen/aktualisieren (unveränderter 60er-Altbestand-Reconcile; ohne Neuimport), anschließend echte Frontend-Sichtkontrolle: Tierkrankenversicherung OHNE Hundehaftpflicht; Hundehaftpflichtversicherung MIT passendem Banner; R2 Haftpflicht & Rechtsschutz sowie Krankenversicherung & Vorsorge MIT Banner direkt auf der R2; keine zweite CTA und kein falsches grün. Haus- und Grundbesitzerhaftpflicht R3 zusätzlich prüfen: fehlender öffentlicher Slot ist durch die R2-Hubslotkorrektur **nicht bereits bewiesen** gelöst. **RC44 nicht als live bestanden behaupten, bis Nutzerbild den tatsächlichen Stand zeigt.**

---

## 14.11.2026, 14:52 – FRONTEND-ABNAHME FEHLGESCHLAGEN: FALSCHE BANNER UND UNNÖTIGER CTA

**Tatsächlicher Nutzer-Screenshot der öffentlichen R3-Seite Tierkrankenversicherung:** Ein als **„Hundehaftpflichtvers.“** beschriftetes Tarifcheck-Banner erscheint auf Tierkrankenversicherung, anschließend separater dunkelgrüner Button „MEHR ERFAHREN“ mit viel Leerraum. Andere drei Nutzerprüfungen: Haus- und Grundbesitzerhaftpflichtversicherung **kein Banner**, Haftpflicht & Rechtsschutz **kein Banner**, Krankenversicherung & Vorsorge **kein Banner**. Damit ist „160 aktiv / 0 gesperrt“ aus dem Backend ausdrücklich **KEINE abgeschlossene erfolgreiche Frontend-Abnahme**.

**GENAUE QUELLCODE-URSACHE DES BUTTONS nachgewiesen:** Im einzigen vorhandenen Runtime-Renderpfad `affiliate-portal-router.php` bei `overview_wide_banner_slot` wird zuerst ein kompletter klickbarer `<a class="ppar-overview-wide-banner-link" href="..."><img ...></a>` erzeugt, anschließend nochmals `<!--ppar-overview-cta-v67280--><div class="ppar-overview-wide-banner-cta-wrap"><a class="ppar-overview-wide-banner-cta" href="...">Mehr erfahren</a></div>`. **Bild und Button zeigen auf dieselbe URL.** Zusätzlicher CTA ist für reine Original-Werbebanner funktional unnötig, falsch positioniert und farblich im CSS mit `#35422A` / Hover `#C89214` fest codiert. **Empfehlung: den separaten CTA ausschließlich für fertig gestaltete Bildbanner entfernen, Bild selbst bleibt anklickbar und der Werbehinweis erhalten.** Keine reine Farbreparatur nötig. Noch **NICHT** im Frontend geändert: bestehende Hard-Rule verlangt Freigabe für sichtbare Gestaltung.

**GENAUE ZWEITE URSACHE DER FALSCHEN ANZEIGE:** RC43 ordnet `deep=hundeversicherung` fest dem R2 `Haftpflicht & Rechtsschutz` zu und der bestehende einzige Owner dehnt eine R2-Zuordnung auf sämtliche Kinder aus. Der echte WP-Baum hat unter dieser R2 **72 Seiten/Kategorien, darunter auch die fachlich getrennten R3 Hundehaftpflichtversicherung und Tierkrankenversicherung**. Das Original-Bannermotiv auf der R3 Tierkrankenversicherung zeigt jedoch ausdrücklich *Hundehaftpflicht*. Generische R2-Banner dürfen also nicht blind auf fachfremde R3-Unterbäume übergreifen. Für die 8 ursprünglichen `hundeversicherung`-Quellen ist deren jeweilige wirkliche Produktart aus einer verifizierten Originalquelle/Motiv zu ermitteln; nicht aus einem mehrdeutigen `deep=`-Wort 1:1 als Tiere-Kranken oder Hundehaftpflicht erraten. **Korrektur nur im EINEN vorhandenen fachlichen Import-/Zielentscheider, nicht als neuer Frontend-Filter/zweite Prüfung.** Die 3 leeren öffentlichen Beispielseiten sind beobachtet, ihre genaue Ursache (passender fertiger Werbeplatz/Ausgabeobjekt/Sichtbarkeit) ist noch nicht belegt. Nicht pauschal „alles behoben“ behaupten.

**Nächster Arbeitsschritt:** 1) Eine globale sichere CTA-Entscheidung treffen: originale Bannerbilder bereits klickbar → redundanten Extrabutton aus Bildbanner-Renderzweig entfernen (nur nach Freigabe), andere Produktkacheln unberührt. 2) Beim einmaligen Backend-Zuordnen für breit gefasste `deep`-Gruppen nur semantisch belegte Unterseiten als gespeicherte Ziele auswählen; vorhandene Ausgabeobjekte entsprechend einmalig korrigieren und andere 160er-Zähler nicht als Frontendbeleg ausgeben. 3) Öffentliche repräsentative R2- und R3-Seiten wirklich auf Bild, Ziel, Position, Abstand und fehlende Anzeige prüfen. Vor weiterem ZIP neue RC44-Simulation mit echten exportierten Produkt- und Ausgabeobjekten einschließlich Negativfall Tierkrankenversicherung zwingend.

---

## 14.11.2026 – RC43 LIVE-BANNER 160/160, VOLLSTÄNDIGE ZIP JETZT IM HAB-004-PLUGINBÜRO ARCHIVIERT

**Echter WordPress-Nutzernachweis (Screenshot vom 14.11.2026 um 14:38 Uhr):** „Werbemittel & Ausspielung“ zeigt **160 Banner gefunden, 160 aktiv, 160 Bilder geprüft, 0 ohne Ziel, 0 Ausgabe fehlt, 0 Ausgabe gesperrt, 0 Bildfehler und 0 blockiert**. Die Diagnose meldet „Alle gefundenen Banner sind gespeichert und veröffentlicht.“ Damit wurde der frühere Live-Fehler (80/80) **nach RC43 tatsächlich behoben**. Eine gesonderte Sichtprüfung einer öffentlichen Versicherungsseite wurde **noch nicht durchgeführt**; der Backend-Status allein beweist noch nicht die konkrete Platzierung im Frontend.

**Installierte/freigegebene vollständige HAB-004 Affiliate-Zentrale:** Plugin **0.1.40-rc43**. **Zwei exakt identische echte Git-Binärdateien im offiziellen Plugin-Büro**, jeweils 2.361.375 Bytes, 36 ZIP-Einträge, SHA256 `7e9a92fa2ee5ac93c6dce8bd4924858d661478921b6768c2103172845ed9e2e8`:
- **Offizieller aktueller Stand:** `ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`
- **Feste versionsgebundene Sicherung:** `ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/HAB_AFFILIATE_RC43_0.1.40-rc43.zip`
Die Dateien sind **im Repository selbst** eingecheckt, nicht nur als Release-Link oder bloßer Vermerk. Original-Release als unabhängiger Download: https://github.com/hallo-netizen/affiliate-pferdeportal/releases/tag/hab-affiliate-rc43-real-160-source-deep-mapping-20261114 .

**Nachweis der Archivierung:** https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43601163695 (SUCCESS). Die Git-Dateien beider ZIPs sind 2.361.375 Bytes groß und identisch; Archiv-/SHA-/36-Einträge-Prüfung bestanden. Die bisherige historische Originalversion RC22 bleibt separat als `HAB_AFFILIATE_RC22_0.1.19-rc22.zip` unverändert erhalten. Der bestehende historische Build `AFFILIATE/IMPLEMENTIERUNG_FULL_CARDS_20261112/build_candidate.py` liest nun ausdrücklich **nur diese eingefrorene RC22-Versionsdatei** als Baubasis und schreibt wie bisher temporär in `CURRENT.zip` im CI-Arbeitsverzeichnis. Dadurch bleibt der vollständige RC23–RC43-Bau reproduzierbar, während im offiziellen Büro dauerhaft RC43 als `CURRENT.zip` liegt. Ein separater RC23-Neubau inkl. vorhandener Original-QA hat im Archivierungsjob bestanden.

**Ursache und Lösung:** Alle 80 zuvor blockierten Originalbanner hatten schon ein eindeutig gespeichertes `deep=`-Versicherungsprodukt. Keine fehlenden Kategorien und keine fehlende Originalinformation. Der zentrale Entscheider erkannte 10 vorhandene Produktbezeichnungen nicht als Alias eines vorhandenen R2-/R3-Ziels. RC43 hat exakt diese 10 Gruppen (je 8 Formate) EINMAL im bestehenden Backend fachlich zugeordnet, keine nachgelagerte Zweitprüfung, keine zusätzliche Tabelle/Worker/Frontend-Logik und kein Neuimport. RC43 vollständige echte PHP-Tests 160/160 PASS: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43598368122. Ein anderes historisch festgestelltes Problem mit entfernten HTML-Attributen bleibt durch RC41s bereits integrierten Vorab-Import-Fix für zukünftige Originale abgesichert, war aber **nicht Ursache der 80 aktuellen Zielprobleme**.

**Nächster fachlicher Schritt:** Kein neues Plugin für die bereits behobene Ziellücke. Nur die **Sichtbarkeit eines konkreten vorhandenen Bannerplatzes auf einer öffentlichen Versicherungsseite** kontrollieren (Backend-„aktiv“/„veröffentlicht“ von wirklicher Bildschirmdarstellung unterscheiden). Wenn bereits sichtbar, Tarifcheck-Arbeit abschließen. Falls nicht, ausschließlich den bestehenden Anzeigenplatz prüfen, keine erneute Kategorie-/Importentwicklung.

---

## 14.11.2026 – RC43: ECHTER EXPORT BEWEIST URSACHE DER 80 BLOCKADEN; VOLLSTÄNDIGE PHP-QA BESTANDEN

**ECHTER WORDPRESS-BESTAND:** Nutzer-Export `hab-tarifcheck-bestandspruefung-20261114-130255.json`: 160 Tarifcheck-Banner, 80 auto_verified, 80 no_match; 2.599 aktive verifizierte WP-Knoten, davon Versicherung mit 5 R2 und 46 R3; 300 gespeicherte Ausgabeobjekte (80 published, 80 review, 140 superseded).

**BISHERIGE HAUPTURSACHEN-ERKLÄRUNG HIERMIT WIDERLEGT:** Ausnahmslos ALLE 80 nicht zugeordneten Originale besitzen eine eindeutige `deep=`-Produktart **im gespeicherten Werbelink und identisch im gespeicherten `_source_evidence.destination`**. Die Informationen sind für diese 80 also **NICHT beim Import verloren gegangen**. Der nachgewiesene HTML-Verlust war ein separater Bug, aber nicht deren Blockierungsursache. Auch alle 80 zugeordneten Banner haben solche Deep-Informationen.

**EIGENTLICHE URSACHE:** Der EINZIGE bisherige Hab-Versicherungs-Entscheider bestand auf wortwörtlichen Zielseiten-Namen; zehn echte spezifische Werbeprodukte haben gegenüber den vorhandenen WP-R2/R3-Kategorien abweichende Begriffe, daher genau 80× `No verified specific/general insurance`.

**BELEGTE EINMALIGE FESTE ZUORDNUNG (jeweils 8 Formate; 10 Gruppen = 80):**
- Riester-Rente, Rürup-Rente, Rentenversicherung, Lebensversicherung, Krankenzusatzversicherung → R2 `Krankenversicherung & Vorsorge` (WP 766; 40 Banner)
- Hundekrankenversicherung → R3 `Tierkrankenversicherung` (WP 815; 8)
- Haftpflichtversicherung und Hundeversicherung → R2 `Haftpflicht & Rechtsschutz` (WP 765; 16)
- Grundbesitzerhaftpflicht → R3 `Haus- und Grundbesitzerhaftpflichtversicherung` (WP 784; 8)
- Firmenversicherung → R2 `Gewerbeversicherungen & Finanzen` (WP 767; 8)
Alle zehn Ziele existieren bereits im echten verifizierten WordPress-Baum. Es müssen KEINE Kategorien angelegt werden. R2 wird nur mit ihren tatsächlichen Unterseiten verbunden; nicht mit anderen R2. Die 80 vorher aktiven Banner (zehn andere Deep-Produktgruppen) bleiben unverändert.

**RC43** (0.1.40-rc43): Nur der bisherige eine zentrale Versicherungs-Owner entscheidet anhand des einmal ausgelesenen Original-`deep`-Texts mit festem Katalog über die vorhandene reale Zielseite. Kein zweiter Klassifikator, kein Frontend-Check, keine neue DB-Tabelle, kein Neuimport. RC41-Vorabauslesen und RC42-Admin-JSON-Export bleiben erhalten.

**END-TO-END ORIGINALCODE-QA BESTANDEN:** https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43598368122 — echte vollständige PHP-Pluginmethoden, alle 20 tatsächlich in den Originaldaten vorkommenden `deep`-Produktbezeichnungen × 8 Originalformate = **160** sichere Zielentscheidungen an echten WP-Seitennamen und IDs; bestehende 80 bleiben korrekt, bisher fehlende 80 sind zuordenbar. R2/R3-Isolierung, unbekannte und Finanzbanner weiterhin gesperrt. Gesamte RC23–RC42-Regression, private JSON-Export-Sicherheit, Bildformate bestanden. Nur 3 bereits vorhandene Plugin-Dateien verändert.

**INSTALLATIONS-ZIP:** https://github.com/hallo-netizen/affiliate-pferdeportal/releases/download/hab-affiliate-rc43-real-160-source-deep-mapping-20261114/HAB_Bewahr_Affiliate_RC43_REAL_160_DEEP_ZUORDNUNG_TEST.zip — 2.361.375 Bytes, SHA256 `7e9a92fa2ee5ac93c6dce8bd4924858d661478921b6768c2103172845ed9e2e8`.

**JETZT:** RC43 als Update des bestehenden Hab-Affiliate-Plugins installieren; `Affiliate-Zentrale → Werbemittel & Ausspielung` **dreimal** öffnen/aktualisieren (unveränderter Backend-Nachlauf: 60 Originale je Besuch). KEIN Neuimport, KEIN neuer HTML-/Bilderexport. Danach Live-Übersicht prüfen: Soll bei unverändertem Bestand **160 aktiv / 0 ohne Ziel** sein – tatsächlicher Live-Nachweis steht weiterhin aus. Original-JSON enthält private Affiliate-IDs und bleibt **ausschließlich im privaten Upload**, nicht in GitHub.

---

## 14.11.2026 – RC42 ECHTER NÄCHSTER SCHRITT ERLEDIGT: EINMALIGER WORDPRESS-BESTANDS-EXPORT

**Stand:** Die dokumentierten Ursachen aus RC39–RC41 bleiben bestehen. Echte Live-Werte zuletzt **160 importiert / 80 aktiv gemeldet / 80 ohne Ziel / 0 Formatsperren** unter RC40. Diese 80 sind weiterhin NICHT geklärt, keine erfundene Wiederherstellung und keine neuen Bannerimporte.

**RC42 (0.1.39-rc42) freigegeben, ausschließlich zur Datenbeschaffung:** Der bereits vorhandene HAB-004/Affiliate-Zentrale-Plugin-Code enthält jetzt im **WordPress-Backend von Hab & Bewahr** auf **Werbemittel & Ausspielung** genau einen geschützten Button **„Tarifcheck-Bestand einmalig als JSON exportieren“**. Ein Klick erstellt **eine einzige lokale JSON-Datei** aus den tatsächlich bereits gespeicherten Tarifcheck-Werbemitteln samt vorhandener Quellfelder, Bild-/Werbelinks, bisheriger Zielentscheidung, aktuellem echtem WordPress-Versicherungsbaum sowie hinterlegten Ausgabeobjekten. **Nur Lesezugriffe: keine neue Tabelle, kein Worker, kein Schreibzugriff, kein Neuimport, keine neuen Zielentscheidungen, keine öffentliche Ausgabe und keine Änderung anderer Portale.** Für neue Banner ist RC41s geprüfte Vorab-Auslesekorrektur enthalten; der Export rekonstruiert aber NICHT früher gelöschte Original-Attribute.

**Original-PHP-Test und Sicherheit:** https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43596932545 **SUCCESS**. 160 strukturgleiche gespeicherte Datensätze (80 zugeordnet/80 ohne Ziel) durch den tatsächlich gepackten Exportcode, vorhandene WordPress-Zielknoten und Ausgabeobjekte, **exakt 0 DB-Schreiboperationen**. Zugriff bei fehlender Berechtigung, ungültiger Bestätigung und von anderen Portalen jeweils gesperrt; 25 PHP-Quelldateien syntaktisch geprüft; RC23–RC41 komplett erneut bestanden. Gegenüber RC41 exakt 3 bestehende Plugin-Dateien geändert (Backend Export, Backend Admin-Registrierung, readme/Version).

**Download:** https://github.com/hallo-netizen/affiliate-pferdeportal/releases/download/hab-affiliate-rc42-once-readonly-tarifcheck-export-20261114/HAB_Bewahr_Affiliate_RC42_EINMAL_EXPORT_TEST.zip — 2.360.773 Bytes, SHA256 `10d6ccfc5b334880040c8aeaf44498c533b0e81f135ac0c34e5da4696967f504`.

**JETZT KONKRET, nur der Nutzer:** 1) ZIP RC42 in WordPress als Update des **bestehenden** Affiliate-Zentrale-Plugins installieren; 2) **Affiliate-Zentrale → Werbemittel & Ausspielung** öffnen; 3) Button **„Tarifcheck-Bestand einmalig als JSON exportieren“** anklicken; 4) **nur diese eine JSON-Datei hier im Chat hochladen**. **Keine Screenshots, keine Banner-Neuimporte, nicht dreimal die Seite öffnen**. Datei ist privat und enthält Affiliate-Links, also NICHT auf öffentliches GitHub hochladen.

**Danach, allein Aufgabe des Assistenten:** Die tatsächlichen 80 fehlenden Fälle in der JSON-Datei anhand der dort vorhandenen gespeicherten Quellhinweise, Links, Bannerbilder, vorhandenen Zielpfade und aktiven WordPress-Kategorien einzeln und gesammelt prüfen. Zuerst belegte Fehlergruppen, erst dann EINE fachliche Korrektur in dem vorhandenen zentralen Importentscheider. Keine neuen Plugin-Zuordnungsversuche auf Verdacht.

**Zentrale Fehlerakte:** [`TARIFCHECK_160_BANNER_FEHLER_UND_NAECHSTER_SCHRITT_20261114.md`](./TARIFCHECK_160_BANNER_FEHLER_UND_NAECHSTER_SCHRITT_20261114.md)

---

## 14.11.2026 – VERBINDLICHE ÜBERGABE: TARIFCHECK 160 / 80 / 80, ALLE FEHLER UND NÄCHSTER SCHRITT

**Status: NICHT GELÖST.** Letzter echter WordPress-Stand nach RC40: 160 Tarifcheck-Banner, 80 als aktiv gemeldet, 80 ohne Ziel, 0 Formatfehler. RC39 und RC40 brachten bei den 80 ungelösten Bannern keinen Fortschritt. RC41 wurde nur auf GitHub mit echtem PHP-End-to-End-Verlauf erfolgreich getestet, **nicht zur Installation ausgegeben** und behebt nicht automatisch vor RC41 verlorene Alt-HTML-Attribute.

**Bewiesene Hauptursache:** Original-HTML wird beim Import nach `creative_library_parse_html_codes()` in `creative_library_normalize_row()` durch `sanitize_text_field()` verarbeitet, wodurch HTML-Attribute verschwinden **bevor** die RC40-Auslesung beginnt. RC40 meldet den unvollständigen Inhalt dennoch als gelesen. Reproduktionsbeweis: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43582129807. RC41 korrigiert diese Reihenfolge für künftig eingelesene Originale, Beleg: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43582511129. **Ob die 80 echten Altbanner alle dadurch betroffen sind, ist noch unbewiesen.**

**Zwingender NÄCHSTER SCHRITT (ohne Benutzer-Screenshots und Neuimport):** Im vorhandenen HAB-004-/Affiliate-Zentrale-Plugin **eine einzige nur lesende, admin-geschützte Exportfunktion** für die 160 bereits gespeicherten Tarifcheck-Banner + echten WordPress-Versicherungsbaum erstellen und mit dem Original-PHP-Plugin gegen Datenverlust/Schreibfreiheit testen. Benutzer betätigt anschließend **einmal den Export-Button** und lädt nur **eine Datei** hoch. Erst die echten Daten dieser Datei entscheiden einmalig über die 80 fehlenden Zuordnungen. Keine neue separate Zuordnungslogik, keine zweiten Prüfungen, keine neuen Worker/Tabellen, keine Bildänderungen und keine erneute Pluginfreigabe auf Verdacht. **Der Export ist derzeit noch NICHT umgesetzt; nicht so darstellen, als stünde ein Button bereit.**

**Vollständige Fehler-, Versions-, Beweis- und Arbeitsakte:**
[`TARIFCHECK_160_BANNER_FEHLER_UND_NAECHSTER_SCHRITT_20261114.md`](./TARIFCHECK_160_BANNER_FEHLER_UND_NAECHSTER_SCHRITT_20261114.md)

---

## 14.11.2026 – QUELLEN-RETTUNG OHNE NEUES PLUGIN: ORIGINALBILDER UND TRACKINGLINKS NOCH IM BESTAND

**Nachfrage „weiter, prüfe“:** GitHub-Baum von RC41 vollständig auf Dateien mit Tarifcheck-Roh-Bannercodes, exportierten Tabellen, HTML/CSV/SQL und Backups kontrolliert (1560 GitHub-Dateien). **Keine vollständigen 160 ursprünglichen HTML-Bannercodes oder Live-WP-Datenbankkopie vorhanden.** Die private WordPress-Datenbank konnte nicht unmittelbar aus GitHub abgefragt werden.

**Wesentliche Entdeckung am echten bestehenden Plugin:** `creative_library_normalize_row()` speichert die Bild-URL (`image_url`) und den Trackinglink (`tracking_url`) separat und unabhängig vom früheren Verlust einzelner HTML-Tags/Attribute. `render_creative_library_page()` zeigt vorhandene Bannerbilder bereits als Vorschaubilder in der bestehenden Kachelansicht. `creative_library_query_rows()` filtert sowohl `provider=direct:tarifcheck` als auch `topic_status=no_match` (obwohl `no_match` im Dropdown „Alle technischen Zustände“ nicht als Option angeboten wird). Der ursprünglich bestehende zentrale Zielentscheider setzt beim nicht zuordenbaren Banner `topic_status=no_match`. Damit gibt es **einen vorhandenen rein lesenden Zugang zur tatsächlichen Galerie der 80 offenen Bannermotive – ohne Neueinlesen, neues Plugin oder zusätzliche Zuordnungsentscheidung**.

**Direkter vorhandener WordPress-Admin-Filter:** `https://hab-und-bewahr.de/wp-admin/admin.php?page=affiliate-portal-creative-library&provider=direct%3Atarifcheck&topic_status=no_match`. Im Admin angemeldet lassen sich die Bannerbilder unterhalb der Filterung ansehen. Ein Screenshot der **tatsächlich gezeigten alten Motive** bietet den Beleg für die Produktart auch dann, wenn der ursprünglich gespeicherte HTML-Text schon verloren ist. Falls ein Bild selbst keine Produktart zeigt, ist die vorhandene Trackinglink-Zielseite bzw. das produktbezogene Originalwerbemittel im offiziellen Tarifcheck-Partnerportal nötig. **Kein blindes Kategorieraten aus ad_id, Bannergröße oder allgemeinem Tarifcheck-Namen.**

**Öffentliche Anbieterprüfung:** Das offizielle Tarifcheck-Partnerprogramm bestätigt, dass Banner für einzelne Produkte und verschiedene Größen bereitgestellt werden (`https://www.tarifcheck-partnerprogramm.de/werbemoeglichkeiten/`). Die ursprüngliche Produktkategorie kann im Tarifcheck-Werbemittelbereich nachgeschlagen werden; die konkrete Zuordnung der 80 privaten Datensätze ist aus öffentlichen Quellen und GitHub allein nicht beweisbar.

**Nächste Datenbeschaffung (keine zweite Engine):** Bestand im vorhandenen WordPress-Admin via bereits implementiertem Filter visuell prüfen, Bildmotive den tatsächlichen Produkttypen zuordnen, dann ausschließlich einmal die bestehende zentrale Quell-/Versicherungszuordnung auf Grundlage nachgewiesener Motive/Landingpage korrigieren. RC41 als root-cause fix für neue Imports lokal getestet, noch **kein neues Plugin zur Installation empfohlen**, weil es verlorene historische Attribute nicht wiederherstellt. Keine Frontend- oder sonstigen Portaländerungen.

---

## 14.11.2026 – Ursachenbeweis: Original-HTML vor erster Speicherung verloren / zentral korrigiert, KEIN Blind-Release

**Echter Website-Stand nach RC40 (Nutzer-Screenshots 10:33/10:34):** 160 Tarifcheck-Banner, 80 aktiv, 80 ohne nachweisbares Ziel, 0 Format-Sperren. Trotz angeblich vollständigem Vorab-Auslesen blieb die 80/80-Zahl unverändert. RC40-Tests hatten Original-HTML künstlich direkt in gespeicherte Datensätze gegeben und damit den produktiven Importpfad umgangen.

**HARTER ORIGINALCODE-BEWEIS:** `creative_library_parse_html_codes()` nimmt das komplette `<a ...><img ...></a>` an. In `creative_library_normalize_row()` läuft jedoch jeder Quellwert durch `sanitize_text_field`, **einschließlich des Felds `html`**. Dadurch werden HTML-Tags und Attribute wie `<a title="Hausratversicherung">` entfernt, bevor RC40s neuer `creative_library_read_original_banner_once()` sie auswertet. Im selben Code wird bei fehlendem echten Bildtitel der Platzhalter `Tarifcheck Banner` erzeugt; Version 1 markiert das unvollständige Quellergebnis trotzdem als vollständig gelesen. Link-URL, Bild-URL, gesondert eingelesener IMG-Titel und Alt-Feld können erhalten bleiben, aber nicht mehr sämtliche HTML-Attribute.

**Echter PHP-End-to-End-Nachweis (keine Simulation durch geänderte PHP-Methode):** https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43582129807 – **SUCCESS**. Die originalen PHP-Methoden des vollständigen RC40-ZIP wurden nacheinander ausgeführt: HTML-Parser → vollständige Original-Normalisierung → Original-Quell-Leser → erneuter Quell-Leser. Ergebnis: `<a title="Hausratversicherung">` wird im Parser gelesen, ist nach Normalisierung verschwunden; `_source_read_version=1` verhindert spätere Wiederherstellung. Echte separat ausgelesene IMG-Titel und Tiefenparameter bleiben vorhanden. **Das beweist einen Quellverlust im Ablauf, nicht dass jede der 80 echten Live-Originale ausschließlich über dieses eine verlorene Attribut erkennbar wäre.**

**RC41 Wurzelkorrektur im vorhandenen zentralen Importpfad, ohne weitere Entscheidung:** Der ursprüngliche HTML-Code wird jetzt direkt beim `creative_library_normalize_row()` **vor der Tag-Bereinigung** an genau den bestehenden einmaligen Quell-Leser übergeben. Dieser speichert **nur bereinigte, nachgewiesene Quellangaben**, nicht den ausführbaren ursprünglichen HTML-Code. Version-2-Kennung verhindert doppelte Auslesung; beim einmaligen Altbestands-Abgleich wird erhaltene originale Evidenz nicht gelöscht, eine bereits entfernte Angabe aber ausdrücklich **nicht erfunden**. Es wurde weder eine neue Ziellogik noch ein neues Format-, Anzeigen-, Worker- oder Tabellenverfahren eingeführt. Exakt vier RC40-Plugin-Dateien würden sich ändern, sonst keine.

**VOLLSTÄNDIGER TEST DER KORREKTUR:** https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43582511129 – **SUCCESS**. Original PHP-End-to-End importiert `<a title="Hausratversicherung">`, erkennt und speichert es jetzt vor der Bereinigung; vorher entfernte Attribute bleiben im separaten Legacy-Simulationstest unwiederbringlich. Alle vorherigen RC23–RC40 PHP-Tests inkl. 160 strukturähnlichen HTML-Quellen, einer Datenbank-Aktualisierung, 32 Formatausgaben und anderer Händler bestehen. Die Quellkorrektur ist unter `AFFILIATE/RC41_SOURCE_PRESERVATION/` gebaut, getestet und protokolliert. **Bewusst noch KEIN neues RC41-Plugin zur Installation veröffentlicht** – nur diese Codekorrektur führt bei bereits vor Monaten datenreduziert gespeicherten 80 Bannern voraussichtlich nicht zu den verlangten zusätzlichen Zuordnungen.

**Unvermeidbare Datenlage:** Bei bereits gespeicherten 80 Bannern gibt es weiterhin `tracking_checked` und `No verified specific/general insurance`. Original-HTML-Attribute, die beim historischen Import entfernt und weder als Link, Bild-Alt/Titel, Text noch im Payload separat erhalten wurden, sind aus diesem WordPress-Datensatz nicht mathematisch rekonstruierbar. Ohne eine nachweislich eindeutige Angabe kann keine korrekte Fachkategorie gewählt werden. Die 80 echten Original-Codes sind nicht als Datei im GitHub-Projekt/Projekt-Uploads verfügbar. **Nächste reale Beschaffung:** Originale Sammel-HTML-/TXT-Datei aus dem Tarifcheck-Werbemittelportal (nur zur Quellprüfung, NICHT erneut in WordPress importieren) oder eine sichere Darstellung der 80 verbliebenen Bannerbilder und Werbelinks. Erst daraus kann eine einzige feste Quell→Versicherungszweig-Zuordnung für alle bisherigen Originale abgeleitet und einmal gespeichert werden. Kein blinder R1-Wurf für unbekannte Finance-/Versicherungsanzeigen.

**Stand:** Nachweis und Source-Root-Fix bestanden, Altdaten-Reparatur noch nicht möglich ohne echte Originalquellen; kein behaupteter Erfolg auf der Live-Website, kein neues Installationspaket freigegeben.

---

## 14.11.2026 – RC40 SOURCE-FIRST KISS – VOLLSTÄNDIG LOKAL GEPRÜFT, LIVE NOCH OFFEN

**Verbindlicher Zielvertrag:** JEDER Banner-Workflow beginnt mit EINER Auslesung der Originalquelle. Erst danach genau EINE zentrale Bestimmung von fachlichem Versicherungsziel und bestehendem Anzeigenplatz, einmal speichern, anschließend nur noch die gespeicherten Entscheidungen anzeigen. Keine zweite/konkurrierende Themenentscheidung, kein spätes Format-Raten, keine Originaldaten überschreiben. Bestehende Bild- und Link-Sicherheitsprüfungen bleiben unverändert.

**Bisheriger Live-Nachweis (RC39, Nutzer-Screenshots 10:00):** 160 Tarifcheck-Banner, 80 aktiv, 80 ohne Ziel; 0 Formatprobleme. Die neuen Quellwörter waren vor RC40 nicht systematisch am Anfang gesichert. Der alte Import vergab beim Fehlen eines Originaltitels den künstlichen Titel `Tarifcheck Banner` und ließ dabei die Herkunftsmarkierung `title_source` weg. RC39s feste Kategorie-/Oberkategorien-Regeln konnten ohne originalen Produktbezug nicht greifen.

**RC40 (0.1.37-rc40):** Genau vier Dateien im bestehenden vollständigen HAB-004 geändert: `trait-ppar-creative-library.php`, `trait-ppar-output-objects.php`, Plugin-Versionskopf und readme. Ein **einziger portalneutraler Originalquellen-Leser** `creative_library_read_original_banner_once()` verarbeitet vor jedem automatischen Zuordnen das gespeicherte Original-HTML, Tracking-/Zieladresse, ursprüngliche Bild-/Anchor-Titel und Alt, Anbieter-Kategorie, Bildtext, aussagekräftigen Bilddateinamen und nachweisbare Tarifcheck-`deep=`-Parameter. Der Leser selbst ordnet **keine Kategorie** zu. Auslesung und Quellstatus werden im **bestehenden** Datensatz-Payload gespeichert und bei Wiederaufrufen nur gelesen (kein zweites Auslesen). Fehlender Originaltitel wird als `manual_missing` markiert; die Ersatzbezeichnung `Tarifcheck Banner` gilt nicht als Produkthinweis.

Für neue Banner wird dieses Quellmaterial im bereits vorhandenen Import erfasst. Bei den 160 bereits importierten Bannern erfolgt dieselbe Erfassung im **bestehenden** 60er-Reconcile, ohne Neuimport und ohne zusätzliche Tabellen/Worker/Frontendfragen. Der bisherige konkrete Hab-Entscheider nutzt ausschließlich diese gespeicherten Belege. Die vorgezogene, konkurrierende Vergleichsfamilien-Entscheidung entfällt für den Hab-Versicherungsweg, bleibt für andere Portale unverändert. Der Zielentscheid und seine Begründung werden in **einer** bereits vorhandenen DB-Aktualisierung abgelegt; auch ein aufgelöstes Ziel schreibt nicht mehr separat vorher. Format, Bildmaß und Anzeige bleiben unverändert, insbesondere niemals vergrößern/abschneiden.

**Vollständige Regression und Beleg:** GitHub Actions **SUCCESS**: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43580106817. Echte PHP-Methoden aus komplett gebauter Original-ZIP mit 160 strukturell realistischen, jedoch **synthetischen** HTML-Quellcodes: 40 Tarifcheck-Deep-Links + 40 echte Bild-Alt-Angaben + 40 echte HTML-Ankertexte → **120 eindeutig richtige Hausratziele**; 40 ohne Produktbezug → **40 blockiert**. Image-Dateiname mit echtem Produkttext erkannt, bloßer generischer Dateiname blockiert. Wiederholtes Lesen derselben Quelle ändert kein gespeichertes Ergebnis. Ein kompletter read-map-save-Vorgang führt zu genau **einer** Datenbank-Aktualisierung. Bisherige RC23–RC39 Original-PHP-Regressionen inklusive anderer Anbieter und 32 Format-Kontextprüfungen bestehen. Exakt vier Dateien verändert; kein neues Pluginmodul oder Anzeigeblock.

**Freigegebenes TEST-Release:** https://github.com/hallo-netizen/affiliate-pferdeportal/releases/tag/hab-affiliate-rc40-source-first-one-owner-20261114 ; `HAB_Bewahr_Affiliate_RC40_SOURCE_FIRST_TEST.zip`, 2.358.113 Bytes, SHA256 `c45eab25fa6b029faaf7c87ca52850ba81d05bc02c8f0e13330c06e6a4e25e4b`.

**Explizite Grenze:** Kein Live-Test der 160 privaten gespeicherten Banner-HREFs im GitHub-Runtime-Test möglich. Die Angaben auf dem tatsächlich gerenderten **Bild selbst** (Pixel-Schrift) werden mangels OCR nicht erkannt; HTML-Alt/Titel und Bilddateiname hingegen schon. Falls bei den restlichen 80 keinerlei auswertbarer Quellbegriff vorhanden ist, bleiben sie weiterhin blockiert. Weder 160/160 Erfolg noch eine einzelne veröffentlichte URL darf behauptet werden.

**Nächster einziger Live-Schritt:** RC40 **statt** RC39 installieren; `Affiliate-Zentrale → Werbemittel & Ausspielung` dreimal öffnen, damit der bestehende 60er-Nachlauf alle 160 gespeicherten Originale verarbeitet, **kein neuer Import**. Danach den Zählerbericht vergleichen und bei verbleibenden Sperren die tatsächlichen Original-HTML-/Bild-Dateien einmal gezielt prüfen; keine neue unbewiesene Fix-ZIP.

---

## 14.11.2026, 10:07 – RC39 reale Abnahme unverändert 80/80; originaler Importfehler reproduziert

**Reale WordPress-Bannerlage (Nutzer-Screenshots 10:00):** Tarifcheck 160 gefunden / 80 aktiv / **80 ohne Ziel** / 0 Formatfehler. RC39 brachte **keine zusätzliche Zielzuordnung**. Für die 80: `tracking_checked`, `No verified specific/general insurance`.

**Neuer Beweis (OHNE Plugin-Veröffentlichung):** https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43578958808 (**SUCCESS**). Der echte RC39-HTML-Parser und Original-PHP-Entscheider wurden mit 160 **synthetischen, strukturgleichen** HTML-Links ausgeführt. 80 mit `deep=hausratversicherung` wurden erkannt; 80 ohne Versicherungsinformation im Link wurden gesperrt – mit **genau der echten Live-Fehlermeldung**. Das Einfügen einer weiteren Kategorie in den Testbaum konnte die 80 nicht retten. Ergebnisbericht: https://github.com/hallo-netizen/affiliate-pferdeportal/blob/hab-rc39-failed-80-real-html-repro-20261114/protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ/AFFILIATE/RC39_REAL_HTML_REPRO/REPRO_ERGEBNIS_20261114.md

**Im Code nachweisbar:** `creative_library_parse_html_codes()` kann `<img title>`/Alt leer erhalten; `creative_library_normalize_row()` ersetzt dann den Titel durch `Tarifcheck Banner`, ohne dabei für diese HTML-Importzeile `title_source=manual_missing` zu belegen. Der eine Fachentscheider kann so eine nichtssagende künstliche Bezeichnung als scheinbaren Quelltext behandeln und meldet `No verified specific/general insurance`, auch wenn keine echte Versicherung ausgelesen wurde. RC39-Namenssynonyme/-Elternzuordnung greifen erst **nach** einer erkannten Versicherungsart. Deshalb war kein Erfolg bei den 80 zu erwarten, solange der Quelldecoder den Produktbezug nicht liefert.

**Grenze:** Die 160 privaten ORIGINAL-HTML-Codes sind nicht in GitHub/Uploads vorhanden; die erfolgreiche künstliche 80/80-Reproduktion beweist **nicht**, dass die 80 echten Codes keinerlei Versicherungsangaben enthalten. Auch nicht, dass alle 80 denselben fehlenden Produkt-Quellcode haben. Keine neue ZIP auf Verdacht.

**Nächster Nachweis:** In der einen WordPress-Bannerablage die 80 originalen href/src-/HTML-Daten und die tatsächlich erkannten Produktangaben **read-only** aggregieren (Partner-IDs nicht veröffentlichen), gegen den aktiven Kategoriebaum abgleichen, dann gezielt **denselben einen Import-/Entscheidweg** reparieren und mit den nachgewiesenen Fallgruppen simulieren. Ziel/Format beim Import einmal entscheiden, niemals im Frontend neu klassifizieren.

---

## 14.11.2026 – RC39 EIN FESTER KATEGORIE-OWNER + OBERKATEGORIE-VERERBUNG / KISS

**Vom Nutzer gewünschter Entscheid:** Kategoriebestand bleibt unverändert. Stabile Versicherungsbezeichnungen werden im bereits vorhandenen Importentscheider fest zugeordnet. Existiert eine konkrete R3-Seite, wird ihre echte WP-Seite mit ihren Unterkategorien als Ziel gespeichert. Existiert sie nicht, darf die **nachweislich relevante vorhandene R2-Oberkategorie** mit ihrem vorhandenen Unterbaum übernehmen. Nur **ausdrücklich allgemeine Versicherungsvergleiche** gelangen unter die gesamte R1-Hauptkategorie mit allen Kindern; eine bloße unbekannte Tarifcheck-Werbung darf nicht automatisch zu einer allgemeinen Versicherung werden. Unterschiedliche konkrete Versicherungsprodukte bleiben getrennt. Kredite/Finanzen dürfen nicht in die Versicherungswelt.

**RC39 (0.1.36-rc39) konkret:** Nur der EINE vorhandene `hb_rc31_insurance_banner_plan()`-Entscheider in `includes/trait-ppar-output-objects.php` erweitert. Feste Bezeichnungsvarianten (z. B. Kfz→Autoversicherung, PKV→Private Krankenversicherung, Hausrat→Hausratversicherung, Wohngebäude/ae/ä) werden nur auf **bestehende verifizierte WP-Zielknoten** abgebildet. Wenn kein R3 existiert, darf eine im aktiven Baum schon vorhandene, explizit passende Endkategorie ihre echte Elternseite bestimmen; alternativ die feste passende R2-Gruppe. Das vom ausgewählten realen Elternknoten ausgehende Zielset ist eine einzige gespeicherte Zuordnung und nicht mehrfach gestreute Bannerkopien. Keine Änderung an Ziel-IDs, WordPress-Kategorien, Layout, Bildskalierung, Werbeplatzvorlagen, Importen oder anderen Portalen.

**Vollständige QA mit Original-PHP statt umgeschriebenem Mock:** GitHub Actions **SUCCESS**: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43578230776
- RC23–RC38 einschließlich ursprünglicher Anbieter (Amazon/eBay/Idealo) und aller 8 Bannerformate/32 Seitenformatfälle erfolgreich.
- Neue echte PHP-Zuordnungsfälle: Hausrat-Kurzform zum echten R3; Kfz-Synonym zum vorhandenen Auto-R3 statt Motorrad; PKV zu Private Krankenversicherung; nur Endkategorie vorhanden → vorhandene R2 mit Unterbaum; spezifischer R3 fehlt → feste passende R2 mit Unterbaum; fachfremder Nachbarzweig ausgeschlossen; unbekanntes Tarifcheck-Banner ohne echten Versicherungsbeweis **blockiert**; zwei widersprüchliche Versicherungsarten **blockiert**; allgemeiner echter Vergleich erreicht weiterhin R1.
- Genau drei bereits vorhandene Original-Plugin-Dateien geändert (Zielentscheid, Versionskopf, readme). **Kein** zweiter Matcher, keine Datenbanktabelle, keine Frontendentscheidung, kein Bild-Fix.

**Freigegebene Test-ZIP:** https://github.com/hallo-netizen/affiliate-pferdeportal/releases/download/hab-affiliate-rc39-fixed-parent-mapping-20261114/HAB_Bewahr_Affiliate_RC39_FIXED_TARGET_KISS_TEST.zip (2.355.709 Bytes, SHA256 `135c97298a20da952d2ec0c1a127123cde54cc903ffbdc06f5f2e2761aa9bcfa`).

**Live-Grenze:** Vor RC39 letzter echter Nutzerstand 160 Tarifcheck-Banner, 80 aktiv, 80 ohne Ziel, 0 Format-Sperren. Die 80 privaten Original-Links liegen weiterhin NICHT im GitHub-Quellarchiv. Die neue feste Namenszuordnung kann nur helfen, wenn ein nachweisbarer Produktbegriff aus einer gespeicherten Originalquelle ausgelesen wird; bei 80 anonymen Tracking-Links ohne verwertbaren Produktnamen **müssen** unklare Banner weiterhin gesperrt bleiben. Kein Versprechen einer 160/160-Abdeckung, keine Behauptung einer echten Live-Seitenanzeige.

**Nächster Nutzerschritt:** RC39 als vorhandene HAB-004-Affiliate-Zentrale installieren (kein zusätzliches Plugin), Affiliate-Zentrale → Werbemittel & Ausspielung dreimal öffnen (bestehender 60er-Batch ohne Reimport). Echten Screenshot prüfen: aktiv / Ziel fehlt / gesperrt. Bei unveränderten 80 unklaren Originalen ist **Quelle nicht eindeutig**, keine pauschale Fehlzuordnung erzwingen. Keine weitere Pluginversion ohne echte Original-HREF-/Rubrik-Belege.

---

## 14.11.2026 – Nachprüfung: 80 ungeklärte Ziele – Plugin oder fehlende Kategorie? / Veröffentlichung belegen

**Reines Quell-Audit erfolgreich (kein Pluginrelease, keine WP-Änderung):** https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43577174436

**Konkrete Feststellungen:**
1. Der tatsächlich benutzte Kategorienbaum wird von `PPAR_HB_Integration::verified_nodes()` **ausschließlich aus den aktuellen WordPress-Optionen** `apkw_target_tree_active_snapshot_v1` und `apkw_target_tree_active_revision_v1` samt den zugehörigen realen WP-IDs zusammengesetzt. Im gepackten Plugin ist **keine vollständige Liste der live vorhandenen Versicherungskategorien gespeichert**. GitHub-Baumdaten sind Entwürfe/Tests und ersetzen keine Live-Daten. 
2. Der belegte C26-Quellplan nennt **46 R3-Owner** (darunter Hausratversicherung, Kfz-Versicherung, Wohngebäudeversicherung, Motorradversicherung, Privathaftpflicht, Rechtsschutzversicherung, Wohnmobilversicherung), ist ausdrücklich mit `NO_WORDPRESS_WRITE__LIVE_IMPORT_SEPARATE` markiert. **Kein Beleg für jede tatsächlich aktive WordPress-Kategorie.**
3. Der eine Fachentscheider `hb_rc31_insurance_banner_plan()` verwendet zur Entscheidung **nur Worttreffer auf Namen/Slugs von R2/R3-Seiten**, nicht ähnlich benannte Kategorie-Blatttexte als eigene Ausgangsziele. Er vergleicht vollständige Phrasen ohne Synonym-Liste/ähnliche Formulierungen. Dadurch kann auch eine vorhandene thematisch ähnliche Kategorie übersehen werden. Das ist eine **bewiesene Beschränkung im Code**, aber noch kein Beweis, dass sie alle 80 unaufgelösten Banner betrifft.
4. Die realen 80 unzugeordneten Datensätze stehen weiter auf `tracking_checked` und `No verified specific/general insurance`. Derselbe Grund entsteht sowohl bei **nicht ausgelesener/eindeutiger Original-Zielangabe** als auch bei **nicht passendem/fehlendem R2/R3-Namen im aktiven WP-Snapshot**. Ohne die 80 gespeicherten Original-HREFs plus den live-aktiven Kategorien-Snapshot ist eine kausale Trennung nicht möglich.
5. Die `aktiv 80`-Zahl im WordPress-Bericht ist **kein Beleg für eine bestimmte öffentlich sichtbare Versicherungsseite**. Der Bericht zeigt weder die konkreten Zielseiten noch einen Seitenlink, und ein öffentlicher Live-Aufruf von `hab-und-bewahr.de` konnte bei diesem Audit nicht verifiziert werden. Daher **keine konkrete Kategorie als 'Banner veröffentlicht' ausgeben**, solange sie nicht tatsächlich im WordPress-Ausgabeobjekt + öffentlichem Aufruf nachgewiesen ist.
6. **Beispiel vorhandene fachliche Zuordnung im C26-Konzept, nicht Live-Nachweis:** `Hausratversicherung` (R3-Owner); ähnliche Bereiche `Haus & Werte` / `Wohnen & Bauen` (je nach historischer Fassung); weder automatisch gleichwertige Versicherungsart noch Beweis eines dort tatsächlich ausgespielten Banners.

**KISS nächster Nachweis (read-only, eine Quelle):** Aus vorhandener WordPress-Bannerablage/zugehörigen gespeicherten Ausgabeobjekten einmal (a) **eine reale bereits aktive Zielseite inkl. URL und zugeordneter Tarifcheck-Banner-ID** ausgeben, (b) **80 Original-Werbelinks** gegen den **einzigen aktiven WP-Kategoriebaum** vergleichen; passende Synonyme und fehlende R3/R2 getrennt zählen. Danach ausschließlich den bestehenden einen Zielentscheider korrigieren oder fehlenden fachlich erforderlichen Kategorien-Bedarf dokumentieren. Keine neuen Entscheidungswege, keine neuen Banner, keine pauschale Zuordnung.

---

## 14.11.2026 – REALE RC38-ABNAHME, 09:06 MEZ: FORMATE ERLEDIGT / FEHLENDE ZIELDATEN VERBLEIBEN

**Echte Nutzer-Screenshots 09:06.07 und 09:06.18:** Tarifcheck: 160 gefunden, 80 aktiv, 80 Ziel fehlt, **0 Ausgabe gesperrt**, 0 Bild offen, 0 Bildfehler, 0 Entwürfe, 0 gesperrte Originale. Diagnose des verbleibenden 80er-Blocks: **80 × `No verified specific/general insurance`**, **80 × `tracking_checked`**, keine gesperrten Bildmaße. Vor RC38: 40 aktiv / 40 Format gesperrt / 80 Ziel fehlt. **Damit sind +40 Originalbanner aktiviert und alle 40 Formatfehler beseitigt**. Noch keine unabhängige Einzelprüfung der 80 öffentlich gerenderten Banner.

**Quellcodeprüfung im Original (RC31→RC38):**
- `creative_library_parse_html_codes()` liest aus dem HTML `<a href>` als `tracking_url`, setzt `destination_url` zunächst auf leere Zeichenkette; `<img title/alt>` wird nur übernommen, wenn belegt.
- `creative_library_normalize_row()` versucht echte Landing-URL zu decodieren oder über den bestehenden Import-Redirect-Resolver zu bestimmen; bei nicht endgültig entschlüsseltem Tracking-Link bleibt Status `tracking_checked`. Der Datensatz bleibt erhalten.
- Der einzige HAB-Versicherungs-Entscheider `hb_rc31_insurance_banner_plan()` prüft echte Landing-Zielinformation, vorhandene Provider-Rubrik, Originaltitel/Beschreibung und (ab RC35) den bereits gespeicherten Original-Ankertext. Nur wenn eine reale R2/R3-Versicherungsart oder ein ausdrücklich allgemeiner Versicherungsvergleich daraus eindeutig folgt, wird eine passende Zielkarte gespeichert.
- Alle 80 `No verified specific/general insurance` bedeuten **nur**, dass in den **vom Entscheider ausgewerteten** Informationen kein passender Fachbegriff gefunden wurde; sie beweisen nicht, dass der HTML-Code keine Zielinformation enthält.
- Der bekannte `deep=`-Parameter wird bisher nur für festgelegte belegte Tarifcheck-Linkhosts erfasst. Für die 80 Original-HREFs ist **weder ihre Host-/Pfadstruktur noch ihr Werbemitteltext in den Screenshots oder den GitHub-Quellen vorhanden**. Kein seriöser URL-Parser-Fix oder freie Themenzuordnung kann ohne diesen Echtdatennachweis behauptet werden.

**Einziger weiterhin notwendiger Schritt:** Die 80 bereits gespeicherten originalen Tracking-HREFs samt zugehörigen Produktnamen/HTML-Titeln einmal read-only sichten und gegen echte Ziel-URL + Anbieter-Kategorie vergleichen. Danach **nur die eine zentrale Importentscheidung** korrigieren und alle 160 prüfen. Keine Banner neu importieren; keine neuen Slots, Bildeingriffe, separaten Klassifikatoren, nachgelagerten Entscheidungen oder pauschalen Versicherungszuordnungen. Keine neue ZIP allein aufgrund einer unbewiesenen Vermutung. Der RC38-Stand bleibt für Format- und Zielabnahmen Grundlage.

---

## 14.11.2026 – RC38 EIN ZENTRALER FORMATENTSCHEID (PFERDE-ATELIER-PRINZIP) – LOKAL GRÜN, LIVE NOCH OFFEN

**Zielvertrag:** Originalbanner unverzerrt und unbeschnitten anzeigen, **niemals vergrößern**, bei Bedarf ausschließlich proportional verkleinern. Fachziel + bestehenden Seitenplatz genau einmal beim Einlesen/Backendreconcile festlegen. Der öffentliche Aufruf darf nur die gespeicherten Zielpfade und Platznamen verwenden. Bild-, Tracking-, Provider-, Freigabe- und Veto-Sicherheitsregeln bleiben bestehen, sind keine zweite thematische Entscheidung. Keine zusätzlichen Worker, Tabellen, neuen Anzeigenflächen oder anderen Portaländerungen.

**Originalbeweis:** RC37 (0.1.34-rc37) hatte noch separate starre Bildformat-Annahmen im einzigen Formatplaner (`output_format_slot`), im zusätzlich aufgerufenen kompatiblen-Slot-Scan, im Speichergate (`output_auto_contract_banner_allowed`) und in zwei öffentlichen Altfiltern (`hb_insurance_original_inline_allowed` / `hb_insurance_original_wide_allowed`). Dadurch wurden echte Formate aus der Website (120×60, 234×60, 120×600, 160×600) abgewiesen, obwohl eine proportionale Darstellung im vorhandenen Hub-/Kategorieplatz möglich ist.

**RC38-Korrektur im vorhandenen HAB-004 (0.1.35-rc38):**
- Für **verifizierte** Versicherungsbanner von Tarifcheck auf dem vorhandenen Hab-Versicherungsbaum genau eine zentrale Formatwahl, über `output_format_slot()`. Die bereits registrierten Plätze `start_after_topics`, `hub_after_cards` und `product_after_category_tiles` bleiben bestehen. Die einmalige Formatfreigabe nutzt echte Maße; kein fiktives Ziel oder Banner.
- Der früher parallel laufende, separate globale Kompatibilitätsscan wird für bereits fachlich entschiedene Tarifcheck-Originale ausgelassen. Die echte Platzliste wird anhand der einmal gewählten Freigabe gespeichert. Für andere Bannerpartner/Portale bleiben die bisherigen Abläufe bestehen.
- Das Speichern liest das Freigabeergebnis, kontrolliert weiterhin echte Bildmaße, Bildhash und gültige originale Trackinglinks, **entscheidet nicht noch einmal über das Format**.
- Beim öffentlichen Anzeigen werden für kanonisch gespeicherte Versicherungskampagnen die zwei alten Format-Fallbackprüfungen nicht mehr ausgeführt. Die bestehende Kampagnenauswahl liest ausschließlich bereits genehmigte Plätze, ohne neue Fach- oder Formatentscheidung. Andere Altbanner bleiben unverändert.
- Die vorhandenen Versicherungs-Bildelemente (normal und Querformat) verwenden intrinsische Bildgröße oder kleiner: `width:auto; height:auto; max-width:100%; max-height:420px; object-fit:contain` (nur Hab-Versicherungszweig). Kein Aufblasen von 120×60, kein Strecken, kein Abschneiden; Hochkant darf proportional bis 420 px Höhe schrumpfen.
- Bestehender einmaliger Backend-Reconcile wird mit der neuen Versionskennung ausgeführt; **keine Neuanlage/kein Neuimport**.

**Lokale Abnahme:** GitHub Actions https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43573754186 **SUCCESS**. Original PHP aus der vollständig gebauten Plugin-ZIP: 8 echte Formatklassen (728×90, 468×60, 300×250, 125×125, 120×60, 234×60, 120×600, 160×600) × 4 vorhandene Zielkontexte = **32 erfolgreich nachgewiesene Format-Kontextfälle**. Drei zu kleine Quellen bleiben ohne Skalier-Trick ausgeschlossen. Öffentliche Kampagnenregel liest gespeicherte Platzliste; alte zwei nachgelagerte Formatfilter springen bei kanonischen Hab-Versicherungskampagnen nicht an. 25 PHP-Dateien Syntaxprüfung sowie RC23–RC37 einschließlich Amazon, eBay, Idealo, Zielkarten- und Berichtstests bestanden. Exakt vier bisherige HAB-004-Dateien verändert, keine neue Engine.

**Release:** https://github.com/hallo-netizen/affiliate-pferdeportal/releases/tag/hab-affiliate-rc38-pferde-central-format-20261114 – `HAB_Bewahr_Affiliate_RC38_PFERDE_KISS_TEST.zip`, 2.354.017 Bytes, SHA256 `ff37c53a3d15479b7ac93be49fc6f4689238e08d5ccc471b24d06cdaff732d46`.

**Noch nicht bewiesen / keine Behauptung:** Wie viele der 40 bisher wegen Format gesperrten Banner nach Einbau auf der echten WordPress-Seite veröffentlicht werden. Die anderen **80** Banner mit `No verified specific/general insurance`, `tracking_checked` haben nach wie vor keine belastbare fachliche Zielkarte. Die 80 originalen HTML-HREFs sind in GitHub nicht lesbar. Keine erfundene Zuordnung, kein neues Ziel-Erkennungssystem ohne Echtdaten.

**Nächster einziger Live-Schritt:** RC38 als vorhandene Affiliate-Zentrale installieren, unter `Affiliate-Zentrale → Werbemittel & Ausspielung` die Seite **dreimal** aufrufen, damit der bisherige 60er-Batch-Nachlauf alle 160 Datensätze verarbeitet. Screenshot von Zähler und Ursachen liefern. Keine Banner neu importieren, keine zusätzliche Plugininstallation. Bei den 80 weiterhin unklaren Quellen Originalzielinformation **an derselben** zentralen Einlesestelle verifizieren; keine neue nachgelagerte Entscheidung.

---

## 14.11.2026, 08:17 – RC37: NACHGEWIESENE ECHTE URSACHENGRUPPEN UND KISS-GRENZE

**Sichtprüfung des vom Nutzer bereitgestellten echten WordPress-Fehlerberichts (zwei Screenshots, 14.11.2026 08:17):**
- 160 Tarifcheck-Originale; 40 `aktiv`, 80 `Ziel fehlt`, 40 `Ausgabe gesperrt`; 80 Originalbilder geprüft, 0 Bildfehler, 0 Bild offen, 0 Entwurf.
- Die gesamten **80 unzugeordneten** Datensätze tragen den **gleichen** im EINEN Importentscheid gespeicherten Grund `No verified specific/general insurance` und den Quellenstatus `tracking_checked`.
- Die **40 Format-Sperren** sind exakt vier Gruppen zu je 10: **120×60, 120×600, 160×600, 234×60 Pixel**.
- Bei diesen Bildmaßen handelt es sich um echte Originalformate, die mit dem realen bestehenden Slot-Vertrag aus RC36 nicht passen. 120×600 / 160×600 sind hochkant, keine bestehenden vertikalen Kategorie-Bannerslots nachgewiesen; 120×60 / 234×60 sind zu schmal für derzeitige breite Bannerplätze. Ein bloßes Absenken der Minima ohne Nachweis einer sinnvollen Darstellung wäre keine KISS-Lösung.
- Gespeicherter Status `tracking_checked` **ist kein Nachweis**, dass das Original-HTML keine fachliche Zielinformation enthält. Die RC35-Leseregel erkennt lediglich definierte Original-Linkstrukturen (bekannter Tiefenparameter und Erstpartei-Zielpfad), nicht alle möglichen externen Partnerlink-Formate. `No verified specific/general insurance` sagt nur, dass keine spezielle WP-Versicherungsseite und kein ausdrücklicher allgemeiner Vergleich im vom Entscheider gelesenen Text erkannt wurden. Quelle und tatsächlicher URL-Pfad der 80 privaten Originale sind aus dem Screenshot NICHT sichtbar.
- **Kein weiterer Blind-Release.** Nächster einzig sinnvoller Ursachenbeweis ist Einsicht in die **bereits gespeicherten Original-HREFs und Zielinfos** (datensparsam nur Link-Domain, Pfad-/Parameter-Namen ohne Partner-ID, gespeicherter Provider-Rubrikenname, erkannter Text). Danach im **einen bestehenden Importentscheid** die tatsächlich belegten Linkinformationen verwerten; keine zweite Prüfung, keine nachgelagerte Entscheidung, keine Wiederimporte.
- **Grenze der vorhandenen Belege:** GitHub enthält Code und synthetische Funktionstests, aber keinen Live-Datenbankexport der 160 Original-HREFs. Eine exakte Korrektur aller 80 aus den Screenshots wäre Spekulation. Auch die 40 „aktiven“ Banner sind als veröffentlicht gezählt, nicht durch einzelne öffentliche Seitenansichten verifiziert.

---

## 13.11.2026 – RC37 geprüft und veröffentlicht: GENAUEN ABLEHNUNGSGRUND DER ECHTEN 80 BANNER LESEN

- **Realer Ausgangsstand nach RC36:** 160 Tarifcheck-Banner; 40 veröffentlicht, 40 mit gespeichertem Ausgabeblocker (vorwiegend Designslot/Format), 80 ohne gespeicherte fachliche Zielkarte. Screenshot vom Nutzer.
- **Nachgewiesener Fehler der Diagnose:** `hab_rc34_tarifcheck_report()` unterscheidet bei `ziel_fehlt` nur `topic_targets` (kein mapped-Eintrag). Die Fachentscheidung `hb_rc31_insurance_banner_plan()` liefert aber selbst einen konkreten Ablehnungsgrund, der zuvor nicht gespeichert/angezeigt wurde. Daher kann „Ziel fehlt“ nicht als „Quelle liefert keine Zielinformation“ ausgelegt werden.
- **RC37 (0.1.34-rc37)** schreibt im bestehenden **einen** Import-Zuordnungsweg bei Tarifcheck/Hab die ursprüngliche Begründung in das **bestehende** Datensatz-`payload`; dieselbe bisherige DB-Aktualisierung, kein neuer Worker, keine neue Tabelle, keine zusätzliche Klassifizierung. Alle übrigen Regeln aus RC36 einschließlich Ziel-/Format-/Sicherheitsblockern bleiben vollständig unverändert.
- Der bestehende WordPress-Bericht liest ausschließlich gespeicherte Gründe und zeigt **aggregiert** (a) alle echten Gründe der 80 fehlenden Zuordnungen, (b) Typ der gesicherten Linkquelle, (c) Bildmaße der 40 blockierten Ausgaben. Partnerlinks, Affiliate-IDs und Original-HTML werden nicht ausgegeben. Keine zusätzliche Zielentscheidung im Bericht.
- **Lokaler Beweis:** Original-PHP aus vollständiger ZIP wurde mit simulierten Daten getestet: unmapped banner liefert genau den im einzigen Importpfad bestimmten Grund; keine erfundene Kategorie, Original-URL unverändert, 65 Originals im 60er-Batch; alle 25 PHP-Dateien, RC23–RC36, Idealo/eBay/Amazon und Format-/Frontendregressionen bestanden.
- GitHub Actions **SUCCESS**: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43482859713.
- Release: https://github.com/hallo-netizen/affiliate-pferdeportal/releases/tag/hab-affiliate-rc37-original-rejection-reasons-20261113 ; ZIP `HAB_Bewahr_Affiliate_RC37_BEWEIS.zip`, 2.353.312 Bytes, SHA256 `1270b6a5c384c701f0c7f3487fc0770e1283aba8a04db787b76377f186fa099e`.
- **Nächster einziger Website-Schritt:** RC37 als vorhandene HAB-004 Affiliate-Zentrale aktualisieren; WordPress → Affiliate-Zentrale → „Werbemittel & Ausspielung“ **dreimal** öffnen, sodass alle 160 vorhandenen Originale einmal den Grund speichern. Dann Screenshot mit neuer gruppierter Ursachenliste. Erst daraus Ursache je Gruppe beweisen, nicht aus 40/40/80 allein. Nicht erneut importieren, keine Live-Format-/Freigabeänderung, kein weiteres Plugin bis echte Gründe ausgewertet.

---

## 13.11.2026, 18:11 MEZ – RC36 ECHTE WEBSITE-ABNAHME: TEILWEISE ERFOLG, KEINE VOLLSTAENDIGE AUSGABE

Nutzer-Screenshot aus Hab & Bewahr → Affiliate-Zentrale → Werbemittel & Ausspielung, Stand Anzeige 13.11.2026 17:11 (internes WP-Anzeige-Uhrzeitfeld):
- Tarifcheck: 160 erfasste Banner, Bild offen 0, Bildfehler 0, Ziel fehlt **80**, Ausgabe fehlt 0, Ausgabe gesperrt **40**, Entwurf 0, aktiv **40**, Original gesperrt 0.
- Vor RC36: aktiv 20, Format gesperrt 60, Ziel fehlt 80. Reale Änderung nach RC36: +20 aktiv und −20 Formatfehler, aber die Hälfte der Originale ohne gespeicherte fachliche Zielzuordnung.
- Alle 40 verbleibenden gesperrten Banner melden „Kein realer Designslot passt zu Zielkontext und Bildformat.“ Die **tatsächlichen 40 Maße/Linkarten sind nicht aus dem Screenshot ablesbar** und weder in GitHub noch in ursprünglichen Uploads vollständig hinterlegt.
- Die 80 als „Ziel fehlt“ klassifizierten Banner haben in `hab_rc34_tarifcheck_report()` lediglich **keinen gespeicherten mapped-Eintrag** in `topic_targets`. Das beweist nicht, dass die Original-HTML-Codes keine Zielinformation enthalten.

**KEIN weitergehender Fix ohne Echtdatennachweis.** RC36-QA war ein isolierter Original-PHP-Test mit simulierten WordPress-Daten und vier Formaten (728×90, 468×60, 300×250, 125×125), **kein vollständiger Test aller 160 real importierten Bannercodes**. Darum nicht auf zusätzliche rechteckige/vertikale Formate oder Wortlisten raten.

Nächster zwingender Einmalschritt für Ursache:
1. Aus den bereits vorhandenen 160 WordPress-Originaldatensätzen **aggregiert und datensparsam** nach Format (Pixel), Zielstatus, gespeicherter Ziel-URL / Linkquelle (nur Typ/Host, niemals Affiliatelink oder IDs) und Fehlerart auswerten.
2. Für die 80 fehlenden Zielkarten prüfen: Ist in `tracking_url` ein eindeutiger Anbieter-Tiefenlink, ist eine echte Landingpage in `destination_url` hinterlegt, oder enthält HTML/Bannertitel eine eindeutig passende Versicherungsart? Damit klar unterscheiden zwischen „vorhandene Evidenz wurde nicht benutzt“ und „Quelle selbst liefert keinen eindeutigen Fachbegriff“.
3. Für die 40 Formatfehler **wirkliche Maße** gegen bestehende reale Designplätze und die bestehende Ausgabe vergleichen. Keine künstlichen Layouts und keine verzerrten Banner. Formatfreigabe und fachliche Zielzuordnung einmalig zentral beim Import; Frontend liest lediglich die gespeicherte Zuordnung.
4. Erst danach eine vollständig lokale End-to-end-Regression gegen die **nachgewiesenen Fallgruppen** und einen einzigen zielgerichteten Release bauen. Keine weiteren Blind-RC.

**Aktuell nachgewiesen:** 40 Banner veröffentlicht (WP-Status), nicht zwingend öffentlich gerendert. Kein weiterer automatischer Umbau auf der Live-Seite erfolgt.

---

## 13.11.2026 – RC36 TARIFCHECK-BANNER EINZIGE FORMATWAHL / LOKALE PHP-ABNAHME GRÜN

**Aktueller Hab-&-Bewahr Banner-Teststand:** `0.1.33-rc36`, komplette `HAB_Bewahr_Affiliate_RC36_TEST.zip`, 2.352.417 Bytes, SHA256 `c209d2ab37b889bd901e4aa665dde6ecce94e43f3541a2458f39e7e525a42dc4`, Release `hab-affiliate-rc36-one-format-decision-20261113`. Original-PHP-Gesamttest `https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43466588171` **SUCCESS**.

**Letzter echter Nutzer-Screenshot mit installiertem RC35:** 160 Tarifcheck-Banner, 20 Ausgabe aktiv, 60 "Kein realer Designslot passt zu Zielkontext und Bildformat", 80 "Kein fachlich freigegebener Versicherungszweig gespeichert". Dies ist **kein** Beweis, dass RC36 die echten 160 bereits freigibt. 20/60/80 sind getrennte **Ergebnisse derselben Regeln** an verschiedenen Originalen, keine verschiedenen fachlichen Prüfverfahren.

**Quellennachweis:** Die bestehende Hab-Brücke `includes/class-ppar-hab-bewahr-bridge.php::slot_matrix()` ließ in `hub_after_cards` und `product_after_category_tiles` nur breite Formate zu (Seitenverhältnis 2,5–12); der echte Versicherungs-Renderer akzeptierte aber 300×250 und 125×125 für passende Versicherungsplätze. Ein späterer `campaign_matches_contract_slot_rule()` testete die Geometrie nochmals unabhängig. Das widersprach der bereits beim Import möglichen fachlichen Bestätigung.

**RC36 nur an vier HAB-Dateien geändert:** Verifizierte Versicherungs-Originalbanner 728×90, 468×60, 300×250 und 125×125 auf dem **bereits vorhandenen** Hub-/R2-/R3-/Kategorie-Bannerplatz nach einer einzigen Importentscheidung zugeordnet, ohne neue Slots, keine gestreckten Motive, keine Fachentscheidung im Frontend; dieses liest bestehende freigegebene Platzierungen. Hohe Skyscraper/zu kleine Vorlagen werden nicht blind erlaubt. Originalbild/Tracking/Veto bleiben geprüft. Einmaliger Nachlauf der bestehenden 60er-Batches mit neuer sicherer Option, kein Reimport; andere sechs Schutzwelten, Pferde Atelier/Hobby Depot unverändert.

**Beweis:** Alle Original-Dateien aus fertiger ZIP: 16 Format-/Kontextfälle einschließlich technischer Materialisierung, negative fremde Seite und unzulässige Formate, finale gespeicherte Frontend-Platzverwendung, ursprüngliche aktive Kampagnenerzeugung, 25 PHP-Syntaxprüfungen und vollständige RC23–RC35 Provider-Regressionen bestanden. GitHub-Test mit simulierten WordPress-Daten, **kein echter private-Live-160-Datensatz**.

**NEXT ACTION:** RC36 als vorhandenes HAB-004 ersetzen; Affiliate-Zentrale → Werbemittel & Ausspielung dreimal öffnen (max. 60 pro Besuch) und neuen Ergebnis-Screenshot liefern. Prüfen, ob ehemals 60 Formatfehler zurückgehen und wie viele der 80 fachlichen Zuordnungen weiter fehlen; erst auf dieser echten Grundlage weitere zielgerichtete Änderungen. Keine Banner neu importieren, keine Verbreiterung in andere Welten, keine neue Engine, kein anderer Pluginumbau.

---

## 13.11.2026 – RC34: KISS, EINE PARTNERERKENNUNG + ECHTES BANNER-FEHLERPROTOKOLL

**NEUESTE GRÜN GEPRÜFTE HAB-004 TESTVERSION:** `0.1.31-rc34` – `HAB_Bewahr_Affiliate_RC34_TEST.zip`, 2.351.032 Bytes, SHA256 `bdd7ba78da62995768ee3c476f60fa7c18352161c7d6f9b5bade35978853cb62`, GitHub Release `hab-affiliate-rc34-single-partner-gate-diagnosis-20261113`; **Actions 43454290216 SUCCESS**, alle Altversionen RC23–RC34 komplett neu gebaut, 25 PHP-Lints, PHP-E2E und altbewährte Idealo-/eBay-/Mehrhändlertests bestanden.

**Quellnachweis doppelter Zuständigkeiten:** Der einzige fachliche Partner-Entscheider erkannte Tarifcheck anhand Anzeigename/Zieladresse, aber die bereits vorhandene 60er-Nachbearbeitung suchte nur **exakt** nach Partnername/ID `tarifcheck`. Dadurch konnten tatsächlich importierte Banner „Tarifcheck Deutschland“ oder mit abweichender Beschriftung vollständig übersehen werden; Einmallauf wurde trotzdem geschlossen. **RC34 verwendet dieselbe Partner-Erkennung in beiden Wegen** und startet nur denselben bisherigen Einmallauf kontrolliert neu. Zudem kein zweites Überschreiben bereits gespeicherter Banner-Zielpfade bei anderer normaler Creative-Library-Materialisierung. Ursprünglich in RC33 gelöste doppelte Versicherungsthema-Namensprüfungen bleiben abgebaut.

**Echtes Fehlerprotokoll:** vorhandene Seite WordPress → **Affiliate-Zentrale → Werbemittel & Ausspielung**, direkt unter Titel „Tarifcheck: Warum wird kein Banner angezeigt?“; zählt tatsächlich gespeicherte Bilder/offene Prüfungen/thematische Ziele/fehlende Ausgaben/gesperrte Kampagnen/Entwürfe/veröffentlichte Banner; nennt max. 15 wirkliche Ursachen. Keine URL-/Partnergeheimnisse im Bericht. Letzter Zählstand als WordPress-Option, **keine neue DB/Tabelle/worker**. Alles getestet auch mit echtem PHP-Kampagnenveröffentlichungsweg.

**Wichtig:** Die Ursache im Quellcode ist bewiesen, aber ohne die bisher nicht einsehbaren konkreten Tarifcheck-Liveoriginale bleibt offen, ob sie auch noch andere Blocker haben (Bild nicht geprüft, fehlender Eintrag usw.). **RC34 noch nicht WordPress-live installiert, tatsächliche Anzeige noch nicht abgenommen.** Nutzer braucht **keine Banner neu zu importieren**. RC34 installieren; **einen** Screenshot des bestehenden Werbemittelberichts senden; weitere Korrektur nur nach echten Werten. Kein weiterer blind erzeugter ZIP.

Querschnitt Pferde Atelier/Hobby Depot: derselbe strukturelle doppelte Creative-Zielkarten-Schreibweg im Quelltext belegt, auf beiden keine Änderung wegen bisher funktionierendem Livebetrieb; im zentralen Fehlerregister offen. Details `AFFILIATE/RC34_KISS_DIAG/ABNAHME_RC34_20261113.md`.

---

## 13.11.2026 – RC33 SINGLE-AUTHORITY ROOTFIX / NEUESTE GEPRÜFTE VERSION

**HAB-004 0.1.30-rc33**: vollständiges installierbares `HAB_Bewahr_Affiliate_RC33_TEST.zip`, 2.348.400 Bytes, SHA256 `b07f9dbde9267bbfa9764e36ed92787d52c96881e306e0409784e5a1ca83f51a`. GitHub Release `hab-affiliate-rc33-one-authoritative-banner-decision-20261113`; **Actions 43447823048 + zusätzliche tatsächliche PHP-Aktivierungsprüfung 43448625395 beide SUCCESS**. Die gesamte Historie RC23–RC33, alle 25 PHP-Dateien, komplette PHP-Kampagnenerzeugung, echte Zielkartenweitergabe und vorhandene eBay-/Idealo-Tests bestanden.

**Ursache, nicht nur Symptom:** Unter den bisherigen Tarifcheck-Regeln gab es bei ein und demselben Versicherungsbanner mehrere fachliche Besitzer: eine Klassifikation beim Import, einen **zweiten, Pfadunterziele wegschreibenden** Werbemittel-Speicher, eine weitere Partner-/Namensprüfung zur Anzeige und eine zusätzliche Namensrangregel für allgemeine Versicherungen. Jetzt entscheidet die vorhandene Klassifikation **genau EINMAL**; alle weiteren Schritte verwenden nur ihren gespeicherten Beleg und die exakten R3-/Endkategorie-Ziele. Die zweite und dritte fachliche Entscheidung entfernt, der zweite Schreiber für diese Versicherungsbanner abgeschaltet; Schutzprüfung auf verifizierte Bilder/Trackinglinks/Format/Veto bleibt. Alte breite Versicherungszuordnungen gesperrt, sichere Re-Zuordnung vorhandener Originale beim Aufruf des bestehenden Affiliate-Backends in 60er-Gruppen; **kein Reimport**.

**Livebeleg:** Versicherungsseiten Hausrat und Motorrad zeigen vor RC33 nur bereits gerenderten internen Ersatzhinweis, keine externe Tarifcheck-Ausgabe (Design-Rahmen funktioniert); Wassermelder drei Produkte. Erst nach RC33-Installation kann die echte gespeicherte Tarifcheck-Ausgabe überprüft werden. **RC33 noch NICHT installiert / Live-Abnahme offen.** Nutzer darf **keine** Banner neu eingeben. Zwei Besuche der Affiliate-Zentrale, dann Hausrat-/Motorrad-Frontendkontrolle.

**Unternehmensübergreifender Audit:** Dieselben zwei `topic_targets`-Schreiber auch im Quellstand Pferde Atelier und Hobby Depot nachgewiesen (einer mit, anderer ohne `path_target_keys`). Ein tatsächlich sichtbarer Fehler auf diesen Portalen ist damit **nicht bewiesen**; beide bleiben bewusst unangetastet, weil funktionierende Portale nicht blind geändert werden. Dieser strukturelle generische Doppel-Schreibweg ist noch **separat und regressiongesichert zu vereinheitlichen**, kein falscher Abschlussanspruch. RC32-Zwischenentwurf bleibt unreleased und ist durch RC33-Wurzelfix ersetzt.

Vollständiger Testbericht und Unternehmensprüfung: `AFFILIATE/RC33_ONE_DECISION/ABNAHME_RC33_20261113.md`.

---

## 13.11.2026 – RC31: TARIFCHECK INSURANCE NUR IM VERIFIZIERTEN ZWEIG, ALLE UNTEREBENEN

**Neueste vollständig getestete HAB-004-Test-ZIP:** `HAB_Bewahr_Affiliate_RC31_TEST.zip`, Version **0.1.28-rc31**. Release `hab-affiliate-rc31-insurance-branch-cascade-20261113`. GitHub Actions **43439019366 SUCCESS**, vollständige RC23–RC31-Kette, 25 PHP-Lints, produktive Zuordnungsmethoden mit Hausrat/Motorrad/generischer Versicherung und tatsächlicher Endkategorie erfolgreich simuliert; bestehende Produktkarten / Händlerfunktionen bleiben unverändert.

**Nachgewiesener RC30-Defekt:** Pauschale Tarifcheck-Mehrziel-Zuordnung verwendete teilweise den falschen früheren Bereich `Wissen > Versicherungen & Recht` statt des echten Versicherungsbaums und konnte spezifische Banner zu breit ausspielen. **RC31 nutzt nur den verifizierten echten Versicherungs-Kategoriebaum**: Spezialbanner ausschließlich auf der fachlich richtigen R2/R3-Seite und ihren echten untersten Nachkommen; echte allgemeine Versicherungsvergleiche innerhalb der gesamten Versicherungswelt. Keine Werbung in fremden Welten, keine erfundenen Zuordnungen. Bereits eingefügte Original-Tarifcheck-Banner werden ohne Reimport beim Besuch der Affiliate-Zentrale in **60er-Gruppen** automatisch neu zugeordnet (nur technisch geprüfte Bilder; keine neue Tabelle / Cron / Benutzeraktionen).

**Idealo-Abdeckung:** 20 von 52 Gruppen hatten beim letzten echten Import sichere **Idealo**-Treffer, 2.147 Produkte. Diese Kennzahl bezeichnet nicht die gesamte Portalabdeckung mit eBay und Amazon; Tresore und Wassermelder hatten öffentlich bereits Produktkarten. Die Bericht-Beschriftung wurde entsprechend korrigiert. Kein Feedwechsel. **32 fehlende Idealo-Gruppen weiter offen**, keine unbelegte Erfolgsmeldung.

**Noch nicht erledigt:** RC31 **nicht live installiert**, echte Tarifcheck-Bestände noch nicht direkt geprüft und Neu-Zuordnung noch nicht live abgenommen. Nutzer muss nur bestehendes Plugin einmal mit RC31 aktualisieren und Affiliate-Zentrale besuchen. **Keine Banner erneut eingeben**, Tarifrechner/Textlinks erst anschließend, Kurzformulare vorerst nicht.

Vollständiger Test-, Ziel- und Versionsbeleg: `RC31_INSURANCE_CASCADE/ABNAHME_RC31_20261113.md`. Historisch darunter stehende Zustände sind überholt.

---

## 13.11.2026 – RC30 NUR ANZEIGE-KENNZEICHNUNG + PRODUKT-STICHPUNKTE (OFFLINE-PASS)

**Aktuelle fertig getestete Test-ZIP:** HAB-004 **0.1.27-rc30**, `HAB_Bewahr_Affiliate_RC30_TEST.zip`, 2.346.028 Bytes, SHA256 `baa8e87cbab1f1bbbbce4f482bd73a706985f583c847f543eb93fbf7c644f34f`. Release `hab-affiliate-rc30-one-ad-label-real-bullets-20261113`; GitHub Actions **43419366272 SUCCESS**.

**Live-Ursache mit originalem öffentlichen Haustürschlösser-HTML eindeutig belegt:** Die Kategoriegruppe zeigt schon `Anzeige`, und innerhalb der ersten echten Idealo-Produktkarte wurde ein **zweites** `Anzeige` eingefügt. Die vorhandene korrekte Faktenzeile `Marke · Maße · Art.-Nr.` wurde als kleine zusammenhängende Textzeile statt Stichpunkten ausgegeben. Im einzigen vorhandenen Produkt-Renderer sind die wiederholte Produktkennzeichnung entfernt und Originalmerkmale als bis zu drei echte Stichpunkte getrennt; übersichtliche reine CSS-Gestaltung. Test mit den **echten PHP-Render-Methoden**: drei Karten, exakt EIN `Anzeige`, pro Karte 2–3 sichtbare Fakten, Originalbilder/Anbieter-Buttons/Verfügbarkeit sowie andere Banner unangetastet. **Nur 3 bestehende Dateien geändert**; Produkt-Matching/Feed/Versicherungen/GitHub-Büros anderer Portale unverändert.

**Nächster Schritt:** RC30 als Update bestehendes HAB-004 installieren, bereits bekannte Haustürschlösser-Seite neu laden, ein `Anzeige` und mehrere Stichpunkte pro Karte bestätigen. **Kein Feedimport, keine API-Prüfung**. WordPress-Liveabnahme noch offen. Vollständiger Prüfbericht `RC30_ONE_LABEL_BULLETS/ABNAHME_RC30_20261113.md`.

---

## 13.11.2026 – RC29: PRODUKTNAMEN + EXAKTE AUSGABE BIS ZUR ENDKATEGORIE (TEST-PASS)

**Neueste geprüfte vollständige TEST-Version:** RC29, Plugin **0.1.26-rc29**, GitHub-Release `hab-affiliate-rc29-product-names-leaf-contract-20261113`, `HAB_Bewahr_Affiliate_RC29_TEST.zip`, 2.345.615 Bytes, SHA256 `089a7dea5ccdd0e243e0a0116e52289bc904f97b3e2397f744b316d6063606f1`. GitHub Actions **43416103306** erfolgreich, sämtliche PHP-/Alt-/Sicherheits-Tests. Im bestehenden HAB-004 wurde die tatsächliche Ursache korrigiert: zusammengesetzte Produktnamen und bei Idealo belegte Produktbezeichnungen (Möbeltresor, Pulverlöscher, Wassersensor) werden als die vorhandenen Produktgruppen erkannt. Zweiter nachgewiesener Fehler: Stoppwörter „für/mit“ waren bereits entfernt, bevor Zubehör geprüft wurde; jetzt wird Zubehör wie „Halter für Feuerlöscher“ ausgeschlossen. Bestehende **exakte** Produktziele auf R3 und zugehörigen untersten WP-Kategorien wurden funktional mit den echten PHP-Routinen nachgewiesen; fremde Kategorien/FAQ ausgeschlossen. Nur 3 bestehende Dateien gegenüber RC28 geändert, CSS und Kategoriebaum unverändert. **Live-Feed-Abdeckung noch NICHT geprüft.** Einmal RC29 installieren und echten Feed erneut verarbeiten; keine weitere API-Prüfung oder blinder Feedwechsel. Vollbeleg `RC29_PRODUCT_NAMES_LEAF_CONTRACT/ABNAHME_RC29_20261113.md`.

---
## 13.11.2026 – HAB AFFILIATE RC28 KISS: PRODUKTGRUPPEN AUS THEMENSEITEN / WORTFORMEN

**Aktuellste geprüfte installierbare TEST-Version:** RC28 (0.1.25-rc28), GitHub-Release `hab-affiliate-rc28-kiss-topic-category-recognition-20261113`, vollständige ZIP `HAB_Bewahr_Affiliate_RC28_TEST.zip` (2.344.644 Bytes). CI `43410070887` **SUCCESS**, 25 PHP-Prüfungen, gesamte RC23–RC28-Kette, vorangegangene Produkt-/Provider-Tests und neue PHP-Fälle für echte Begriffe und Ausschlüsse PASS. Der authentifizierte WordPress-Live-Neuimport ist **noch nicht durchgeführt**, reale neue Produktabdeckung daher **unbekannt**.

**Nachgewiesene Ursache:** bisher nur Produktnamen aus untersten WP-Kategorien erkannt, nicht aus ihren veröffentlichten übergeordneten Themenseiten; zudem deutsche Umlaute, Bindestriche und Plurale zu eng gefiltert. Öffentliche REST-Abfrage zeigt **2.199 WP-Kategorien**, darunter zahlreiche redaktionelle Intent-Kategorien; **1.487 ungeklärte** sind daher **nicht** 1.487 nachgewiesene Waren. KISS-Korrektur ergänzt aus vorhandener Elternseite nur eindeutig physische Produkte, behält Versicherungs-/FAQ-Sperren und verhindert blindes Wechseln der Idealo-Quelle. **Nur 4 bestehende HAB-004-Dateien geändert**, CSS unverändert; kein neues System, kein zweiter Importer, kein anderes Portal.

**Letzter echter WP-Bericht vor RC28:** 2.194.075 Feedzeilen geprüft, 1.949 importierte Produkte, Gesamtbestand 1.960, **14 von 35** Produktgruppen versorgt, 21 ohne; die restlichen 2.180.337 `no_product_concept_match` sind **nicht automatisch relevante Sicherheitsprodukte**. Idealo-API-Daten 2747=548.821, 2901=0 allein rechtfertigen keinen Feedwechsel. **Nächster Schritt:** RC28 statt bestehendem HAB-004 installieren; **ein** realer Feed-Neuverarbeitungslauf, danach Abdeckungsdifferenz auslesen. Kein erneuter Verbindungstest nötig. Vollbeleg `RC28_CATALOG_KISS/ABNAHME_RC28_20261113.md`.

**Archivhinweis:** `HAB-004-AFFILIATE/CURRENT.zip` im Bürogebäude enthält aus Gründen der reproduzierbaren historischen Testkette weiterhin RC22 als archivierte **Ausgangsbasis** – nicht als nachgewiesen letzten Live- oder Installationsstand lesen. Für RC28 die explizit veröffentlichte vollständige Test-ZIP im verlinkten GitHub-Release verwenden. Ältere Statusabschnitte unterhalb sind historisch und teilweise überholt.

---

## 12.11.2026 – HAB-PRODUKTKARTEN GESAMTABLAUF IMPLEMENTIERT / ECHTDATEN-ABNAHME OFFEN

**Offizieller Live-/CURRENT-Stand bleibt RC22** (0.1.19-rc22); es wird KEINE halbfertige ZIP veröffentlicht. Separat im Hab-Büro wurde aus exakt diesem Stand ein eigenständiger **RC23-Quellkandidat** erstellt (kein Pferde-Atelier-Code kopiert). Er verbindet die vorhandene iPN-API zu Feed 2901/Adspace 568944 direkt mit dem bestehenden CSV.GZ-Produktimport, aktiviert Bild-Produktkarten nur nach tatsächlicher passender Materialisierung, lässt den echten Kategorie-Slot durch alle Selektoren laufen, behält bei Mehrfachanbieter-Angeboten den ursprünglichen Idealo-Button neben eBay/Amazon und bewahrt die bisherige GTIN/ASIN- und Versicherungs-Sperrlogik. **42 echte Quell-Funktionstests PASS**, 25 PHP-Syntaxprüfungen, 36/432 ZIP-CRC; GitHub Actions **43260584857**. Dennoch ausschließlich **synthetische Feedzeilen**, da private WordPress-iPN-Credentials nicht in GitHub vorliegen. Kein authentifizierter Idealo-Vollimport oder echtes Hab-Liveproduktbild nachgewiesen. Verbindliches Gesamtprotokoll + reproduzierbare Skripte: `RC23_FULL_PRODUCT_CARDS_QA_20261112.md` und `IMPLEMENTIERUNG_FULL_CARDS_20261112/`. **Keine weitere Teil-ZIP oder behauptete Fertigstellung vor echter öffentlicher Bild-/Linkabnahme.**

---

## 12.11.2026 – KORRIGIERTE PFERDE-ATELIER-LIVE-REFERENZ: Produktbilder und Mehrfachanbieter SIND FERTIG

**Belegt im echten Chrome (GitHub Run 43250905816):** Pferde Atelier /category/schabracken-beratung/ zeigt 3 konkrete Produktkacheln mit **3 echten Bildern** (2× idealo-CDN, 1× eBay) und korrekten Anbieter-Kombinationen **idealo+Amazon, eBay, idealo+Amazon**. Pferdeatelier hat auf der Live-Website Affiliate-CSS `6.72.331`, der geprüfte GitHub-Zweig `affiliate-release-current` jedoch nur Quellversion `6.72.211`: alten Quellstand **nicht als aktuellen Live-Stand kopieren**. Hab & Bewahr zeigt derzeit echte 3er-Kachelstruktur, aber **0 Produktbilder und nur 3 Amazon-Buttons**, weil die Datenquelle DataForSEO-ASINs ohne Amazon-Bilder erzeugt und Idealo-Feedprodukte weder in Live-Karten noch als Anbieter-Button nachgewiesen sind. **Der gesamte bestehende Bild-/Produkt-/Anbieter-Workflow muss wie beim Pferde Atelier übernommen werden, nicht ein weiteres CSS-Patch-Plugin. Keine neue Installations-ZIP ohne nachgewiesenen echten Hab-End-to-End-PASS.** Vollbeleg und technische Aufgaben: `REFERENZ_PFERDEATELIER_LIVE_PRODUKTKACHELN_20261112.md`. Versicherungs-Ausschluss unverändert.

---

## 12.11.2026 – HAB AFFILIATE RC22 0.1.19-rc22 – CACHE-VERSION BEI DESIGNUPDATE

**Aktuelles HAB-004:** `CURRENT.zip`, zusätzlich `HAB_AFFILIATE_RC22_0.1.19-rc22.zip`; 36 Dateien, 2.337.621 Bytes, SHA256 `c9d501396d5500e699eb6dd8d867318c41e8ea8efc43c8fe00ad9ee4ab4e32d1`. Nach RC21-Installation melden Betreiber unveränderte Kacheln; echte Website liefert jedoch RC21-Grid mit altem CSS-Versionsparameter `-hb-rc16-20261108`. Reproduktion mit altem RC20-CSS auf der echten Seite: sofort 3 riesige Blöcke untereinander; neues CSS: 3 kompakte Karten nebeneinander. RC22 koppelt CSS-URL über WP-Core `get_file_data` dauerhaft an echte Pluginversion statt alten Hardcode. **GitHub-Run 43247959556 Browser-/PHP-PASS**, neues CSS-Etikett `6.72.211-hb-plugin-0.1.19-rc22`; alle bisherigen Anbieter-/Versicherungs-/Designfunktionen unverändert. **WP-RC22 noch nicht live installiert/abgenommen**. Fotos und weitere Anbieterbuttons bleiben wegen fehlender echter Daten/GTIN offen. Gesamtbeleg: `RC22_CSS_CACHE_LIVE_20261112.md`.

---

## 12.11.2026 – HAB AFFILIATE RC21: PRODUKTKARTEN KATEGORIE KOMPAKT (OFFLINE-PASS)

Aktuelles HAB-004: **RC21 0.1.18-rc21**, vollständiges `CURRENT.zip` und `HAB_AFFILIATE_RC21_0.1.18-rc21.zip` (2.337.596 Bytes, 36 Dateien, SHA256 `0f40eddb4526434c03acdd370d2763ac5a01eaea862a40cb9ae25bb8754363bf`). Nutzer beanstandet in der Kategorie `c22-haustuerschloesser-dd9773fd40` drei riesige Amazon-Textkarten untereinander. Vorhandenes Pferde-Atelier-Slotprinzip geprüft, bestehende Hab-Kategorie-Bridge und erzwungene Alt-Mindesthöhen ursächlich. **Rootfix:** Drei existierende Affiliate-Slots im 3/2/1-Grid, reduzierte Höhen, kein neues System; weiterhin Original-ASIN/Titel/Links, echte Mehrfachanbieter-Schaltflächen nur bei exakter GTIN und aktivem Idealo-Feed. Versicherungen bleiben produktwerbefrei, andere Portale unverändert, Design RC19 unverändert. Runner 43244276656: 11 PHP-Funktions-/Integrationsprüfungen inklusive Original-Design-RC19, 25 PHP-Lints, beide ZIP-CRC PASS. **Noch nicht live installiert/abgenommen.** Release-Vertrag: `RC21_KATEGORIE_PRODUKTKACHELN_20261112.md`.

---

## 12.11.2026 – HAB IDEALO RC20 FIX; LIVEINSTALLATION AUSSTEHEND

HAB-004 RC19 enthielt die nachgewiesen falsche Sperre `feed_id === 2901` und deaktivierte dadurch beim Laden den Idealo-Haken trotz richtiger Hab-Adspace `568944`. Der Partner bietet denselben Feed für mehrere Adspaces an. Der minimale RC20-Fix bewahrt nur die fremde Adspace-Sperre `568313`; eigene Hab-Paarung `568944/2901` bleibt erlaubt. Neue vollständige RC20-`CURRENT.zip` auf GitHub, SHA256 `532d3ef2552c44cc9652881e1ff943ad7bcd8ddd93fb779f5dab1d55a08b8d97`. Fünf PHP-Testfälle, 25 PHP-Lints, 36 ZIP-CRC PASS; GitHub-Actions 43240486920. **Nicht live installiert oder live auf API geprüft.** Öffentliche Produktausgabe und automatische Aktualisierung bleiben bis zur Abnahme aus; Versicherungsbereich bleibt produktwerbefrei. Anderes Portal Hobby Depot HD-009 bleibt unverändert.

---

## 11.11.2026 – HAB-004 AFFILIATE RC19 (0.1.16-rc19) – VERSICHERUNGSBEREICH EXKLUSIV, LÜCKENLOS EIGENBANNER

**Vollständige CURRENT.zip als RC19-Kandidat im HAB-Pluginbüro gebaut:** 2.336.726 Bytes, 36 Dateien, SHA256 6d72fcd41a8b365e84815770014098946774bab7f2425c3546e48da66cd262f0 (nach bestandenem GitHub-Merge gültiger offizieller Current). Direkter, reproduzierbarer Build ausschließlich aus HAB-004 RC18 (0.1.15-rc18, verifizierte SHA256 a98063820d1564bf7cc7312c4c232369ac198bbaa49fbb6b173f76cd5096da89). **Nur vier bestehende Dateien im vollständigen Plugin verändert**: affiliate-portal-router.php, includes/trait-ppar-hb-amazon.php, assets/frontend.css, readme.txt. Keine neue Plugin-Identität, keine neue Tabelle, keine Änderung der sechs anderen Themenwelten oder des Designplugins HAB-001 RC19.

**Nutzer-Zielvertrag umgesetzt (offline):** Alle vorhandenen, aktiven Bannerplätze im Versicherungszweig von der R1-Hauptwelt über 5 R2, 46 R3, 323 Kategorien bis zu den eindeutig verknüpften Artikeln zeigen – wenn kein freigegebener Partnerbanner existiert – einen eigenen internen Hab-&-Bewahr-Versicherungs-Themenbanner. Der eigene Hinweis enthält einen aus dem aktiven Kategorie-Snapshot ermittelten internen R1/R2-Link, ist kein angebliches Tarifcheck-Angebot und hat keine erfundene Provision. Produktkarten-/Amazon-/Shop-Fallbacks werden im Versicherungszweig unterbunden; vorhandene 300×250- und 125×125-Originalbanner sind für passende Artikel/Glossar-Slots unverzerrt zulässig; 728×90 und 468×60 für entsprechende Versicherungs-Querbanner. Direktpartner Tarifcheck, Awin und ADCELL verwenden weiterhin die vorhandene zentral verwaltete Kampagnenauswahl. Ein echtes, freigegebenes allgemeines Versicherungsprogramm kann unterhalb exakt passender Programme als Fallback erscheinen; sonst eigener interner Themenbanner. Kein externes Frontend-HTTP und keine neue Werbe-Engine.

**Harter Runner-Test PASS:** 1.421 ausgeführte PHP-Funktionsprüfungen gegen 1 R1 + 5 R2 + 46 R3 + 323 Kategorien plus Beiträge / Gegenfälle, einschließlich Amazon/Finanzen-Sperre, Partner-Verbot, Freigabe allgemeiner Versicherungsvergleiche, internem Fallback in jedem geplanten Bannerplatz, 728×90 / 468×60 / 300×250 / 125×125 und Gegenproben auf eine fremde Welt. Alle 25 PHP-Dateien ohne Syntaxfehler, 36/36 ZIP-Inhalte mit CRC geprüft. GitHub-Actions-Run 43014867482; reproduzierbarer Build und echte PHP-Testquelle in AFFILIATE/IMPLEMENTIERUNG_RC19_INSURANCE.

**WICHTIGE GRENZE:** Die Tarifcheck-Partner-Bannercodes, echten Direktlinks, Rechnercodes und providerseitigen Freigaben wurden nicht übergeben. Die neue Version **erstellt keine erfundenen oder provisionsfähigen Tarifcheck-Anzeigen** und führt noch keinen Live-Test durch. Vor echtem Tarifcheck-Banner müssen Original-Werbemittel in der zentralen Affiliate-Zentrale freigegeben/zugeordnet werden. Die internen Themenbanner garantieren vorerst die optische Belegung. Vollständiger Vertrag: AFFILIATE/VERSICHERUNGEN_TARIFCHECK_KONZEPT_20261111.md Abschnitt 9. **WordPress-Installation/Liveabnahme OFFEN.**

---

## 11.11.2026 – Versicherungswerbung: ALLE Slots fachlich belegen, Tarifcheck-Backend tatsächlich geprüft

Nutzerziel **100 % Belegung mit echter Versicherungs-Partnerwerbung** für R1/R2/R3, Blätter, passende Artikel. **Priorität:** exakter Banner → belegte ähnliche/übergeordnete Versicherung → fehlendes Angebot bei Awin/ADCELL suchen → nachgewiesener allgemeiner Versicherungsvergleichsbanner (Tarifcheck oder gleichwertig) → konkrete Lücke protokollieren, kein Amazon oder Fantasieangebot. Jedes Haupt-/Bereichsthema mindestens ein fachlich passender Originalbanner nach Verfügbarkeit. Details: `VERSICHERUNGEN_TARIFCHECK_KONZEPT_20261111.md`, Abschnitt 9.

**HAB-004 RC18-CURRENT.zip am Quellcode geprüft:** „Banner & Werbemittel“ = Tarifcheck-Direktpartner, mehrere vollständige `a/img`-Bannercodes oder Bild-URL+Tracking-Link einzeln, CSV/JSON/TXT. „Rechner & Textlinks“ = eigener Tarifrechner mit Name+Original-HTML und separat Textlink mit Partner/Name und Code oder Text+Tracking-Link. Speichern allein erzwingt keine fachlich korrekte WordPress-Ausspielung; Rechner-/Textlink-Platzierung braucht noch den bestätigten zentralen Anschluss. Deshalb Nutzer darf **jetzt echte Banner erfassen**, aber RC19-Entwicklungsstand nicht als live ausgeben. Offizielles RC18-ZIP bleibt unverändert.

---

## 11.11.2026 – TARIFCHECK HAUSRAT: KONKRETE WERBEMITTEL UND SEITENPOSITIONEN (KONZEPT)

Drei Nutzer-Screenshots aus dem eingeloggten Tarifcheck-Partnerkonto bestätigen für **Hausrat** die vorhandenen Bereiche **Tarifrechner/Formulare**, **Direktlinks** und **Banner**. Tatsächlich sichtbar sind acht Maße: 120×60, 120×600, 125×125, 160×600, 234×60, 300×250, 468×60, 728×90. Der Tarifrechner bietet einen Mobilrechner; konkrete Einbettungs- und Partnerlinks sind im Screenshot **nicht** sichtbar. **Website-Platzierungsvertrag** in `VERSICHERUNGEN_TARIFCHECK_KONZEPT_20261111.md`, Abschnitt 8 ergänzt: Querbanner nur auf passend bestätigtem Hausrat-R3, 300×250 rechteckig im Fachartikel (mobil nach Text), echter Rechner einmal zentral bei der bestehenden Vergleichs-Endkategorie, Direktlink als Fach-CTA, kleines 125×125 nur unverzerrt; die Hauptwelt Versicherungen erhält nicht blind ein einzelnes Hausratbanner. Kein Amazon-/Produkt-Fallback im gesamten Versicherungszweig. Vor Installation zwingend Code/Format-/Tracking-/Datenschutzprüfung. **Dies ist eine dokumentierte Konzeptentscheidung, kein Pluginupdate.** RC18 und RC19 bleiben unverändert.

---

## 11.11.2026 – VERSICHERUNGSWERBUNG EXKLUSIV: TARIFCHECK ZUERST (KONZEPT, NOCH KEIN PLUGINUPDATE)

**Nutzerentscheidung:** Im vollständigen Versicherungszweig (Hauptseite, R2/R3, Endkategorien, eindeutig zugeordnete Beiträge/Glossare) nur nachweislich passende Versicherungs-Partnerwerbung; **kein Amazon, eBay/idealo oder Kredit-Fallback**. Quer- und quadratische Banner an bereits vorhandenen Slots. **Strategie:** Tarifcheck zunächst als bestehender Direktpartner, Awin und ADCELL erst für nachgewiesene Versicherungslücken, ohne Duplikate; Tarifcheck-„Finanzen“ bleibt außerhalb des Versicherungszweigs.

**Original-HAB-004 RC18 als ZIP auf GitHub read-only geprüft:** Die bestehende Affiliate-Zentrale besitzt bereits Direct, Awin, ADCELL, Banner-/Zielzuordnung sowie Artikel-/Glossarslots. **Aber** die Amazon-Fallbacks erlauben `core:world:insurance` mit Dokumententaschen/Tresorbild; außerdem gilt die bisherige Tarifcheck-Versicherungs-Einsortierung nur für einen fremden „Versicherungen & Recht“-Pfad, nicht lückenlos für die siebte HAB-Welt. **Also derzeit nicht umgesetzt und kein Live-PASS**. Technischer Umbau nur in HAB-004: ein einheitlicher Root-basierter Schutzfilter vor allen Ausgaben/Fallbacks und passgenaue Versicherungsziele. Design RC19 und alle CURRENT-ZIPs unverändert.

**Vollständiges Konzept und Prüfvertrag:** `VERSICHERUNGEN_TARIFCHECK_KONZEPT_20261111.md`. Erst Sperre offline prüfen, dann Original-Werbemittel aus Tarifcheck zentral freigeben und an R1/R2/R3/Beiträgen (breit und quadratisch) live testen. **Keine WordPress-Inhalte manuell bearbeiten.**

---

## 08.11.2026 – HAB-004 Affiliate RC18 0.1.15-rc18 – weltweite Amazon-Kachel-Ursache behoben (geprüfte Current-ZIP)

**Physisch im eigenen Pluginbüro:** `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`, 2.332.375 Bytes, 36 Dateien, Git-Blob `9d415e7dcae70ec1ff23a466ed6b1186134564ec`; GitHub-Runner-SHA256 `a98063820d1564bf7cc7312c4c232369ac198bbaa49fbb6b173f76cd5096da89`. **Partnerplugin HAB-001 Design bleibt RC18 0.1.191 unverändert** (84.538.023 Bytes). Vorheriges HAB-004 RC17 ist historischer Stand, nicht länger Current.

**Reproduzierte Ursache, nicht nur Symptom:** Amazon-Weltbild wurde aus `sanitize_title($world['name'])` bestimmt. Deutsches WordPress formt dabei Umlaute zu `oe/ae`; die handgeschriebenen Bildzuordnungen erwarteten `o/a`. So fehlten sämtliche Banner in den Welten *Vandalismus & Zerstörung* und *Technik & Ausfälle* einschließlich ihrer Unterebenen. Zusätzlich wurde bei Seiten die bereits vorhandene feste Knotenkennung nicht bis zum Banneranbieter weitergereicht.

**KISS-Fix:** Nur vier vorhandene Dateien im vollständigen HAB-004 geändert: Pluginheader, Original-Hab-Brücke, ursprüngliche Amazon-Fallback-Funktion und Readme. Die sechs Schutzwelten nutzen nun ausschließlich ihre **festen aktiven Knoten-IDs**. Das Design übergibt seine reale ID, die Affiliate-Brücke verifiziert sie zusätzlich gegen Seiten-ID und aktuellen Snapshot; alle vorhandenen Kampagnen, Produkte, Bilder, Amazon-Tracking, eBay/Idealo, Speicherregeln und andere Portale bleiben unverändert. Keine neue Tabelle/Engine, keine neue kostenpflichtige Suche.

**Ursachenbeweis mit echtem HAB-001-Designbaum und deutscher Umlautbehandlung:** vor Änderung nur **282/415** Bannerkontexte mit Ausgabe (4/6 Welten, 21/31 R2, 63/93 R3, 194/285 Blattkategorien); danach **415/415** (6/6, 31/31, 93/93, 285/285). Zusätzlich 25/25 PHP-Syntax, 36/36 ZIP-CRC, alle 32 unbetroffenen Einträge inhaltsgleich. Build des tatsächlichen GitHub-CURRENT aus unabhängig abgezogener offizieller RC17-Datei mit 36/36 identischen Datei-Inhalten; GitHub-Actions-Run `42505319754` erfolgreich. Der Dateisatz ist für die vier geänderten Dateien per SHA256 abgesichert und der Build reproduzierbar dokumentiert: `AFFILIATE/RC18_BUILD_FROM_RC17.py`.

**Noch nicht behaupten:** Eine WordPress-Live-Abnahme dieser neuen RC18 fehlt. Nutzer-Screenshots hatten Wasser & Leckage für RC17 bestanden, Vandalismus RC17 NICHT. **Nach Installation nur HAB-004 Affiliate RC18 zusätzlich zum installierten Design RC18 prüfen:** Vandalismus und Technik plus je eine Unterseite und Blattkategorie; bereits bestätigte Wasser-Kacheln dürfen nicht verschlechtern.

---

## 08.11.2026 – VERBINDLICHE HAB CURRENT-RELEASE: DESIGN RC18 + AFFILIATE RC17

**Tatsächlich im offiziellen Pluginbüro als vollständig neu gebaute, geprüfte `CURRENT.zip` auf dem geschützten Releasezweig; Veröffentlichung nach Merge:**
- **HAB-001-DESIGN 0.1.191 (RC18)**: `PLUGINS/ISOLIERTE_PLUGINS/HAB-001-DESIGN/CURRENT.zip`; 84.538.023 Bytes; **SHA256 `def9ceb5a99eb965aa55805038d92e93e53747191786edc9f44fe74bbe560a7e`**, Git-Blob `04f8ef38c649049cebcc12f240471a66d270a465`; **432 Dateien**, 35/35 PHP-Lint und 432/432 ZIP-Inhaltsverifikation.
- **HAB-004 Affiliate-Zentrale 0.1.14-rc17**: `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`; 2.331.918 Bytes; **SHA256 `b22e4d49a56b25e3fc2e46c9bdd0ccbd7c6c16eb7c1f6bb48ae005db0ba50a03`**, Git-Blob `e8f5d5c77459a2e94b77c093f7c58883a2e4386c`; **36 Dateien**, 25/25 PHP-Lint und 36/36 ZIP-Inhaltsverifikation.
- Ausgangs-ZIPs **wort-/bytegenau aus dem offiziellen Pluginbüro erneut geprüft**: Design 0.1.189 SHA256 `947a950273edb6bf47e76ffeef67ff51425db620adc2650c742831e73093134c`; HAB-004 RC11 SHA256 `cf8cf7946aa7605dadecda1f041cfc6fb150c7971f7c9feb9dbb6dd1ac8eabda`. Alle Altdateien übernommen. Nur belegte Quelländerungen von RC18/RC17 zugespielt; sieben bereits in HAB-001 vorhandene Themenfotos für HAB-004 bytegleich kopiert. **Kein neues Plugin, keine neue DB, keine Änderungen an Pferdeatelier/Hobbydepot, kein bezahlter Suchlauf.**

**Nutzer-Liveabnahme der VORGÄNGER RC17 Design + RC16 Affiliate vom 08.11. 15:25–15:36:** Kachelfotos PASS, Raster-Kacheln formatfüllend PASS. **Noch offen / durch neuen RC18-Kandidaten offline korrigiert:** Einteilungslogik auf allen Kategorieebenen, auch bei vollständig gefüllten Zeilen; hoch-nach-unten-Bildverlauf in Amazon-Rasterkacheln, größerer am unteren Rand platzierter offizieller Amazon-Button, Hover auf Beitragsvorschauen, präzise Produktsuche statt „Wasser & Feuchtigkeit“ → Luftbefeuchter. Browser mit echten Originaldateien/CSS: **42 Konstellationen** aus sechs Bildschirm-/Rastertypen, darunter Hauptwelt/R2/R3, 900/390 px, plus 12 gesonderte Screenshots/Prüfungen bei 1250px, keine Überläufe, CTA sichtbar, Originalbutton und Hover. PHP-Funktionstest: **17 konkrete Zielzuordnungen** bestanden. **Echte WordPress-Liveabnahme dieser NEUEN Versionen noch offen**; nicht als schon installiert ausgeben.

**Korrekturregel Amazon:** Nicht die bloße Themenüberschrift „Wasser & Feuchtigkeit“ als Suchwort: gezielt `Wassermelder Leckagesensor Wasserstopp`; für Leckage/Rückstau/Siphon passende physische Schutz-/Reparaturprodukte; feste Themenbäume statt geratenem Amazon-Kategorieausgang; nur bestehender Hausbanner als nachrangiger Fallback. Benutzerwunsch gilt für alle Schutz-/Kategorienebenen, einschließlich voller Reihen. Versicherungsstrang bietet thematisch Dokumentenschutzartikel, **keine als Versicherungsleistung ausgegebenen Amazon-Produkte**.

**Zulässige nächste Aktion:** Die beiden neuen aktuellen `CURRENT.zip` im WordPress-Backend als Updates installieren; dann an mehreren Hauptwelten und R2/R3 inklusive Vandalismus, Wasser und unterster Kategorie testen, volle Reihen, Handyansicht, Amazon-Ziel und Beitrag-Hover. Keine RC16/RC17-Vorinstallation nötig; immer beide aktuellen Zips zusammen. 

---

## 08.11.2026 – HAB-004 RC14 – Kategorie- und Beitragsbanner, CHAT-TESTVERSION

**Aktueller vollständig installierbarer CHAT-KANDIDAT**: `Hab-und-Bewahr-Affiliate-RC14-Kategorien-und-Beitraege.zip`, **0.1.11-rc14, 2.092.433 Bytes, SHA256 b524b5fbd06b15bbe8425c0d7da2b5c28b2eb2b1896dee9a7e8fd84443e8a7e4**, 35 Dateien (28 Originale + sechs freigegebene Hab-Weltmotive + originaler Hobbydepot-Amazon-Badge). RC11/RC12/RC13 als notwendige Zwischeninstallation **NEIN**. `HAB-004/CURRENT.zip` auf GitHub bleibt bis zur gesonderten Synchronisierung weiter RC11, NICHT RC14. **Noch nicht live abgenommen.**

**Harter Quellabgleich:** HAB-001 Original, HAB-004 RC13, Hobbydepot HD009 **0.1.25**. Bereits vorhandene Banner-/Kampagnen-/Glossar-/Artikel-Slots wiederverwendet, keine neue Architektur. 6 eindeutige Hauptwelten mit je eigenem ORIGINAL-Hab-Themenfoto; alle nachgeordneten Themen, WordPress-Kategorien und eindeutig zugeordneten Beiträge/Glossarbegriffe erben das Weltmotiv; Amazon-Suchthema bleibt konkret. Versicherungen: ohne passende physische Amazon-Kategorie KEIN täuschender Amazon-Banner. Breite Banner 6:1 PC, 4,2:1 mobil, Glossar und Beitrags-Seitenleistenquadrat 1:1. Offizieller, einziger Amazon-Button aus HD009 in Orange, kein Portal-Logo/Zusatztext, keine Mehrfachrahmen. Echte Kampagnen haben Vorrang. Keine neuen bezahlten Suchläufe und keine Änderungen an eBay/Idealo-Produkten.

**Prüfung:** 63 PHP-Funktionstests bestanden, 25/25 PHP-Lint, 35/35 ZIP-CRC, alle bisherigen Originaldateien enthalten. In Chromium bei 1250/390 px alle 4 realen Bilder geladen, kein horizontaler Überlauf, korrekte Formate. Detailbericht: `AFFILIATE/RC14_BANNER_KATEGORIEN_BEITRAEGE_20261108.md`.

**Nächster Schritt:** RC14 als reguläres HAB-004-Update in WordPress installieren, echte Screenshots Kategorie Wassermelder + zweite Schutzwelt, Glossar + Beitrag prüfen. Erst dann Live-PASS. Einzelproduktbilder (Amazon ASIN) weiterhin **nicht** behoben.

---

## 07.11.2026 – RC13 BANNER: IM CHAT ALS TEST-ZIP, NOCH NICHT LIVE

**Aktuell erzeugte vollständige HAB-004-Testversion:** `Hab-und-Bewahr-Affiliate-RC13-Banner-Test.zip`, Version `0.1.10-rc13`, 627700 Bytes, SHA256 `4179371267f4d983b095ab846166c9d9dd44eb010c54e18ca3d808585c617f1e`. Im **Chat zum Herunterladen**, **NICHT** im GitHub-`CURRENT.zip`. Es gilt weiterhin: **GitHub-`CURRENT.zip` = RC11, live 16:47 durchgefallen**; RC12 wurde vom Nutzer nie installiert. RC13 enthält RC12 vollständig, also kein vorheriges RC12-Upgrade nötig.

**Was tatsächlich offline bestanden hat:** vorhandene RC12-House-Banner-Ausgabe nach dem HD009-Original für 4.2:1-Quer-/1:1-Quadratbanner mit Original-Hab-Themenfotos und Amazon-Kategoriesuchlinks; echtes HAB-001-Glossar nutzt bisher ungenutzten Original-Filter `hbdp_glossary_ad_markup` für das Quadrat in der Seitenleiste, statt tote `the_content`-Hooks. Gebuchte Werbung/Schalter/keine passenden Bilder beachtet; keine neue Engine und keine Fremdportal-Änderung. 20 Funktionsproben, 25 PHP-Lints, 28 ZIP-CRC, Original-WebP mit 1200/1024/390px-Layout PASS. **WordPress-Live-Abnahme fehlt**, echte Amazon-Einzelproduktfotos weiterhin ungelöst. Details: `AFFILIATE/RC13_BANNER_ABNAHME_20261107.md`. **Keinen neuen kostenpflichtigen DataForSEO-Lauf auslösen.**

---

## 07.11.2026, 16:47 Uhr – RC11 live NICHT BESTANDEN (Screenshotbeweis)

- Wassermelder-Frontend: 3 ASIN-Produkttitel und Amazon-Links, **riesige leere Bildkarten**, nicht die funktionsfähige Pferdeatelier-Produktdarstellung. Das ursprüngliche `hb_amazon_product_family_markup` übergibt bewusst `image_url=''` an unveränderten Karten-Renderer, der eine 150-Pixel-Bildzeile und 360-Pixel-Mindesthöhe erzwingt.
- Bestehender Affiliate-Bannerslot im Design meldet **kein passendes Werbemittel**. In `PPAR_HB_Integration::area` wird bei echten WordPress-Kategorie-Knoten `kind=banner` ausdrücklich verweigert. Für Seiten benötigt die reguläre Bildbanner-Ausgabe eine gültige Bild-URL; Hab-Amazon-Fallback erzeugt nur Textlinks. Damit fehlen Amazon-Übergangsbanner.
- Harter Quellabgleich mit aktuellen Originalen **Pferdeatelier**, **Hobbydepot HD009 0.1.20**, **HAB-001 Design** und **HAB-004 RC11** vom 07.11.2026. Hobbydepot benutzt für freie Bannerplätze bereits einen Amazon-Suchlink **mit thematisch freigegebenem Portalbild** in der bestehenden Ausgabe; Pferdeatelier rendert reale Produktkarten mit echten Quellbildern und Mehranbieter-Buttons. Keine Erweiterungsarchitektur nötig.
- Hab speichert aus DataForSEO bewusst nur ASIN/Titel; **keine rechtlich abgesicherte Amazon-Produktbildquelle**, keine Creators-/PA-API in HAB-004. Drittanbieter-`image_url` nicht ohne geprüfte Nutzungsrechte als Amazon-Foto übernehmen. Amazon-Partnernet-Richtlinien: https://partnernet.amazon.de/help/operating/policies
- **Status: RC11 ist kein live abgenommener Fix; vor weiterem Installer vollständige Produkt-/Bannerquelle und Ausgabe prüfen.** KISS-Ziel: gebuchte Kampagnen zuerst, sonst Themenbanner nach Hobby-Modell im gleichen Slot; Einzelprodukte nur mit echtem zulässigem Produktbild, bei identischem Artikel eBay/idealo im vorhandenen Mehranbieter-Renderer. Keine neue Datenbank, keine andere Portaländerung, keine kostenpflichtige DataForSEO-Suche ohne Bedarf.

---

## 07.11.2026 – HAB-004 0.1.8-rc11 – EINZIGER AKTUELLER STAND

**Installations-ZIP:** `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`; **624,020 Bytes**, **SHA-256:** `cf8cf7946aa7605dadecda1f041cfc6fb150c7971f7c9feb9dbb6dd1ac8eabda`; 28 ursprüngliche Dateien, davon **24 gegenüber RC10 unverändert**. WordPress-Pluginordner bleibt `affiliate-portal-router/`. Vorgänger RC10 ist nur noch über Git-Historie, kein zweites CURRENT.

**Ursache beseitigt (Quell- und offline simulierte Frontend-Ausgabe):** HAB-001 reicht echte WordPress-Kategorien an den bestehenden Filter weiter; HAB-004 wies bislang alle Kategorien ab. RC11 verbindet **nur den vorhandenen Kategorie-Anschluss** mit `provide_leaf_category_affiliate_slot_html`, priorisiert die unveränderte Kampagnenauswahl und zeigt bereits gespeicherte, fachlich passende DataForSEO-Amazon-ASINs als **einzelne Produktkarten** mit dem ursprünglichen `render_banner`. R3-Themenseiten erhalten ebenfalls einzelne Karten statt zusammengeklebter Textlinks. **Ohne gespeicherte gültige ASIN kein leeres/erfundenes Produktangebot.** Keine falschen Bilder, Preise oder Verfügbarkeit.

**Abnahme:** Original-RC10-Fehler reproduziert; vollständiges HAB-004-RC11 samt tatsächlichem HAB-001-Designaufruf offline getestet. Kategorie „Wassermelder“ und R3 „Leckwarnung & Absperrung“ jeweils zwei getrennte geprüfte Amazon-Testlinks mit Hab-Tracking-ID, gebuchte Anzeigen haben Vorrang, Hauptschalter AUS respektiert, unbekannte/produktlose Kategorien bleiben leer. **18 getrennte PHP-Regressionstests, 34 PHP-Syntaxprüfungen (einschließlich Prüfscripten), 28/28 ZIP-CRC, alle erfolgreich.** Testnachweis `AFFILIATE/IMPLEMENTIERUNG_RC11/PRUEFBERICHT.md`. Pferdeatelier 6.72, Hobbydepot HD009 0.1.19 und HAB-001/002/003 nicht geändert. Kein weiterer bezahlter DataForSEO-Auftrag.

**Noch nicht live abgenommen:** RC11 muss als **Update des bestehenden HAB-004** in WordPress installiert werden; dann die vorhandene Kategorie „Wassermelder“ und R3 „Leckwarnung & Absperrung“ im Frontend prüfen. Hauptschalter der Affiliate-Zentrale muss eingeschaltet sein. Die separate serverseitige WP-Cron-Ursache ist nicht hiermit repariert. **Keinen neuen kostenpflichtigen Suchlauf anstoßen**; gespeicherte ASINs genügen zum Test.

---

## 07.11.2026 – VERBINDLICHE KISS-SPERRE VOR WEITEREM HAB-004-CODE / KEINE NEUE VERSION

**Dreifachprüfung Pflicht:** Vor jeglicher weiteren Änderung zuerst Pferdeatelier-Originalquelle und Hobbydepot-Originalplugin lesen, dann prüfen, welche Ausgabe bereits im aktuellen HAB-004/HAB-001 vorhanden ist. Keine neue Ausgabe-Architektur, keine zusätzlichen Plugins oder Datenbanken, keine unerprobten Kleinfixes. Vollständiger Quell- und Screenshotabgleich: `AFFILIATE/PRUEFUNG_BESTEHENDE_AUSGABE_20261107.md`.

**Ursache bei „Wassermelder“ im echten Design und Affiliate-Code nachgewiesen:** Das aktuelle HAB-001-Design ruft `hbdp_area_product_cards_html` mit einem Kategorie-Knoten auf; HAB-004s vorhandener Anschluss `PPAR_HB_Integration::area()` verwirft alle Knoten außer `type=page`. Dadurch erscheint bei der Kategorie „Wassermelder“ die vorhandene Empfehlung leer. Die Seite „Leckwarnung & Absperrung“ hat dagegen drei ASIN-Links innerhalb eines selbstgebauten Text-Fallbacks, nicht als reguläre Produktkampagnen. **Grundfunktionen für echte Kategorien-Produktslots und Kampagnenausgabe sind bereits im HAB-004 vorhanden.** Der Fehler liegt primär in der Verbindung/Verwendung.

**Status:** BISHER NUR LESEND GEPRÜFT – NICHT BEHOBEN, KEIN NEUER HAB-004-BUILD, KEINE LIVE-ÄNDERUNG. Für späteren Build zuerst die aktuelle vollständige HD009-ZIP selbst gegen Hab und Pferdeatelier vergleichen und dann einen einzigen End-to-End-Test im echten HAB-001/HAB-004-Hook-Weg bestehen lassen. DataForSEO-Titel und ASIN rechtfertigen keine erfundenen Produktfotos oder Preise.

---

## 07.11.2026 – HAB-004 RC10, einziger aktueller ZIP-Stand
**ZIP:** `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`, **623469 Bytes**, SHA-256 `f3b6b0ac4fd05310fa32ce68e2715b29d022003ac68f32ceb051443832364ced`, Git-Blob `03a79f162ab37b7913b67106988ea9edd4d3ca30`. Version `0.1.7-rc10`; 28 Dateien, 25 davon gegenüber RC9 byteidentisch. Ausschließlich bestehendes HAB-004 geändert; HAB-001/002/003 und andere Portale nicht angerührt.

**Produktiv gemeldete Ursache:** 07.11.2026 13:51 wurde ein kostenpflichtiger DataForSEO-Task für `Wassermelder` angelegt; am Screenshot 15:10 war immer noch nur `geplant` zu sehen und kein weiterer Lauf. RC9 bewies mit `wp_next_scheduled()` bloß einen Zeitplan, aber keine tatsächliche Ausführung. Weshalb der Server den Cron nicht ausführt, ist noch ungeklärt. **Nicht so tun, als sei serverseitiger Cron bereits repariert.**

**RC10 KISS:** Bei offenem, bereits bezahltem DataForSEO-Task führt das Öffnen der bestehenden WordPress-Seite `Affiliate-Zentrale → Amazon-Automatik` höchstens alle 120 Sekunden einen **kostenlosen GET-Ergebnisabruf** durch; kein neuer bezahlter POST. Sichtbar: Uhrzeit letzter realer automatischer Lauf, letzter API-Ergebnisabruf, Status/Error, tatsächlicher geplanter Termin mit ÜBERFÄLLIG statt irreführendem `geplant`. Bei offenem Task nur Knopf `Offenen Auftrag jetzt prüfen (keine neue Suche)` mit eigener garantiert poll-only Behandlung, selbst wenn Auftrag zwischenzeitlich verschwindet; separater eindeutig kostenpflichtiger Startknopf erst nach Abschluss. Ungültige/abgelaufene Task-ID löst nie unbemerkt neue bezahlte Suche aus. Kostenbudget 5/Tag, regulärer WP-Cron, Kategorien- und Ausspielungslogik unverändert.

**Echte lokale Belege:** vollständiges HAB-004 geladen mit WordPress- und DataForSEO-Simulation, 2720 Knoten/2714 Zuordnungen, 6/7/8 Hauptwelten. Vom bezahlten Erstauftrag über bewusst ausbleibenden WP-Cron, kostenlose GET-Anfrage per Admin-Ansicht, später fertiges Ergebnis und Speicherung bis zur Ausgabe im vorhandenen Hab-Designslot. Auch pending, API-Fehler, ungültiger/veralteter Auftrag, Doppelklick, funktionierender Cron, bestehende Regressionen getestet. **400 bestandene Funktionen in 52 Testläufen, 25/25 PHP-Lint, ZIP-CRC 28/28.** Anbieterantworten sind nachgestellt; noch **kein** echter produktiver DataForSEO-Abfragetest, keine serverseitige Cron-Abnahme.

**Direkte nächste Live-Prüfung (keinen neuen bezahlten Auftrag beauftragen!):** RC10 in WordPress als Update installieren; `Affiliate-Zentrale → Amazon-Automatik` öffnen. Die Seite fragt den bisher offenen Task sofort kostenlos ab und zeigt tatsächlichen Ergebnisstatus. Wenn `Letzter automatischer Lauf` nicht weiterläuft und Termin überfällig ist, ist die serverseitige WP-Cron-Ausführung getrennt zu untersuchen. Keine neue Architektur oder weitere App installieren.

---

## HAB-004 – RC9: Sieben Hauptwelten ohne Gesamtsperre

**07.11.2026 – HAB-004 0.1.6-rc9 (einzige aktuelle Voll-ZIP):** `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`, **618.212 Bytes, 28 Dateien**, SHA256 `04de5f4492887686c5a224640ffa5e4d64175927186dc3fe7f19d546e0ea4120`, Git-Blob `500d70b04607373a133966859de02b03ec7f62cb`.

**Harte Ursache:** Kategorienstruktur kennt sechs bestehende Welten plus `core:world:insurance` (siebte Welt), aber RC8 verlangte exakt sechs. Original-RC8 mit sieben Hauptwelten reproduzierbar `hb_worlds_unexpected`. Die 2.720 Knoten/2.714 Bindungen sind Live-Screenshot-Werte, kein heruntergeladener WP-Datenbankabzug.

**KISS-Korrektur:** Es wird nur verlangt, dass mindestens eine gültige gemappte Hauptwelt existiert; Welt- und Bereichszahlen folgen dem tatsächlich aktiven Bestand. Eine zusätzliche oder nicht gemappte einzelne Welt blockiert die restlichen Welten nicht. Bei vollständig fehlendem/ungültigem Snapshot werden weiterhin sicher keine kostenpflichtigen Aufträge gestartet. Der Affiliate-Hauptschalter `ppar_enabled` bleibt unverändert und muss bei Bedarf in WordPress (`Affiliate-Zentrale → Übersicht → Hauptschalter → Affiliate-Automatik aktiv`) ausdrücklich aktiviert werden.

**Echte lokale Prüfungen:** 116 vollständige Original-Plugin-/Design-WP-Simulationen (6/7/8 Welten, 2.720 Knoten/2.714 Mapping, Klick→DataForSEO-Mock→ASIN→Speicherung→R3-/Kategorie-Ausgabe, 1 Welt ohne Mapping, falsche Revision, Altwerbe-Vorrang, global AUS); 104 DataForSEO-Worker-/Kosten-/Fehler-/Beitragstests mit sieben Welten; 96 Regressionstests; **316 PASS, 0 FAIL, keine PHP-Warnungen**, **25/25 PHP-Lints**, **ZIP 28/28 CRC**. 25/28 Plugindateien gegenüber RC8 identisch. Kein echter WordPress-Produktivlauf oder bezahlter DataForSEO-API-Auftrag. Dokument: `AFFILIATE/IMPLEMENTIERUNG_RC9/PRUEFBERICHT.md`, minimaler Patch `RC8_TO_RC9_SOURCE_DIFF.patch`.

**Nächster Schritt:** RC9 in WordPress als Update des bestehenden Plugins einspielen. Wenn die oben sichtbare Meldung „Affiliate-Zentrale insgesamt ausgeschaltet“ besteht, über `Affiliate-Zentrale → Übersicht → Hauptschalter → Affiliate-Automatik aktiv → Einstellung speichern` einschalten. Erst dann unter `Amazon-Automatik` einmal `Jetzt einen Suchlauf starten`; der Status muss zeigen, ob ein Auftrag erzeugt wird, ein Fehler vorliegt oder bereits geprüft ist. Max. fünf neue kostenpflichtige DataForSEO-Aufträge/UTC-Tag. Die Live-Wirkung erst danach bestätigen.

---

## 07.11.2026 – HAB Affiliate AMAZON RC8: geprüfter kompletter Workflow, echte Diagnose und Ausgabe

**07.11.2026 – HAB-004 Affiliate-Zentrale 0.1.5-rc8 ist einzige aktuelle Voll-ZIP:** `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`, **620242 Bytes**, 28 ZIP-Dateien, SHA256 `f2d09e649fbb6a69a54e64b01df239013975999e46921f08b722adff139ccd30`, Git-Blob `35d32677fb7232a8c0891cc0e730b4b02851b945` (bei GitHub binär geprüft).

**Vollständige lokale Workflow-Simulation: 234 bestandene Prüfungen, 25/25 PHP-Syntax, ZIP-CRC 28/28; nur 3/28 Originaldateien verändert** (`affiliate-portal-router.php`, `includes/trait-ppar-hb-amazon.php`, `readme.txt`). RC7 hatte beim echten Screenshot nach manuellem Run null Kandidaten, aber irreführend bloß „Keine neuen passenden Produkte“. Nachstellung mit den originalen aktiven Hab-Quelladapter-Klassen beweist: bei fehlendem/falschem/inhaltlich nicht freigegebenem WP-Kategoriebaum wurde dessen WP_Error als leere Kandidatenliste verschluckt. Zudem vorherige RC7-Simulation des Frontends hatte einen falschen Kategorie-Slot und ignorierte leere Kategorien/Produktseiten. RC8 zeigt direkt nach Klick oben den echten Workflow- und Kategoriebaum-/Provider-Status und lässt DataForSEO bei ungültiger Quelle gesperrt; echte DataForSEO-API-Taskfehler werden erkannt, statt als unendliches „noch in Bearbeitung“ zu gelten. Wiederverwendung des bestehenden Workers, API-Kostenlimits und Slots, plus die vorhandenen Hab-Design-/Kategorie-Hooks für Amazon-Affiliate-Links auf relevanten Produktseiten selbst ohne redaktionelle Beiträge. Bereits vorhandene Werbung hat Vorrang. Keine zweite DB, kein zweiter Cron, keine Fremdportale/K0 verändert.

**Ehrliche Testgrenze:** Die originalen vollständigen Hab-Plugin-Dateien inkl. originalem Portal-Quelladapter und originalem Design-Plugin-Hook wurden offline mit nachgestellten WordPress-Optionen und DataForSEO-API-Antworten ausgeführt; **keine echte WordPress-Produktivabnahme, keine kostenpflichtige Provider-Abfrage, kein Einblick in Live-Kategoriebaum-Optionen**. RC8 zeigt die genaue Quelle des noch offenen Live-Blockers erst nach Installation.

**Nächster Schritt:** Auf Hab-&-Bewahr-WordPress das bestehende HAB-004-Affiliate-Plugin durch diese RC8-Voll-ZIP ersetzen, `Affiliate-Zentrale → Amazon-Automatik → Jetzt einen Suchlauf starten` **einmal** drücken, dann die **oben sichtbare Statusbox** prüfen. Kein wiederholtes blindes Klicken; bis zu 5 neu bezahlte DataForSEO-Aufträge je UTC-Tag. Falls Quelle blockiert, dort die genaue Ursache lesen statt neue Suche zu behaupten.

Details und Reproduktionsnachweis: `RC8_WORKFLOW_SIMULATION_20261107.md`. Vorherige RC7-Nennungen darunter nur Historie.

---

## 07.11.2026 – HAB-004 RC7: automatische Amazon-Recherche für neue Beiträge

**HAB-004 Affiliate-Zentrale 0.1.4-rc7**, vollständige einzige `CURRENT.zip`: **616209 Bytes, 28 Dateien**, ZIP-SHA256 `08725e5cf9d18654345b4b18b9f3c63ade54ce7a6da932d9768bc2b9867b1d6e`, GitHub-Binär-Blob `3df1bd941aa051f6706a66fd857a8745d0209420`. Gegen RC6 25/28 Dateien byteidentisch; nur die vorhandene Amazon-Datei, der bisherige Hab-Router und `readme.txt` geändert. Keine Fremdportale.

**Nach Prüfung des wirklichen RC6-Codes:** Die vorhandene Artikelerkennung und Werbeplan-Neuberechnung bei Speicherung blieb unangetastet. Neu nutzt **derselbe DataForSEO-Worker** künftig auch veröffentlichte Artikel, wenn die direkte Hab-Produktkategorie wirklich passt und der Artikel-Titel die konkrete Produktfamilie nennt. Bewusste Ausschlüsse: Entwürfe, allgemeine Ratgeber ohne explizites Produkt, Werbesperren, falsche Produktfamilien. Änderungen an Titel/Kategorie machen alte Treffer sofort ungültig. Alle aktuellen Produkt-/Bannerkampagnen behalten Vorrang; bei fehlenden passenden Produkten nur klar gekennzeichneter Amazon-Suchlink, nach verifiziertem API-Ergebnis reale Amazon-Textlinks. Kein zweiter Worker, keine neue API-Suche beim Beitragsspeichern und keine zusätzliche Datenbank; fünf bezahlte DataForSEO-Aufträge/UTC-Tag bleiben.

**Tests:** Alle 25 PHP-Dateien ohne Syntaxfehler, ZIP-CRC PASS, 23+16+23+34 lokale Assertions PASS (96 nicht notwendigerweise unabhängige Fälle). Echte Artikel-Produktslot-Funktion aus Original-Hauptdatei mit globaler Sperre, bestehender Werbung und Hybrid-/Legacy-Modus geprüft. **Kein** WordPress-/DataForSEO-/echter Produktiv-End-to-End-Test; Portal enthält derzeit noch keine echten Beiträge. RC7 bleibt ein geprüftes Upgrade-Paket, nicht produktiv abgenommen.

Arbeits- und Testnachweise ausschließlich im eigenen Hab-Affiliatebüro: `IMPLEMENTIERUNG_RC7/`. RC6 und ältere Angaben sind historisch.

**Nächster Schritt:** Auf ausschließlich `hab-und-bewahr.de` das bereits vorhandene HAB-004 mit der RC7-ZIP kontrolliert aktualisieren. Amazon-Partner-ID und gespeicherte Zugangsdaten bleiben über dieselben bestehenden WordPress-Optionen erhalten, deren tatsächliches Fortbestehen nach dem Upgrade zu prüfen ist. Beim nächsten real veröffentlichten, korrekt kategorisierten Produktbeitrag erfolgt die themenbezogene Suche über den bestehenden WP-Cron. Keine manuellen Amazon-Einzelkampagnen, keine neuen Plugins. HAB-001/002/003, Pferdeatelier, Hobbydepot und K0 unverändert.

---

## 07.11.2026 – HAB AMAZON RC6: STARTKNOPF UND EIGENSTÄNDIGE KATEGORIERECHERCHE

**Stand 07.11.2026 – einzige aktuelle HAB-004-Voll-ZIP 0.1.3-rc6:** `CURRENT.zip` 618.152 Bytes, 28 Dateien, SHA-256 `ef51d931d0c104e8cbb1ed0b27d33e0b6855c1202e605fe06440afc50d0574b9`, Git-Blob `c9026cbcfaa44a03a69820d9d35207f8b6ce5c27` (Größe und Hash aus echtem GitHub-Binärarchiv geprüft).

**Nachgewiesene Ursache aus dem RC5-Quellcode:** kein manueller Start; erster WP-Cron-Lauf erst nach mindestens 5 Minuten plus Website-Aufruf; DataForSEO-Kandidatensuche ausschließlich bei bereits aktiven eBay-/idealo-Produktkampagnen, obwohl Hab diese Anbieter noch nicht eingerichtet hat. Dass der WP-Cron eingetragen ist, beweist keinen tatsächlichen Suchlauf. **RC6:** im selben vorhandenen Hab-Amazon-Modul ein authentifizierter Admin-Button `Jetzt einen Suchlauf starten` an **denselben** vorhandenen Worker angebunden; stündlicher WP-Cron unverändert. Bei fehlenden eBay-/idealo-Kandidaten werden ausschließlich nachweislich im aktiven Hab-Zielkatalog vorhandene konkrete Produktfamilien recherchiert. DataForSEO-Ergebnisse werden nur bei organischen Amazon.de-Produktlinks, gültiger ASIN und im Titel tatsächlich genannter Produktfamilie als maximal 3 schlichte Textlinks pro Kategorie in **bereits vorhandenem Banner-Slot** zugelassen. Keine erfundenen Produktkarten, keine Bilder/Preise/Bewertungen oder Lagerbehauptungen. Bestehende Kampagne hat Vorrang. Ungültige/fremde Treffer bleiben gesperrt. Keine zweite Produktdatenbank, kein neues Plugin.

**Belege/Grenzen:** 25/25 PHP-Syntaxprüfungen, vollständiger ZIP-CRC, 62 lokale Positiv-/Negativprüfungen in drei Testdateien, 25/28 RC5-Dateien byteidentisch (neu geschrieben nur `affiliate-portal-router.php` Version, `includes/trait-ppar-hb-amazon.php`, `readme.txt`). Kein echter WordPress-/DataForSEO-/Amazon-Produktivtest und keine Ausführung kostenpflichtiger API-Abfragen durch den Build. Bestehende Einstellungen beim WordPress-Update sollen erhalten bleiben; unverändert bleiben auch HAB-001/002/003, Pferdeatelier, Hobbydepot, K0. In der WordPress-Sitzung müssen tatsächliche DataForSEO-Zugangsdaten gespeichert und die Amazon-Automatik aktiv sein. Maximal 5 neue kostenpflichtige POST-Suchaufträge pro UTC-Tag auch beim manuellen Start; offener Auftrag wird lediglich per kostenlosem GET abgefragt.

Arbeitsbelege im eigenen Büro: `IMPLEMENTIERUNG_RC6/RC5_TO_RC6.patch` und `IMPLEMENTIERUNG_RC6/test_hab_rc6.php`; RC5/RC4 nur historische Belege.

**NÄCHSTER SCHRITT:** Bestehende Hab-&-Bewahr-Affiliate-Zentrale in WordPress durch die neue RC6-ZIP ersetzen. `Affiliate-Zentrale → Amazon-Automatik → Jetzt einen Suchlauf starten` einmal klicken. Danach zeigt dieselbe Seite **Letzter tatsächlicher Lauf**, **Letzte Meldung**, **Offener Auftrag**, **gefundene Einzelproduktlinks** und **bezahlte Suchaufträge heute**. Kein zweites Plugin. Ein neuer Suchauftrag kostet DataForSEO-Guthaben. Ein Ergebnis kann erst bei einem späteren Worker-Durchlauf eintreffen. Nach echten Daten prüfen, ob die globale Affiliate-Ausspielung und die Kategorie-Slots aktiviert sind; keine Live-Ausgabe vorher behaupten.

---

## 07.11.2026 – HAB-004 RC5: AMAZON-DATENFELD + AUTOMATISCHE SUCHLINKS KORRIGIERT

**Version 0.1.2-rc5 (07.11.2026), allein HAB-004:** Voll-ZIP `CURRENT.zip` 616.662 Bytes, 28 Dateien, SHA-256 `84b4c071f69c6da3e6a3a92dac519ced45a9ba331b09f9d395914a96baa3a7c7`, Git-Blob `13ecb1aa84e1050f4c7fc53a06c32e6c9369a2d6` (GitHub-Ordner: Größe/Blob unabhängig abgeglichen). RC4 aus PR #664 bleibt über Git-Historie wiederherstellbar.

**Gezielte RC4-Korrektur:** Der DataForSEO-Merchant-Amazon-Products-Endpunkt liefert die Kennung als `data_asin`; RC4 las nur `asin`. RC5 liest das tatsächliche `data_asin` und prüft zusätzlich Amazon-Domain, exakten Titel, eindeutige Kennung, Packungsvarianten und keine bezahlten Treffer. Wenn noch kein eBay-/idealo-Produktkatalog existiert, wird **nur für reale Produktfamilien-Kategorien aus dem eigenen Hab-Workflow**, und nur im vorhandenen Banner-Slot `product_after_category_tiles`, ein einfacher automatischer Amazon-Suchlink erzeugt (mit `habundbewahr-21`, Anzeige-/Werbelinkkennzeichnung). Keine erfundene Amazon-Produktkarte, kein zweiter Bannermotor, keine Bilder/Preise/Bewertungen aus DataForSEO. Vorhandene Werbekampagne hat Vorrang. Für echte Einzelprodukt-Direktkarten benötigt der bestehende DataForSEO-Worker weiterhin ein vorhandenes freigegebenes eBay-/idealo-Ausgangsprodukt.

**Tests:** 25/25 PHP-Syntaxprüfungen, ZIP-CRC 28/28, 40 lokale Positiv-/Negativtests (darunter 16 neue RC5-Fälle), 25 originale RC3-Dateien unverändert. Keine authentifizierte WordPress-/Provider-Liveprüfung; DataForSEO kostet bei eingeschalteter Recherche, max. fünf neue Tasks je UTC-Tag. Die gesamte Automatik ist standardmäßig aus. Keine Änderungen an HAB-001/002/003, Pferdeatelier, Hobbydepot, K0 oder externen Zugangsdaten.

**Nächster Schritt:** Nur die bestehende Hab-Affiliate-Zentrale in WordPress kontrolliert mit RC5 aktualisieren. `Affiliate-Zentrale → Amazon-Automatik`: Tag `habundbewahr-21` speichern, Amazon-Produktbuttons aktivieren; DataForSEO noch aus lassen. Erst echten Kategorien-Suchlink mit eigener Tracking-ID prüfen, danach die kostenpflichtige DataForSEO-Suche getrennt freigeben und Datenbasis für konkrete Produktkarten prüfen.

Quellpatch/Test der gezielten RC5-Korrektur: `IMPLEMENTIERUNG_RC5/`.

---

## 07.11.2026 – AMAZON-AUTOMATIK RC4 IM EIGENEN HAB-PLUGIN IMPLEMENTIERT

HAB-004 0.1.1-rc4: vollständige CURRENT.zip, 616072 Bytes, 28 Einträge, SHA256 c601c1f540fccdd18dde59b7c15fc55cfe53b68a59459d45182a2cf1bcd55017, Git-Blob f3a77efff2cb16de34c91eb0c4ec3b072a3999db (remote Größe und Blob bytegleich geprüft).

Original: Hab-RC3, 27 Dateien. Von deren Dateien 25 byteidentisch, geändert Haupt-PHP und includes/trait-ppar-idealo.php, hinzugefügt includes/trait-ppar-hb-amazon.php. Existing Banner-, Frontend-, Produktkarten-, Ausgabe- und Artikelplandateien unberührt. DataForSEO: Opt-in, stündliche WP-Cron-Verarbeitung, max. 5 kostenpflichtige POSTs/UTC-Tag, gespeicherte offene task-ID, eindeutiger Variantenabgleich. Amazon: eigene Tracking-ID habundbewahr-21 ausschließlich nach Speicherung/Aktivierung; direkte Links nur für belegte einzelne ASIN aus idealo oder streng geprüfte DataForSEO-Treffer. Kein eigener manueller Amazon-Kampagnenweg. Alte fremde idealo-Defaults (Adspace 568313, Feed 2901) aus Hab entfernt/gesperrt. Keine Fremd-Provider-Zugangsdaten übertragen.

Lokal geprüft: PHP Syntax 25/25, 24 Assertions (Positiv/Negativ, Variantenabweichung, falsche Portal-ID, bezahlter POST vs kostenloser GET, Tagesgrenze, keine doppelten Buttons), ZIP CRC, installierbare Original-Pluginwurzel, 25/27 originale Dateien bytegleich. Keine authentifizierte WordPress-Installation oder echte Provider-Verbindung und keine Google-/Frontend-Liveprüfung; nur ein Upgrade-Testkandidat. Die Standardautomatik bleibt deaktiviert.

Arbeitsquelle, exakter Zwei-Dateien-Patch und ausführbarer Regressionstest: IMPLEMENTIERUNG_RC4/. Original-Pferdeatelier und Hobbydepot wurden ausschließlich als Recherchevorbild betrachtet, nicht modifiziert.

Nächster Schritt: nur das bestehende Hab-004-WordPress-Plugin mit CURRENT.zip aktualisieren; Affiliate-Zentrale → Amazon-Automatik öffnen; habundbewahr-21 speichern, Amazon-Produktbuttons einschalten; eigene DataForSEO-Zugangsdaten erst nach Kostenfreigabe eingeben; an einer echten passenden Produktkarte Ziel/Tracking und Slot prüfen. Pferdeatelier und Hobbydepot/K0 unverändert.

---

## 07.11.2026 – HARTER AMAZON-/DATAFORSEO-RC3-ABGLEICH (NACH ORIGINAL-ZIP)

**Prüfbeleg:** [AMAZON_AUTOMATIK_ABGLEICH_20261107.md](AMAZON_AUTOMATIK_ABGLEICH_20261107.md).

**Ergebnis:** Die amtliche Hab-004-RC3-ZIP (605.196 B, SHA `2e5f6790...`) hat die generischen idealo-/Banner-/Output-Wege, aber **kein** DataForSEO-Modul und keine aktive Amazon-Produktrecherche. Die vorhandene Amazon-Providerkarte ist `prepared`, nicht `active`. Die Anwenderforderung bleibt ausdrücklich **vollautomatisch**, **keine** manuellen Einzelkampagnen. PartnerNet-Website und separate Hab-Tracking-ID sind vorhanden. Die ältere Pferdeatelier-Referenz weist eine spätere DataForSEO-/Amazon-Automatik nach; ihre vollständigen Originalbytes waren in diesem Durchlauf trotz Bibliotheksnachweis nicht exportierbar. **Kein ungeprüftes Wiederprogrammieren oder RC4 auf Vermutung.**

**NEXT ACTION:** Vollständiges zugängliches originales Pferdeatelier-Affiliate-ZIP mit Amazon-Automatik gegen eigenständige Hab-RC3-Quelle vergleichen, nur fehlende allgemein wiederverwendbare Funktionen isoliert portieren und vollständig samt WP-/Negativ-/Tracking-Gates testen. Bis dahin keine Pluginaktualisierung und keine Aktivierung von Amazon-Produktanzeigen. eBay/Pferdeatelier/Hobbydepot unverändert.

---

## 07.11.2026 – AMAZON-/EBAY-EINRICHTUNGSSTAND (AKTUELLE OPERATIVE FORTSETZUNG)

**Verbindlicher Gesprächs-/Kontostand:** [SETUP_EBAY_AMAZON_BANNER_20261107.md](SETUP_EBAY_AMAZON_BANNER_20261107.md). Amazon-Tracking-ID für Hab & Bewahr laut Nutzer **bereits angelegt**; Website-Liste und Anbindung im WP-Plugin noch zu prüfen. Amazon im Plugin „Adapter vorbereitet“, nicht live verbunden. Eigene breite/quadratische Banner sind Designentwürfe, noch keine Produktions-/Amazon-Freigabe. eBay: eigene Hab-EPN-Kampagne im Plugin gespeichert; Zusatz-Keysets für Hobby Depot und Hab & Bewahr beantragt, Ticket 261106-000039, eBay-Rückfrage zur Begründung, Antwortversand noch unbestätigt. **Pferdeatelier-/Hobbydepot-Developer-Einstellungen und Plugins nicht verändern.**

**NEXT ACTION:** Amazon PartnerNet → Kontoeinstellungen → Website-Liste bearbeiten: `hab-und-bewahr.de` auf Vorhandensein prüfen. Tracking-ID nicht noch einmal erstellen; danach einen Testlink ausschließlich mit Hab-Tracking-ID erzeugen. Keine automatische Auslieferung einschalten. Der folgende RC3-Stand bleibt die autoritative Plugin-Basis.

---

## 06.11.2026 – RC3 BEREINIGUNG / OFFIZIELLE HAB-004-PLUGINABLAGE

**Neue gültige Version:** 0.1.0-rc3, vollständige ZIP im ursprünglichen `../PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip` (605.196 Bytes; SHA-256 `2e5f6790ab3a64b446e34d132037684ad8fa637f76f43974e2816a1f75bc11eb`). RC2 unten ist nur Historie.

**Ursache und Korrektur:** Die RC2-Produktlistenprüfung bezog sich ausschließlich auf Produktbegriffe in Seitenüberschriften. Der tatsächliche Design-Kategoriebaum liegt in der bestehenden WordPress-Zielrevision mit 6 Schutzwelten. In RC3 werden 285 Artikelkategorien und 13 klar benannte Produktprofile aus dem offiziellen Design-Nodes-Stand erkannt; nicht pauschal jedes Sicherheitsthema als Produkt deklariert. Die Werbung nutzt die echten gemappten WP-Zielseiten, nie die Pferde- oder Hobby-Quellkataloge. Welt-/Unterbereich-/Magazin-/Anzeigenmarkt- und Artikel-Brücken nach tatsächlichen Designfiltern, 92 reale Boot-Hooks, 24/27 Dateien gegenüber RC2 unverändert, keine Funktionen aus neutraler Engine gelöscht.

**Performance mit Beleg:** Einmaliger, pro Seitenaufruf zwischengespeicherter WP-Seitenindex ersetzt wiederholtes Durchsuchen des gesamten Zielbaums. Keine unbelegte globale Laufzeitverbesserung behauptet. ZIP-Bau zweimal identisch, alle PHP/JS-Tests, 546 Design-Knoten als Testkorpus, negative und positive Tests, SHA + unabhängiger GitHub-Readback PASS (GitHub Run 42252394077).

**Restgrenzen:** noch kein echter WordPress-/Provider-Livetest; eBay-Quellstand 6.72.306 als 66-Datei-Referenz nicht physisch im Hab-Büro, daher keine zugesagte vollständige Parität; Glossar-Einzelseiten ohne echte CPT-Zielbindung bleiben sicher leer statt erfundene Werbung zu zeigen. Automatische Affiliate-Ausgabe standardmäßig inaktiv.

---

## 06.11.2026 – HAB-004 AFFILIATE – ISOLIERTER WORDPRESS-RELEASE 0.1.0-rc2
<!-- HAB_AFFILIATE_RC2_20261106 -->
**Neue Ausgabe im zuständigen eigenen Pluginbüro:** `../PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`, 27 Dateien, 603.323 Bytes, SHA-256 `014e42b9657eed74b4d2e1f29ea51c6c6bf5c276ec30402011289b3821cbe153`. Build und Prüfquellen ausschließlich auf isoliertem Zweig `hbd-affiliate-port-20261106` in `AFFILIATE/HAB_BAU`; unveränderter fachlicher Originalstamm `NEUTRAL_STAMM` bleibt erhalten.

**Belegt:** Vollständiger neutraler 26-Dateien-Grundstock mit eBay, idealo, Awin, ADCELL, Digistore24, Tarifen, Werbebannern, manuellen Kampagnen, Affiliate-Automatisierung, Chefsteuerung, Ausgabeobjekten, Produktkarte und Artikelplanung erhalten. PHP-Signaturen der 26 Originaldateien nicht entfernt. Fünf vorhandene Zusatzmodule (Produkt-Source-Plan, Admin KISS, Deal-Radar, Partneranalytik, DS24-Nachverarbeitung) waren in neutraler Quelle nicht am Bootstrap angebunden; im neuen Paket geprüft gestartet. Alle Horse-/Hobby-Designreferenzen aus Installationscode entfernt; Hab-Adapter liest nur aktive, passende WordPress-Revision aus Kategorie-Workflow. Anbindung an HBDP-Artikel-/Bereichsfilter (Design 0.1.189) und fail-closed ohne Kategorievertrag. 27/27 ZIP CRC, alle PHP-Lints, JS Syntax, echte Start-Hooks (90), Positiv-/Negativkatalogtests sowie unabhängig über frischen GitHub-Klon erneut gelesene ZIP: **LOCAL PASS** (GitHub-Run 42246580133).

**Harte Grenzen:** Vollständiges Pferdeatelier 6.72.306 Paket mit 66 Files / 5.343.938 Bytes ist lediglich als Referenz beschrieben und befindet sich nicht als Vollarchiv im Hab-Büro. Deshalb **keine behauptete volle Versions-/Featuregleichheit zu 6.72.306**; belegt ist die neutrale Stammfunktions-Erhaltung. Kein realer WordPress-/Provider-/eBay-API-/HivePress-Livetest und keine Lastmessung im Live-Hosting. Kein belegter genereller Performancefehler, daher keine blind gelöschten Alt- oder Sicherungsfunktionen. Standardeinstellung Auslieferung deaktiviert. Der neue Hab-Katalog benötigt aktive WP-Kategorien, echte veröffentlichte Produktziele und kann andernfalls leer bleiben.

**NEXT ACTION (einziger freigegebener operativer Schritt):** Hab-Plugin als neue, bereits separat benannte Instanz unter `affiliate-portal-router` auf Hab-&-Bewahr-WordPress kontrolliert installieren, aktivieren, im Backend Ist-Zustand/Partner-Sperre prüfen. Erst nach klarem WordPress-Readback Providerdaten neu für Hab & Bewahr hinterlegen und Tests durchführen. K0 und alle anderen Projekte unverändert.

---

# HAB & BEWAHR – AFFILIATE CURRENT

STAND: 2026-10-26
STATUS: NEUTRALER STAMM GESICHERT / NO LIVE PASS / HAB-&-BEWAHR-ANPASSUNG NOCH OFFEN

## Verbindlicher Stand

Für Hab & Bewahr wurde ein eigenes Affiliate-Büro angelegt.

Gesicherte technische Ausgangsbasis:
`NEUTRAL_STAMM/affiliate-portal-router/`

Der Stamm basiert auf der bereits pferdeatelier-bereinigten HD-009-Engine, wurde aber vor Ablage hier zusätzlich von Hobby-Depot-spezifischer Bindung getrennt.

Entfernt bzw. neutralisiert wurden insbesondere:
- Hobby-Depot-Pluginidentität und Routerklassenbindung
- HD-004-Kategorie-/Zielquellenbindung
- HD-003/Hobby-Depot-Designprofilbindung
- fest verdrahtete Hobby-Depot-Slotmatrix
- Hobby-Depot-spezifische eBay-/idealo-Zieltexte, Defaults und Zielquellenklassen
- Hobby-Depot-spezifische Provider-/Deal-Radar-Bezeichnungen

Erhalten wurden:
- allgemeine Affiliate-Engine
- eBay- und idealo-Providerlogik
- Awin / ADCELL / Digistore24 / Direktpartner-Basis
- Kontroll-, Veto-, Output- und Automationslogik
- bestehende Credential-/Konfigurationsschnittstellen

Zugangsdaten sind nicht im Campus gespeichert.

## Wichtig

Der neutrale Stamm ist **keine installierbare Hab-&-Bewahr-Livefreigabe**.
Die Portal-Zielquelle ist absichtlich ungebunden und fail-closed.

## Herkunft

Hobby-Depot-Arbeitsquelle:
`hobbyrausch/hd009-affiliate-port-20261026`
Head bei Ableitung:
`56b91b171cb68129369b67e411da5345957af4f2`

Die Hobby-Depot-Entwicklung bleibt davon getrennt und wird nicht zurückgesetzt.

## NEXT ACTION

Für den späteren Hab-&-Bewahr-Chat:

1. Hab-&-Bewahr-Zielquelle aus dem zuständigen Kategorie-/Portal-Current anbinden.
2. Hab-&-Bewahr-Design-/Slotvertrag separat anbinden.
3. Portalnamen und projektspezifische Defaults setzen.
4. Positiv-, Negativ-, Regression-, Installations- und Runtimeprüfung durchführen.
5. Erst danach einen Hab-&-Bewahr-Installationskandidaten bauen.

Nicht HD-004 übernehmen. Nicht Hobby-Depot-Slotmatrix übernehmen. Nicht wieder aus Pferdeatelier kopieren.
