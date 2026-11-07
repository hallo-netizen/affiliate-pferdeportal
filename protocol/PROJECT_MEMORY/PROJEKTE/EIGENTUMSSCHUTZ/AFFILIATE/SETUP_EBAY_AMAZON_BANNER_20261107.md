# Hab & Bewahr – Affiliate-Einrichtung: eBay, Amazon und eigene Banner
**Stand: 07.11.2026 | Gesprächs-/Backendstand, keine behauptete Livefreigabe**

## Sicher bestätigter Ist-Stand
- Website: `hab-und-bewahr.de`.
- WordPress: `Hab & Bewahr – Affiliate-Zentrale` Version `0.1.0-rc3` installiert, aktiviert, Backend-Menü öffnet sich. Dashboard-Screenshot: 9 Provider erfasst, 0 Werbemittel, 0 aktiv, 0 Zuordnungen. Amazon: „Adapter vorbereitet“, keine produktive Amazon-Verbindung. eBay: „Nicht eingerichtet“.
- Die drei anderen Eigenplugins wurden nicht für dieses Affiliate-Update geändert: Design `0.1.189`, Kategorie-Workflow `1.14.8.37`, Bildzentrale `1.0.0`.
- Vollständige originale Eigenplugin-ZIPs sind unverändert im zuständigen `../PLUGINS/ISOLIERTE_PLUGINS/HAB-001…004/CURRENT.zip`. Eintrag hier ist **nur Arbeitsnotiz**, keine Plugin-ZIP und keine zweite Current-Autorität.
- Amazon PartnerNet: Nutzer hat am 07.11. bestätigt, dass eine **eigene Hab-&-Bewahr-Tracking-ID bereits hinzugefügt** wurde. **Konkreter Wert nicht im Campus speichern**. Ob `https://hab-und-bewahr.de` in der Amazon-Website-Liste eingetragen ist, ist noch nicht bestätigt. Es wurde **keine** Amazon-API-/Produktverbindung im WordPress-Plugin als erfolgreich belegt.
- Idealo: vom Nutzer beantragt, Freigabe/Verbindung ausstehend. eBay/weitere Partner noch nicht verbunden.

## eBay getrennte Portale – Verlauf und Schutz
- eBay Partner Network: drei bei Screenshot vorhandene Kampagnen: Pferde Atelier, Hobby Depot, default. Nutzer hat danach **Hab & Bewahr** als eigene EPN-Kampagne angelegt und deren ID im Plugin unter **Affiliate-Zentrale → Netzwerke & API → eBay → EPN-Campaign-ID** gespeichert (vom Nutzer bestätigt). Die konkrete ID nicht in Dokumentation übernehmen.
- eBay Developer: ein vorhandenes Production-Keyset heißt `Pferde Atelier Affiliate`. Dessen Marketplace Account Deletion-Notification-Endpoint zeigt wieder korrekt auf Pferdeatelier. Vorher war dort versehentlich eine Hobbydepot-Adresse; dies wurde vor dem Gespräch korrigiert. **Nicht ändern, keine Rotation, keinen fremden Token/Endpoint überschreiben.**
- „Request another keyset“ öffnet Supportanfrage, keinen direkten zusätzlichen Schlüssel. eBay-Supportantrag für **zwei zusätzliche Production-Keysets** (Hobby Depot und Hab & Bewahr) unter demselben Developer-Konto erfolgreich übermittelt. Ticket **261106-000039**. eBay hat per Mail am 07.11. nach (a) Business Use Case und (b) Current Keyset Limitations gefragt. Eine englische Antwort dafür wurde im Chat formuliert; **Versand dieser Antwort bislang nicht bestätigt**. Keine Genehmigung oder neuen Schlüssel behaupten.
- Keine eBay-Zugangsdaten, Prüf-Tokens, Schlüssel oder fremden Portal-Voreinstellungen im GitHub-Text speichern. Die aktuelle Pferdeatelier-/Hobbydepot-Konfiguration bleibt unangetastet.

