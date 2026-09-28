# PILOT-TESTVERTRAG – PFERDEHAFTPFLICHT VERGLEICHEN

STATUS: BOUND / NO SOURCE WRITE UNTIL PERFORMANCE CLOSEOUT

## Ziel

Beweisen, dass eine optisch normale dritte Kachel auf `Pferdehaftpflicht` zu einer technisch getrennten Landingpage führen kann, ohne Kategorie-, Textmaschinen-, Journal- oder Performancepfade zu vermischen.

## Positivfall

Nur auf der gebundenen Pilotseite:
- Kachel `Pferdehaftpflicht vergleichen` sichtbar;
- optisch identische vorhandene Kachelkomponente;
- Ziel ist eine normale WordPress-Seite;
- Tarifcheck-Rechner genau einmal ausspielbar;
- bestehende Affiliate-Veto-/Providersteuerung greift;
- bestehende Beratung-/FAQ-Kacheln bleiben unverändert.

## Negativfälle

Müssen alle PASS sein:
1. keine neue WordPress-Kategorie;
2. keine Änderung an KATEGORIEN.tsv;
3. keine PSTE-/PSERC-/TEXT-Zuordnung für die Landingpage;
4. keine automatische Journalproduktion für die Landingpage;
5. keine Zusatzkachel auf einer anderen Ebene-3-Seite;
6. keine Rechnerausgabe auf Startseite;
7. keine Rechnerausgabe auf normaler Kategorie;
8. keine Rechnerausgabe auf normalem Journalartikel;
9. keine Rechnerausgabe bei unbekanntem Provider;
10. keine Rechnerausgabe bei Provider-Pause/Veto;
11. CHECK24 erzeugt im Pilot keinen zweiten Versicherungsrechner;
12. keine zusätzliche Menü-, Taxonomie- oder Kategorieabfrage auf Negativseiten;
13. keine zusätzliche externe Provideranfrage auf Negativseiten;
14. vorhandene Bannerverteilung bleibt byte-/verhaltensgleich außerhalb des Piloten;
15. vorhandene Ranking-/Veto-/Slotlogik bleibt unverändert.

## Performance-Hardlock

- kein globaler `the_content`-Scan zum Finden der Landingpage;
- kein `pre_get_posts`-Hook;
- keine globale Menü-/Kategorie-/Taxonomieauflösung;
- Rechner nur bei explizitem Shortcode auf der Pilotseite;
- Provider-Registry-Requestcache bleibt unverändert;
- null Frontend-Provider-Netzwerkzugriff auf Seiten ohne Rechner;
- kein neues periodisches Frontend-Polling;
- kein zweiter Bannerrouter.

## Abbruchregel

Bei erstem belegten FAIL:
STOP am ersten gebrochenen Punkt.
Nur diesen Punkt fixen.
Bereits PASSende Teile bleiben tabu.

## Freigabebedingung

Erst nach vollständigem Positiv-/Negativ-PASS darf über eine zweite Landingpage oder Verallgemeinerung entschieden werden.
