# ÄNDERUNGS- UND ERKLÄRUNGSREGISTER

STAND: 2026-09-05

Zweck: dauerhaft beantworten können:
**Was wurde geändert – und warum?**

Jeder relevante Eintrag enthält:
- WAS
- VORHER
- NACHHER
- WARUM
- BELEG
- ENTFERNBAR?

Wenn WARUM nicht belastbar geklärt ist:
`WARUM: UNGEKLÄRT`
`ENTFERNBAR: NEIN, BIS GEKLÄRT`

## ARCH-001 – Campus/Bürogebäude-Modell
WAS: Campus → Projektgebäude → Büro → Hobbyraum.
WARUM: neue/wechselnde Chats sollen ohne Vorwissen Stand, Regeln, Fehler und Arbeitswege finden.
BELEG: Architekturentscheidung 2026-09-05.

## ARCH-002 – Hauptpförtner als Resetpunkt
WARUM: bei Kontextverlust verbindlich neu lesen statt raten.
NACHWEIS: Pflicht-Rückmeldung von Projekt/Büro/Stand/Nächstem Schritt/Arbeitsweg.

## ARCH-003 – Ein Hobbyraum pro Büro
WARUM: Seitensprünge und Parallelreparaturen verhindern.

## ARCH-004 – Paul isoliert über eigenen Branch
WARUM: vollständiges Projektwissen + freie Tests ohne Einfluss auf offizielle Stände.
REGEL: kein Blind-Merge.

## ARCH-005 – Modulares Gebäude
WARUM: Räume, Büros, Abteilungen und Projekte ohne Gesamtumbau ergänzen können.

## ARCH-006 – Technischer Standort unter protocol/
WAS: `protocol/PROJECT_MEMORY/`.
WARUM: bestehender `hardlock` deckt `protocol/**` bereits ab; keine neue CI-Architektur.
BELEG: Draft-PR #134.

## ARCH-007 – Externer Notfall-Tresor
WARUM: vollständiger Wiederaufbau aus geprüftem Gesamtstand.
REGEL: nur `TRESOR_PASS`; alte PASS-Stände nicht überschreiben.

## ARCH-008 – Organischer Campus
WAS: Campus ausdrücklich als fortlaufender Prozess definiert.
WARUM: reale Projektarbeit entwickelt neue Anforderungen; Struktur muss mitwachsen können.
REGEL: ergänzen, zusammenlegen oder zurückbauen nach Bedarf, ohne Gesamtneubau.
ENTFERNBAR: nein, solange mehrere wachsende Projekte/Bereiche existieren.

## ARCH-009 – Allgemeingültige Bausteine
WAS: eigenes projektübergreifendes Gebäude.
WARUM: geprüfte universelle Plugins/Workflows sollen bei neuen Projekten wiederverwendet werden statt neu erfunden oder blind aus einem Altprojekt kopiert zu werden.
BELEG: `ALLGEMEINGUELTIGE_BAUSTEINE/`.

## ARCH-010 – Vollständige Masterdatei-Verwertung
WAS: jeder Bestandteil jeder Masterdatei wird inventarisiert und zugeordnet.
WARUM: Archive, alte Stände, Tests, Fehlergründe und Produktionshistorien dürfen beim Aufbau des Projektgedächtnisses nicht verloren gehen.
REGEL: nichts still verwerfen; UNGEKLÄRT = nicht anfassen.
BELEG: `BAUCONTAINER/MASTERDATEIEN_REGEL.md`.

## ARCH-011 – BILD-Büro
WAS: BILD als eigenes Fachbüro im Pferde-Atelier.
WARUM: eigenständige Bildzentrale mit eigener Technik, Historie, Regeln, Fehlern und allgemeingültigem Potenzial.
BELEG: `PROJEKTE/PFERDE_ATELIER/BILD/`.

## BILD-001 – Lokaler Magnific-Readback 2.4.9
WAS: lokale WordPress-Bild-URL wird nach Import/Zuordnung vor temporärer Magnific-URL verwendet.
WARUM: externe Magnific-Ergebnis-URLs liefen ab und hinterließen leere Vorschauen trotz lokal vorhandenem Bild.
BELEG: BILD-Masterdatei 049 / Statusprotokoll.
ENTFERNBAR: nein, solange temporäre externe URLs ablaufen können.

## BILD-002 – Allgemeingültige Bildzentrale 2.6.9
WAS: aktueller LIVE-Stand 2.6.9 wird als allgemeingültige Bildzentrale beschrieben.
NACHHER: Beiträge, WordPress-Taxonomien, optional HivePress, Pixabay/Pexels/Magnific, sichere Profile, Export/Import, Readback-Fallback.
WARUM: allgemeingültige Wiederverwendung über Projekte ist ausdrücklich gewünscht; exakte historische Einzelcommits 2.4.9→2.6.9 sind noch nicht vollständig belegt.
BELEG: Nutzerbestätigung 2026-09-05 + vorhandener 2.6.6-Konfigurationsbeleg.
ENTFERNBAR: nein; genaue Implementierungsdetails nach 2.6.9-Codebeleg ergänzen.

## TECH-KEYFLOW-001 – Schlüsselübergabe
Bereich: TEXT / Maschinenraum
WAS: historisch wurde Schlüssel-/Signer-Übergabe verändert.
WARUM: UNGEKLÄRT.
ENTFERNBAR: NEIN, BIS WARUM GEKLÄRT.
