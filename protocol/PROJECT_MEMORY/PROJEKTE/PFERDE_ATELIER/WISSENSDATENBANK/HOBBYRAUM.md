# WISSENSDATENBANK – HOBBYRAUM

STAND: 2026-09-16
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
- Textpflege der 196 veröffentlichten Rassen: **WORDPRESS-LIVE PASS 2026-09-16**.
- Nachgelagerter Dry-Run der Textpflege: `LIVE veröffentlicht 196 / würde aktualisieren 0 / bereits Zielstand 196`.
- Nutzer-Live-Stichprobe: American Cream Draft, American Bashkir Curly/Curly Horse und Shire Horse bestätigt; Rechtschreibung/Fließtext, metrische Maße und unveränderte Listen wie vorgesehen.
- Veröffentlichungsrekonstruktion: 196 Posts / 194 eindeutige WDB-IDs; zwei Doppel-IDs, kanonische Direktprüfung weiterhin offen.
- 13 letzterstellte Artikel: Rassengruppenbindung nicht vertragsfest; kein Artikel-PASS für diesen Batch.

## NEXT ACTION
1. WordPress direkt auf `breed-pantaneiro` und `breed-posavje-horse` lesen; beide jeweiligen Posts/Slugs/Inhalte/Batches feststellen. Nichts automatisch löschen.
2. Für die 13 letzten Identitäten die sechs Managergruppen autoritativ binden oder das Gruppenmodell verbindlich ändern; keine Ratzuordnung.
3. Die Textpflege 196 ist abgeschlossen und darf nicht erneut als offene Hauptarbeit behandelt werden.

## VERBINDLICHER ARBEITSWEG
WDB-Datensatz/Schreibvertrag → Fachfehler/Ziel → lokaler Manager-Test → WordPress-LIVE-Test → Plugin-Artefaktsync. Für Artikel zusätzlich: autoritative Rassengruppenbindung vor Ausgabe.

## NICHT ANFASSEN
- keine weitere allgemeine Rassensuche;
- keine automatische Löschung doppelter WordPress-Posts;
- keine freie Sechs-Gruppen-Zuordnung;
- keine Relationsberechnung im Frontend/bei Aktivierung;
- abgeschlossene 196er-Textpflege nicht erneut überschreiben;
- Design-Parallelstand nicht überschreiben;
- alte Adresse `../PFERDERASSEN/` bleibt reiner Weiterweiser.

## RÜCKGABEWEG
Status neu bewerten, wenn die beiden verbleibenden Fachblocker – Doppel-ID-Readback und 13er-Gruppenbindung – geschlossen sind. Forschung, Manager 0.2.7 und Textpflege 196 bleiben PASS.
