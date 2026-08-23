# ARBEITSPROTOKOLL – Produktbild Cache-Rootfix ONLY

Stand: 23.08.2026

## Auftrag
Ausschließlich den sichtbaren Fehler korrigieren, dass einzelne Produktfotos in den drei Produktvorschlägen auf Produkt-/Kategorieseiten nicht in der verbindlichen einheitlichen Bildfläche erscheinen. Keine andere Design-, Inhalts-, Auswahl-, Provider-, eBay-, Scheduler- oder Workflow-Funktion ändern.

## Verbindlicher Ausgangspunkt
Final automatisch freigegebenes V6.55-Actions-Artefakt `V655_FINAL_VERIFIED_RELEASE`, Artifact-ID `9492650547`, SHA-256 `5446bd14f3e0d035e8ed74da1cd86393574f890fce5d81eb77d2aea0b611a955`.

## Live-Gegenbeweis gegen die beiden ersten Ansätze
Der reale Screenshot vom 23.08.2026 um 22:13 zeigt nach Installation weiterhin die alte sichtbare Geometrie. Damit sind sowohl der erste `contain`-Ansatz als auch der anschließend gebaute `cover`-Installer als Live-Freigabe ungültig.

Die CSS-Regel selbst war im zweiten Installer vorhanden, konnte aber im Browser weiter durch die alte CSS-Datei ersetzt werden: `frontend.css` wurde mit der unveränderten Plugin-Version `self::VERSION` als Asset-Version eingebunden. Da die Plugin-Version bei diesem eng begrenzten Fix bewusst 6.55.0 blieb, blieb auch die CSS-URL/Cache-Kennung unverändert. Browser/Proxy/CDN konnten deshalb die alte Datei weiterverwenden.

## Rootcause
Nicht Position 1 und nicht die Produktwahl. Die drei Slots `category_product_1/2/3` besitzen denselben Renderer. Der reale Wiederholungsfehler entsteht durch fehlende cache-sichere Auslieferung der geänderten CSS-Datei bei unveränderter Plugin-Version.

## Rootfix
Exakt zwei Produktionsdateien dürfen abweichen:
1. `affiliate-portal-router/assets/frontend.css`: alle drei Produkt-Slots erhalten identisch einen festen 150×150-px-Rahmen und ein 150×150-px-Bild mit `object-fit: cover` und zentrierter Position.
2. `affiliate-portal-router/pferdeportal-affiliate-router.php`: ausschließlich die Version von `ppar-frontend` CSS wird aus `self::VERSION` plus den ersten 12 Stellen des SHA-256 der realen `frontend.css` gebildet. Damit ändert sich die CSS-URL automatisch genau dann, wenn sich die CSS-Datei ändert. Der JS-Enqueue bleibt unverändert.

Nicht betroffen: Artikelprodukt-Renderer, Banner, HivePress-PRIVATE-Bilder, Produktwahl, Texte, Karten-/Buttondesign, eBay-Fachlogik, Provider, Scheduler und Designplugin.

## Prüfvertrag
- Pinned V6.55-Baseline + Hashes.
- Negativbeweis: Baseline hat keine Bildregel und nutzt statisch `self::VERSION` für CSS.
- Patch nur auf exakte CSS- und PHP-Baseline-SHAs.
- Produktionsdiff exakt zwei Dateien und nur die genannten.
- Bildregel identisch für Slots 1/2/3; keine Position-1-Sonderregel; kein Banner-Slot.
- PHP-Diff exakt der CSS-Enqueue-Cachebuster; JS-Enqueue unverändert.
- Real WordPress 7.0.1 und 6.8.3 müssen die tatsächlich registrierte CSS-Version `6.55.0-<CSS-SHA12>` ausgeben.
- bestehende V6.55 Architektur-, Artikelprodukt- und Heartbeat-Regressionen bleiben PASS.
- Installer/Fresh-Unpack/MASTER-Parität und finaler Counterproof Pflicht.

`main` bleibt unverändert; PR bleibt Draft bis ausdrückliche Freigabe.
