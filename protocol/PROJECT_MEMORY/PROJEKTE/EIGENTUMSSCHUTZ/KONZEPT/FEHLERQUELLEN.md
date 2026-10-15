## NACHHOLPRÜFUNG V9 – AKTUELLE FEHLERKETTE, 15.10.2026 (kein eigener Current)
**Einzig maßgeblicher STATUS und NEXT ACTION:** `KONZEPT/CURRENT_STATE.md`. **LIVE-R3/V8-Readback 546/546 PASS vom 13.10.2026.** Die unten historisch fortgeschriebenen Behauptungen „R3 nicht live“, „WP-Sync ausstehend“ und „maximal 10“ sind für den gegenwärtigen Fachauftrag **ÜBERHOLT**. Gültiger Zielvertrag: `ZIELVERTRAG_KATEGORIEN_MINDESTENS_3_OHNE_MAXIMUM_20261015.md`.

### HB-CONCEPT-V9-001 – Künstlich auf drei gestoppter Ausbau
- **Fehler:** 31/31 Bereiche besitzen exakt drei Unterbereiche, 87/93 Unterbereiche exakt drei Blätter, sechs je vier, obwohl allein fachliche Notwendigkeit die Zahl bestimmen sollte.
- **Belegte Ursache:** R2 hatte 19×1, 10×2, 2×3 Unterbereiche; R3/V7 ergänzte rechnerisch genau 48 Unterbereiche mit je drei Endblättern. Der so erreichte 3–10-Struktur-PASS beweist **keine fachliche Vollständigkeit**. Es ist keine Menü-Anzeige-Abschneidung belegt.
- **Korrektur:** Alter 3–10-Vertrag als HISTORISCH markiert; Zielvertrag V2 fordert mindestens 3, keine Obergrenze, pro CORE-Blatt ≥3 (vorzugsweise 5+) individuelle Artikelideen. 31/31 Bereiche und 93/93 Unterbereiche in V9-Daten erneut aufgenommen.
- **Test:** Original-V9-JSON mit 31 Bereichen, 93 Unterbereichen, 285 bestehenden Blättern; 546/546 V8-Readback laut Current und V9-Fachprotokoll. **Status: FACHREGEL KORRIGIERT / WP-V9-ERWEITERUNG BLOCKED.**

### HB-CONCEPT-V9-002 – Achtzehn nicht textgenau verfügbare R2-Originalideen
- **Fehler/Blocker:** Für vier am 12.10. ergänzte Kategorien fehlen **18 exakte alte Titel**: `core:leaf:exp:c140`, `core:leaf:exp:c216`, `core:leaf:exp:gartenhaus-feuchte-20261012`, `core:leaf:exp:gartentor-20261012`.
- **Ursache:** Im tatsächlich textgenau gelesenen alten Paket vom 10.10. nur 686 Ideen/137 Blätter; spätere R2-Stufe meldete 704/141, die 18 Titel sind aus den bisher zugänglichen Originaldateien nicht belegt. Sie **dürfen nicht rekonstruiert** werden.
- **Gate:** 686 R2 + 432 R3/V8 = 1.118 von 1.136 Originaltiteln lexikalisch prüfbar. **Status: OPEN / ERSTER OPERATIVER BLOCKER.**

### HB-CONCEPT-V9-003 – Fachliche Doppelungen / falsche Eltern
- **Fehler:** V9 enthielt 57 Kandidatenblätter und 239 Ideen, davon 3 Kandidatengruppen mit **9 Blättern/27 Ideen** wegen möglicher Dublette oder falscher Elternzuordnung zurückgestellt.
- **Gegenmaßnahme:** nicht still umbenennen/importieren; nur 48/57 Blätter mit 212 Ideen **weiter prüfen**, nicht freigeben. **Status: BLOCKED FÜR 9; WEITERE 48 IN REVIEW.**

### HB-CONCEPT-V9-004 – Fehlende SEO-Owner-Abnahme
- **Fehler:** 57 neue Blatttitel/239 neue Artikeltitel sind zwar textuell eindeutig; vollständige Alt-Themenabdeckung und eindeutige semantische SEO-Owner sind damit nicht bewiesen. Vier+ weitere auffällige lexikalische Nähen erfordern Prüfung.
- **Nachweis:** Current nennt lokale 57/57-Gegenprüfung und 6/6 Negativfälle mit absichtlich falschen Daten, darunter 2-Ideen-Blatt, doppelte Titel und unberechtigtes WP-Write. Die im Arbeitsverzeichnis separat vorhandenen V9-Entwurfsdateien enthalten 31/93/285 Bestandsregister und 57/239 Vorschläge. Die V9-Zweitprüfung ist nicht gleich WP-/SEO-Release-PASS.
- **Status: OWNER-FREIGABE OFFEN / RELEASE-GATE BLOCKED.** Keine kostenpflichtige SERP-Pflicht, keine automatischen neuen Provideraufrufe.

