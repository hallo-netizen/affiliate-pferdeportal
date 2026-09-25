# CAMPUS – KISS-EINSTIEG / BÜROTÜR → CURRENT_STATE → FRISCHECHECK

DATUM: 2026-09-16
ART: CAMPUSWEITE ARCHITEKTURREGEL
STATUS: IMPLEMENTIERT UND STRUKTURELL GEPRÜFT

## WAS

Campusweit gilt für alle bestehenden und neuen Büros und Bürotüren:

**BÜROTÜR → genau eine zuständige CURRENT_STATE → FRISCHECHECK → NEXT ACTION.**

Die Bürotür bleibt reiner Wegweiser und führt keine eigene dynamische Fachwahrheit. `CURRENT_STATE` bleibt aktuelle Büro-Zusammenfassung. Vor Weiterarbeit und vor Übergabe wird sie gegen den tatsächlich neuesten autoritativen Arbeits-/Teststand des Büros frisch geprüft.

Bei Abweichung wird zuerst `CURRENT_STATE` nachgezogen. Ist der aktuelle Stand nicht belastbar bestimmbar, gilt `BLOCKED` statt Raten oder Weiterarbeit auf altem Stand.

## WARUM

Bei Chatwechseln konnte ein neuer Chat zwar die richtige Bürotür finden, aber trotzdem an einem veralteten aktuellen Stand einsteigen. Ursache waren fehlende campusweite Frischepflicht und dynamische Angaben in Wegweisern. Die oberste Campus-Tür enthielt beispielsweise noch einen fest verdrahteten alten Branch-Hinweis.

Die Lösung bleibt KISS: keine neue Statusdatei, kein zweiter Handoff-Stand, keine zusätzliche Fachwahrheit.

## UMGESETZT

- `BAUCONTAINER/EINGANGSSTANDARD.md`: campusweite Regel für bestehende und neue Bürotüren ergänzt.
- `BAUCONTAINER/NEUES_PROJEKT_VORLAGE.md`: Regel und Positiv-/Negativabnahme für künftige Büros verankert.
- `START_HERE.md` am Campus-Eingang: alten dynamischen Branch-Hinweis entfernt; nur noch Navigation zum Hauptpförtner und zur zuständigen Bürotür/CURRENT_STATE.

Fachliche CURRENT_STATE-Inhalte einzelner Büros wurden nicht pauschal umgeschrieben. Ihre Fachwahrheit darf nicht ohne bürospezifischen Frischebeleg verändert werden.

## POSITIVPRÜFUNG

Die vorhandenen operativen Campus-Bereiche mit eigener CURRENT_STATE wurden auf ihrer aktuellen Campus-Linie geprüft. Die 16 vorhandenen operativen Türen besitzen jeweils `START_HERE.md` und `CURRENT_STATE.md`, und die Tür nennt `CURRENT_STATE.md` als ersten bzw. eindeutigen aktuellen Büroeinstieg:

Allgemeine Bereiche:
- AFFILIATE
- BILDZENTRALE
- DESIGN
- KATEGORIENMODELL
- UNIVERSAL_RESEARCH_FILL

PB ONE:
- ANGEBOTE_FLYER
- ENTWICKLUNGSRAUM
- IDEENWERKSTATT

PFERDE_ATELIER:
- AFFILIATE
- BILD
- DESIGN
- GEMEINSAM
- HIVEPRESS
- PLUGINS
- PRODUKTVERGLEICH
- TEXT

Ergebnis: PASS für die Tür→CURRENT_STATE-Struktur.

## NEGATIVPRÜFUNG

- Die oberste Campus-Tür führt keinen festen aktuellen Arbeitsbranch mehr.
- Campus-/Gebäude-/Flur-/Archiv-/Tresor-Türen werden durch die neue Regel nicht zu zusätzlichen CURRENT_STATE-Wahrheiten.
- Für Büros ohne eigene CURRENT_STATE darf keine neue zweite Standwahrheit erzeugt werden; sie müssen auf die bereits zuständige bestehende CURRENT_STATE verweisen.
- Dynamische Branch-/Head-/Run-/Blocker-/NEXT-ACTION-Kopien in Türen sind campusweit verboten.

Ergebnis: PASS für die zentrale KISS-Regel und die Vermeidung einer zweiten Standwahrheit.

## OFFENER FORMALER REGISTER-SYNC

`AENDERUNGSREGISTER.md` und `BAUCONTAINER/BAUPROTOKOLL.md` sind große bestehende Sammeldateien. Der aktuell verfügbare Connector kann bestehende Dateien nur vollständig ersetzen, nicht sicher zeilenweise anhängen. Eine unvollständige Vollersetzung wäre ein Datenverlust-Risiko und ist deshalb ausdrücklich unterlassen worden.

Dieser Beleg ist keine zweite CURRENT_STATE und keine zweite Fachwahrheit. Er hält WAS/WARUM/Testbeleg dieser Campusänderung dauerhaft fest. Der formale Rückverweis in die beiden Sammelregister bleibt als erster noch offener Dokumentationsschritt bestehen, sobald ein patch-/append-fähiger autoritativer Schreibweg verwendet wird.

## NICHT ANFASSEN

- keine Fach-CURRENT_STATE ohne bürospezifischen Frischecheck umschreiben;
- keine zweite CURRENT_STATE erzeugen;
- keine Historie in Bürotüren verschieben;
- keine dynamischen Arbeitsstände in START_HERE zurückkopieren.
