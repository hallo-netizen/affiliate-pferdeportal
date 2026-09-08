# P13 – BESTEHENDE HARD-RULE-REGISTER

Datum: 2026-09-08
Status: TEIL-GO, FREIHEITS-AUDIT ERFORDERLICH

## Ziel

Prüfen, ob die problematischen Fachregeln bereits innerhalb der unveränderten Originalkomponente verankert sind, statt sie in der Alternativarchitektur neu außen anzubauen.

## Harte Befunde aus dem unveränderten PPM-6.7.9-Paket

### Tabellenregeln – INNEN VERANKERT

Im bestehenden `contracts/hard-rule-registry-v1.json`:

- aktiver Vertrag: `contracts/table-contract-v1.json`
- HR-TABLE-001
- HR-TABLE-002
- HR-TABLE-003
- HR-TABLE-004
- Validator: `PPM679_Table_Hard_Rule_Validator`
- vorhandene Positiv-/Negativtests
- weitere blockierende Tabellenregeln, u.a.:
  - genau eine kanonische Tabelle
  - Mindestanzahl Inhaltszeilen
  - Pflicht-/Verbotssektionen
  - konkrete Tabellen-Nützlichkeit

Folgerung:
Die Tabellenregel wird NICHT neu als externer Gate-/Worker-Baustein gebaut.
Die vorhandene PPM-Regelautorität bleibt zuständig.

### Linkregeln – INNEN VERANKERT

Im selben Hard-Rule-Register:

- `contracts/wordpress-link-target-snapshot-v1.json`
- HR-LINK-001
- HR-LINK-002
- HR-LINK-003
- `PPM679_WordPress_Link_Target_Validator`
- vorhandene Positiv-/Negativtests
- weitere blockierende Regeln:
  - exakt drei sichtbare interne Links
  - jede gebundene Linkrolle exakt einmal
  - gebundene Links müssen wirklich vorhanden sein
  - Linkziel muss im Portalregister aktiv/exakt gebunden sein
  - Platzierung gebunden
  - echte relative Portal-URL

Folgerung:
Auch die Linkregeln dürfen NICHT noch einmal außen an die Zentralmaschine angehängt werden.

### LanguageTool – HARD RULE VORHANDEN

Hard-Rule-Register enthält explizit:
`The complete visible text requires exact LanguageTool 43 raw evidence with zero unresolved findings.`

Folgerung:
LanguageTool-Pflicht ist bereits bestehende Regelautorität und darf nicht neu interpretiert werden.

### Dubletten/Kannibalisierung – HARD RULES VORHANDEN

U.a.:
- Duplicate sentence ratio
- Section duplicate
- Duplicate headings
- Systemwide duplicate guard
- Keyword ownership collisions across portal/journal/all WordPress statuses -> BLOCK

### SEO – HARD RULE VORHANDEN

U.a.:
- `TITLE_MUST_CONTAIN_TARGET_KEYWORD`
- Keyword-Ownership-Kollisionen blockieren

### Publish-Safety – HARD RULE VORHANDEN

U.a.:
- `No publish path or publish permission`
- zahlreiche vorhandene Publish-Prohibition-Tests

### Artikeltyp/Struktur – HARD RULES VORHANDEN

U.a.:
- Article-Type-Contract muss existieren
- Production-Allowed muss stimmen
- Evidence muss Schema entsprechen
- Evidence Article Type muss Registry Key entsprechen
- Content-Structure-Language-Gate besitzt bestehende Implementierung und Tests

## Zentrale KISS-Folgerung

Die Alternativarchitektur soll NICHT zwölf Fachvalidatoren neu bauen.

Stattdessen:
- Zentralmaschine erzwingt den vollständigen 12-Gate-Vertrag.
- Bestehende unveränderte Fachkomponenten bleiben Eigentümer ihrer Regeln.
- Wenn PPM mehrere Regeln bereits atomar absichert, wird PPM als bestehender Baustein genutzt.
- Kein zweites Tabellen-Gate.
- Kein zweites Link-Gate.
- Keine Kopie der Textregeln.

Das reduziert Architektur statt sie zu vergrößern.

## FREIHEITSALARM

Im bestehenden Hard-Rule-Register wurde für HR-LINK-002 gefunden:

`validator_or_reviewer = PPM679_WordPress_Link_Target_Validator + Claude`

Das ist für die Alternativarchitektur NICHT automatisch akzeptabel.

Unklar ist noch:
- Ist Claude nur dokumentierender Reviewer?
- Hat Claude fachliche PASS/FAIL-Autorität?
- Kann sein Urteil den technischen Validator überstimmen?
- Ist sein Ergebnis frei/interpretativ?

Solange das nicht geklärt ist:
P13 = TEIL-GO, NICHT FULL PASS.

## Nächster Schritt P14

Harter Freiheits-Audit aller bestehenden Rule-Owner/Reviewer.

Suche insbesondere nach:
- Claude
- ChatGPT/GPT
- AI/LLM
- human/manual reviewer
- frei interpretierenden Reviewern

Ziel:
Kein solcher Akteur darf im neuen automatischen Produktionsweg eine freie PASS/FAIL-, Workflow- oder Reparaturentscheidung besitzen.

Keine bestehende Regel ändern.
Nur Autoritätsstruktur prüfen.
