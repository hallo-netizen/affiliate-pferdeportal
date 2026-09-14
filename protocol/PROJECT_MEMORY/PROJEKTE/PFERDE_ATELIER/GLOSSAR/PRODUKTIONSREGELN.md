# GLOSSAR – PRODUKTIONSREGELN

STAND: 2026-09-14
STATUS: VERBINDLICH

## 1. Themencluster statt isolierter Beziehungen

Sobald bei einem neuen Glossarbegriff fachlich sinnvolle verwandte Glossarbegriffe festgestellt werden, werden diese als technische Beziehungen mitgedacht und – nur bei frisch belegter `GEPRUEFT`-WDB-Quelle – im selben Produktionszusammenhang ergänzt.

Ein Glossar-Produktionslauf gilt erst als vollständig, wenn:
- jeder als verwandt ausgewiesene Begriff als echter Glossarbeitrag existiert;
- die Beziehungen technisch auflösbar sind;
- die Box `Verwandte Begriffe` nur echte veröffentlichte Glossarbeiträge verlinkt;
- kein verwandter Begriff zusätzlich redundant im Fließtext verlinkt wird;
- jeder Begriff genau einen passenden Fließtext-Link zur primären Portal-Kategorie besitzt;
- kein Linkziel doppelt gesetzt ist.

## 2. Veröffentlichungsreihenfolge

Für maschinell erzeugte neue Cluster gilt:
1. alle Cluster-Mitglieder zunächst als Entwurf anlegen;
2. Inhalte, Kurzdefinition, Kategorie/Portalbindung, Metaangaben und Beziehungen für alle Mitglieder setzen;
3. Text-/Linkregeln für sämtliche Mitglieder positiv und negativ prüfen;
4. erst wenn der gesamte Cluster vollständig ist, alle Cluster-Mitglieder veröffentlichen.

Damit kann kein halber Cluster öffentlich werden.

## 3. Interne Links

Verbindlich je Begriff:
- im Fließtext genau ein sinnvoller Link zur passenden übergeordneten Portal-Kategorie;
- Journal-Bereich/Kategorie nur ersatzweise, wenn kein passendes Portal-Ziel existiert;
- verwandte Glossarbegriffe ausschließlich als Links in der eigenen Box `Verwandte Begriffe`;
- dasselbe Ziel niemals doppelt im selben Begriff.

Details und Formulierungsregeln ausschließlich in `TEXT_UND_LINKREGELN.md`.

## 4. Verwandte Begriffe

`Verwandte Begriffe` ist kein Freitext-Friedhof.

Ein Begriff darf dort nur erscheinen, wenn:
- ein veröffentlichter `uge_term` dazu existiert;
- der Link auf diesen echten Glossarbeitrag auflösbar ist.

Fehlt der verwandte Begriff, darf er nur erzeugt werden, wenn seine WDB-Quelle frisch als `GEPRUEFT` belegt ist. Keine Erzeugung aus Chatwissen oder Alt-Paketen ohne Fachbeleg.

## 5. Pferderassen

**Pferderassen und Ponyrassen sind im Glossar tabu.**

Sie gehören ausschließlich in das separate Pferderassen-System/Büro und werden weder als Glossarbeitrag noch als automatisch nachgezogener verwandter Begriff erzeugt.

## 6. Textaufbau

Standard und Pflicht für Glossarbeiträge:
- Titel;
- sichtbare Kurzdefinition/Zusammenfassung;
- ca. 150–200 Wörter;
- wenige natürliche Absätze;
- **keine Zwischenüberschriften**;
- genau ein Fließtext-Link gemäß Abschnitt 3;
- verwandte Links ausschließlich in der Seitenbox.

Keine H2/H3 im Begriffstext aus SEO-, Schema- oder Gestaltungsmotiven.

## 7. Paketregel

Ein neuer Pluginstand erzwingt **nicht automatisch** neue Glossarbegriffe. Neue Begriffe werden nur erzeugt, wenn die fachliche WDB-Grundlage `GEPRUEFT` vorliegt und der Produktionsauftrag dies tatsächlich umfasst.

## 8. Bestehende Glossarbeiträge

Bereits veröffentlichte oder angelegte Glossarbeiträge werden wegen neuer Regeln nicht pauschal gelöscht.

Stattdessen gilt:
1. vorhandenen Beitrag eindeutig per Slug/ID bestimmen;
2. in `BEGRIFFSREGISTER.md` auf `NACHPRÜFUNG` führen;
3. bestehenden Datensatz gezielt überschreiben/aktualisieren, ID und URL erhalten;
4. Inhalt, Kurzdefinition, Metaangaben, Portalbindung, Relationsdaten und Links prüfen;
5. verwandte Links aus dem Fließtext entfernen und in die rechte Relationsbox verlagern;
6. Doppellinks negativ prüfen;
7. erst nach vollständiger technischer und erforderlicher Liveprüfung auf `FERTIG` setzen.

Löschen ist nur zulässig, wenn ein echter Dublette-, Fehl- oder Testdatensatz nachgewiesen ist.

## 9. Autoritatives Begriffsregister

Die Produktionswahrheit `OFFEN / IN ARBEIT / NACHPRÜFUNG / FERTIG / GESPERRT` liegt ausschließlich in:

`BEGRIFFSREGISTER.md`

Kein zweites paralleles Erledigt-/Unerledigt-Register anlegen.
