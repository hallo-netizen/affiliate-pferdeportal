# Idealo iPN – Zwei getrennte Publisher-Feeds, Freigabe gemeldet (12.11.2026)

## Status: bestehende Plugins startbereit; private Kontoverbindung NOCH NICHT aktiviert

Der Betreiber meldet am 12.11.2026: **iPN-Produktdatenfeeds („Sheets“) für Hobby Depot und Hab & Bewahr sind jetzt durch idealo freigegeben.** Die Freigabe wird als Betreiberangabe erfasst, nicht als unabhängiger erfolgreicher Login/API-Test ausgegeben.

| Portal | Eigene Werbefläche (Adspace) | Aktueller, tatsächlich geprüfter GitHub-CURRENT | Eigenständige Feed-ID |
| --- | --- | --- | --- |
| Hobby Depot | **568912** | HD-009 **0.1.32**, 41 ZIP-Einträge, SHA256 `d433db74b493407a4c26faef591574e644201846078b7aa7aa3541126f9359b8` | Muss im iPN-Konto abgelesen werden, nicht erraten |
| Hab & Bewahr | **568944** | HAB-004 **0.1.16-rc19**, 36 ZIP-Einträge, SHA256 `6d72fcd41a8b365e84815770014098946774bab7f2425c3546e48da66cd262f0` | Muss im iPN-Konto abgelesen werden, nicht erraten |

**Prüfung:** tatsächliche vollständige CURRENT-ZIPs am 12.11.2026 erneut via GitHub Actions `43233587036` (CRC) und `43233830615` (Bedienung/Sperren) geprüft. Beide enthalten den seit Langem vorhandenen iPN-Adapter `includes/trait-ppar-idealo.php`. Keine Altwerte des Pferde-Ateliers in Hobby Depot. Hab & Bewahr schützt vor alten Pferde-Atelier-Werten. Beide nutzen die **Publisher-API `api.ingenious.cloud/creatives/productdata/findFeeds`**, **nicht** die idealo-Business-Händler-API. Die reale Freigabe ist nur bei erfolgreichem API-Check für die **jeweils eigene** Paarung aus Adspace und Feed nachgewiesen.

## Umsetzung – Kein neues Plugin, kein Code-/Designumbau

Jeweils im WordPress-Backend **Affiliate-Zentrale → Anbieter & APIs → idealo** (bzw. Menü `affiliate-portal-provider-idealo`):

1. Im richtigen iPN-Publisher-Konto die eigene Feed-ID und die sichere echte Download-URL prüfen. Für die Verbindung braucht es den jeweiligen **iPN-API-Key**, den nur der Betreiber geschützt in WordPress eingibt.
2. `idealo-Verbindung verwenden` aktivieren, iPN-API-Key geschützt hinterlegen, **portalrichtige** Adspace-ID aus Tabelle und die zugehörige echte Feed-ID eintragen. **Hobby Depot:** zusätzlich `Dieser Feed ist für Hobby Depot geprüft` ankreuzen (`hobby_feed_verified`). **Hab & Bewahr:** hat keine entsprechende zusätzliche Checkbox.
3. Bis zum Import: **`Portalweite Affiliate-Ausgabe = Nur bestehende eBay-/Bestandslogik`** beibehalten, **Feed automatisch aktualisieren AUS**. Auf **`Speichern & API prüfen`** klicken.
4. Erst bei eindeutiger Meldung `idealo-Partner-API PASS: Feed <eigene Feed-ID> für Adspace <eigene Werbefläche> gefunden` weitermachen. Eine Fehlermeldung bedeutet: **nicht** spekulativ den Pferde-Atelier-Feed 2901 oder die Adspace 568313 einsetzen.
5. Die vom iPN für exakt diesen Feed bereitgestellte **private HTTPS-Download-URL** im Idealo-Backendfeld speichern. Die bestehende Schaltfläche **`Feed jetzt aktualisieren`** löst den vorhandenen Hintergrundimport aus. Keine Händler-CSV erfinden; der bereits vom Advertiser freigegebene iPN-Feed wird verwendet. Bei einem separat heruntergeladenen Original-`.csv[.gz]` darf alternativ die bereits vorhandene **Feed-Test/Import**-Funktion benutzt werden.
6. In der bestehenden Idealo-Fachseite die vorhandenen Zähler **Staged / PASS / WARN / Materialisiert / Portalabdeckung** auslesen. Veröffentlichung erst nach realem Test: eigene Feed-Zuordnung, echtes Ziel, funktionierender Trackinglink, Themenrelevanz, Bilderrechte, kein Mischimport und passende Kachelplätze.
7. Nach PASS `Portalweite Affiliate-Ausgabe = Provider getrennt als Karten` (`separate`) und **`idealo-Linkstrategie = Hybrid`** belassen. In Hobby Depot Amazon **unverändert**, in Hab & Bewahr Versicherungswelt **ohne Idealo, Amazon, eBay**. Die anderen Welten dürfen nur passende Idealo-Angebote verwenden. Nach einem ersten funktionsfähigen Import kann der bestehende **12-Stunden-Auto-Refresh** aktiviert werden; öffentliche Idealo-Kampagnen erfordern im vorhandenen Programm importiertes Material, aktuelles Paar, abgeschlossenen API-Test und Feed nicht älter als 48 Stunden.

## Technische Feststellung – vorhandene Sicherungen

**Hobby Depot HD-009:** `hobby_feed_verified` verlangt ausdrückliche Bestätigung der Feedpaarung. Beim Wechsel der Adspace-/Feed-ID werden alte URL, alte Importzuordnung und API-Prüfung zurückgesetzt. Publizierung ist erst nach aktivem Feedimport, API-Prüfung und richtigem Ausgabemodus zulässig.

**Hab & Bewahr HAB-004:** Frühere Pferde-Atelier-Testwerte 568313/2901 werden beim Laden verworfen. Öffentliche Idealo-Produktkarten verlangen Produktidentität/GTIN, frischen Import, passende Kampagnen-Zielzuordnung und aktiven Ausgabemodus. Die in RC19 geprüfte Versicherungs-Ausschlussregel bleibt unverändert. Partnerprogramme und Design unverändert.

## Grenzen dieser Sitzung

- **Nachweisbar abgeschlossen:** reale Original-ZIPs geprüft; Backendwege und erforderliche Eingabefelder geprüft; portalgetrennte Freigabezuordnung dokumentiert; kein neues Plugin nötig.
- **Nicht behaupten:** WP-Kontoverbindung, authentifizierte iPN-Anmeldung, iPN-Feed-ID, privater Download, produktiver Import, tatsächliche Live-Werbeausgabe. Ohne Zugriff auf die beiden eingeloggten Konten und Backend-Konfiguration sind diese Schritte nicht ausgelöst.
- Keine API-Keys, geheimen Download-URLs oder private Trackingwerte in GitHub, Protokolle, Chat oder Screenshots schreiben.
- Keine WordPress-Artikel, Kategoriehierarchien, Bilder, Templates oder anderen Portale manuell ändern; kein WordPress-Core-Eingriff. **CURRENT.zip bleibt unverändert.**

**Nächste Betreiberaktion:** Bei beiden Portalen `Affiliate-Zentrale → idealo` öffnen und die konkreten Werbeflächen-/Feedpaare mit dem jeweiligen iPN-Zugang **Speichern & API prüfen**. Danach kann anhand der Statusmeldungen die Import-/Ausgabefreigabe gezielt abgenommen werden.
