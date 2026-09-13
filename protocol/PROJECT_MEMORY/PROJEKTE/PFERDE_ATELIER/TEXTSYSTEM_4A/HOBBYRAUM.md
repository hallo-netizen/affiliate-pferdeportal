# TEXTSYSTEM 4A – HOBBYRAUM

STAND: 2026-09-13
STATUS: AKTIV / AUDIT- UND HÄRTUNGSRAUM

## AKTUELLE ARBEITSBINDUNG

THEMA: `KONZEPT_4_GEGEN_4A_HARTAUSWERTUNG`
STATUS: `4A_STANDALONE_VORERST_VERWORFEN`

AUFTRAG:
Konzept 4 gegen die ursprünglich gedachte 4a-Zielarchitektur hart prüfen und nur die nachweislich sinnvollen Vereinfachungen in einen Härtungsplan für Konzept 4 überführen. **Keine zweite Textmaschine und keine zweite Laufzeitarchitektur bauen**, solange kein irreduzibler Vorteil eines eigenständigen 4a bewiesen ist.

## ERGEBNIS DER KRITISCHEN PRÜFUNG

Der aktuelle System-4-Kern erfüllt bereits fast alle wesentlichen 4a-Ziele:
- ein kanonischer Artikelzustand;
- Codex als ein fachlicher Arbeiter;
- Recherche → Fakten → gebundener Produktionskontext → Text;
- echte unveränderte Prüfer;
- Same-Article-Repair;
- artikelübergreifende Prüfung;
- finaler WordPress-Handoff.

Separate Guard-/Prüfermodule sind **keine echten Handoffs**, solange derselbe Controller sie intern aufruft und allein die Phase verändert.

Die feste 7er-/`Beratung`-Bindung ist ein behebbarer Implementierungsfehler und ausdrücklich **kein 4a-Entscheidungskriterium**.

## ECHTER HÄRTUNGSPUNKT IN KONZEPT 4

Der aktuelle `controller.py` bietet neben dem verbindlichen FULL-Pfad technisch weitere erreichbare Wege (`check`/BASIC-Release sowie Signaturpfad). Der System-4-Zielvertrag verlangt dagegen den einen FULL-Produktion-→-Batch-→-Direct-Import-Weg.

Damit lautet die richtige Härtung:
**eine technisch erreichbare Produktionsstraße statt mehrerer auswählbarer Controllerpfade.**

## VERBINDLICHER ZIELPROZESS

`WordPress/SEO-Metadatenbatch -> kanonischer Artikelzustand -> Codex-Recherche -> gebundene Evidence -> Fakten/Fact-Pack -> Text unter unveränderter Textmaschine -> FULL-Prüfer -> Same-Article-Repair bei Finding -> Artikelbytes einfrieren -> artikelübergreifende Prüfung -> genau eine SYSTEM4_WORDPRESS_HANDOFF_V1.json -> Elternchat -> WordPress-Direct-Importer 0.28.23 -> Entwürfe`

## NEXT ACTION

1. keinen 4a-Controller bauen;
2. Konzept 4 auf **genau eine technisch mögliche Produktionsstraße** auditieren;
3. BASIC-Release und alten Signaturpfad aus der Produktionsoberfläche/-CLI entfernen oder technisch unerreichbar machen;
4. 7er-/`Beratung`-Hardcodes separat entfernen, ohne sie als 4a-Vorteil zu werten;
5. vorhandene FULL-Prüfer, Content-/Designregeln und Same-Article-Repair unverändert lassen;
6. finalen Handoff exakt gegen den realen WordPress-Importer 0.28.23 prüfen;
7. erst danach vollständige Positiv-/Negativtests 1/3/25/1000 und mehrere bereits freigegebene Beitragsarten.

## STOPPREGELN

- Keine neue Fach-/Text-/Design-/Qualitätsregel.
- Kein Ersatzprüfer.
- Kein zweiter Controller/Workflow-Besitzer.
- Kein neuer Signer/Receipt-/Room-/Package-Weg.
- Kein Merge/Publish/Pluginbau aus diesem Büro.
- Falls nach Bereinigung von Konzept 4 kein struktureller 4a-Vorteil übrig bleibt, bleibt 4a dauerhaft ein Auditbegriff und wird nicht als fünftes System gebaut.
