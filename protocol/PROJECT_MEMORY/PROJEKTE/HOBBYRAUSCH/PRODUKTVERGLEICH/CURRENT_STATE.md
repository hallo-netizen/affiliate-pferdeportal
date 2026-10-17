# HOBBYRAUSCH – PRODUKTVERGLEICH – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **KONZEPT AKTIV / 10ER-PILOT KALIBRIERT / V7.1 AUF 381/381 HOBBYS LOKAL AUSGEROLLT / LIVE NOCH NICHT SYNCHRONISIERT**

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_PRODUKTVERGLEICH`.

## Verbindliche Regel

Für jeden HOBBY_HUB wird Kauf-/Vergleichsbedarf geprüft.

Zwei Vergleichstypen:
1. Produktgruppen-/Lösungsvergleich;
2. konkrete Produkt-/Modellvergleiche.

Ein eigener sichtbarer Leaf `Vergleich & Kaufberatung` existiert nur bei mindestens **3 eigenständigen Vergleichs-/Beratungsintents**.

Bei weniger als 3:
- keine künstliche Kategorie;
- Themen liegen in `Ausrüstung & Kosten` oder einem passenden Fachleaf.

Kein Doppelowner:
- Methodenvergleich kann im Fachleaf liegen;
- Kauf-/Produktauswahl gehört zu `Vergleich & Kaufberatung`.

## Kalibrierung und Rollout

Der 10er-Pilot wurde fachlich kalibriert:
Buchbinden · Balance Board · Glasmalerei · Lasergravieren · Fledermausbeobachtung · Hydrokultur · Riffaquaristik · Briefmarken sammeln · Geocaching · Imkerei.

Danach wurde dieselbe Regel lokal auf den vollständigen V7.1-CORE-Bestand angewandt.

Aktueller lokaler V7.1-Befund:
- 381/381 terminale Hobbyseiten geprüft;
- 381/381 besitzen dokumentierte >=3 Beratungs-/Vergleichsintents;
- 381/381 besitzen deshalb im aktuellen V7.1-Kandidaten `Vergleich & Kaufberatung`;
- vorhandene gute Ausrüstungs-/Fachleafs wurden nicht durch Standardschema dupliziert;
- konkrete Produkte erzeugen niemals selbst die Kategorie.

Struktur-/Live-Wahrheit bleibt bei:
`../SEO_KATEGORIEN/CURRENT_STATE.md`.

## Affiliate-Bindung

Vergleichsartikel dürfen Affiliate-Produkte enthalten, aber:
- Nutzerintent entscheidet;
- Produktverfügbarkeit erzeugt keine Kategorie;
- konkrete Produktdaten müssen aktualisierbar bleiben;
- Produktgruppenvergleich und konkrete Produktvergleiche bleiben redaktionell unterscheidbar.

## ERSTER OFFENER BLOCKER

**V7.1 ist noch nicht live synchronisiert; echter WordPress-Dry-Run steht aus.**

## EXAKT EINE NEXT ACTION

**Keine weitere Vergleichsstruktur bauen. Dem operativen V7.1-Dry-Run aus `../SEO_KATEGORIEN/CURRENT_STATE.md` folgen.**
