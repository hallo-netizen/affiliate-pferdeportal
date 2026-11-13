
# Hobby Depot HD003 1.50.811 – Kategorie-Empfehlungen

Datum: 13.11.2026. Nur Design HD003; 1.50.810 bleibt unverändert archiviert.

Echter Problembeleg: Auf der Airbrush-Kategorieseite wurden drei
kürzende 84px-Anzeigenkacheln gezeigt; vollständiger Affiliate-Produktplatz
unter der Kachel hatte bereits 416px Höhe, war aber abgeschnitten.
Zusätzlich doppelte Angabe Anzeige Partner über dem Gitter und auf jeder Karte.
Beweis https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43399151033

KISS-Lösung: Eine einzige sichtbare und zugängliche Kennzeichnung
Anzeige vor dem Block Empfehlungen. Die Gruppenkarten geben kein
eigenes Anzeige Partner mehr aus; außerhalb dieses Blocks bleiben alle
anderen Werbekennzeichnungen unverändert. Die vorhandenen echten
Produktkacheln in einem 3/2/1-Raster erhalten ihre vollständige
Originalhöhe, echte Bilder mit 150px, lesbare 14px Produkttitel.
Kein neues Affiliate- oder Bilder-System und keine Änderung an Hero,
Footer, Kategorien, Banner, Mobil-Hobbyfinder, Register oder Partnerdaten.

Harte Tests: 1291/1291 ZIP-CRC, 13/13 PHP-Lint, ausschließlich zwei
bestehende Plugin-Dateien geändert (Version und Kategorieprofil),
echter Headless-Chrome-Test auf unveränderter öffentlicher Airbrush-Seite
bei 1440px (3 Spalten), 850px (2), 390px (1).
Kartenhöhe exakt 418px, nicht abgeschnitten, Bilder 150px, Titel 14px,
ein sichtbares Anzeige und keine Kartenlabel-Duplikate.
https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43401407288

Die Änderung wurde im Browser mit testweise eingefügtem CSS nachgewiesen,
noch nicht in echtes WordPress installiert. Die thematische Produktwahl
gehört getrennt zu HD009 0.1.35.

SHA256: 3cc8118ed5d9d22acadfd2e9aa9184068f71cbe9ccb2574bcffacdd16d8ac6df
