# WISSENSDATENBANK – CURRENT STATE

STAND: 2026-09-16
STATUS: THEMENPOOL AKTIV / PFERDERASSEN GRUNDRECHERCHE ABGESCHLOSSEN / MANAGER 0.2.7 LIVE PASS / TEXTPFLEGE 196 LIVE PASS / PFERDERASSEN ARTIKELINTEGRITÄT WEITER BLOCKED / GLOSSAR STARTBEFÜLLT

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
- Plugin-Artefakt ist als isolierte `PPA-011/CURRENT.zip` synchronisiert.

## PFERDERASSEN – TEXTPFLEGE 196
- 196 veröffentlichte `pa_breed` wurden mit dem einmaligen Textpflege-Updater gegen einen festen Zielbestand geprüft.
- WordPress-Dry-Run nach dem Update: **PASS / LIVE veröffentlicht 196 / würde aktualisieren 0 / bereits Zielstand 196**.
- Nutzer-Live-Stichprobe 2026-09-16: American Cream Draft, American Bashkir Curly/Curly Horse und Shire Horse geprüft; neue Textfassung, metrische Maße und unveränderte Listen vom Nutzer bestätigt.
- Textpflege-Scope: nur `post_content`; Titel, Slug, Status, Beitragsbild, Rassengruppe, Relationen und Post-Meta bleiben außerhalb des Schreibpfads.
- Verbindliche Listen bleiben Listen; Reihenfolge und Faktenpositionen bleiben erhalten. Fremdmaße wurden metrisch normalisiert; Rechtschreibung/Grammatik und holpriger Fließtext wurden geglättet, ohne neue Fachfakten einzuführen.
- Dieser Textpflege-Auftrag ist **LIVE PASS / ABGESCHLOSSEN**.

## PFERDERASSEN – ARTIKEL / BESTANDSINTEGRITÄT
Weiterhin **BLOCKED**; die Textpflege schließt die beiden älteren Fachblocker nicht. Details ausschließlich in `AKTENSCHRAENKE/PFERDERASSEN/FEHLERQUELLEN.md`.

Belastbare offene Punkte:
- Rekonstruktion aus WordPress-Export + den danach veröffentlichten Batches: 196 veröffentlichte `pa_breed`-Posts, aber 194 eindeutige `_prm_source_id`;
- doppelte IDs in dieser Rekonstruktion: `breed-pantaneiro`, `breed-posavje-horse`; direkter aktueller WordPress-Readback zur kanonischen Bereinigung weiterhin offen;
- letzter 13er-Artikelbatch ist **nicht Schreibvertrags-PASS**, weil die gewählten sechs Managergruppen durch die jeweiligen WDB-Felder `typ`/`rassegruppen` nicht eindeutig getragen sind.

## GLOSSAR – FORTSCHRITT
7 erste Begriffe quellengebunden angelegt: Stockmaß, Widerrist, Ganasche, Röhrbein, Aalstrich, Kötenbehang, Zuchtbuch/Studbook.

## EINE WAHRHEIT
- Forschungs-/Faktenwahrheit: dieser WISSENSDATENBANK-Bereich;
- aktuelle Fehlerdetails Pferderassen: ausschließlich `AKTENSCHRAENKE/PFERDERASSEN/FEHLERQUELLEN.md`;
- Arbeitsbindung / NEXT ACTION: ausschließlich `HOBBYRAUM.md`;
- alter Pfad `../PFERDERASSEN/` bleibt nur Weiterweiser.