### HB-CONCEPT-V9-005 – Fehlerquelle/Routinghistorie veraltet
- **Fehler:** Ältere Teile dieser Fehlerakte, das zentrale Fehlerregister, der Konzept-Hobbyraum und die Projekt-Bürotür verwiesen noch auf R2/3–10 bzw. R3-live-offen.
- **Korrektur:** V9-Nachholvermerk hier; zentraler Fehler-Wegweiser und rein navigierende Projekt-/Hobbyraumtexte auf Current-Routing und Vertragsautorität korrigiert. Nicht die historisch dokumentierten Tests umetikettieren.
- **Status: NACHGEHOLT, Delta vom 15.10.2026.**

# EIGENTUMSSCHUTZ – KONZEPT – FEHLERQUELLEN

## HB-CONCEPT-001 – Ein-Kind-/Zwei-Kind-Klickebenen
Status: bestätigt in WordPress-R2-Konzept, **R3 nur strukturell gelöst; Live-Fix NICHT umgesetzt**.
Befund: 19 von 31 L2-Bereichen nur 1 L3, 10 nur 2; Nutzerregel 3–10 direkte Unterebenen. Nicht durch ein rein optisches Menü kaschieren.

## HB-CONCEPT-002 – SEO-Owner- und Artikel-Doppelungsrisiko
Status: **EDITORIAL-VORPRÜFUNG ERLEDIGT, SEO-SERP-FREIGABE OFFEN**. Für 144 R3-Kandidaten sind je drei konkrete Vorschläge (432) formuliert, exakt mit den 704 alten Titeln abgeglichen und 17 lexikalische Nähen fachlich vorsortiert. Die 21 früher offenen R2-Owner haben vorläufige redaktionelle Abgrenzungen; im aktuellen V8-Fachplan insgesamt 19 vorgeschlagene Themenumhängungen (keine Kopien), eine Keyword-Aliasregel. Trotz exakter Titeldeduplizierung sind semantisch getrennte Suchintents und organische SERP-Owner weiterhin nicht nachgewiesen. Autoritative Detailakten im KONZEPT-Büro: `R3_REDAKTION_144_KATEGORIEN_432_IDEEN_20261013.md` und `R3_BESTANDSOWNER_21_FACHPRUEFUNG_20261013.md`.

V5-Arbeitsfassung: `R3_V5_144_KATEGORIEN_432_IDEEN_EDITORIAL_FACHPLAN_20261013.md`. Trotz 14 redaktionellen Titelpräzisierungen und 0 exakten Wiederholungen **bleibt echte organische Suchintent-/Google-SERP-Überschneidung offen**. Quelle für verbindlichen Status und NEXT ACTION: `CURRENT_STATE.md`.


Aktuelle V6-Gegenprüfung vom 13.10.2026: 144 neue Kategorien mit 432 konkreten Artikeltiteln, 0 exakte Titelduplikate, 155 automatisch markierte lexikalische Paare (Schwelle 0,29), davon 3 ab Score 0,50. Koax-/Satellitenschutz war tatsächlich in Datenleitungen und Antennen doppelt vorgesehen, **in V6 auf nur Antennen-Owner korrigiert**. 14 konkrete fachliche Paargrenzen sowie alle 10 auffälligen neuen/bisherigen Kategoriebezeichnungs-Nähen wurden redaktionell eingeordnet. 19 Umhängungen: 9 Alt→Alt, 10 Alt→Neu, noch nicht ausgeführt. **V6 redaktionell verbessert, organische SEO-Kannibalisierungsfreiheit weiterhin NICHT NACHGEWIESEN.** Maßgeblich: `R3_V6_144_KATEGORIEN_432_IDEEN_OWNER_BEREINIGT_20261013.md`; nur `CURRENT_STATE.md` ist aktuelle Zustandsautorität.

