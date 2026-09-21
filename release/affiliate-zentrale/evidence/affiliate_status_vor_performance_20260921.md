# Affiliate-Zentrale – sicherer Unterbrechungsstand vor Performance-Arbeit

Stand: 21.09.2026
Repository: hallo-netizen/affiliate-pferdeportal
Arbeitsbranch: affiliate-release-current

## Unveränderlicher Rückfallpunkt
- `AFFILIATE_ZENTRALE_V6.72.142_AWIN_TRANSPORT_LIVEPATH_ROOTFIX_HARDTEST.zip`
- 6.72.142 ist der letzte vom Benutzer für den Awin-Partnerimport ausdrücklich live bestätigte PASS-Punkt.
- Dieser ZIP-Stand darf nicht überschrieben, ersetzt oder rekonstruiert werden.
- Bei einer Regression eines späteren Testplugins ist zuerst auf exakt 6.72.142 zurückzugehen; keine Kette improvisierter Minifixes.

## Danach gebaut, aber noch nicht live abgenommen
- `AFFILIATE_ZENTRALE_V6.72.143_BANNER_TARGETURL_EXACT_TIER_ROOTFIX_HARDTEST.zip`
- 6.72.143 basiert auf der echten 6.72.142-Datei.
- Änderung war ausschließlich für AFF-ERR-041 / Banner-Relevanz gedacht: echte Ziel-/Deeplink-Evidenz sollte als Exact-Topic-Stufe vor allgemeinen Partner-/Keyword-Signalen wirken.
- Lokale Positiv-/Negativtests wurden durchgeführt.
- 6.72.143 ist NICHT als Live-PASS zu behandeln, solange der Benutzer sie nicht produktiv geprüft hat.

## Pausierter Arbeitsstrang
Referenzseite:
`https://pferde-atelier.de/ausruestung/ausruestung-reiterbedarf/reithelme/`

Zielregel:
1. technisch gültig
2. exakter Themenbezug
3. erweiterter Themenbezug
4. allgemeiner Pferde-/Shop-Fallback
5. letzter technisch gültiger aktiver Banner

Der Banner-Arbeitsstrang ist ab jetzt PAUSIERT und darf erst nach Abschluss des Performance-Blockers fortgesetzt werden.

## Dazwischengeschobener Blocker: massive Performanceprobleme
Produktionsmessungen zeigen seitenabhängig mehrere Sekunden bis über 10 Sekunden Serverzeit und mehrere Tausend bis >13.000 Datenbankabfragen.
Der aktuelle Hauptverdacht ist eine N+1-/Repeat-Query-Explosion im Affiliate Router, insbesondere:
- `control_get_decision()` / `ppar_control_decisions`
- eBay-Lookup nach `creative_identity_hash` + `seller_account_type='BUSINESS'`
- wiederholte Creative-Library-Lookups nach `identity_hash`

HARD RULE für Performance-Fix:
- keine fachliche Affiliate-Entscheidung verändern
- keine Daten/Freigaben/Vetos/Ziel-/Slotbindungen verändern
- eBay BUSINESS/PRIVATE-Regeln unverändert
- ausschließlich identische DB-Lesezugriffe innerhalb desselben Requests reduzieren
- zuerst request-lokale Caches; Batch-Queries nur falls danach noch nötig
- Write-Pfade müssen Cache aktualisieren oder invalidieren
- Positiv-/Negativtests und Gesamtworkflowprüfung vor neuem Plugin
- danach Produktionsmessung vorher/nachher mit Performance Diagnose Safe 2.0.0

## Wiedereinstieg nach Performance-PASS
Erst wenn Performance-Fix fachlich neutral und messbar PASS ist:
1. neuen Performance-fixierten Pluginstand als eigene Version sichern
2. Banner-Relevanzarbeit aus diesem Dokument wieder aufnehmen
3. 6.72.143-Banneränderung gegen den dann aktuellen Performance-Stand erneut integrieren oder, falls 6.72.143 live bereits getestet worden sein sollte, entsprechend fortführen
4. keine 6.72.142-Sicherung überschreiben
