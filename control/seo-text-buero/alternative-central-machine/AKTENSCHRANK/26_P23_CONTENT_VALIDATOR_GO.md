# P23 – CONTENT-VALIDATOR ALS BESTEHENDER FACHKERN

Datum: 2026-09-08
Status: GO / RESTGATES SEPARAT PRÜFEN

## Harte Befunde

Der reale Normal-Draft-Pfad ruft über `check_all()` exakt:

`PPM679_Content_Validator::check`

Dieser ruft fest:
- `PPM679_Article_Type_Validator::type_definition`
- `PPM679_Content_Structure_Language_Gate::evaluate`
- `PPM679_Known_Error_Gate::evaluate`
- `PPM679_Fail_Closed_Aggregator::merge_content_validation_with_structure`

## Bereits intern gebündelt

Der Content-Structure-Language-Gate prüft u.a.:

- Artikeltyp / gebundene Struktur
- sichtbaren Titel / Marker
- Blöcke und Intro
- Zwischenüberschriften
- FAQ-Direktantwort-Regeln
- Listen
- interne Links
- Fazit
- Tabellen-Nützlichkeit
- LanguageTool-Evidence
- bekannte Sprachfehler
- Basic HTML

Der Known-Error-Gate ergänzt u.a.:
- Body-H1 verboten
- Titel nicht im Body wiederholen
- Dublettenüberschriften
- generische/technische Überschriften
- direkt aufeinanderfolgende Überschriften

Der Fail-Closed-Aggregator verlangt gleichzeitig:
- Base PASS
- Known-Error PASS
- Structure/Language PASS
- keine Fehler

und setzt in dieser Prüfstufe:
- draft_create_allowed=false
- publish_allowed=false

## Wichtig

Der bestehende Gate nennt seinen eigenen Scope ausdrücklich:
`deterministic structure, bindings and LanguageTool evidence; no final editorial or visual PASS`

Daher wird NICHT behauptet, dass damit bereits alle 12 Pflichtgates erledigt sind.

## KISS-Folgerung

Nicht neu bauen:
- Tabellen-Gate
- internes Link-Gate
- LanguageTool-Gate
- Artikelstruktur-Gate
- bekannte Content-Regressionen
- Basis-HTML-/Formatprüfung

Diese bleiben Bestandteil des unveränderten PPM-Fachkerns.

## Noch separat zu beweisen

1. systemweite Duplicate-/Cannibalization-/SEO-Planprüfung
2. Recherche / Fact-Pack / PSTE-Herkunft
3. finales Design / Visual PASS
4. PSERC/PSTE genaue Rollen im neuen Einmaschinenweg

Publish-Safety ist durch P22 bereits separat hart bewiesen.

## Nächster Schritt P24

Exakt:
`PPM679_Editorial_Plan_Runtime_Gate::preflight`

prüfen auf:
- systemweite Dubletten
- Keyword Ownership
- WordPress-Inventar
- Canonical Plan Slot
- SEO-/Planbindung

Keine neue Logik.
