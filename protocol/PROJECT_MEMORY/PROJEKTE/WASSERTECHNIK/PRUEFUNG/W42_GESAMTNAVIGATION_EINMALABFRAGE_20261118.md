# W42 – WT001-Navigation einmalig einlesen statt bis zu 79+ Einzelabfragen
**18.11.2026 · ein bestehendes Gesamtplugin · Offline-Gesamtprüfung PASS · keine Installation**

## Verbindlicher Ausgangszustand
- Laut echter Nutzer-WP-Pluginliste ist WT001 0.1.7 aktiv auf `wasser.oliver-beil.de`.
- W41 0.1.11 enthält sieben kaufnahe Hauptbereiche + Fachtechnik, 218 alte SEO-Owner, 81 noch ungeprüfte neue Produkte, W35-219er-Einmalimport / 17 Redirects. ZIP war aufgrund nicht vollständig verfügbarer originaler 0.1.7-Quellbytes **nicht installationsfreigegeben**.
- W40-Zusatzdiagnose wird nicht vom Nutzer verlangt. Keine zweite Pluginidentität, kein manueller erneuter SEO-Abgleich.

## Festgestellter und korrigierter konkrete Menüengpass
- W41 rief beim Erzeugen der Navigation für jedes der 79 alten Produkte `get_page_by_path()` auf, bei umgehängten Seiten unter Umständen zusätzlich mit dem alten Pfad. Die Navigation erscheint auf jeder Frontend-Seite; dieser wiederholte Zugriff war unnötig.
- W42 nutzt genau **eine Abfrage der veröffentlichten WP-Seiten** pro Menürenderer und ordnet die vorhandenen 79 Besitzer-Produktlinks danach im Arbeitsspeicher zu. Kein zweiter Entscheider, keine neue Keyword-/Produktfreigabe, kein WP-Schreiben.
- 71 Kaufprodukte bleiben ihren sieben Hauptbereichen und 8 Industrieprodukte dem separaten Fachtechnikzugang zugeordnet. Pool & Teich bleibt als Hauptbereich vorhanden, ohne fiktive Produkt-URLs.
- Entwürfe, fremde Seitenpfade sowie doppelt vorhandene Besitzerzuordnungen werden nicht verlinkt. W35 alt/neuer WP-Pfad bleibt berücksichtigt, die 17 301-Umzüge und 219 Besitzerziele bleiben unverändert.

## Echte Gesamtprüfung (nicht WordPress-live)
- GitHub Actions **44282970502: SUCCESS**; der vollständige W33/W42 Gesamtbuild ist reproduzierbar. W42-Paketversion: **0.1.12 NUR OFFLINE/NICHT INSTALLIEREN**.
- W41-Kontrollen plus W42-Neutests: eine gemeinsame WP-Seitenlistenabfrage statt 79+ Einzelsuchen; ein konkreter doppelter Owner unterdrückt den Link; Entwürfe und falsche Besitzer gesperrt; keine doppelte Frontendnavigation.
- W35 zehn WordPress-Import-/Rollback-/Redirect-Szenarien PASS, einschließlich alter neun WP-Hauptbereiche. SEO 81er insgesamt 15 Provider-/UI-Mock-Szenarien PASS, 218-Alt-SEO-/DataForSEO-Originalquellen und Fingerprint unverändert; Zielvertragsabgleich, PHP-Syntax und ZIP-CRC PASS.
- Es gab **keine** WordPress-Liveinstallation, **keine** WordPress-Schreibvorgänge und **keine** kostenpflichtigen DataForSEO-Abfragen.

## Stand und nächste fachliche Grenze
Originales vollständiges WT001 0.1.7 war laut W11-Protokoll nur als früher Chat-ZIP verfügbar. Nochmals GitHub-W11-Quellbaum, GitHub-Läufe, persönliche Wassertechnik-Library und ihre übergeordneten ZIP-Ablagen durchsucht: keine identische 0.1.7-ZIP im tatsächlich überprüften Quellenbestand. Die installierte **Versionsnummer 0.1.7 ist bekannt**, aber der **exakte alte Programmcode** ist hier nicht verfügbar. W42 darf daher nicht als bewiesen verlustfreie 0.1.7-Überschreibung oder WordPress-Livetest beschrieben werden. Keine neue Zusatzdiagnose und keine blinde Installation. Ziel bleibt das eine bestehende WT001-Gesamtupdate.
