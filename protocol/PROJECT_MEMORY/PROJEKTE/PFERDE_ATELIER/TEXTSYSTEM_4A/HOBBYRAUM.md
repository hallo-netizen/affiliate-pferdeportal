# TEXTSYSTEM 4A – HOBBYRAUM

STAND: 2026-09-13
STATUS: AKTIV

## AKTUELLE ARBEITSBINDUNG

THEMA: `KONZEPT_4A_UNIVERSELLE_ARTIKELKAPSEL`
STATUS: `PROTOTYP_AUFBAU`

AUFTRAG:
Einen minimalen, isolierten 4a-Kern beweisen, der den vollständigen Ablauf vom gebundenen Produktionsanstoß bis zur finalen WordPress-JSON technisch führen kann, ohne Fach-, Design- oder Qualitätsregeln selbst zu besitzen oder zu verändern.

## VERBINDLICHER PROZESS

1. **Ingress:** ausschließlich gebundene Metadaten (`title`, `target_keyword`, `category`, `article_type`, `plan_slot`) plus Batch-/Snapshot-Identität.
2. **Kapsel anlegen:** eine unveränderliche Artikelidentität; `publish_allowed=false`.
3. **Recherche:** Codex recherchiert; reale Quelle/Evidence/Hash erforderlich.
4. **Rechercheprüfung:** kein Fortschritt ohne gültige Evidence.
5. **Fakten/Fact-Pack:** aus akzeptierter Recherche; keine selbstzertifizierten Fakten.
6. **Faktenprüfung:** kein Fortschritt ohne gebundenes Pack.
7. **Text:** bestehende Textmaschine/Fachregeln READ-ONLY.
8. **Fullcheck:** echte bestehende Prüfer; 4a erzeugt kein eigenes Qualitäts-PASS.
9. **Repair:** nur derselbe Artikel und nur konkrete Findings; Recherche/Fakten/Metadaten bleiben gebunden.
10. **Artikel-PASS:** Artikelbytes einfrieren.
11. **Querschnitt:** Dubletten/Kannibalisierung/Schablonenwiederholung über alle fertigen Kapseln.
12. **Finalisierung:** universelle 1–∞-JSON; keine feste Beitragsart im Controller.
13. **WordPress-Handoff:** exakt eine kanonische Datei; `publish_allowed=false`; bytegleich in den Elternchat.

## AKTUELLE NEXT ACTION

1. isolierten GitHub-Hobbyraum `hobbyroom/system4a-capsule-v1-20260913` von aktuellem `main` anlegen;
2. minimalen Controller/Kapselvertrag bauen – noch ohne Ersatzprüfer;
3. harte Negativtests zuerst: Außensteuerung, State-Sprung, Publish-Manipulation, Artikelzahl-Hardcode, Beitragsart-Hardcode, fremde Artikelmutation;
4. danach vorhandene reale Prüfer READ-ONLY anbinden;
5. erst dann positiver Einzelartikel-E2E;
6. danach 1/3/25/1000 und mindestens zwei tatsächlich freigegebene Beitragsarten;
7. finalen JSON-/Chat-/WordPress-Weg positiv und negativ testen.

## STOPPREGELN

- Wenn 4a einen neuen fachlichen Prüfer benötigt: STOPP.
- Wenn 4a Text-/Designregeln kopieren oder verändern müsste: STOPP.
- Wenn 4a mehr Laufzeitautoritäten/Übergaben als System 4 erzeugt: STOPP und Konzept verwerfen.
- Wenn eine neue Beitragsart nur durch Controller-Umbau möglich wäre: Architekturziel verfehlt.
- Kein Merge/Publish/Pluginbau aus diesem Hobbyraum.
