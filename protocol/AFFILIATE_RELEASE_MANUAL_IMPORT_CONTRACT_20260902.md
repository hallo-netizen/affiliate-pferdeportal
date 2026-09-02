# AFFILIATE-ZENTRALE — MANUELLER DATEIIMPORT / SCOPE-ÄNDERUNG

Stand: 2026-09-02
Branch: `affiliate-release-current`
Status: `WORKING / NOT RELEASED / LIVE PENDING`

## Autorisierte Änderung

Der Nutzer hat den bisherigen Zielvertrag ausdrücklich geändert: Wenn ein Provider seine vollständige Bestandsliste nicht zuverlässig über eine unterstützte API liefert, darf ein manueller Dateiimport als regulärer Betriebsweg verwendet werden.

Damit ist die frühere Regel „Digistore24-CSV niemals als Runtime-Importquelle“ für den **explizit manuell gestarteten Import** aufgehoben. Sie bleibt nur insoweit bestehen, dass ein CSV-Upload niemals als Beweis einer automatischen Remote-Discovery ausgegeben werden darf.

## KISS-Bedienvertrag

Es gibt genau einen sichtbaren manuellen Dateieingang:

`WordPress-Dashboard -> Affiliate-Zentrale -> Anbieter & APIs -> Datei importieren`

Der Nutzer wählt **keinen Provider**. Der Importer erkennt den Provider ausschließlich aus starken Dateisignaturen. Unbekannte oder widersprüchliche Dateien werden fail-closed ohne Mutation abgewiesen.

## Unterstützte Wege im aktuellen Arbeitsstand

- Digistore24: Export `Partnerschaften mit Vendoren`; nur `Genehmigt/approved`; Produktpartnerschaften bleiben einzeln erhalten und werden zusätzlich nach Werbemittel-ID/Vendor als Quelle gruppiert.
- Digistore24-Werbemitteldateien: nur bei eindeutiger Digistore24-/checkout-ds24-Signatur plus Banner-/Trackingstruktur; Delegation an die vorhandene Creative-Library.
- idealo: nur Standardfeed mit exakt dem bereits bestehenden idealo-Headervertrag und passendem `productdata_<id>.csv[.gz]`-Dateinamen; danach Delegation an den vorhandenen idealo-Importer.
- Awin: nur bei eindeutiger Awin-Trackingdomain im Dateiinhalt; Delegation an die vorhandene Creative-Library.
- ADCELL: nur bei eindeutiger ADCELL-Trackingdomain im Dateiinhalt; Delegation an die vorhandene Creative-Library.
- eBay: kann erkannt werden, wird aber bewusst nicht in einen Dateipfad umgeleitet, weil der vorhandene Produktworkflow API-basiert ist.

## Digistore24-Sicherheitsvertrag

Vor DS24-Persistenz muss der aktuell gespeicherte API-Schlüssel exakt zum zuvor erfolgreich getesteten Schlüssel-Fingerprint und zur gespeicherten Affiliate-ID gehören. So kann eine CSV nicht versehentlich unter einen anderen DS24-Accountbestand gemischt werden.

Der Import:

- übernimmt ausschließlich genehmigte Zeilen,
- verlangt numerische Produkt- und Werbemittel-IDs,
- erkennt mehrere Produkte je Vendor/Werbemittel-ID,
- blockiert Werbemittel-ID/Vendor-Konflikte vollständig,
- erhält bestehende nichtmanuelle Quellen und Last-Known-Good-Ausgaben,
- entfernt bei einem späteren vollständigen CSV-Abgleich nur veraltete **manuell importierte Inventurquellen**, nicht veröffentlichte LKG-Ausgaben,
- erhält die aktuelle manuelle DS24-Inventur auch dann, wenn der bestehende Marketplace-Abruf später seinen Cache aktualisiert,
- mischt manuelle DS24-Inventur niemals in einen anderen API-Key-/Affiliate-Identitätsstand,
- lässt eine im neuen manuellen Vollabgleich entfernte Quelle nicht durch einen späteren Marketplace-Refresh wieder auferstehen,
- erzeugt keinen synthetischen Promolink,
- veröffentlicht beim Upload nichts ungeprüft.

Die reale Kontrollmenge 02.09.2026 ergibt: 18 genehmigte Produktpartnerschaften, 10 Werbemittelquellen, 10 Vendoren.

## Lokaler Positiv-/Negativ-/Regressionstest

Der bestehende universelle Importer ist byte-identisch zum bereits geprüften Stand und wird nicht unnötig erneut verändert. Der neue Hardening-Block wurde separat positiv/negativ geprüft; PHP-Lint für alle drei beteiligten Dateien ist PASS.

POSITIV:
- reale 18er-Struktur -> 18 Produktpartnerschaften / 10 Quellen / 10 Vendoren,
- Linnon 3 Produkte bleiben erhalten,
- Faszienloesen 5 Produkte bleiben erhalten,
- wiederholter Import ist idempotent,
- bestehende nichtmanuelle DS24-Quelle bleibt erhalten,
- vorhandene gültige Support-URL bleibt beim Reimport erhalten,
- manuelle DS24-Inventur überlebt einen späteren Marketplace-Cache-Refresh derselben getesteten Identität,
- entfernte manuelle Quellen werden nicht wiederhergestellt,
- idealo wird nur mit Dateiname + vollständigem realen Headervertrag erkannt,
- Awin/ADCELL sowie Digistore24-Werbemittel werden nur mit eindeutigen Providersignaturen erkannt.

NEGATIV:
- unknown -> keine Mutation,
- widersprüchliche Provider-Signaturen -> keine Mutation,
- idealo-Dateiname ohne vollständigen Headervertrag -> kein idealo-Import,
- pending/rejected -> nicht übernommen,
- ungültige Produkt-ID -> nicht übernommen,
- gleiche Werbemittel-ID bei verschiedenen Vendoren -> gesamter DS24-Import fail-closed,
- falscher/ungeprüfter DS24-Account-Fingerprint -> keine Mutation,
- manuelle DS24-Inventur wird nicht in eine andere getestete Identität übernommen,
- eBay-Datei -> keine falsche Weiterleitung in einen Creative-/Feedpfad.

REGRESSION:
- Die Providertraits für eBay, idealo, Awin und Digistore24, Output-/Slotlogik, LKG, Partner-Analytics und Automationslogik bleiben unverändert.
- Der bestehende idealo- und Creative-Library-Importer wird delegiert statt dupliziert.
- Die zusätzliche Persistenzsicherung liegt ausschließlich im Manual-Import-Guard und greift nur auf die Option des DS24-Marketplace-Caches ein, wenn eine identitätsgebundene manuelle Inventur vorhanden ist.

## Abnahmegrenze

Dieser Stand ist ein lokaler/Repository-Arbeitsstand. Kein Live-PASS und kein Release-PASS wird behauptet, bevor der tatsächlich installierbare Kandidat aus der gebundenen Source erzeugt und der reale Backend-Upload mit dem aktuellen Digistore24-Export ausgeführt wurde.
