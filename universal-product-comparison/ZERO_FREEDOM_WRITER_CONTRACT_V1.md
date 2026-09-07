# UNIVERSAL PRODUCT COMPARISON – ZERO-FREEDOM WRITER CONTRACT V1

Stand: 2026-09-07

## Oberste Regel

**Der Produktions-Writer besitzt keinerlei freie Autorität.**

Er darf nicht:
- recherchieren;
- browsen;
- Fakten ergänzen;
- Fakten umdeuten;
- Regeln erzeugen;
- Regeln auswählen;
- Regeln abschwächen;
- Struktur verändern;
- Abschnitte ergänzen oder entfernen;
- Empfehlungen erfinden;
- Formulierungsvarianten wählen;
- Fallbacks erzeugen;
- alternative Wege benutzen;
- externe Modelle/LLMs aufrufen;
- Zufall, Uhrzeit oder Umgebungszustand zur Textvariation verwenden.

Gleicher gebundener Input + gleiche Versionen = byte-identisches Ergebnis.

## Übernommene Grundidee aus STARTMASTER/TEXT

Übernommen wird das bewährte Prinzip:
**Prompt ist keine Sicherung. Technische Akzeptanzsperren erzwingen den Ablauf.**

Bewusst übernommen:
1. Single Door;
2. exakt gebundene Eingaben;
3. Hash-Bindung;
4. fail-closed statt Ersatzroute;
5. Output-Quarantäne bis Validator-PASS;
6. feste Zustandsreihenfolge;
7. PASS-Receipt;
8. kein Auto-Publish;
9. bekannte reale Fehler werden Regressionstests;
10. Test darf nur behaupten, was wirklich geprüft wurde.

Bewusst NICHT übernommen:
- STARTMASTER-Raumkette;
- PPM/PSERC/PSTE;
- Signer-/Capsule-Kaskade;
- mehrere Executor-/Gate-Ebenen;
- freie Worker;
- alte Handoff-Komplexität.

## Produktionskette V1

BOUND_INPUT -> QUARANTINED_RENDERED -> VALIDATED -> DRAFT_READY_FOR_REVIEW

Nur diese Reihenfolge ist zulässig.

### 1. BOUND_INPUT
Gebunden sind:
- Vergleichs-ID;
- Produkt-/Variantenidentitäten;
- Produktwissen/Fakten;
- festgelegte Vergleichsmerkmale;
- expliziter Artikeltitel;
- Projektkonfiguration;
- Ruleset-ID + Ruleset-Version + SHA-256;
- Artikelvertrag-Version;
- Renderer-Version.

### 2. QUARANTINED_RENDERED
Renderer setzt ausschließlich fest definierte Daten und Textbausteine in das feste Template ein.

Keine Veröffentlichung und keine direkte Sichtbarkeitsfreigabe.

### 3. VALIDATED
Unabhängiger deterministischer Validator prüft:
- Pflichtabschnitte und Reihenfolge;
- Hash des Outputs;
- keine externen Links/Skripte/Formulare;
- No-Winner-Regel;
- Entscheidungsspalte;
- Regel-/Faktbindung;
- keine unbekannte Regel;
- keine fehlenden Pflichtfakten.

### 4. DRAFT_READY_FOR_REVIEW
Nur nach Validator-PASS.
publish_allowed=false.

## Regelbuch

Produktionscode akzeptiert keine frei übergebenen Callbacks oder Prompt-Regeln.

Erlaubt ist nur:
project_key + ruleset_id.

Das Rulebook:
- liegt als Datenfile vor;
- ist versioniert;
- ist im Manifest per SHA-256 gebunden;
- ist an einen Vergleich gebunden;
- enthält exakte erwartete Fakten-Signaturen;
- enthält nur bereits freigegebene Texte/Zuordnungen.

Ändert sich ein gebundener Fakt:
UPC_DECISION_RULE_FACT_BINDING_MISMATCH -> BLOCKED.

Ändert sich das Rulebook ohne Manifestupdate:
UPC_RULESET_HASH_MISMATCH -> BLOCKED.

Fehlt eine Regel für unterschiedliche verifizierte Fakten:
UPC_DECISION_RULE_MISSING -> BLOCKED.

## Keine unsichtbare Freiheit

Auch kleine vermeintliche Komfortfunktionen sind verboten:
- kein Fallback-Titel;
- kein Synonymwechsel;
- keine zufälligen Übergänge;
- keine automatische „schönere“ Formulierung;
- keine inferierte Pro-/Contra-Aussage;
- keine inferierte Bedarfszuordnung;
- keine freie Zusammenfassung.

Neue Textqualität entsteht ausschließlich durch eine neue, geprüfte Version des Artikelvertrags oder Rulebooks.

## Änderungsprinzip

Eine gewünschte Verbesserung wird nie live improvisiert.

Ablauf:
1. Änderung als neuer Vertrags-/Ruleset-Kandidat;
2. Positiv-/Negativtest;
3. Golden-Output prüfen;
4. neue Version freigeben;
5. erst dann produktiv verwenden.

Alte Version bleibt reproduzierbar.

## Leitsatz

**Nicht der Writer schreibt den Artikel. Der Vertrag schreibt den Artikel.**
