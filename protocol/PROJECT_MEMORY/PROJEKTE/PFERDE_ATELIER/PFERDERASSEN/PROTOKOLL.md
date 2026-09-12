# PFERDERASSEN – PROTOKOLL

## 2026-09-12 – Büro initial eingerichtet

AUSLÖSER:
Der Nutzer möchte im Vorgriff auf eine neue Beitragsart Pferde- und Ponyrassen vollständig und stichpunktartig recherchieren und die Informationen zentral, flexibel und wiederverwendbar im Campus ablegen.

KRITISCHE ENTSCHEIDUNG:
Keine getrennte Pony-Datenbank und keine WordPress-Live-Datenbank.

UMSETZUNG:
- Büro `PFERDERASSEN` angelegt;
- `START_HERE.md`, `CURRENT_STATE.md`, genau ein `HOBBYRAUM.md`;
- gemeinsames erweiterbares `RASSEN_DATENMODELL.md`;
- zentraler Wegweiser `RASSEN_REGISTER.md`;
- einzelne Datensätze künftig unter `DATEN/`;
- Pferd/Pony/Kleinpferd wird als Klassifikation gespeichert;
- Schema kann versioniert um neue Felder erweitert werden;
- Fakten bleiben quellengebunden und dienen zunächst nur als Recherchegrundlage.

WARUM:
Ein einzelner monolithischer Datensatz oder getrennte Pferde-/Pony-Silos würden Pflege, Dublettenabgleich und spätere Erweiterungen erschweren. Ein Datensatz pro Rasse unter einem gemeinsamen Schema hält Änderungen klein, nachvollziehbar und erweiterbar.

WEBSEITENWIRKUNG:
Keine. Die Campus-Datenbasis wird nicht im Frontend live abgefragt.

NOCH NICHT GETAN:
- keine vollständige Rassen-Masterliste;
- keine Einzelrassen recherchiert/eingepflegt;
- keine TEXT-/SEO-/WordPress-Anbindung;
- kein Auto-Publish.
