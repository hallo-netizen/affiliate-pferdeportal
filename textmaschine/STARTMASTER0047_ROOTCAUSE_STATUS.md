# STARTMASTER0047 – ROOTCAUSE STATUS

Stand: 2026-08-20

Verbindliche Master: `NULLPUNKT_TEXTMASCHINE_STARTMASTER0047_LIVE_DRAFT_WRITE_BOUNDARY_ROOTCAUSE_AUDIT_PPM679_UNCHANGED_20260820.zip`

Master SHA-256: `b0c27ad7d5147ca7fad51a87499fb0966c6b8d7a16433c5f344bc8f9ee3f0654`

Diagnoseplugin: `pferde-textmaschine-write-boundary-audit_0.1.0.zip`

Diagnoseplugin SHA-256: `b2d46b86652ca6e71281b5181c7953a9752a0ec04ab820847bb614844f0e578b`

Produktionsplugins gegenüber STARTMASTER0046 unverändert: PSTE 0.56.4, PSERC 0.27.0, PPM 6.7.9.

Live-Fehler: PPM erreicht den echten WordPress-Draft-Insert und WordPress blockiert mit `empty_content`. Die lokale PPM-Testschicht nutzt einen In-Memory-Teststore und deckt die reale WordPress-Save-Filterkette nicht ab. Das ist F-30, die nachgewiesene QA-Testlücke.

Kein Produktionsfix vor Beweis des konkreten Live-Callbacks. Nächster Schritt ausschließlich hash-only Write-Boundary-Audit am unveränderten PPM-Draftversuch.

`main` bleibt unangetastet. Masterdatei bleibt bindend.
