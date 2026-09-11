# PRODUKTVERGLEICH – ARCHITEKTURENTSCHEIDUNG PLUGIN FINAL AUTHORITY

Stand: 2026-09-11
Status: VERBINDLICHE FACH-/ARCHITEKTURENTSCHEIDUNG

## Entscheidung

Die letzte verbindliche Entscheidung darüber, **welche zwei Produkte tatsächlich als A-vs-B-Vergleich zulässig sind**, liegt im PRODUKTVERGLEICH-System/Plugin.

Research und SEO liefern Eingaben, dürfen aber keine finale Paarung erzwingen.

## Rollen

### Research / Product Knowledge
Liefert und aktualisiert:
- reale Herstellerfamilien;
- aktuelle konkrete Modelle;
- exakte Produktidentitäten;
- Herstellerquellen;
- gruppenspezifische Fakten;
- offene Konflikte/Abkündigungen/Ersetzungen.

### SEO
Liefert Nachfrage-/Priorisierungssignale:
- konkrete A-vs-B-Suchanfragen;
- produktbezogene Suchnachfrage;
- Kannibalisierungs-/Keyword-Signale.

SEO darf einen Paar-Kandidaten anstoßen oder priorisieren, aber keine fachlich unzulässige Paarung freigeben.

### PRODUKTVERGLEICH / Plugin
Ist die letzte Entscheidungsinstanz und prüft fail-closed:
- beide Produktidentitäten aktuell und gültig;
- Herstellerfamilienregel;
- gleiche Produktgruppe/Nutzungsebene;
- gemeinsames Vergleichsprofil/Faktenmatrix;
- Decision-Policy;
- fachliche Zulässigkeit;
- keine abgekündigten/ersetzten/falsch klassifizierten Produkte;
- erst danach SEO-Eignung/Dossierfreigabe.

## Aktualisierungsregel

Produktvergleiche sind **kein einmalig statischer Bestand**.

Das System muss wiederholbar neu bewerten können, wenn sich der Produktbestand ändert, insbesondere bei:
- neuen Produkten/Modellen;
- Modellwechseln/Nachfolgern;
- Abkündigungen;
- Hersteller-/Marken-/Familienänderungen;
- neuen oder geänderten Herstellerfakten;
- neuen SEO-Vergleichsanfragen;
- entfallener Suchnachfrage;
- geänderten Vergleichsprofilen/Decision-Policies.

Bei einer Aktualisierung wird das zulässige Paaruniversum aus dem **aktuellen gebundenen Produktwissen** neu berechnet. Vorhandene Paare dürfen dadurch neu entstehen, entfallen oder BLOCKED werden.

## Fail-closed-Grenze

- Research-Fund != freigegebenes Paar.
- SEO-PASS != fachlich zulässiges Paar.
- alter Vergleich != dauerhaft gültiger Vergleich.
- Affiliate-/Preis-/Verfügbarkeitssignale dürfen die fachliche Paarentscheidung nicht verändern.
- Keine Top-N-/Pair-Cap als Ersatz für fachliche Entscheidung.

## Konsequenz für den aktuellen Researchblock

Die laufende 175er Marktrecherche sammelt **Produktinventar und belastbare Kandidaten**, nicht manuell festgeschriebene End-Pärchen.

Die spätere Paarbildung und regelmäßige Neubewertung bleibt Aufgabe des bestehenden PRODUKTVERGLEICH-Systems/Plugins. Eine technische Umsetzung/Änderung wird erst gebaut, wenn der Researchblock groß genug ist und die bestehende Pluginlogik gegen diese Regel konkret geprüft wurde.

Kein Pluginbau allein aufgrund dieser Dokumentation.
Kein SEO-Lauf aus Research-Evidence.
Kein Merge.
Kein Publish.
