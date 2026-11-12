# Pferdeatelier PSTE 0.57.144.31 – KISS: Kategorieauswahl und Speichern

**Status 09.11.2026:** Nur WordPress-TEST. **Nicht auf Produktion installieren.** K0/PSERC/PPM/externes MINI und erste zwei Worker unverändert. Kein tatsächlicher WordPress/MySQL-Endtest, kein K0-Handoff.

## Nachgewiesener Fehler

Auf der echten installierten .30-WordPress-Testseite sind die offenen Redaktionsbüro-Themen sichtbar (vom Betreiber eingefügter HTML-Text, 09.11.). Aber der ursprüngliche PHP-Code gibt im Formular nur `target_category_name` weiter, die globale Kategorien-Auswahlliste enthält **nur 1.165 Fach-Leafs** und **keine Magazinkategorie**. Im ursprünglichen Speicherweg löst `categoryIdByName()` Namen nur gegen Fach-Leafs auf und verweigert bei mehrfach identischen sichtbaren Namen die Zuordnung. **45 sichtbare Namen mehrfach, fünf vollständig identische Pfade** im originalen WordPress-Testexport vom 09.11. (u.a. FAQ Weidezaungeräte IDs 291 und 381). Auch der gespeicherte Kategoriename für eine manuell gewählte Magazinkategorie würde im originalen `categoryNameById()` leer bleiben. Keine neue Fachregel: reines Auswahl-/Speicherproblem.

## Bestehender KISS-Pfad nach Korrektur

- **Genau die bereits vorhandene manuelle Fach-/Magazinentscheidung:** WordPress stellt in EINER Liste jede Fachkategorie und alle auf WordPress tatsächlich vorhandenen, registrierten Magazinkategorien als eindeutige **Kategorie-ID + nachvollziehbaren Pfad** dar. Keine neuen Kategorien und keine Keyword-/SEO-Neubewertung.
- Beim Speichern wird dieselbe Kategorie-ID aus dem eindeutig ausgewählten Listeneintrag gelesen und gegen die aktuelle Liste abgeglichen. Alte freie Texte für eindeutige Fachnamen werden weiterhin akzeptiert; doppelte Fachnamen und manipulierte Listeneinträge lösen einen klaren Fehler aus. Bereich Fach/Magazin wird wie zuvor anhand des Original-WordPress-Terms geprüft.
- Der **bestehende** Repository-Schreibweg speichert neben der ID den echten Magazinkategorienamen, bevor die manuelle Zuordnung im bestehenden `topic_assignments` und `topic_pool` geschrieben wird. Unbekannte IDs werden ohne Teilcommit abgewiesen.
- Offene Kategorie: `REVIEW_REQUIRED`, ID=0, **kein** K0-Übergabeversuch. Ausgewählte Kategorie: `REASSIGNED` + `PROVISIONAL`, dann nur der **bereits bestehende** gebundene Ein-Thema-Recheck. Das allein beweist weder `NORMAL_PASS` noch PSERC/K0-Freigabe.

## Prüfungen aus frisch entpackter installierbarer ZIP

- Alte KISS-Regressionen **2.564/2.564**.
- Original v30 Redaktionsbüro-Routing, SQL-Reader und gerenderter Adminbildschirm **469/469**.
- Tatsächliche .31-Kategorieauswahl aus **1.165 echten Fach-Leafs** und **9 simulierten, ausschließlich über die originalen Journal-Slugs registrierten WordPress-Kategorien**, inkl. **vollständiger Pfaddubletten** **3.524/3.524**.
- Tatsächlicher Admin-POST-Handler (isoliert, Fake WordPress) Fach, Magazin, doppelte Namen, offener Kategorieplatz, ungültige ID, fremder Bereich und Hardblock **40/40**.
- Tatsächliche `PSTE_Repository::saveManualDecision()` und `PSTE_DB_Write_Guard` mit Fake-WordPress-DB: Schreibtransaktion, Wiederlesen des Zuordnungszustands, Speicherung Name+ID, offene Fälle und fehlende Kategorie vollständig zurückrollen **49/49**.
- **GESAMT 6.646/6.646**, 83 PHP-Syntax, ZIP-CRC 121/121, **121/121 SHA256** aus frischem Entpacken, identische 121 Pluginpfade wie v30, genau **3 bestehende PHP-Dateien** verändert.

ZIP: `PSTE-0.57.144.31-KISS-KATEGORIE-SPEICHERUNG-NUR-TEST.zip`
SHA256: `0552539fc7eb4e6bfa32d3dea2b8c7e9949f69fc4c3259e2930fb12713e30d3c`

**Keine fachliche Kategorie automatisch geraten, kein selbst gestarteter K0-Schritt.** `FULL_WORKFLOW_PASSED=false`. Ein echter WordPress-Test muss jetzt belegen: Ein eindeutig passender Fach-/Magazin-Termin wird ausgewählt, gespeichert, nach dem Laden wiedergefunden und von dem vorhandenen Recheck verarbeitet, während das offene Thema ohne Kategorie gesperrt bleibt. Nur wenn WordPress das bestätigt, weitere Schritte Richtung PSERC/PPM/K0.

GitHub: QA-Branch `fix/pste-kisten-einmalige-pruefung-20261107`, PR #682 bleibt Draft, **nicht mergen**.