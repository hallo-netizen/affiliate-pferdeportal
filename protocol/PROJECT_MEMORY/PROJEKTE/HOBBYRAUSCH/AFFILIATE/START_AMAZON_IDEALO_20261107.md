# Hobby Depot – Affiliate-Start mit Amazon UND idealo (07.11.2026)

**Vom Betreiber bestätigt:** Hobby Depot ist im Amazon PartnerNet als Website eingetragen, der Webseiten-Code liegt bereits vor. Hobby Depot ist zusätzlich im idealo Partnernetz als Website registriert und bestätigt. Eine aktive technische Verbindung / gültige Tracking-ID / echter idealo-Feed und erfolgreiche WordPress-Ausgabe wurden in diesem Auftrag **nicht** live geprüft.

## Verbindlicher Startvertrag

- **Zwei sichtbare Affiliate-Partner zum Start: Amazon und idealo.** eBay, OTTO usw. bleiben gespeichert, dürfen in diesem Startmodus noch keine öffentliche Werbeausgabe erhalten.
- **Zwei unabhängige Recherchewege:** (1) Amazon über DataForSEO-Amazon-Produkte; (2) idealo über den echten Hobby-Depot-iPN-Feed/Partnerzugang. Keine Abhängigkeit der Amazon-Suche von einem idealo-Treffer.
- **Zusätzliche Brücke:** idealo-Daten dürfen Amazon-Recherche auslösen, ersetzen sie aber nicht. Produktgleichheit nur bei nachweisbarer exakter Kennung (z. B. passender, geprüfter Produktcode); bloß ähnliche Produkttitel sind kein Identitätsnachweis. Fehlt die Kennung: getrennt anbieten, nicht verschmelzen.
- **Ein Zielsystem:** Die vorhandenen Hobby-Depot-Kategorie- und Seitenzuordnungen (HD004; Hobbyregister HD007) gelten für beide. Keine neue Kategoriehierarchie, keine zweite Produktdatenbank, keine fremden Pferde-Zielbestände.
- **Eigene Motive statt kopierter Providerbilder:** Querbanner für Hub-/Kategorie-/Magazinseiten; Quadratbanner für Hobbyregister/Glossar. Ein klares Motiv pro Thema, keine Collage. Eigenbanner verlinken auf die exakt passende interne Hobbyseite, nicht pauschal auf Amazon.
- **Nur nach vollständiger technischer Prüfung ausspielen:** valider Affiliate-Link und Zielzuordnung, Partner/Feed aktiv, korrekte Anzeigenkennzeichnung; kein falscher Preis, keine automatisch übernommenen Amazon-Bilder.
- Bereits vorhandene Partner-/Providerdaten im WordPress-Plugin nicht löschen.

## Harte Prüfung der bereits existierenden Hobby-Pluginquelle

Geprüfte Vorbereitungsarbeitskopie unter `affiliate-portal-router/` (lokaler Entwicklungsstand mit Amazon-Startcode, noch nicht als neuer GitHub-Current freigegeben), verglichen mit dem freigegebenen GitHub-Stand **HD009 0.1.10-dev**:

1. `includes/trait-ppar-idealo.php` hat bereits eigenständigen iPN-Feedimport, Aktivierung und Modus `separate` (getrennte Providerkarten). Es gibt auch `combined` und `automatic`, die ohne exakt belegte Produktidentität nicht als Standard verwendet werden sollten.
2. Die bisherige idealo-Quelle enthält die **festen Werte** `adspace_id=568313` und `feed_id=2901`; an mehreren Stellen wird `2901` erzwungen. **Es ist nicht belegt, dass diese IDs zur bestätigten Hobby-Depot-Partnerschaft gehören.** Vor dem ersten Hobby-Import unbedingt entfernen/auf die realen Hobby-Depot-Kontowerte binden, niemals still vorausfüllen. Kein echter idealo-API-Test behauptet.
3. Die Amazon-ASIN-Trackingbrücke aus der installierten 0.1.7-Portierung wurde in HD009 0.1.10-dev erhalten. Die direkte DataForSEO-Amazon-Recherche ist in einer jüngeren **lokalen Arbeitskopie** als manueller Administrator-Abruf vorbereitet; sie gehört noch nicht zum freigegebenen GitHub-CURRENT. DataForSEO selbst ist keine Affiliate-Provisionsquelle. API-Aufrufe nur gezielt, kein kostenpflichtiger Dauerabruf ohne Freigabe.
4. Die vorbereitete Amazon-only-Ausgabesperre unterdrückt idealo ebenfalls und ist damit **überholt**. Vor der nächsten vollständigen Installations-ZIP in einen einzigen **Amazon+idealo-Startmodus** ändern: beide freigeben, übrige Partner nur für öffentliche Ausgabe sperren; ihre Datensätze unangetastet lassen.
5. Partnerausspielung nur über die existierende Affiliate-Zentrale, keine zweite Engine/kein Zusatzplugin. Unzugeordnete Inhalte bleiben leer statt auf fremde Hobbys zu verweisen.

## Exakter nächster Umsetzungsschritt

**In HD009, nicht in einem neuen Plugin:** Die angefangene DataForSEO-Amazon-Admin-Recherche fertigstellen, die idealo-Konto-/Feed-IDs vollständig vom ehemaligen festen Wert lösen, den Start-Ausgabefilter auf **Amazon ODER idealo** umstellen, getrennte Slot- und Fachrelevanz mit Positiv-/Negativtests nachweisen, die zwei Eigenbannerformate anbinden. Daraus eine einzige vollständige ZIP erstellen und unter dem bestehenden `PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip` nach wirklichem Byte-/ZIP-Readback führen. Bis dahin bleibt 0.1.10-dev der GitHub-Current, kein erfundener Live-PASS.

Für die eigentliche Verbindung müssen die **tatsächlichen Hobby-Depot-idealo-Adspace-/Feedwerte** über das geschützte WordPress-Backend ermittelt werden. Weder Credentials noch Daten anderer Portale in GitHub eintragen.

Prüfquellen: aktueller GitHub-Hobby-Pluginstand; tatsächliche PHP-Providerkonfiguration; offizielle Dokumentation zum DataForSEO-Endpunkt `/v3/merchant/amazon/products/live/advanced`.
