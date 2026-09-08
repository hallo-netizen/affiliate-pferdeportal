# POC 001 – HARTER POSITIV-/NEGATIVTEST

Datum: 2026-09-08
Status: ARCHITEKTUR-POC PASS, KEIN PRODUKTIONS-PASS

## Testgegenstand

Nur die alternative Zentralmaschinen-Architektur mit synthetischen Dummy-Workern.

Nicht angefasst:
- Textmaschine
- PPM / PSERC / PSTE / LanguageTool
- Fach-/SEO-/Qualitäts-/Designregeln
- STARTMASTER-State
- WordPress

## Lokaler Testlauf

14/14 Tests PASS.

Positiv:
1. feste vollständige Reihenfolge S1 -> S2 -> S3
2. Neustart setzt exakt am nächsten gebundenen Schritt fort
3. fertiges Ausgabepaket ist hashgebunden
4. externe Ed25519-Signatur akzeptiert exakt unverändertes Paket

Negativ:
5. Worker versucht Schritt zu überspringen -> BLOCKED
6. Worker versucht `next_step` einzuschleusen -> BLOCKED
7. falsche Job-ID -> BLOCKED
8. gefälschter Input-Hash -> BLOCKED
9. Output nach Worker-Rückgabe verändert -> BLOCKED
10. Worker liefert FAIL -> BLOCKED
11. Validator liefert nicht PASS -> BLOCKED
12. manipulierter/reorderter Checkpoint -> BLOCKED
13. Worker manipuliert seine Input-Kopie -> zentraler Zustand bleibt unverändert
14. Paket wird nach externer Signatur verändert -> Signaturprüfung FAIL

## Erste Bewertung

Der Kernunterschied zur Raum-/Raum-Lösung ist technisch darstellbar:

- weiterhin genau ein Mikroschritt pro Worker,
- weiterhin Prüfung nach jedem Schritt,
- aber nur ein Eigentümer des kanonischen Zustands,
- keine Worker-zu-Worker-Handoffs,
- Worker können keinen Folgeschritt anweisen,
- externe Endsignatur kann die exakten Ausgabebytes bis zur Importseite binden.

## Noch ausdrücklich offen

Dieser POC beweist NICHT:
- dass alle bestehenden Textregeln korrekt eingebunden sind,
- dass die echte Textmaschine ohne Änderung sauber aufgerufen werden kann,
- dass alle heutigen M01-M33-Sicherheitsanforderungen in dieser Architektur erhalten oder einfacher abgebildet werden,
- dass die WordPress-Seite die Signatur tatsächlich fail-closed prüft,
- dass alle notwendigen textlichen Qualitätsprüfungen ohne freie KI-Entscheidung abbildbar sind.

Nächster zulässiger Schritt dieser Alternativroute:
bestehende unverhandelbare Anforderungen gegen die Zentralmaschine mappen, ohne Produktionscode oder Textmaschine zu verändern. Erst danach zweiter POC mit echten Schnittstellen, aber weiterhin ohne reale Artikelproduktion.
