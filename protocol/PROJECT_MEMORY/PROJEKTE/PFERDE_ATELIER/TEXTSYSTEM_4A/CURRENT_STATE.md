# TEXTSYSTEM 4A – CURRENT STATE

STAND: 2026-09-13
STATUS: AKTIV / PROTOTYP NICHT PRODUKTIONSFREIGEGEBEN

## Gesicherter Ausgangsbefund

- System 4 läuft isoliert in PR #238, Branch `hobbyroom/system4-true-single-room-v1`, aktueller geprüfter Head bei Büroanlage: `77c02a9df1745a28157fcc27f65f74e9c4fb1153`.
- System 4 ist aktuell BLOCKED, weil der vollständige aktuelle Unittest-/E2E-Beweis auf genau diesem Head noch fehlt.
- Der aktuelle System-4-Einzelartikelkern ist bereits deutlich verbessert: kanonischer Zustand, feste Phasen, Same-Article-Repair, interne Content-/Designprüfungen und ein zentraler Fullcheck.
- Deshalb ist 4a **keine neue Textmaschine** und kein Ersatz der vorhandenen Qualitätslogik.

## Nachgewiesene Restprobleme / 4a-Anlass

1. Der aktuelle System-4-Handoff validiert exakt `len(articles)==7`.
2. Derselbe Handoff akzeptiert aktuell ausschließlich `article_type == Beratung`.
3. `batch_gate.py` schreibt als nächsten Schritt weiterhin `SIGNED_WORKFLOW_RELEASE`, obwohl der aktuelle System-4-Zielweg mit deaktivierter Signaturprüfung und direktem WordPress-Import arbeitet.
4. Damit ist der Ausgangsweg noch nicht universell für 1–∞ Artikel und neue Beitragsarten.
5. Historisch sind gerade Übergabe-, Signer-, Receipt-, Package- und Zustandsgrenzen wiederholt zu Hauptfehlerquellen geworden.

## Unverändert / unangetastet

- bestehende Textmaschine und Fachregeln;
- PPM 6.7.9;
- LanguageTool 6.8 / Bestand 43;
- PSERC/PSTE/SEO-/Link-/Tabellen-/Metadatenregeln;
- Design, Theme/CSS, WordPress-Plugin;
- offizieller STARTMASTER/CURRENT_STATE;
- System 4 / PR #238;
- `publish_allowed=false`.

## 4a-Status

Büro angelegt. Architekturentscheidung getroffen: 4a wird ausschließlich als isolierter Universalitäts-/Vereinfachungsprototyp aufgebaut.

Noch NICHT bewiesen:
- realer vollständiger Validatoranschluss;
- echter positiver End-to-End-Lauf;
- 1/3/25/1000;
- mehrere reale Beitragsarten;
- direkte WordPress-Importprüfung gegen den aktuell installierten Importer.

Kein PASS darf daraus abgeleitet werden.
