# LANDINGPAGES – TECHNISCHER PILOTBEFUND

STATUS: READ-ONLY BEFUND / KEINE PLUGINÄNDERUNG

## Geprüfter Designstand

Aktueller geprüfter Template-Kit-Stand:
`pferde-template-kit.php`

Relevanter Befund:
- die Kartenvalidierung kann echte `page`- und `category`-Objekte getrennt validieren;
- die vorhandene Kartenansicht verwendet für Navigationskarten dieselbe Grundstruktur;
- die Ebene-3-Produktseite übernimmt ihre Artikel-/Kategorie-IDs ausschließlich aus Objekten vom Typ `category`;
- direkte veröffentlichte WordPress-Unterseiten einer Ebene-3-Seite werden jedoch an anderer Stelle als Themenquelle für deren Textlogik gelesen.

## Konsequenz

Eine Landingpage kann optisch als dritte Kachel erscheinen und intern trotzdem eine Seite bleiben.

Sie darf dafür **nicht** als normale direkte Unterseite von `Pferdehaftpflicht` angelegt werden.

Sicherer Pilot:
- standalone WordPress-Seite;
- explizite Kachelzuordnung nur für `Pferdehaftpflicht`;
- keine Aufnahme in normale Kategorieermittlung;
- keine Aufnahme in normale Textproduktion;
- keine globale Kachel-Automatik.

## Affiliate-Befund

Die aktuelle Affiliate-Zentrale besitzt bereits:
- zentrale Provider-Registry;
- Provider-Capabilities;
- Adapter-Hooks;
- Creative-Library;
- Relevanz-/Verteilungs-/Veto-Logik;
- providerneutrale Erweiterungsschnittstellen.

Neue Provider müssen deshalb nicht als neues Plugin oder neue Bannerarchitektur gebaut werden.

Tarifcheck/CHECK24 sollen später ausschließlich als Provider/Adapter an diese bestehende Logik angebunden werden.

## Aktuelle Sperre

Die Affiliate-Current-Autorität erlaubt derzeit ausschließlich den dort gebundenen Performance-Arbeitsstrang. Deshalb wurde **kein Affiliate-Quellcode geändert**.

Zusätzlich fehlen noch die exakt belegten internen Werbemittelquellen von Tarifcheck und CHECK24. Kein API-/Feed-/Banner-Endpunkt wird geraten.
