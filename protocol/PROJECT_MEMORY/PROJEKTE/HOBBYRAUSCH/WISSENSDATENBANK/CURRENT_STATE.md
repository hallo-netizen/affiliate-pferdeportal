# HOBBYRAUSCH – WISSENSDATENBANK – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-22
STATUS: **HOBBYREGISTER 862/862 / 54 TRAITS VOLLSTÄNDIG / 57ER ZIELSCHEMA FEST / SCHEMA F V1 FEST**

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_WISSENSDATENBANK`.

Fester Registervertrag:
`HOBBYREGISTER.md`

Fachlich beschlossene Ergänzung:
`HOBBY_EIGENSCHAFTEN_SCHEMA_1_2_DELTA.md`

Verbindlicher Register-Seitenvertrag:
`HOBBYREGISTER_SCHEMA_F_V1.md`

## Eine zentrale Datenwahrheit

Persistente zentrale Daten:
- `/Hobby Depot/Hobby-Klassifikation/HOBBY_KLASSIFIKATIONSREGISTER_V1.json`
- `/Hobby Depot/Hobby-Klassifikation/HOBBY_EIGENSCHAFTEN_SCHEMA_V1.json`
- `/Hobby Depot/Hobby-Klassifikation/HOBBY_KURZPROFIL_SCHEMA_V1.json`

Finder, Magazin, SEO-Views, Registerdarstellung und Design führen keinen eigenen Hobbybestand.

## Bestehender vollständig geprüfter Datenstand

- **862** kanonische Hobbyidentitäten;
- bisherige Schema-Version **1.1**;
- **54** bestehende Eigenschaften in 8 Gruppen;
- **862/862** Hobbys mit **54/54** geprüften bestehenden Traits;
- **862/862** Hobbys mit **4/4** Kurzprofilfeldern:
  - Was ist das?
  - Was macht man?
  - Was braucht man?
  - Was ist der Reiz?
- eindeutige Registry-IDs: PASS;
- eindeutige kanonische Namen: PASS;
- bestehende 54 Traitwerte gegen Schema 1.1: PASS;
- Gesamtfehler im geprüften Altbestand: **0**.

Finaler Register-SHA-256 des 54er Vollbestands:
`4deb4be2b235db450d58f02485ec40e780fc2671f9dfc6edf8cbbba0f738af78`

## Entscheidung 2026-10-22 – Schema 1.2 / 57 Merkmale

Die bestehenden 54 Eigenschaften wurden kritisch gegen Hobbyfinder, Registerdarstellung und Schema-F-Bedarf geprüft.

Drei echte Lücken wurden bestätigt:
1. `equipment_maintenance` – Pflege / Wartung der Ausrüstung;
2. `strength_need` – Kraftbedarf;
3. `coordination_balance_need` – Koordination / Balance.

Integritätsprüfung:
- ursprüngliche 54 Definitionen in der lokalen 1.2-Kandidatenfassung **1:1 unverändert**;
- neue Gesamtzahl **57**;
- Property-IDs **57/57 eindeutig – PASS**;
- weiterhin exakt **8 Gruppen**;
- Gegenprüfung an stark unterschiedlichen Hobbytypen durchgeführt;
- keine weitere zwingende Merkmalslücke festgestellt.

Wichtig:
Die drei neuen Traits werden **nicht geraten**. Bis zur hobbyweisen Klassifikation gelten sie als UNKNOWN. Die bereits geprüften 54 Werte werden nicht neu angefasst.

## Schema F V1 – verbindlich

Alle Register-Einzelprofile folgen demselben Seitenvertrag:
- F1 Sofort verstehen;
- F2 Passt das zu mir?;
- F3 Wo und wann?;
- F4 Platz, Alltag und Verträglichkeit;
- F5 Kosten und Ausrüstung;
- F6 Anforderungen;
- F7 Ergebnis/Erlebnis;
- F8 Grenzen/Sicherheit;
- F9 kompakter Vergleichsblock;
- F10 ähnliche Hobbys.

Die 57 Traits werden nicht als Tabellenwand ausgegeben, sondern in natürlichen hobbybezogenen Fließtext übersetzt.
UNKNOWN darf nicht in Behauptungen umgewandelt werden.

## Hobbyfinder

Der geprüfte Finder bleibt funktional auf Basis der bestehenden 54 vollständig klassifizierten Traits.
Die drei neuen Traits sind Ergänzungen; sie verändern den bestehenden 8-Schritte-Hauptfunnel nicht automatisch.

## SEO-/Registerbezug

Alle 862 Hobbys bleiben im zentralen Register.
Schema F gilt für alle identisch.
Die Entscheidung, ob ein Registerprofil Google-seitig sichtbar bleibt oder zugunsten einer starken CORE-Hauptseite unterdrückt wird, ist eine getrennte SEO-/Owner-Entscheidung und verändert den Registerinhalt nicht.

## EXAKT EINE NEXT ACTION

**Die drei neuen Traits `equipment_maintenance`, `strength_need` und `coordination_balance_need` hobbyweise für den 862er-Bestand klassifizieren und gegen Schema 1.2 prüfen. Bestehende 54 Werte unverändert lassen; UNKNOWN statt Raten. Danach erst die Schema-F-Seitenproduktion auf den vollständigen 57er-Datenstand umstellen.**
