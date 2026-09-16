# BILD – HOBBYRAUM

STAND: 2026-09-16
STATUS: AKTIV

## GEBUNDENER AUFTRAG

Bildzentrale 2.6.9 kontrolliert auf **Pferderassen-Hero-Bilder** erweitern.

KISS-Ziel:
- der allgemeingültige Kern erhält einen generischen Hero-Bildweg für einen konfigurierten WordPress-Custom-Post-Type;
- im Pferde Atelier wird damit `pa_breed` bedient;
- das erzeugte Bild wird als Beitragsbild/Featured Image der Rasse gesetzt;
- Pferde-Design 1.50.536 nutzt auf `pa_breed` bereits das Beitragsbild und fällt nur ohne Beitragsbild auf das gebündelte Standardbild zurück. Deshalb zunächst **kein Design-Umbau**; nur wenn ein realer Test diese vorhandene Logik widerlegt, geht ein separater Minimalpatch ins DESIGN-Büro.

## ARBEITSBASIS

Autoritativer Ausgangsbeleg:
`ALLGEMEINGUELTIGE_BAUSTEINE/BILDZENTRALE/` → Bildzentrale 2.6.9.

Gebundener Release-Ausgang:
`ALLGEMEINE_BILDZENTRALE_2.6.9_PROMPTGRENZE_REPARIERT.zip`
SHA-256: `748f77602bc3d4f64bd24a2f163c53829f0c1e8dc2102a82a642ceb4778e160e`

WICHTIGER FRISCHER BEFUND:
Die isolierte Plugin-Ausgabekopie `PPA-003/CURRENT.zip` stimmt aktuell nicht mit ihrem Manifest überein und darf **nicht** als Entwicklungsbasis verwendet werden. Vor Release der neuen Bildzentrale muss PPA-003 aus der geprüften autoritativen Bildzentrale neu synchronisiert werden.

## NICHT IN DIESEM RELEASE

Wasserzeichen-Konzept und späterer Mediathek-Nachhol-Lauf liegen ausschließlich als Backlog in `TODO.md` (`TODO-BILD-WASSERZEICHEN-001`). Keine Wasserzeichenlogik in den Pferderassen-Hero-Release mischen.

## NEXT ACTION

1. Bildzentrale auf generischen Custom-Post-Type-Hero erweitern.
2. `pa_breed`-Pfad positiv und fremden Post-Type negativ prüfen.
3. Featured-Image-Readback + Rollback + Formatprüfung ausführen.
4. Regression: Beiträge, WordPress-Taxonomien, HivePress unverändert.
5. Design 1.50.536 gegen die bestehende Fallback-Logik prüfen.
6. Erst bei vollständigem PASS neue Pluginversion/Artefakt synchronisieren und CURRENT_STATE nachziehen.

## VERBINDLICHER RÜCKGABEWEG

Neue belastbare Version → allgemeine Bildzentrale als technische Hauptquelle → Pferde-BILD-CURRENT nur als Projektstatus → isolierte Plugin-Ausgabekopie PPA-003 mit Hash-/Versions-/ZIP-Readback.

## GLOBALE ARBEITSORT-SPERRE

Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle. Ein verifiziertes Archivartefakt darf lediglich in eine neue Arbeitskopie wiederhergestellt werden; bearbeitet und getestet wird ausschließlich die Arbeitskopie.
