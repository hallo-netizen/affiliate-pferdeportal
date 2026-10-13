# Hab & Bewahr – 15 priorisierte R3/V8 SERP-Paare: echter WordPress-Ergebnisabgleich vom 13.10.2026
**Status:** echte Anbieter-Daten ausgewertet, 15/15 redaktionell kommentiert, **0/144 SEO-Owner final freigegeben**, keine WordPress-Kategorie-/Artikeländerung.

**Quellen:** Zwei in den Chat hochgeladene wort- und byte-identische Originalexports `hab-bewahr-r3-serp-20261013-133040-utc.json` und `hab-bewahr-r3-serp-20261013-133041-utc.json`, SHA256 `f2f143fddafaf8c2b3deaab85bc192ae4f996993d0817570721738cb1e4368da`. Vertrag `HB_R3_SERP_PAID_ONCE_RESULT_V1`, Plan `17cd5721ba6d134bb7d4c0d234ff609b35a941e85dcbdb941bf6d4e8ba4a454b`, Germany/de, 13:25:18–13:30:08 UTC. Ein einziger Lauf, 15 Paare / 30 Keywords. 24 Taskstatus 20000, 6 Taskstatus 40101 (interner Anbieterfehler trotz HTTP 200), 10 beidseitig messbar, 5 nicht vollständig messbar. Export-Kosten `0.06 USD`. Status COMPLETE = Lauf abgeschlossen, nicht SEO-Freigabe. Anbieter-TASK 40101 = nicht Null-Treffer. Ausgewiesene WP-Writes: Kategorien 0, Artikel 0.

## Evidenz für jede Prioritäts-Kategorie
Die folgende korrigierte gemeinsame URL-Zahl basiert auf identischer URL einschließlich inhaltstragender Queryparameter (nur Tracking-IDs entfernt). Eine Null ist keine Aussage über identischen Suchintent.

| Neue R3-Kategorie | Provider-TASK R3 / Vergleich | korrigierte gemeinsame SERP-URLs | Redaktionelle Entscheidung / Grenze |
|---|---|---:|---|
| Grenzüberwachung im Garten | 40101 / 20000 | — | R3-Primärfrage nicht gemessen; R2-Kameradatenschutz-SERP allein unzureichend. |
| Außenrollläden vor Vandalismus | 40101 / 40101 | — | Beide SERPs nicht gemessen; keine Freigabe. |
| Spielgeräte vor Vandalismus | 20000 / 20000 | 0 | Erste SERP überwiegend Wartung/Verschleiß, zweite Vandalismus; kein belegter R2-Owner, nicht automatisch freigeben. |
| Trocknung kleiner Ladenflächen | 20000 / 20000 | 0 | Sonderthema Nachweis/Gewerbemietverhältnis vs allgemeine technische Bautrocknung; keine doppelte Trocknungsanleitung. |
| Löschmittel im Freizeitfahrzeug | 40101 / 20000 | — | Spezialphrase Befestigung/Vibration nicht gemessen; allgemeine Löschmittel-SERP reicht nicht. |
| Warnsysteme bei Starkregen | 20000 / 20000 | 0 | Warn-App/NINA vs baulicher Keller-/Schadenfolgen-Schutz; nur unterschiedlichen Prozessschritt besetzen. |
| Hausrat vor Hochwasser | 20000 / 20000 | 0 | Viele SERP-Titel behandeln allgemeine Gebäudeschutzmaßnahmen; R3 allein Hausrat/Dokumente, nicht Bauvorsorge. |
| Überspannung im Zählerschrank | 40101 / 20000 | — | R3-spezifische SERP nicht gemessen; keine Freigabe. |
| Datenleitungen & Überspannung | 20000 / 20000 | 0 | Beide SERPs Ethernet/PoE-Ableiter; trotz null URL-Overlap starke fachliche Schnittmenge, Owner offen. |
| Balkonkraftwerke bei Gewitter | 20000 / 20000 | 0 | Minisolaranlage vs allgemeine Photovoltaik; genaue Grenzen offen halten. |
| Antennen & Blitzschutz | 40101 / 20000 | — | SAT-/Koax-Primärfrage nicht gemessen, kein Owner-PASS. |
| Außenkabel & Blitzfolgen | 20000 / 20000 | 0 | Garagen-/Garten-Außenleitung vs allgemeiner Gebäudeblitzschutz; keine allgemeinen Kapitel duplizieren. |
| Dachboxen bei Unwetter | 20000 / 20000 | 2 (statt 3) | Zwei tatsächlich identische URLs. Die vom Plugin als drittes gezählte YouTube-/watch-Seite zeigt verschiedene v= Video-IDs. Allg. Sturmfahrhinweise nur R2; R3 Dachboxbefestigung. |
| Heizungsalarme über Mobilfunk | 20000 / 20000 | 0 | R3-GSM-SERP teils allgemeine Alarmtechnik; R2-Heizungsfernalarm-Vergleich viele themenfremde Treffer. Kein sicherer automatischer Owner. |
| Gewächshaus-Temperaturalarme | 20000 / 20000 | 0 | R3 teils Rollladenfrostalarm; R2-Vergleich zeigt eher Sensorik/Frostschutz als Sturm. R3 eng Temperaturmeldung. |

## Dokumentierter Fehler im Original-SERP-Overlap
In `includes/class-apkw-serp-r3.php` normalisiert `url_key()` derzeit ausschließlich Host und Pfad und entfernt **alle Queryparameter**. Dadurch erhalten verschiedene YouTube-Videos `/watch?v=...` denselben künstlichen Schlüssel `youtube.com/watch`. Im Dachbox-Paar: vom Plugin 3, echte identische URLs **2**. Derselbe Normalisierungsausdruck ist im alten `class-apkw-serp-review.php` vorhanden; dessen historische Paarzählungen sind daher ohne Stichproben-Korrektur nicht universell verlässlich. Das ist **kein Grund zur kostenpflichtigen Wiederholung**. Für dieses Konzept die korrigierten Evidenzzahlen nutzen. Derzeit **kein Pluginupdate** und keine Änderung des historischen R2-Codes.

## Abnahme und NEXT
- **9 Paare** haben 0 geteilte URLs; **1 Paar** hat nach Korrektur 2; **5 Paare** wegen Anbieterfehler unbestimmt. Kein automatischer SEO-PASS, keine Veröffentlichung aus diesen Zahlen.
- Alle 15 neuen Kandidaten fachlich auf genau einen Artikel-/Suchintent-Owner mit dem alten R2-Kategorienschema und den originalen 704 Artikeln abgrenzen. Besonders riskant: Spielgeräte (Wartung statt Vandalismus), Ethernet/PoE (gleichartige Produkte trotz null URL-Overlap), Heizungsalarme (ungenauer Vergleich), Dachboxen (zwei gemeinsame allgemeine Wind-Fahrt-URLs).
- Für die übrigen 129 R3-Kategorien gibt es hier keinen neuen SERP-Nachweis. 143er Keyword Overview und diese 30er SERPs nicht blind wiederholen; neue kostenpflichtige Recherche nur mit ausdrücklicher Kostenfreigabe.
- Vor Live-R3: SEO-Owner-Entscheidungen, 3–10-Validator-Negativtest, 19 Artikel-Umhängungen, alte IDs/URLs/Redirects und echten WordPress-Readback verifizieren.
