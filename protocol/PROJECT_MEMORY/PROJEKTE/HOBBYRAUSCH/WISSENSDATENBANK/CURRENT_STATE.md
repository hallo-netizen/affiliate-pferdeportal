# HOBBYRAUSCH – WISSENSDATENBANK – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-20
STATUS: **HOBBYREGISTER COMPLETE / 862 VON 862 REVIEWED / HOBBYFINDER-VOLLBESTAND 862 LOKAL PASS**

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_WISSENSDATENBANK`.

Fester Registervertrag:
`HOBBYREGISTER.md`

## Eine zentrale Datenwahrheit

Persistente zentrale Daten:
- `/Hobby Depot/Hobby-Klassifikation/HOBBY_KLASSIFIKATIONSREGISTER_V1.json`
- `/Hobby Depot/Hobby-Klassifikation/HOBBY_EIGENSCHAFTEN_SCHEMA_V1.json`
- `/Hobby Depot/Hobby-Klassifikation/HOBBY_KURZPROFIL_SCHEMA_V1.json`

Finder, Magazin, SEO-Views und Design führen keinen eigenen Hobbybestand.

## Datenvertrag

- **862** kanonische Hobbyidentitäten;
- **54** Eigenschaften in 8 Gruppen;
- Schema-Version **1.1** eingefroren;
- je Hobby **54/54 Traits**;
- je Hobby **4/4 Kurzprofilfelder**:
  - Was ist das?
  - Was macht man?
  - Was braucht man?
  - Was ist der Reiz?
- Kurzprofil ist Präsentationsinhalt, keine Filtereigenschaft;
- Aliasnamen erzeugen keine zweite Hobbyidentität.

## Finaler geprüfter Stand

Zentrales Register:
`/Hobby Depot/Hobby-Klassifikation/HOBBY_KLASSIFIKATIONSREGISTER_V1.json`

Ergebnis:
- REVIEWED: **862/862**;
- PENDING_REVIEW: **0/862**;
- Kurzprofile REVIEWED: **862/862**;
- eindeutige Registry-IDs: **PASS**;
- eindeutige kanonische Namen: **PASS**;
- 54 Traits je Hobby: **PASS**;
- alle Traitwerte gegen Schema 1.1: **PASS**;
- alle Kurzprofile 4/4: **PASS**;
- Gesamtfehler: **0**.

Finaler Register-SHA-256:
`4deb4be2b235db450d58f02485ec40e780fc2671f9dfc6edf8cbbba0f738af78`

Schlussbatches:
- Batch 017: 50 Hobbys, 855/862, Audit `HOBBY_KLASSIFIKATION_BATCH017_AUDIT.json`;
- Batch 018: 7 Hobbys, 862/862, Audit `HOBBY_KLASSIFIKATION_BATCH018_AUDIT.json`.

Gesamtprüfung:
`/Hobby Depot/Hobby-Klassifikation/HOBBY_KLASSIFIKATION_COMPLETE_AUDIT.json`

## Current-Datei-Reparatur

Die zuvor mehrfach angehängten Satzreste am Dateiende waren eine reine Beschädigung dieser Statusdatei. Sie wurden entfernt. Der zentrale JSON-Registerbestand war davon nicht betroffen.

## Hobbyfinder

Konzept:
`/Hobby Depot/Hobby-Klassifikation/HOBBYFINDER_FUNNEL_V1.json`

Prototyp:
`/Hobby Depot/Hobby-Klassifikation/HOBBYFINDER_PROTOTYP_V1.html`

Grundoptik und Ablauf wurden vom Nutzer positiv bestätigt.

Vollbestand:
- Prototyp nutzt **862/862** zentrale Hobbyidentitäten;
- **862/862** Kurzprofile vorhanden;
- JavaScript-Syntax: PASS;
- 4 stark unterschiedliche Positivprofile: jeweils belastbare Treffer;
- harte Filter für Sozialform, Ort, Zeit, Budget und Platz gegen alle zulässigen Treffer geprüft: PASS;
- gezielte Negativtests: **5/5 PASS**;
- „Überrasch mich“ priorisiert ungewöhnliche/sehr schräge Hobbys wie vorgesehen.

QA:
`/Hobby Depot/Hobby-Klassifikation/HOBBYFINDER_FULL_862_QA.json`

QA-SHA-256:
`718d7e499f5f4729ec8886add6af4b67a2b9d0fe58d080933874aa4ea6dc0e20`

## ERSTER OFFENER BLOCKER

**Kein Daten- oder Finderlogik-Blocker mehr.** Der vollständige 862er-Bestand ist zentral klassifiziert und im Vollbestands-Prototyp geprüft.

## EXAKT EINE NEXT ACTION

**Den lokal geprüften 862er-Hobbyfinder in die WordPress-/Designstrecke überführen, ohne eine zweite Hobby-Datenbank anzulegen. Vor Liveeinsatz weiterhin lokale Positiv-/Negativtests und danach echten WordPress-Readback durchführen.**