## HB-CONCEPT-002a – Konkrete V7-Korrekturen wegen semantischer Wiederholung
Status: **IM V7-KONZEPT KORRIGIERT / SEO-SERP-FREIGABE NOCH OFFEN**.
- Neuen Blattkandidaten `Eiszapfen & Dachkanten` aufgrund der bestehenden Kategorie `Schnee & Eis am Grundstück` als zu nah erkannt und im Entwurf in `Glatteis an Garagenzufahrten` geändert; drei eigenständige Zufahrts-/Rampen-Artikelvorschläge.
- Fünf weitere Artikelintents eindeutiger abgegrenzt: Camper-Gasinstallation vs Gasprüfungen; Ladentrocknung vs allgemeines Verfahren; Wohnmobil-Löschmittel vs Fettbrand-Grundregel; Offline-Smart-Home-Automation vs bereits vorhandene Offline-Alarmtechnik (zwei Artikel).
- Alte 223 CORE-Objekte inklusive Elternzuordnung unverändert, alle 144 neuen Kandidaten weiterhin 3 Artikelentwürfe, Struktur 3–10 PASS, **keine Live-Umsetzung**.
- **WICHTIG:** redaktionelle Doppelungsvorsorge ist kein gemessener Google-SERP-/Keyword-Nachweis. Status/next action ausschließlich im `CURRENT_STATE.md`; Volltext in `R3_V7_144_KATEGORIEN_432_IDEEN_FACHPLAN_20261013.md`.

## HB-CONCEPT-002b – V8: reale Alt-Neu-Artikelüberschneidungen
Status: **REDAKTIONELLE PRÜFUNG FÜR DIESE FÄLLE ERLEDIGT / ORGANISCHE GOOGLE-SEO-FREIGABE UNERLEDIGT**.
- 432 neue konkrete Titelformulierungen gegen 704 R2-Originale mit **304.128** realen Textpaaren gegengeprüft, statt nur Kategorienamen. Fünf bisher zu allgemeine R3-Titel fachlich präzisiert (Camper-Feuerlöscher, Alarmquittierung, manuelles Markisen-Einfahren bei Sensorsignalfehler, Akku-Ladehalterung, Kunden-/Lieferfluchtwege).
- **17** verbliebene textähnliche Neu-Alt-Top-Paare bei Schwelle 0,48 sowie **zwei** textähnliche Neu-Neu-Paare einzeln im Konzeptbüro erörtert. Die **zwei besonders grenznahen fachlichen Owner** sind Heizungsalarm/Mobilfunkempfang ↔ Router-/Mobilfunk-Backup und Sumpfpumpen-Wartung ↔ USV-/Notstromwartung. Für alle bleibt echter organischer Google-SERP-Vergleich offen.
- Positiver Konzept-Regressionsstatus: 6/31/93/285, keine <3/>10-Zwischenstufen, 223/223 Original-Core-ID/Name/Eltern identisch, **704+432** Titel, keine exakt wiederholten Titel, **19 geplante** Umsortierungen nur als TRANSFER, nicht COPY, Quellkategorien jeweils >=3. **0 WP-Writes**.
- **Autoritativer Status:** `CURRENT_STATE.md` V8. **Vollständiger Plan:** `R3_V8_144_KATEGORIEN_432_IDEEN_FACHPLAN_20261013.md`. **Prüffälle:** `R3_V8_17_NEU_ALT_OWNER_PRUEFFELLE_20261013.md`. **Maschinen-QA:** `R3_V8_QA_20261013.json`. Die V7-Historie nicht zur Live- oder SEO-Freigabe heranziehen.

## HB-CONCEPT-002c – aktueller V8-Gesamtstatus
**STATUS: NICHT GELÖST FÜR GOOGLE-SEO-/WORDPRESS-RELEASE.** Der echte V8-Neu-vs-R2-Titelvergleich (432×704) führte zu fünf redaktionellen Titelkorrekturen; alle 17 deutlichsten Alt-Neu-Signale und zwei Neu-Neu-Signale wurden einzeln redaktionell eingeordnet. Zwei technische Überschneidungsfragen wurden mit Handbuch-/Fachquellen präzisiert. **Keine vollständige SERP-/Keyword-Freigabe** für 144 neue Kategorien.
Der aktuelle V8-Entwurf bestand eigene lokale **15/15 Negativtests**, nicht das unveränderte WordPress-Plugin. Quellen: `R3_V8_144_KATEGORIEN_432_IDEEN_FACHPLAN_20261013.md`, `R3_V8_QA_20261013.json`, `R3_V8_17_NEU_ALT_OWNER_PRUEFFELLE_20261013.md`, `R3_V8_2_TECHNISCHE_OWNER_GRENZEN_20261013.md`, `R3_V8_15_NEGATIVTESTS_20261013.json`. **Einzige Current-Autorität und NEXT ACTION: `CURRENT_STATE.md`.**

