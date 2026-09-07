# AFFILIATE RELEASE – OTTO / AWIN AUTOMATISIERUNGS-SCOPE

STAND: 2026-09-07
STATUS: AKTIVER NUTZER-SCOPE

## Nutzerentscheidung

OTTO hat die Programmzusage erteilt und wird vor Digistore24 priorisiert.
Digistore24 bleibt dokumentiert, wird während dieses Scopes aber nicht weiterbearbeitet.

## Ziel

OTTO wird **nicht als eigenes WordPress-Plugin und nicht als eigener Transportadapter** gebaut.
Transport, Programmstatus, Feed und Tracking laufen über den bestehenden Awin-Weg.

Die Affiliate-Zentrale muss OTTO weitgehend automatisch versorgen:

1. realen OTTO/Awin-Produktfeed sicher erkennen und synchronisieren;
2. neue/geänderte Produkte paketweise importieren;
3. reale Bilder technisch prüfen;
4. Produkte fachlich gegen Portalziele klassifizieren;
5. nur eindeutige, sichere Treffer automatisch aktivieren;
6. Kategorie-/Hub-/Journal-Produktpositionen 1–3 aus derselben zentralen Rangliste versorgen;
7. passende verifizierte Produkte auch für Beitrags-Produktblöcke verwenden;
8. verschwundene/inaktive Produkte weiterhin quarantänisieren bzw. zurückziehen;
9. nach vollständiger Verifikationswelle Artikelpläne automatisch neu bewerten.

## Harte Grenzen

- Kein eigener OTTO-Gesamtworkflow.
- Kein zweites OTTO-Plugin.
- Keine neue Providerarchitektur.
- Keine manuelle Produkt-Einzelpflege als Normalbetrieb.
- Keine willkürliche Auswahl bei mehreren Awin-Feeds.
- Kein Produktbild als erfundener Banner.
- Banner nur aus realem OTTO/Awin-Werbemittelbestand.
- Fehlende oder nicht belegte Bannerquelle blockiert nur den Bannerzweig, nicht die Produktversorgung.
- Keine öffentliche Aktivierung ohne Awin-Programme-Gate, gültiges Tracking, reale Bildprüfung und eindeutige Zielklassifikation.
- Last-Known-Good bleibt bei Fehlern erhalten.

## Abnahme

LOKAL:
- Positiv-/Negativprüfung der OTTO-Automatik.
- Nicht-OTTO-Awin muss unverändert bleiben.
- Fail-closed-Gegenfälle müssen blockieren.

REAL:
- echter OTTO/Awin-Advertiser im eigenen Konto;
- realer, eindeutig gebundener OTTO-Produktfeed;
- reale Produktzeilen;
- WordPress/MariaDB-Lauf;
- reale Kategorie-/Beitragsausgabe;
- Banner nur nach belegtem echten Creative-Zugang.

Kein REAL-PASS ohne diese Belege.

## OTTO-spezifische Pflichtdaten

Für konkrete OTTO-Produktwerbung ist der reale Verkäufername Pflicht.
Die Affiliate-Zentrale darf OTTO deshalb erst automatisch öffentlich aktivieren, wenn der Verkäufer aus dem **realen OTTO/Awin-Feed** eindeutig gebunden wurde.
Die generische Awin-Schnittstelle rät keinen Verkäufer-Spaltennamen.

Produktaktualisierung:
- Automationsplan nur `daily` oder `twicedaily`;
- für OTTO mindestens täglich betreiben;
- realer Betriebszustand wird erst im Live-Test abgenommen.

Mehrprovider:
Ein zentral verifiziertes OTTO/Awin-Produkt darf durch die alte eBay-Kohortenregel nicht pauschal entfernt werden.
In diesem Fall entscheidet die bestehende fachliche Rangfolge. Unverifizierte Fremdquellen erhalten diese Ausnahme nicht.


## Produktwissen-Schnittstelle

Die parallel entwickelte zentrale Produktwissen-Datenbank ist für den OTTO-Scope **relevant**, aber nicht als zweite Affiliate-Datenbank.

Verbindliche Trennung:
- Produktwissen = fachliche Produkt-/Variantenidentität und quellengebundene Fakten.
- Affiliate/Awin = Angebot, Preis, Bestand, Verkäufer, Tracking, reales Werbemittel.
- Affiliate liest keine Produktwissen-Tabellen direkt und schreibt dort nichts.

Consumer-Vertrag:
`ppar_affiliate_exact_product_requirements`

Wenn ein Beitrag/Produktvergleich über diese Schnittstelle exakte Produktkennungen liefert, gewinnt die exakte Identität vor generischem Affiliate-Ranking.
Nur identische GTIN/EAN bzw. belastbare echte MPN dürfen matchen.
Kein Match = keine Affiliate-Karte. Ein ähnlich benanntes Produkt darf niemals als Ersatz eingesetzt werden.

Die kanonische technische OTTO-Identität im Awin-Transport ist Advertiser-ID `14336`.
Der Programmname wird nicht als technische Hauptidentität verwendet.

Detailkonzept:
`protocol/AFFILIATE_RELEASE_OTTO_AUTOMATION_CONCEPT_20260907.md`
