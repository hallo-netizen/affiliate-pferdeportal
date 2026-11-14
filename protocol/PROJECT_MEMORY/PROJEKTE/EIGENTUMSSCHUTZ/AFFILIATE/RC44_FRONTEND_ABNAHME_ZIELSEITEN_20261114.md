# Hab & Bewahr – RC44 verbindliche Frontend-Abnahme (14.11.2026)

## Wo stehen wir?
- **Technisch gebaut und auf GitHub archiviert:** Affiliate-Zentrale HAB-004, **RC44 / 0.1.41-rc44**. Vollständige Original-ZIP **`PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`**, identischer unveränderter Versionsstand unter `HAB_AFFILIATE_RC44_0.1.41-rc44.zip`. Beide Git-Dateien sind vorhanden; SHA256 `2a9701c465fdf4ac1830a6b02b9329f5613337587c65379f09be94c20b00e681`, **2.361.654 Bytes, 36 Dateien**.
- **Original-PHP-Test RC44 bestanden:** https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43605029576 (160 echte Produkt-Typ-/Formatkombinationen simuliert, Original-Zielentscheider, R2/R3-Slot, 25 PHP-Syntaxprüfungen, keine fremden Plugin-Änderungen).
- **Letzter tatsächlicher WordPress-Live-Nachweis stammt ausdrücklich von RC43, nicht RC44:** 14.11.2026 14:38, **160 Banner aktiv / 0 ohne Ziel / 0 gesperrt**. Die anschließende RC43-Frontend-Sichtprüfung war **NEGATIV**.
- **RC44 in WordPress installiert, Backend-Altbestand erneut zugeordnet oder öffentlich sichtbar? NOCH NICHT NACHGEWIESEN.** Keine Erfolgsmeldung, bevor diese Abnahme erfolgt.

## Bisher beobachtete Fehler bei RC43 und in RC44 geänderte Ursache
1. Auf **Tierkrankenversicherung** erschien ein **Hundehaftpflicht-Banner** (falsch). RC44 ordnet `deep=hundeversicherung` zur **Hundehaftpflichtversicherung** (R3, WP-ID 786), nicht zur Tierkrankenversicherung (815). Generische R2-Angebote bleiben auf der tatsächlichen R2 statt an fachfremde Kinder durchgereicht.
2. Auf **Haftpflicht & Rechtsschutz** (R2, 765) und **Krankenversicherung & Vorsorge** (R2, 766) wurden keine Banner gesehen. Im Originalcode war `product_after_category_tiles` statt des tatsächlich vorgesehenen R2-Platzes `hub_after_cards` vorrangig; RC44 korrigiert die **eine** bisherige Slotentscheidung. Die echte Sichtbarkeit dieser zwei R2-Seiten ist noch offen.
3. Auf **Haus- und Grundbesitzerhaftpflichtversicherung** (R3, 784) wurde **kein** Banner gesehen. Für diesen Fall wurde noch keine unabhängige tatsächliche Ursache bewiesen; RC44s R2-Änderung garantiert nicht automatisch die Behebung. Unbedingt getrennt prüfen.
4. Der Extrabutton **„Mehr erfahren“** war bei bereits anklickbarem Originalbild doppelt, falsch eingefärbt und abgesetzt. RC44 entfernt im bestehenden Bildbanner-Renderer nur diesen zweiten CTA und seinen ungenutzten Ausgabezweig. Ein Klick auf das Bannerbild, **„Anzeige“** und das Originalformat bleiben.
5. Das vom WordPress-Backend gemeldete **„aktiv“** bedeutet weiterhin nicht, dass jede Zielseite tatsächlich ein Banner rendert.

## Exakte Frontend-Testseiten – WordPress-ID ist aus dem tatsächlichen verifizierten WP-Baum bekannt
Die `?page_id=`-Links sind bewusst gewählt, damit keine ungeprüften Pretty-URL-Pfade erraten werden. WordPress sollte zur aktuellen sprechenden URL weiterleiten. Die aktuelle Verfügbarkeit konnte von außerhalb der Installation nicht bestätigt werden.

