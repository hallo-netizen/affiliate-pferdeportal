# Affiliate-Zentrale – nächster Funktionsscope

Stand: 2026-08-30

## Gebundener Nutzerauftrag

Die bestehende Affiliate-Zentrale soll nach dem abgeschlossenen V6.63.8-Release um genau einen zusammenhängenden Funktionsblock erweitert werden. Keine Nebenarchitektur und kein separates Plugin.

## 1. Klare Rollen der Quellen

### Produktbreite
- Amazon – fest eingeplant
- OTTO – eigene Produktquelle im Backend, technische Anbindung darf über Awin laufen
- Kelkoo – Produkt-/Preisvergleichs- und Dealquelle
- idealo – bestehende Produkt-/Preisquelle
- eBay – ergänzende Produktquelle, nicht Mittelpunkt

### Banner-/Partnernetzwerke
- Awin
- ADCELL
- Digistore24
- weitere vergleichbare Netzwerke

Banner-/Partnernetzwerke und Produktquellen werden in der Oberfläche fachlich getrennt dargestellt, auch wenn eine Produktquelle technisch über ein Netzwerk geliefert oder abgerechnet wird.

## 2. Zentrales Partner- und Einnahmen-Cockpit

Die bestehende Statistikseite wird zu „Partner & Einnahmen“ erweitert.

Providerübergreifend anzeigen:
- lokale Klicks
- vom Partner gemeldete Klicks, sofern vorhanden
- Verkäufe/Leads
- Verkaufswert/Umsatz
- Provision/Einnahmen
- Conversion
- letzter Datenabruf / Datenquelle
- Zeiträume: heute, 7 Tage, 30 Tage, gesamt

OTTO wird als OTTO ausgewiesen, auch wenn Feed/Abrechnung technisch über Awin erfolgt.

Fehlende Umsatz-/Provisionsdaten werden niemals geschätzt oder erfunden, sondern als nicht verfügbar markiert.

Bestehendes lokales Klicktracking (`ppar_click_total`, `ppar_click_daily`, Slots/Seiten) wird wiederverwendet.

Provideradapter liefern externe Reportdaten in ein einheitliches internes Format. Keine zweite Statistik-Wahrheit pro Provider.

## 3. „Kracher-Angebot“ – erster Live-Test nur Reithelme

Erster Test ausschließlich auf der bestehenden Reithelm-Seite.

Darstellung:
- ein großer horizontaler Angebotsblock
- genau ein aktuell bestes Angebot
- Produktbild, Produktname, aktueller Preis, belastbarer Preisvorteil, Anbieter, CTA
- kein echtes Angebot = kompletter Block unsichtbar

Zulassung nur wenn:
- fachlich eindeutig Reithelm
- aktuell lieferbar
- Preis aktuell geprüft
- Preisvorteil belastbar und deutlich
- keine reine Händler-UVP als alleiniger Rabattbeweis

Automatik:
- zeitlich begrenzte Angebote automatisch überwachen
- abgelaufen / Preis gestiegen / nicht lieferbar => sofort nicht mehr ausspielen
- besseres gültiges Angebot => automatisch ersetzen
- Quelle und Prüfzeitpunkt intern speichern

Dealquellen zunächst aus vorhandenen/zugänglichen Produktquellen. Kelkoo soll nach Freischaltung als zusätzliche Deal-/Preisquelle angebunden werden. Amazon wird später zusätzlich mit Amazon-Daten und optional Keepa als Preis-/Deal-Intelligence ergänzt. Keepa ist keine Affiliate-Provisionsquelle.

## 4. Harte Grenzen des ersten Schritts

- kein globaler Rollout des Kracher-Blocks
- keine Änderung der bestehenden eBay-Lauf-/Recovery-Logik
- keine Änderung von Design-, Content-, SEO- oder STARTMASTER-Workstreams
- kein separates Plugin
- bestehende Affiliate-Zentrale erweitern
- erst nach positivem Test auf Reithelme breiter ausrollen

## Governance-Hinweis

V6.63.8 ist im aktuellen Release-State bereits als RELEASED gebunden; `CURRENT_RELEASE.json` steht noch auf `FINALIZING_RELEASE` und erlaubt derzeit keine Änderung am kanonischen Source-Tree. Dieser Scope ist deshalb als nächster Nutzerauftrag dokumentiert, aber noch nicht als neue Sourceänderung freigegeben. Vor Implementierung muss der bestehende Release-Controller den nächsten legalen Arbeitszustand für Sourceänderungen binden; kein Bypass und keine Nebenbranch-Lösung.
