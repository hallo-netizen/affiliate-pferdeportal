# BILD – TODO / BACKLOG

STAND: 2026-09-16
ROLLE: BACKLOG ONLY – keine CURRENT_STATE, keine NEXT ACTION.

## TODO-BILD-WASSERZEICHEN-001 – Zentrales Wasserzeichen für redaktionelle Mediathek-Bilder

STATUS: GEPLANT / NICHT TEIL DES AKTUELLEN PFERDERASSEN-HERO-RELEASES

ZIEL:
Die Bildzentrale soll Wasserzeichen technisch nach der Bilderzeugung bzw. beim kontrollierten Medien-Import anwenden können. Nicht im KI-Prompt erzeugen.

GELTUNGSBEREICH:
- redaktionelle Bilder in der WordPress-Mediathek;
- unabhängig vom Bildtyp, z. B. Artikelbild, Kategorie-Hero, Pferderassen-Hero;
- bestehende Mediathek später optional über einen einmaligen kontrollierten Nachhol-Lauf.

FESTE GRENZEN:
- Logo selbst, Icons, SVGs, Screenshots/UI-Grafiken und ausdrücklich nicht-redaktionelle Medien ausnehmen;
- bereits verarbeitete Bilder nicht erneut markieren;
- Verarbeitung maschinenfest kennzeichnen, damit kein Doppel-Wasserzeichen entsteht;
- bestehende Bilder nicht blind irreversibel überschreiben; Original/Restore-Weg vor Nachhol-Lauf sichern;
- Positiv-/Negativ-/Idempotenz-/Rollbackprüfung vor LIVE-Einsatz.

NOCH FESTZULEGEN:
- konkretes Wasserzeichen/Logo;
- Position;
- Abstand;
- relative Größe;
- Deckkraft;
- Regel für Altbestand.

AKTUELLE ARBEIT:
Nicht hier. Siehe `HOBBYRAUM.md`.
