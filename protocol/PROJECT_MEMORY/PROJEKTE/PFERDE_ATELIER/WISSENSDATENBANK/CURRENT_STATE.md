# WISSENSDATENBANK – CURRENT STATE

STAND: 2026-09-15
STATUS: THEMENPOOL AKTIV / PFERDERASSEN GRUNDRECHERCHE ABGESCHLOSSEN / MANAGER 0.2.7 LIVE PASS / PFERDERASSEN ARTIKELINTEGRITÄT BLOCKED / GLOSSAR STARTBEFÜLLT

## AUTORITÄT
Diese Datei ist die einzige aktuelle Standzusammenfassung dieses Büros.

- aktuelle Hauptarbeit / NEXT ACTION → `HOBBYRAUM.md`
- Themenstatus → `THEMENPOOL.md`
- Recherche-/Trust-Regeln → `RECHERCHE_STANDARD.md`
- Forschungsbereiche → `AKTENSCHRAENKE/`

## AKTUELLER BELASTBARER STAND
- `WISSENSDATENBANK` aktiv.
- Aktenschränke: `PFERDERASSEN`, `GLOSSAR`.
- Recherchewissen bleibt von SEO, Kategorien, Textproduktion und Veröffentlichung getrennt.
- Trust-Regeln bleiben verbindlich; offene Detailfelder bleiben offen.

## PFERDERASSEN – FORSCHUNG
- **200 reale Rassendatensätze** unter `AKTENSCHRAENKE/PFERDERASSEN/DATEN/`.
- Internationale Grundrecherche bleibt abgeschlossen.
- Altai, American Walking Pony, Andravida und Anglo-Kabarda bleiben bewusste Grenzfälle bis zu starker Primärquelle.
- Keine neue allgemeine Rassensuche.

## PFERDERASSEN – MANAGER / RELATIONEN

- `Pferde Atelier – Pferderassen Manager` Version **0.2.7**: lokale Positiv-/Negativ-/Mutationstests PASS.
- WordPress-LIVE: **PASS**, Nutzerbestätigung 2026-09-15.
- `Ähnliche Rassen` und `Zur gleichen Rassengruppe` bleiben fachlich getrennt; Same-Group/Self/Unknown-Hardlocks verbindlich.
- Plugin-Artefakt darf nach dem PLUGINS-Sync-Vertrag als isolierte `CURRENT.zip` synchronisiert werden.

## PFERDERASSEN – ARTIKEL / BESTANDSINTEGRITÄT

Weiterhin **BLOCKED**; Details ausschließlich in `AKTENSCHRAENKE/PFERDERASSEN/FEHLERQUELLEN.md`.

Belastbare offene Punkte:
- Rekonstruktion aus WordPress-Export + den danach veröffentlichten Batches: 196 veröffentlichte `pa_breed`-Posts, aber 194 eindeutige `_prm_source_id`;
- doppelte IDs in dieser Rekonstruktion: `breed-pantaneiro`, `breed-posavje-horse`; direkter aktueller WordPress-Readback noch offen;
- letzter 13er-Artikelbatch ist **nicht Schreibvertrags-PASS**, weil die gewählten sechs Managergruppen durch die jeweiligen WDB-Felder `typ`/`rassegruppen` nicht eindeutig getragen sind.

## GLOSSAR – FORTSCHRITT
7 erste Begriffe quellengebunden angelegt: Stockmaß, Widerrist, Ganasche, Röhrbein, Aalstrich, Kötenbehang, Zuchtbuch/Studbook.

## EINE WAHRHEIT
- Forschungs-/Faktenwahrheit: dieser WISSENSDATENBANK-Bereich;
- aktuelle Fehlerdetails Pferderassen: ausschließlich `AKTENSCHRAENKE/PFERDERASSEN/FEHLERQUELLEN.md`;
- Arbeitsbindung / NEXT ACTION: ausschließlich `HOBBYRAUM.md`;
- alter Pfad `../PFERDERASSEN/` bleibt nur Weiterweiser.
