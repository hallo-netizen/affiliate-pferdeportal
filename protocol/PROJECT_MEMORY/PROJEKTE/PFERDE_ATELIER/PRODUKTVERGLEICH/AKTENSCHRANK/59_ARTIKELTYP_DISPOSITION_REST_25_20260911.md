# PRODUKTVERGLEICH – ARTIKELTYP-DISPOSITION REST 25

Stand: 2026-09-11
Status: FACHLICH ENTSCHIEDEN / PRODUCT_COMPARISON V1 FAIL-CLOSED

## Verbindliche Basis

`05_FACH_DOSSIER_ARTIKELTYP_VERTRAG_V1.md` verlangt für `PRODUCT_COMPARISON V1`:
- exakt zwei konkrete konkurrierende **Produkte**;
- mindestens zwei Hersteller;
- gleiche Produktgruppe;
- gleiche fachliche Nutzungsebene.

Darum darf kein Service-, Rechts-, Wissens-, Checklisten-, Bau-/Infrastruktur- oder reiner Synonym-/Obergruppen-Key künstlich in V1 gezwungen werden.

## Acht bisherige Artikeltyp-/Servicefälle

Diese acht sind für `PRODUCT_COMPARISON V1` ausdrücklich **NOT_APPLICABLE**, können aber später einen eigenen separat gebundenen Artikeltyp/Vertrag erhalten:

- `mistlagerung` — Bau-/Lagerinfrastruktur, nicht einheitliches Serienprodukt;
- `heulagerung` — Hallen-/Lager-/Trocknungs-/Bausystem;
- `turnierplaner` — Papier/Vorlage/App/Tool-Mix, eigener Tool-/Formatvergleich nötig;
- `haftung-im-stall` — Rechts-/Versicherungs-/Vertragsthema, eigener Versicherungs-/Rechtsvergleich nötig;
- `weidebrunnen` — Wassererschließung/Bau-/Infrastrukturleistung;
- `reitplatzdrainage` — Bau-/Drainagesystem und Planung, kein homogenes Serienprodukt;
- `wasserleitungen-im-stall` — Infrastruktur-/Rohrnetz-/Planungssystem; konkrete Komponenten besitzen eigene präzisere Produktklassen;
- `weideunterstaende` — verbleibender nichtmobiler Intent ist Bau-/Anlagenklasse; mobile Unterstände/Weidezelte besitzen eigene Produktkeys.

Keiner dieser Keys darf im V1-Plugin ein Produktpaar erzeugen.

## Bereits fachlich NOT_APPLICABLE gebundene 17

- `checklisten-fuer-pferdeanhaenger`;
- `tuev-beim-pferdeanhaenger`;
- `transportrecht-pferde`;
- `stallbau-beratung`;
- `stallwechsel-checkliste`;
- `weidecheckliste`;
- `futterumstellung-checkliste`;
- `weidemanagement-grundlagen`;
- `heunetze-fuer-staubarmes-heu`;
- `weidezaungeraete` (redundanter Legacy-/Obergruppen-Key; kanonischer Residual-Key ist `weide-zauntechnik-weidezaungeraete`);
- `bahnplaner` (Synonym-/Overlap zu kanonischem `reitplatzplaner`);
- `sandverteiler` (keine eigenständige Produktklasse belegt; Funktion von Planern);
- `heupruefer` (keine eigenständige Klasse neben `heufeuchtemesser`);
- `offenstalltore` (Einsatzort-Duplikation von präziseren Tor-/Panelgruppen);
- `unterstand-boden` (Einsatzort-Duplikation von Liegefläche/Bodenbefestigung);
- `festzaeune-fuer-pferde` (Obergruppe; präzisere Holz/Kunststoff/Elektro-Keys vorhanden);
- `offenstallraufen` (Einsatzort-Duplikation präziser Raufen-Klassen).

## Ergebnis

Alle 25 verbleibenden Nicht-Produkt-/Overlap-/Inhaltsfälle sind für `PRODUCT_COMPARISON V1` fachlich final fail-closed entschieden.

Neuer fachlicher Endstatus des 175er ersten Coverage-/Klassifikationslaufs:
- 150 Registry-Keys mit konkreter Produkt-Evidence;
- 25 Registry-Keys `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`;
- 0 ungeklärte Coverage-/Primärursachen.

Wichtig:
150 Produkt-Evidence-Keys sind **nicht automatisch READY**. Vor Product Knowledge/Pairing bleiben je Gruppe exakte Faktenmatrix, Quellenstatus, Herstellerbreite, Vergleichsprofil und Decision-Policy Pflicht.

Keine alternative Artikeltyp-Implementierung wird hier gebaut.
Kein Product-Knowledge-Import.
Kein SEO-/Providerlauf.
Kein Merge.
Kein Publish.
