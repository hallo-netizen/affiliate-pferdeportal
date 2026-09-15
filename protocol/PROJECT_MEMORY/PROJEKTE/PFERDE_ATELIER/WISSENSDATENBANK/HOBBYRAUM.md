# WISSENSDATENBANK – HOBBYRAUM

STAND: 2026-09-15
STATUS: BLOCKED

## AKTUELLE ARBEITSBINDUNG
THEMA: `PFERDERASSEN – ARTIKEL-/WORDPRESS-INTEGRITÄT`
STATUS: `BLOCKED`
AKTENSCHRANK: `AKTENSCHRAENKE/PFERDERASSEN/`
FEHLERQUELLE: `AKTENSCHRAENKE/PFERDERASSEN/FEHLERQUELLEN.md`
ZIEL: `AKTENSCHRAENKE/PFERDERASSEN/ZIELVERTRAG_RELATIONEN.md`
TECHNIK: `AKTENSCHRAENKE/PFERDERASSEN/TECHNIK_PFERDERASSEN_MANAGER_CURRENT.md`

## JETZT BELASTBAR
- Grundrecherche: 200 WDB-Datensätze, abgeschlossen.
- Veröffentlichungsrekonstruktion: 196 Posts / 194 eindeutige WDB-IDs; zwei Doppel-IDs, WordPress-Direktreadback offen.
- 13 letzterstellte Artikel: Rassengruppenbindung nicht vertragsfest; kein Artikel-PASS für diesen Batch.
- Manager 0.2.7: lokaler Kandidat, harte 196-Post-Positiv-/Negativ-/Mutationstests PASS.
- WordPress-LIVE-PASS 0.2.7: OFFEN.

## NEXT ACTION
1. WordPress direkt auf `breed-pantaneiro` und `breed-posavje-horse` lesen; beide jeweiligen Posts/Slugs/Inhalte/Batches feststellen. Nichts automatisch löschen.
2. Für die 13 letzten Identitäten die sechs Managergruppen autoritativ binden oder das Gruppenmodell verbindlich ändern; keine Ratzuordnung.
3. Manager 0.2.7 installieren.
4. Vor Backfill eine normale Pferderassen-Einzelseite laden: kein Endlosladen.
5. Backend-Relations-Neuaufbau genau einmal manuell starten.
6. Aegidienberger prüfen: `Zur gleichen Rassengruppe` und `Ähnliche Rassen` ohne gemeinsame Rasse; zweite Einzelrasse gegenprüfen.
7. Erst bei LIVE-PASS Pluginstand im PLUGINS-Büro als isolierte `CURRENT.zip` synchronisieren.

## VERBINDLICHER ARBEITSWEG
WDB-Datensatz/Schreibvertrag → Fachfehler/Ziel → lokaler Manager-Test → WordPress-LIVE-Test → erst danach Plugin-Artefaktsync.

## NICHT ANFASSEN
- keine weitere allgemeine Rassensuche;
- keine automatische Löschung doppelter WordPress-Posts;
- keine freie Sechs-Gruppen-Zuordnung;
- keine Relationsberechnung im Frontend/bei Aktivierung;
- Design-Parallelstand nicht überschreiben;
- alte Adresse `../PFERDERASSEN/` bleibt reiner Weiterweiser.

## RÜCKGABEWEG
Erst wenn die drei aktiven Blocker – Doppel-ID-Readback, 13er-Gruppenbindung, Manager-LIVE-Test – geschlossen sind, Status neu bewerten. Forschung selbst bleibt abgeschlossen.