| Nr. | Seite | URL | Gewünschter sichtbarer Nachweis |
|---|---|---|---|
| 1 | **Tierkrankenversicherung** (R3, 815) | https://hab-und-bewahr.de/?page_id=815 | **Kein Hundehaftpflicht-Banner mehr**; Tierkranken-/Hundekrankenversicherungsbanner nur passend; kein zusätzlicher „Mehr erfahren“-Button |
| 2 | **Hundehaftpflichtversicherung** (R3, 786) | https://hab-und-bewahr.de/?page_id=786 | **Passendes Hundehaftpflicht-Banner**; anklickbares Bild ohne separaten CTA |
| 3 | **Haftpflicht & Rechtsschutz** (R2, 765) | https://hab-und-bewahr.de/?page_id=765 | **R2-Banner direkt auf der Oberseite**; keine fachfremden R3-Banner; Bildplatz nach Kacheln überprüfen |
| 4 | **Krankenversicherung & Vorsorge** (R2, 766) | https://hab-und-bewahr.de/?page_id=766 | **Passendes R2-Banner direkt auf der Oberseite** (z. B. Riester/Rürup); keine Weitergabe von R2-Anzeigen auf völlig andere R3 |
| 5 | **Haus- und Grundbesitzerhaftpflichtversicherung** (R3, 784) | https://hab-und-bewahr.de/?page_id=784 | **Passendes Grundbesitzerhaftpflicht-Banner**; falls weiterhin fehlend, Fehler NICHT als behoben markieren |
| 6 | **Gewerbeversicherungen & Finanzen** (R2, 767) | https://hab-und-bewahr.de/?page_id=767 | **Passendes Firmenversicherungs-Banner auf R2**; keine beliebigen Finanzwerbemittel als Versicherungsbanner |

## Abnahme – einmalig, keine fortlaufenden neuen Prüfungen
**Einzige Nutzerhandlung:** RC44 als Update des vorhandenen WordPress-Affiliate-Zentrale-Plugins installieren, **„Werbemittel & Ausspielung“ dreimal aufrufen** (historischer 60er-Altbestandsabgleich; keine Banner-Neuimporte), dann **diese 6 Seiten öffentlich, bevorzugt in einem privaten Browserfenster ohne Administrator-Anzeige, prüfen**. Die sechs Ergebnisse reichen als kurze Ja/Nein-Angaben; keine Einzelscreenshots und keine weitere Original-Banner-Datei anfordern.

Auf jeder Seite: (1) richtige Versicherungsart, (2) Banner vorhanden oder absichtlich nicht vorhanden, (3) Bannerbild anklickbar, (4) **kein** weiterer „Mehr erfahren“-Button, (5) sichtbare Bildgröße nicht vergrößert/gestreckt/beschnitten, (6) Hinweis „Anzeige“ erhalten.

**Abnahmeentscheidung:** Positiv nur, wenn alle für den jeweiligen Seitentyp vorgesehenen Bilder fachlich passen und der Anzeigenplatz sichtbar funktioniert. Falls eine der sechs Testseiten ausfällt, diese **eine konkrete** Ausgabeart am bestehenden KISS-Owner untersuchen; keine Vermutungen, kein zusätzliches Plugin, keine zweite Themenprüfung im Frontend.

## Bereits protokollierte und behobene historische Ursachen
RC39–RC40: unsinnige Testfreigaben trotz 80 fehlender Ziele. RC41: echter, aber für die 80 fehlenden Ziele nicht ausschlaggebender HTML-Attributverlust beim ersten Import, korrigiert. RC42: geschützter Originalbestands-JSON-Export. RC43: fehlende Aliaszuordnung zehn echter `deep=`-Produktnamen zu bestehenden R2/R3, Backend danach 160/0. RC44: falsch breit gewähltes R2-Kindziel, R2-Hub-Slot falsch priorisiert und doppelter Bildbanner-CTA. Alle technischen Belege stehen in `AFFILIATE/CURRENT_STATE.md` und in dieser Abnahmeakte.
