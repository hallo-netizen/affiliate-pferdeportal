# Fehlerkatalog – V6.55 Inline Image Rootfix

## E-655-IMG-001 – CSS-Only-PASS war kein Live-Bild-PASS

**Symptom:** Trotz angeblich erfolgreicher 150×150-CSS-Korrektur blieb auf echten Kategorie-/Produktseiten mindestens ein Produktbild sichtbar anders groß bzw. verschoben; auffällig war wiederholt das erste Bild einer Reihe.

**Ursache der falschen Freigabe:** Der vorherige Test prüfte CSS-Deklarationen bzw. synthetische Boxen, nicht den tatsächlichen `render_banner()`-HTML-Pfad unter konkurrierenden Live-Regeln. Ein CSS-Cache-Key-Fix beweist außerdem nicht die sichtbare Bildgeometrie.

**Korrektur:** Die Geometrie wird für Produkt-Creatives ausschließlich in `category_product_1/2/3` direkt am erzeugten Wrapper und `<img>` mit inline `!important` gebunden: exakt 150×150 px, `object-fit: cover`, zentriert.

**Schutz:** Browser-Gegenbeweis mit absichtlich kollidierender `:first-child`-CSS-Regel. Alle drei realen DOM-Rechtecke müssen trotzdem exakt 150×150 px sein.

## E-655-META-001 – WordPress zeigte falsche Pluginversion

**Symptom:** Beim Installieren/Aktualisieren wurde nicht die erwartete V6.55 angezeigt.

**Belegte Ursache:** Im finalen V6.55-Basisinstaller stand im WordPress-Pluginheader `Version: 6.54.0`, während `const VERSION = '6.55.0'` und der obere Readme-`Stable tag` bereits `6.55.0` waren.

**Korrektur:** Ausschließlich der WordPress-Pluginheader wird auf `6.55.0` synchronisiert.

**Schutz:** Der Releasegate liest die tatsächlich installierte Pluginmetadaten-Version mit WordPress `get_plugin_data()` zurück und verlangt Header = `const VERSION` = oberer `Stable tag` = `6.55.0`. Der eBay-Runtime-Build muss unverändert bleiben.

## E-655-SCOPE-001 – Kein erneuter breiter Reparatureingriff

**Schutzvertrag:** Exakt eine Produktionsdatei darf sich gegenüber dem gepinnten V6.55-Basisinstaller ändern: `pferdeportal-affiliate-router.php`. `frontend.css` und alle übrigen Produktionsdateien müssen byte-identisch bleiben. Keine Änderung an Designplugin, eBay-Runtime, Scheduler, Provider, Auswahl, Texten, Karten/Buttons, Banner- oder Artikelproduktlogik.

## Live-Status

Der automatische Releasegate kann technische Freigabe erteilen. Der tatsächliche sichtbare Pferde-Atelier-Livezustand bleibt bis zur Installation des final erzeugten Installers und anschließender Sichtprüfung ausdrücklich `OPEN_NOT_CLAIMED`.
