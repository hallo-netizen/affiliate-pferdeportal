# Robotik V66 – bestätigter Fehler 0.2.4, leerer Header für Admins – Korrektur 0.2.5
Stand: 14.11.2026

## Eindeutig nachgewiesene Ursache
- Originalcode 0.2.3 erlaubt eingeloggten Administratoren Entwurfs-, private und pending Seiten in der Ansicht und nutzt dafür WordPress-Vorschau-URLs. Besucher sehen ausschließlich veröffentlichte Seiten.
- In 0.2.4 wurde **trotz des bekannten laufenden Import- und Entwurfsbetriebs** dieser Admin-Fall entfernt: `get_posts` fragte nur `publish` ab, `permitted()` ließ nur `publish` zu. Damit verschwindet die komplette Navigationsstruktur, sofern die Hauptseiten noch Entwürfe sind.
- **Reproduzierter Regressionstest mit realem V62-188er-Fachprofil:** 172 sichere Seiten als Entwürfe, 16 SEO-HOLDs nicht angelegt: 0.2.4 zeigte für einen eingeloggten Administrator 0/172 Menüpunkte und 0/8 Welten. Derselbe Bestand: 0.2.5 zeigt 172/172 Verweise auf Vorschau-URLs und 8/8 Welten.
- Ursache ist im Designplugin, **nicht** in WordPress-Zugang, Keywords, Beitragskategorien, CSS-Spalten oder Kategorie-Import. Der aus dem vorherigen Live-Bericht belegte Stand war 16/227 und kein Abschluss; ein aktueller Publikationsstatus der 104 Altseiten ist nicht belegt.

## Minimaler Fix in identischer bestehender Designplugin-ID
- Version **0.2.5**; exakt eine funktionale Änderung am Statusfilter der Originaldatei. Admin darf die früher sichtbaren `draft`, `private`, `pending` wieder sehen; Verweise auf die WordPress-Vorschau. Nicht angemeldete Besucher bekommen ausschließlich veröffentlichte Ziele.
- ACHT-Welten-Hauptnavigation inklusive Humanoide, gleichmäßige 2–4 Spalten und KISS-Menügruppen **unverändert von 0.2.4**. Die beiden übrigen geänderten Dateien sind nur README und der Versionsmarker im HTML-Template.
- **Keine** Änderung an WordPress-Inhalten, Poststatus, Kategorie-Importer, SEO-Gebühren, URLs, Beitragskategorien oder Footerlogik. Entwürfe werden durch diesen Fix **nicht** veröffentlicht; öffentliche Sichtbarkeit erfolgt erst über das bestehende, ausdrücklich freizugebende WordPress-Veröffentlichungsmenü nach abgeschlossenem Import.

## Testbelege
- Gleicher V62-Master: 104 Altseiten / 68 sichere neue Seiten / 16 gesperrte Seiten; Quelle unverändert.
- 0.2.4 Regression mit 172 Entwürfen: **0 Admin-Menülinks** => vorherige Version in diesem Fall bewiesen defekt.
- 0.2.5 mit 172 Entwürfen: **Admin 172/172; Besucher 0**.
- 0.2.5 mit 104 veröffentlichten Altseiten + 68 neuen Entwürfen: **Admin 172/172; Besucher 104/104**, acht bzw. sieben Hauptwelten entsprechend dem jeweiligen tatsächlich veröffentlichten Inhalt.
- 0.2.5 mit 172 veröffentlichten Seiten: **Besucher und Admin jeweils 172/172 und 8/8 Welten**. Alle Links genau einmal; Humanoide, Industrie und gebündelte Robotertypen geprüft.
- C-Vertrag: vertiefende Kategorien nur auf konkreter Produktseite, leere Archive ohne Link. PHP-Lint (2), ZIP-CRC, Vergleich alte/neue ZIP (nur drei Dateien geändert) PASS. Keine echten WordPress-Änderungen oder Liveinstallation von 0.2.5.

## Ergebnis und Nutzerweg
- Wiederherstellung ohne Rückbau des Fachbaums: **Bestehendes Robotik-Strukturdesign auf 0.2.5 aktualisieren**. Kategorie-Workflow 0.4.10 und vorhandenen V63-Import nicht anfassen.
- Bei Bedarf schneller alter Zustand: Zurück auf vorhandenes 0.2.3, allerdings ohne Humanoide und neue Spaltenlogik.
- 0.2.5 ist eine geprüfte TEST-Version; reale WordPress-Ansicht muss bestätigt werden.
- Archiv: `DESIGN/PLUGIN/CURRENT.zip` = `DESIGN/PLUGIN/VERSIONEN/0.2.5.zip`.
- SHA256: `4e16fe90fce977eb1d9ea3bb4a2d6b9dff740399b1f0f8c5b6e439b89c09771f`; Größe: `10585` Bytes.