## HB-CONCEPT-003 – Beleggrenze für Live
Status: **OFFEN**. R3 weiterhin ausdrücklich nichtimportierbarer Konzeptentwurf, trotz Struktur- und Redaktionstiteltests. Keine neuen WordPress-Kategorien, keine neue veröffentlichte URL. R2 weiter maßgeblich für WordPress.

Sperre: Vor tatsächlichem Umbau erst vollständige fachliche Abnahme, Kollisionstest, Redirect-/URL-Prüfung und freigegebenes Zielprofil.

## HB-CONCEPT-004 – 3–10-Auswahlregel im Live-Validator fehlt noch
Status: **TECHNISCHE REGEL-LÜCKE BESTÄTIGT / NICHT MODIFIZIERT**. Prüfung der lokalen Original-ZIP `HAB_UND_BEWAHR_KATEGORIE_WORKFLOW_1.14.8.17_SERP_FORTSETZUNG_34V40.zip` vom 13.10.2026: `class-apkw-target-tree.php` validiert bereits das Minimum an Artikeltiteln je Blattkategorie und `min_categories_per_third_page` (3); `class-apkw-target-tree-dry-run.php` begrenzt `max_megamenu_children` auf 10 und fordert bei Welten bisher nur **mindestens 1** direktes Kind. **Ein allgemeiner harter Mindestwert 3 für jeden anklickbaren Zwischenknoten wird im geprüften Plugin noch nicht erzwungen.** Die R2-Struktur mit 19/10 Ein-/Zwei-Kind-Bereichen konnte daher gültig sein. Vor R3-Release muss die verbindliche 3–10-Strukturprüfung im bestehenden Validator nachvollziehbar ergänzt und mit Negativfällen getestet werden; keine Architekturänderung und kein vorgezogenes Pluginupdate nötig.


## HB-CONCEPT-006 – Organische Webbelege vor Fachbehauptung nicht belastbar geöffnet
Status: **QUELLENFEHLER KORRIGIERT; SEO-BLOCKER 002 WEITER OFFEN (13.10.2026)**.
- Zwei vormals angeführte DEHN-Unterseiten leiten auf die allgemeine Startseite und sind kein belastbarer, spezifischer Fachnachweis.
- Ein zuvor behaupteter Pumpen-USV-Beleg auf einer Merten-Seite ist für Pumpenanwendungen nicht bestätigt; diese Aussage wurde ausdrücklich zurückgezogen.
- Angeblicher neuer V8-Doppelartikel „Outdoor-Ethernet“ ist nach Lesen der drei tatsächlichen Außenkabel-V8-Titel **nicht vorhanden**. Allgemeine Keyword-/Leitungsüberschneidungen bleiben möglich und Google-SERP-UNBEKANNT.
- Einzelfall-Nachprüfung und 15 priorisierte, unterschiedlich starke Fachbelege im `R3_V8_PRIORITAET_15_QUELLENAUDIT_20261013.md`; beide vorherigen Stichproben am Dokumentanfang mit klaren Warnungen ergänzt.
- Gegenprobe: weiterhin 144/144 gelistete Kategorien, 432/432 V8-Ideen, keine SERP-/Suchvolumen-Freigabe; keine Änderungen am R2-WordPress oder Plugin.

## HB-CONCEPT-005 – Übergaberouting und Zielvertragsablage lückenhaft
Status: **LOCAL CLOSED – 2026-10-13; FRISCHE-READBACK BESTÄTIGT**.
- Fehler 1: Die Eigentumsschutz-Bürotür enthielt den veralteten Satz, eine Konzept-Current sei nicht unabhängig verifiziert. Das widersprach dem vorhandenen `AUTORITAETSPLAN.json` mit dem eindeutigen `EIGENTUMSSCHUTZ_KONZEPT`-Routing und der real existierenden `KONZEPT/CURRENT_STATE.md`.
- Fehler 2: Der `KONZEPT/HOBBYRAUM.md` referenzierte als Arbeitsbindungsquelle noch einen alten R3-Delta-Pfad, obwohl die Current inzwischen einen V8-Fachplan bindet.
- Fehler 3: Das zentrale Zielvertragsregister enthielt bisher keinen eigenen Hab-und-Bewahr-Kategorienzielvertrag, obwohl die neue 3–10-Nutzerentscheidung im Current bindend war.
- Korrektur: Tür auf die vorhandene Current geroutet, Hobbyraum auf ausschließlich aus Current abgeleitete Daten umgestellt, `ZIELVERTRAG_KATEGORIEN_3_BIS_10_20261013.md` angelegt und in `ZIELVERTRAEGE/REGISTER.md` registriert. WAS/WARUM im `AENDERUNGSREGISTER.md`, Türänderung im `BAUCONTAINER/BAUPROTOKOLL.md`.
- Testbedingung: Frischer Readback von Tür, Routing, Current, Hobbyraum und Zielvertrag; **genau eine Current und genau eine NEXT ACTION**. Keine WordPress-/Pluginänderung.


