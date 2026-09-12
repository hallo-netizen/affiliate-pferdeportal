# PFERDERASSEN – DATENMODELL

STAND: 2026-09-12
SCHEMA_VERSION: 1.0
STATUS: VERBINDLICHE V1-FACHSTRUKTUR / ERWEITERBAR

## ZWECK

Diese Datei definiert die gemeinsame Struktur für Pferde-, Pony- und Kleinpferderassen.

Die Daten sind Recherchegrundlage für spätere Texte und weitere Funktionen. Sie sind **keine fertigen Artikeltexte**.

## GRUNDREGEL – EINE DATENBASIS

Keine getrennten Pferde- und Pony-Datenbanken.

Jede Rasse ist genau ein Datensatz. Die Einordnung erfolgt innerhalb des Datensatzes.

Grund: Rassebezeichnungen, Größenklassen, nationale Einordnungen und Begriffe wie Pony/Kleinpferd überschneiden sich. Getrennte Datenbanken würden Dubletten und Widersprüche fördern.

## KERNFELDER

Diese Felder sollen für jeden Datensatz vorhanden sein; fehlende Inhalte dürfen ausdrücklich als `nicht_recherchiert`, `nicht_belegt` oder `nicht_anwendbar` markiert werden.

1. `id` – stabiler interner Schlüssel
2. `schema_version`
3. `rassename_de`
4. `originalname`
5. `synonyme`
6. `typ` – Pferd / Pony / Kleinpferd / sonstige fachlich belegte Einordnung
7. `rassegruppen` – z. B. Warmblut, Kaltblut, Vollblut, Gangpferd, Landrasse; Mehrfachwerte möglich
8. `herkunft_land`
9. `herkunft_region`
10. `geschichte_entstehung`
11. `urspruenglicher_lebensraum`
12. `urspruengliche_nutzung`
13. `heutiger_einsatz`
14. `stockmass`
15. `gewicht` – nur soweit sinnvoll/belegt
16. `exterieur_gesamt`
17. `kopf`
18. `hals`
19. `ruecken_rumpf`
20. `kruppe_hinterhand`
21. `gliedmassen_fundament`
22. `fellfarben`
23. `zeichnungen_besonderheiten`
24. `maehne_schweif_behang`
25. `bewegung_gangarten`
26. `charakter_temperament`
27. `lernverhalten_arbeitsbereitschaft`
28. `robustheit_klimaanpassung`
29. `haltung_besonderheiten`
30. `fuetterung_besonderheiten`
31. `gesundheit_genetik`
32. `lebenserwartung` – nur bei belastbarer Datengrundlage
33. `heutige_verbreitung`
34. `zucht_zuchtziel`
35. `bestand_gefaehrdungsstatus`
36. `besondere_fakten`
37. `quellen`
38. `recherche_status`
39. `letzte_pruefung`

## QUELLEN PRO FAKT

Wo sachlich nötig, soll nicht nur eine allgemeine Quellenliste existieren, sondern die Zuordnung einzelner Fakten zu Quellen möglich bleiben.

Mindestens speicherbar:
- Quelle / Organisation
- Titel oder Dokument
- URL bzw. stabile Referenz
- Abruf-/Prüfdatum
- Quellentyp
- betroffene Felder
- Status: bestätigt / ergänzend / widersprüchlich / veraltet

Quellenpriorität:
1. offizieller Zuchtverband / Zuchtbuch / zuständige Behörde / internationale Stelle;
2. wissenschaftliche bzw. universitäre Quelle;
3. seriöse Fachquelle ergänzend.

## CHARAKTER – BESONDERE VORSICHT

Charakter ist keine Garantie für ein einzelnes Tier.

Gespeichert werden nur belegbare **rassetypische Tendenzen oder Zuchtziel-Aussagen**. Aussagen wie „immer kinderlieb“, „für Anfänger geeignet“ oder ähnliche pauschale Versprechen sind ohne belastbare Grundlage unzulässig.

## GESUNDHEIT – BESONDERE VORSICHT

Rassetypische Erkrankungen, genetische Varianten und Prädispositionen nur aufnehmen, wenn belastbar belegt.

Trennen zwischen:
- bestätigter genetischer Besonderheit;
- dokumentierter Prädisposition;
- häufig genannter, aber nicht ausreichend belegter Behauptung.

Letztere wird nicht als Tatsache gespeichert.

## FLEXIBLE ERWEITERUNG

Das Schema ist bewusst nicht eingefroren.

Wenn später ein neuer sinnvoller Punkt auftaucht:
1. fachlichen Nutzen prüfen;
2. neues Feld hier zentral definieren;
3. `schema_version` erhöhen, wenn die Änderung strukturell relevant ist;
4. vorhandene Rassen bleiben gültig;
5. neue Felder bei Alt-Datensätzen zunächst als `nicht_recherchiert` behandeln;
6. anschließend kontrolliert für alle betroffenen Rassen nachrecherchieren.

Keine Massenbefüllung durch Vermutung nur damit ein Feld nicht leer ist.

## ERWEITERUNGSBEREICH

Jeder Datensatz darf zusätzlich einen klar benannten Bereich `zusatzfelder` besitzen.

Dieser dient neuen fachlich sinnvollen Informationen, bevor entschieden wird, ob daraus ein dauerhaftes Standardfeld für alle Rassen wird.

Regel:
Ein wiederholt relevantes Zusatzfeld wird ins zentrale Schema übernommen; keine dauerhaft chaotischen Freitext-Sonderfelder pro Rasse.

## DATENSATZABLAGE

Ein Datensatz pro Rasse unter `DATEN/`.

Empfohlener Dateiname:
`<stabile-id>.json`

Vorteile:
- keine riesige monolithische Datei;
- kleine, prüfbare Änderungen;
- weniger Konflikte bei paralleler Recherche;
- einzelne Rassen leicht austauschbar/prüfbar;
- zentrale Struktur bleibt trotzdem über dieses Schema und `RASSEN_REGISTER.md` verbindlich.

## TECHNISCHE GRENZE

Diese Campus-Datensätze werden nicht bei jedem Webseitenaufruf geladen.

Sie dienen als Arbeits-/Recherchequelle. Eine spätere WordPress-, Filter- oder Rassenfinder-Funktion benötigt einen gesondert geprüften Export-/Importweg.
