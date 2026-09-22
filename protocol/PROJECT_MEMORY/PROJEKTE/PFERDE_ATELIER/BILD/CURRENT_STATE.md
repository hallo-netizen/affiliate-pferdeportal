# BILD – CURRENT STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

> **Einzige aktuelle Zustandsautorität dieses Scopes.** Status, erster offener Blocker und NEXT ACTION werden nur hier gepflegt.  
> `HOBBYRAUM.md` ist lediglich abgeleitete Ausführungsfläche.


STAND: 2026-09-16
STATUS: **BILDZENTRALE 2.7.6 LOCAL HARD PASS / WORDPRESS-LIVE FUNKTION PASS**

## AUTORITÄT
Diese Datei ist die einzige aktuelle Campus-Standzusammenfassung des BILD-Büros.

- Ausführungsdetails/Locks → `HOBBYRAUM.md` (abgeleitet, nicht autoritativ)
- Zielvertrag → `ZIELVERTRAG_BILDZENTRALE_PFERDERASSEN_HERO_20260916.md`
- technische allgemeine Hauptquelle → `ALLGEMEINGUELTIGE_BAUSTEINE/BILDZENTRALE/`
- Protokoll 2.7.0/2.7.1 → `PROTOKOLL_20260916.md`
- Protokoll 2.7.2–2.7.6 → `PROTOKOLL_2.7.2_BIS_2.7.6_20260916.md`

## AKTUELLER TECHNISCHER STAND

Bildzentrale **2.7.6**.

Release:
`ALLGEMEINE_BILDZENTRALE_2.7.6_RASSEN_BATCH_AUTOMATIK_INSTALLIEREN.zip`

SHA-256:
`12edc4405560ac3b149cf76a0b6e65694337b1533c0ea5e3a777d3b6c98ccbf0`

Isolierte Pferde-Ausgabekopie:
`/Campus-Plugins/PFERDE_ATELIER/PPA-003/CURRENT.zip`

Allgemeine Ausgabekopie:
`/Campus-Plugins/ALLGEMEINGUELTIGE_BAUSTEINE/BILDZENTRALE/CURRENT.zip`

## ENTWICKLUNG SEIT 2.7.1

- 2.7.2: Pferderassen-spezifische Hero-Regeln/Profilmigration weitergeführt.
- 2.7.3: fehlerhaften Magnific-GET-Preflight entfernt; Erzeugung läuft über den gebundenen POST-Weg. Nutzer-LIVE: funktioniert.
- 2.7.4: Prompt/Framing für vollständiger sichtbare Pferdemotive angepasst.
- 2.7.5: `post_type_hero` auf native 21:9-Ausgabe 1260×540 ohne nachträglichen 3:1-Recrop umgestellt; bestehende Kategorie-/HivePress-Wege nicht verändert.
- 2.7.6: ausschließlich für `pa_breed` eine serielle Batch-Bedienung für die nächsten 10 offenen Rassen ergänzt; vorhandene Featured Images werden nicht überschrieben.

## PRÜFUNG

2.7.6 lokal:
- Version/ZIP/PHP-Lint: PASS;
- pa_breed-only Scope: PASS;
- serielle Einzelverarbeitung, keine parallele Verarbeitung: PASS;
- nur Rassen ohne Featured Image: PASS;
- bestehende Featured Images nicht überschreiben: PASS;
- andere Bildprofile/Wege unverändert: PASS;
- Regression/Negativkontrollen laut gebundenem Testreport: PASS.

WordPress-LIVE 2026-09-16:
- Nutzer bestätigte den Batchweg mit `klappt`;
- Live-Anzeige zeigte einen 10er-Batch in serieller Verarbeitung ohne gemeldeten Fehler.

GRENZE:
Das ist ein **LIVE-Funktions-PASS des 2.7.6-Batchwegs**, kein Beleg, dass bereits alle Pferderassen vollständig bebildert sind.

## FEHLERSTATUS

`BILD-LIVE-20260916-001` (2.7.0 Tab nicht bedienbar) ist für den aktuellen 2.7.6-Pfad geschlossen. Die historische Fehlerkette bleibt im Protokoll erhalten.

`BILD-OPEN-RATIO-001` bleibt als historischer ungeklärter Kategorie-Profilpunkt separat bestehen und ist kein Blocker des aktuellen Rassen-Batchwegs.

## NEXT ACTION

Keine technische Reparatur von 2.7.6 offen.

Die bestätigte serielle 10er-Rassenbebilderung darf bei weiterem Bebilderungsauftrag weiterverwendet werden. Bei neuer technischer Änderung zuerst diese Current-Autorität frisch prüfen, bestehenden Bildweg regressiv schützen, positiv/negativ testen, WordPress-LIVE prüfen und erst danach allgemeines Artefakt + PPA-003 synchronisieren.
