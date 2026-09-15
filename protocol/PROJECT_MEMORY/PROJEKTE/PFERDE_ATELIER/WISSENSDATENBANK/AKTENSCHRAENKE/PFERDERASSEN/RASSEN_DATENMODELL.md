# PFERDERASSEN – DATENMODELL

STAND: 2026-09-14
SCHEMA_VERSION: 1.2
STATUS: VERBINDLICH / ERWEITERBAR

## GRUNDREGEL

Ein Datensatz pro fachlich bestätigter Rasse bzw. ausdrücklich gekennzeichneter Population. Pferde, Ponys und Kleinpferde liegen in derselben Datenbasis.

## KERNFELDER

1. `id` – stabiler interner Schlüssel
2. `schema_version`
3. `rassename_de`
4. `originalname`
5. `synonyme`
6. `formaler_status` – anerkannte Rasse / Zuchtpopulation / ferale Population / historische-ausgestorbene Rasse / Wild-Equide / unklar / keine eigenständige Rasse
7. `anerkennungsquelle` – zuständiges Zuchtbuch/Verband/Behörde/FAO etc.
8. `typ` – Pferd / Pony / Kleinpferd / sonstige fachlich belegte Einordnung
9. `rassegruppen` – z. B. Warmblut, Vollblut, Kaltblut, Gangpferd, Landrasse; Mehrfachwerte möglich
10. `herkunft_land`
11. `herkunft_region`
12. `geschichte_entstehung`
13. `urspruenglicher_lebensraum`
14. `anpassungen_aus_lebensraum`
15. `urspruengliche_nutzung`
16. `heutiger_einsatz`
17. `stockmass`
18. `gewicht` – nur soweit sinnvoll/belegt
19. `exterieur_gesamt`
20. `kopf`
21. `hals`
22. `ruecken_rumpf`
23. `kruppe_hinterhand`
24. `gliedmassen_fundament`
25. `fellfarben`
26. `zeichnungen_besonderheiten`
27. `maehne_schweif_behang`
28. `bewegung_gangarten`
29. `charakter_temperament`
30. `lernverhalten_arbeitsbereitschaft`
31. `robustheit_klimaanpassung`
32. `haltung_besonderheiten`
33. `fuetterung_besonderheiten`
34. `gesundheit_genetik`
35. `lebenserwartung` – nur bei belastbarer Datengrundlage
36. `heutige_verbreitung`
37. `zucht_zuchtziel`
38. `bestand_gefaehrdungsstatus`
39. `besondere_fakten`
40. `aehnliche_rassen` – kuratierte Liste stabiler `breed-*`-IDs fachlich ähnlicher/verwandter Rassen
41. `quellen`
42. `recherche_status`
43. `letzte_pruefung`
44. `zusatzfelder`

## ÄHNLICHE RASSEN – HARTE REGEL

`aehnliche_rassen` ist die einzige autoritative Quelle für einen Frontend-/Designblock „Ähnliche Rassen“.

Zulässige Form:

```json
"aehnliche_rassen": [
  "breed-beispiel-1",
  "breed-beispiel-2"
]
```

Regeln:
- ausschließlich stabile vorhandene `breed-*`-IDs;
- keine freien Namen, Slugs oder URLs;
- keine automatische Ableitung allein aus derselben Importkategorie;
- eine Rasse darf nur aufgenommen werden, wenn die Ähnlichkeit/Verwandtschaft durch vorhandene Fakten fachlich begründbar ist, z. B. gemeinsame dokumentierte Abstammung, gleiche klar belegte Untergruppe, vergleichbarer historischer Zuchtursprung oder ausdrücklich dokumentierte enge Typ-/Nutzungsverwandtschaft;
- reine optische Ähnlichkeit, gleicher Kontinent oder bloß gleiche Obergruppe reichen nicht;
- keine Selbstreferenz;
- keine erfundenen oder vermuteten Beziehungen;
- bevorzugt 2–4 Einträge, wenn belastbar vorhanden;
- wenn nicht belastbar bestimmt: `"aehnliche_rassen": "nicht_recherchiert"`;
- der Design-/Frontendcode darf bei `nicht_recherchiert` oder leerer Liste keinen Ähnliche-Rassen-Block erzwingen.

Für spätere Korrekturen bleibt die Beziehung im jeweiligen Rassendatensatz gespeichert; das Design darf sie nicht selbst berechnen oder verändern.

## STATUS FÜR FEHLENDE INFORMATION

- `nicht_recherchiert`
- `nicht_belegt`
- `nicht_anwendbar`
- `quellenkonflikt`

Keine leeren Felder durch Vermutung füllen.

## QUELLEN PRO FAKT

Mindestens speicherbar:
- Organisation/Autor;
- Titel/Dokument;
- URL/stabile Referenz;
- Abruf-/Prüfdatum;
- Trust-Tier A/B/C;
- betroffene Felder;
- Status: bestätigt / ergänzend / widersprüchlich / veraltet.

Verbindlicher allgemeiner Quellenstandard:
`../../RECHERCHE_STANDARD.md`.

## CHARAKTER

Nur belegte rassetypische Tendenzen oder Aussagen aus anerkanntem Zuchtziel speichern. Keine Garantie für das Einzeltier und keine pauschalen Eignungsversprechen.

## GESUNDHEIT / GENETIK

Nur bestätigte genetische Besonderheiten oder dokumentierte Prädispositionen. Häufig wiederholte Behauptungen ohne belastbare Evidenz werden nicht als Fakt gespeichert.

## FLEXIBLE ERWEITERUNG

Wenn ein neuer sinnvoller Punkt auftaucht:
1. fachlichen Nutzen prüfen;
2. Feld hier zentral definieren;
3. `schema_version` erhöhen, wenn strukturell relevant;
4. Alt-Datensätze bleiben gültig;
5. neue Felder dort zunächst `nicht_recherchiert`;
6. anschließend kontrolliert nachrecherchieren.

`zusatzfelder` darf neue fachliche Informationen aufnehmen, bis geklärt ist, ob daraus ein Standardfeld für alle Rassen wird.

## DATENABLAGE

Ein Datensatz pro Rasse/Population unter `DATEN/`, bevorzugt JSON mit stabiler ID.

Keine monolithische Riesendatei. Kleine Einzeldatensätze sind leichter prüfbar, versionierbar und erweiterbar.