## Amazon – Ziel und gesicherte Grenzen
- Nutzer möchte vorerst auf Hab & Bewahr **nur Amazon-Werbung und eigene gestaltete Banner**, bis weitere Partner freigeschaltet sind.
- Amazon-Tracking-IDs dienen der getrennten Auswertung unter *einem* PartnerNet-Konto. Nach Amazon-Hilfe unter „Mein Konto → Ihre Tracking-IDs verwalten“. Nutzer hat Tracking-ID bereits angelegt.
- Website eintragen/prüfen laut offizieller Amazon PartnerNet Hilfe: **PartnerNet → Maus über eigene E-Mail-Adresse → Kontoeinstellungen → Website-Liste bearbeiten → URL eingeben → Hinzufügen → Weiter**. Existenz des Eintrags noch offen.
- Direkte Amazon-Partnerlinks können über Amazon SiteStripe bei angemeldetem Partnerkonto erstellt werden; **Hab-&-Bewahr-Tracking-ID pro erzeugtem Link auswählen**. Prüfen, dass genau diese ID verwendet wird.
- Historisch aus Pferdeatelier im Gespräch: Produktrecherche über DataForSEO; Banner als breites Querformat und quadratisches Glossarformat. Dieser Weg ist im aktuellen Hab-Plugin **nicht als vollständig betriebsfertige Amazon-Echtproduktintegration nachgewiesen**. Amazon im Plugin nur „Adapter vorbereitet“. Keine automatische Produkterkennung/Preise/Bilder als live-fertig behaupten. Technische Prüfung gegen die autorisierte Pferdeatelier-Referenz bleibt offen.
- Eigene bildliche Banner können *intern* auf passende Hab-&-Bewahr-Kategorien verlinken; sie sind dadurch zunächst **redaktionelle Eigenwerbung**, keine automatische direkte Amazon-Provision. Bei direkt zu Amazon führenden Bannerlinks nur zulässige Partnerlinks verwenden und auf Werbekennzeichnung/Markenrichtlinien achten.
- Affiliate-Automatik bis zum vollständigen Live-/Partner-Test ausgeschaltet lassen.

## Bannerwünsche / Entwürfe
- Markenauftritt: Hab & Bewahr, sympathisch, freundlich, vertrauenswürdig; Salbei/Grau und dezente warme Akzente; kein Bedrohungs-/Alarmbild.
- Format 1: **Querbanner über Seitenbreite**, angelehnt an bisheriges Pferdeatelier-Format.
- Format 2: **Quadratisches Banner**, besonders für Glossar und mobile Ausgabe.
- Motivvarianten (visuelle Chat-Entwürfe, **noch keine abgenommene oder eingebundene Produktionsgrafik**):
  1. Geborgenes Zuhause: warmer Hauseingang, Garten und Tor; Headline „Schützen, was zählt.“
  2. Sicher unterwegs: Wohnmobil/Camping am See.
  3. Gut vorbereitet: regnerisches Haus, Schutz vor Wetter/Technikausfall.
- Bild-/Markenrechte und endgültige Verlinkung vor Einbau prüfen. Kein ungeprüftes Amazon-Logo in die Eigenwerbung übernehmen. Glossar-Einzelplatz-Zuordnung ist in RC3 noch nicht vollständig nachgewiesen.

## Nächster sinnvoller konkreter Schritt
1. **Nicht erneut Tracking-ID erstellen** – bereits vom Nutzer erledigt.
2. Im deutschen Amazon PartnerNet prüfen, ob `hab-und-bewahr.de` in **Kontoeinstellungen → Website-Liste bearbeiten** bereits eingetragen ist; nur falls nicht dort hinzufügen.
3. Dann einen einzelnen Amazon-Link mit explizit ausgewählter Hab-&-Bewahr-Tracking-ID testweise erzeugen und dessen Zuordnung prüfen; keine Eigenpluginänderung nötig für diesen Nachweis.
4. Für die echte automatische Amazon-Produktsuche/-Auslieferung getrennt die tatsächliche Pluginfunktion/Providerfreigabe prüfen, bevor etwas aktiviert wird.
5. Bannerwunsch konkretisieren, finales Format/Ziel definieren und nur im Hab-&-Bewahr-Design/Pluginbereich umsetzen; bestehende Pferdeatelier-/Hobbydepot-Plugins und -Accounts nicht verändern.

**Quellen aus Nutzerbelegen:** eBay-Developer- und EPN-Screenshots vom 06.11., WordPress-Affiliate-Screenshot vom 06.11., eBay-Supportmail vom 07.11., Amazon-Tracking-ID-Bestätigung vom 07.11. Andere Portale dienen nur als lesende Referenz.