## NACHHOLPRÜFUNG 13.10.2026 – LIVE PREFLIGHT PASS, ÄLTERE FEHLERSTATUS GELTEN NUR HISTORISCH
Quelle und Statusautorität: `KONZEPT/CURRENT_STATE.md`, dortiger Abschnitt `LIVE-R3/V8-PREFLIGHT PASS – Nutzer-Rückmeldung 13.10.2026`. **Dies ist ausschließlich das Fehler-/Korrekturdokument, KEINE zweite Current-Quelle und KEINE eigene NEXT ACTION.**

- **HB-CONCEPT-001 (Ein-/Zwei-Kind-Zwischenebenen):** Frühere R2-Strukturschwäche im R3/V8-Zielbaum behoben; nach gemeldetem **echten WordPress-Preflight PASS** enthält das finale **geprüfte** Profil 6 Welten, 31 Bereiche, 93 Unterbereiche, 285 Kategorien und 1.136 Artikelideen. **Status: LOCAL CLOSED / LIVE PREFLIGHT PASS / LIVE-SYNC OFFEN.** Dies bedeutet noch nicht, dass der Baum WordPress-live geschrieben wurde.
- **HB-CONCEPT-002, 002a–c (SEO-/Owner-Dubletten):** Alle 19 vorgesehenen Artikelideen-Transfers sind vom echten WordPress-Preflight als **exakt einmal verschoben** geprüft, bestehende R2-Knoten, Live-IDs, Slugs und Eltern geprüft. **Status: REDAKTIONELLE SCOPE-GRENZEN VORLIEGEND / ORGANISCHE SEO-GESAMTMESSUNG OPTIONAL, NICHT BLOCKIEREND.** Explizite Nutzerentscheidung: fachlich sinnvolle Kategorien brauchen keine Google-Treffer, kein gemessenes Suchvolumen und keine 144/144-SERP-Prüfung. Historische Formulierungen `SEO-BLOCKER` und `SERP-Pflicht vor R3-Import` sind **überholt und NICHT als aktive Release-Sperre zu verwenden**.
- **HB-CONCEPT-003 (R3 nicht live bereitgestellt):** Nach gemeldetem WordPress-Preflight **PASS**, aber Meldung sagt ausdrücklich **0 WordPress-Daten geschrieben**. Das geprüfte R3-Profil wurde noch nicht als bereitgestellt bestätigt; Live-Sync/Readback noch offen. **Status: LIVE OFFEN**, keine zusätzliche SEO-Sperre.
- **HB-CONCEPT-004 (3–10-Validator in altem Plugin fehlte):** Ursprüngliche Quellbeobachtung bezog sich auf Plugin `1.14.8.17`; neuere gebaute Hab-&-Bewahr-Version `1.14.8.19` hat nach lokalem Arbeitsnachweis 28/28 Sicherheits-/Negativtests bestanden; WordPress-Preflight wurde vom Nutzer mit Struktur-PASS gemeldet. **Status: HISTORISCHER CODEFEHLER / LOKAL CLOSED / LIVE PREFLIGHT PASS.** Installierte Live-Versionsnummer und schreibender WordPress-Sync sind durch die PASS-Nachricht allein **nicht** unabhängig nachgewiesen.
- **URL-/Live-Schutz:** Die PASS-Rückmeldung bestätigt Prüfen der bestehenden IDs, Slugs, Eltern und R2-Knoten. **Noch nicht nachgewiesen**: schreibende Live-Umsetzung, vollständiger Post-Sync-Readback, Redirect-Verhalten im Frontend und ein möglicher Live-Rollback. **Status: LIVE OFFEN**, nicht mit bereits bestandenem Preflight verwechseln.

**Befundgrenze:** Das PASS-Zitat stammt aus der WordPress-Oberfläche, vom Nutzer in den Chat übertragen. Es ist echte Nutzer-Rückmeldung über einen durchgelaufenen Preflight, jedoch kein hier separat per WordPress-API erhobener Post-Sync-Datensatz. Fehlende spätere Stufen nicht als FAIL raten.
