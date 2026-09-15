# WISSENSDATENBANK – HOBBYRAUM

STAND: 2026-09-15
STATUS: BLOCKED

## AKTUELLE ARBEITSBINDUNG
THEMA: `PFERDERASSEN – ARTIKEL-/BESTANDSINTEGRITÄT`
STATUS: `BLOCKED`
AKTENSCHRANK: `AKTENSCHRAENKE/PFERDERASSEN/`
FEHLERQUELLE: `AKTENSCHRAENKE/PFERDERASSEN/FEHLERQUELLEN.md`
ZIEL RELATIONEN: `AKTENSCHRAENKE/PFERDERASSEN/ZIELVERTRAG_RELATIONEN.md`
TECHNIK: `AKTENSCHRAENKE/PFERDERASSEN/TECHNIK_PFERDERASSEN_MANAGER_CURRENT.md`

## JETZT BELASTBAR
- Grundrecherche: 200 WDB-Datensätze, abgeschlossen.
- Manager 0.2.7: lokal hart PASS und WordPress-LIVE **PASS**.
- Relationsfehler `PR-PLUGIN-001`: CLOSED.
- Veröffentlichungsrekonstruktion: 196 Posts / 194 eindeutige WDB-IDs; zwei Doppel-IDs, WordPress-Direktreadback offen.
- 13 letzterstellte Artikel: Rassengruppenbindung nicht vertragsfest; kein Artikel-PASS für diesen Batch.

## NEXT ACTION
1. WordPress direkt auf `breed-pantaneiro` und `breed-posavje-horse` lesen; beide jeweiligen Posts/Slugs/Inhalte/Batches feststellen. Nichts automatisch löschen.
2. Für die 13 letzten Identitäten die sechs Managergruppen autoritativ binden oder das Gruppenmodell verbindlich ändern; keine Ratzuordnung.
3. Der Managerweg ist für Version 0.2.7 fachlich nicht mehr blockierend; Plugin-Artefaktsync erfolgt im PLUGINS-Büro nach `SYNC_VERTRAG.md`.

## VERBINDLICHER ARBEITSWEG
WDB-Datensatz/Schreibvertrag → Fachfehler/Ziel → lokaler Manager-Test → WordPress-LIVE-Test → Plugin-Artefaktsync. Für Artikel zusätzlich: autoritative Rassengruppenbindung vor Ausgabe.

## NICHT ANFASSEN
- keine weitere allgemeine Rassensuche;
- keine automatische Löschung doppelter WordPress-Posts;
- keine freie Sechs-Gruppen-Zuordnung;
- keine Relationsberechnung im Frontend/bei Aktivierung;
- Design-Parallelstand nicht überschreiben;
- alte Adresse `../PFERDERASSEN/` bleibt reiner Weiterweiser.

## RÜCKGABEWEG
Status neu bewerten, wenn die beiden verbleibenden Fachblocker – Doppel-ID-Readback und 13er-Gruppenbindung – geschlossen sind. Forschung selbst und Manager 0.2.7 bleiben PASS.
