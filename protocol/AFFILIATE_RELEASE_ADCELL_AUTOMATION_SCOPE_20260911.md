# AFFILIATE RELEASE – ADCELL API-V2 AUTOMATISIERUNG – SCOPE 2026-09-11

STAND: 2026-09-11
STATUS: AKTIV / AUTH-VERTRAG BELEGT / LIVE-ZUGANG BLOCKED / KANONISCHER SOURCE-FIX OFFEN

## AUSLÖSER

Explizite Nutzerentscheidung am 11.09.2026:
- Digistore24 bleibt nicht erledigt und zurückgestellt;
- aktuelle Arbeit wechselt zu ADCELL;
- ADCELL soll im Normalbetrieb vollautomatisch eingelesen werden;
- kein manueller Import/Export als Betriebsweg;
- vor jeder Pluginabnahme harte lokale Positiv-/Negativprüfung gegen den Gesamtworkflow.

OTTO/Awin bleibt fachlich ungelöst/pausiert und wird durch diesen Auftrag weder als erfüllt noch als abgelöst erklärt.

## KANONISCHE BASIS

Technische Release-Autorität:
- Branch `affiliate-release-current`
- Source `release/affiliate-zentrale/current/affiliate-portal-router/`
- Kandidat vor ADCELL-Änderung: `6.72.8`
- Source-Manifest SHA-256: `816f49dc5178e32ead1ea7fd53f0962acb3f457b08a0139f6b9ff1f9239a0a8d`

Release-scoped Änderungen dürfen gemäß Release-Governance nicht über einen parallelen Side-Branch zur zweiten Standwahrheit werden.

## LIVE / DOKUMENTATION HART BELEGT

Autoritativer Auth-Beleg:
`release/affiliate-zentrale/evidence/adcell_api_v2_auth_contract_20260911.txt`

Aus der offiziellen, vom Nutzer am 11.09.2026 geöffneten ADCELL-API-v2-Dokumentation ist jetzt technisch belegt:
- API-Basis: `https://api.adcell.org/api/v2/`;
- Token-Verfahren;
- Token-Erzeugung über `/user/getToken` mit `userName` und `password`;
- dokumentierte Standardgültigkeit des Tokens: 15 Minuten;
- jeder weitere API-v2-Request benötigt den Parameter `token`;
- kein Basic-Auth- oder Bearer-Auth-Vertrag für diesen belegten API-v2-Weg.

Programme:
- GET `https://api.adcell.org/api/v2/affiliate/program/export`;
- angenommene Programme können über `affiliateStatus=accepted` gefiltert werden;
- Ergebnis enthält u. a. `programId`, `programName`, `isActive`, `affiliateStatus`.

Werbemittel:
- GET `https://api.adcell.org/api/v2/affiliate/promotion/getPromotionTypeCsv`;
- GET `https://api.adcell.org/api/v2/affiliate/promotion/getPromotionTypeBanner`;
- GET `https://api.adcell.org/api/v2/affiliate/promotion/getPromotionTypeDeeplink`.

Belegt ist außerdem:
- CSV-Werbemittel liefern eine `csvUrl`;
- Banner liefern programmspezifische IDs/Status, Ziel-/Trackingdaten, Maße und `bannerUrl`;
- Deeplinks sind programmspezifisch und besitzen eine eigene `promotionId`.

Damit ist der frühere Auth-Beleg-Blocker geschlossen. Der 6.72.18-Scratch bleibt trotzdem verworfen und wird nicht übernommen.

## VERBINDLICHER ZIELWEG

Normalbetrieb:

`ADCELL API v2 -> accepted + active Programme -> interne explizite programId-Allowlist -> CSV/Banner/Deeplink API -> bestehende zentrale Creative-/Output-/Veto-/Relevanzlogik`

Pflichtregeln:
1. Provider-spezifische ADCELL-Automatisierung; kein Fallthrough in den Awin-Adapter.
2. Allowlist ausschließlich über explizit freigegebene ADCELL-`programId`s; Namen sind keine Freigabeautorität.
3. Fail closed: nicht freigegebene, inaktive oder nicht mehr `accepted` Programme werden nicht importiert/materialisiert.
4. Alte angenommene, fachfremde Programme bleiben dadurch intern gesperrt, auch wenn sie im ADCELL-Konto weiter vorhanden sind.
5. `getPromotionTypeCsv`: Feed-URL automatisch aus API beziehen; keine manuell eingetragene ADCELL-CSV-Export-URL als Normalbetrieb.
6. `getPromotionTypeBanner`: reale Banner automatisiert beziehen; Maße/Quelle/Tracking weiter durch bestehende Prüfungen.
7. `getPromotionTypeDeeplink`: programmspezifische Deeplink-Erzeugung/Übernahme nur aus dokumentiertem API-Weg.
8. Keine automatische Veröffentlichung ohne bestehende zentrale Relevanz-, Creative-, Output- und Veto-Prüfungen.
9. Provider-Pause/Veto bleibt zentrale Laufzeitsperre und darf durch ADCELL nicht umgangen werden.

## AKTUELL ENTDECKTE FEHLER

Detailautorität bleibt ausschließlich:
`AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md`

Dort gebunden:
- AF-058: ADCELL-Automatisierungsbutton fällt in den vorhandenen Awin-orientierten Automationspfad;
- AF-059: ADCELL-Automation ist im kanonischen Stand noch an eine manuell konfigurierte CSV-Export-URL gebunden statt an den bestätigten API-v2-Weg;
- AF-060: historische falsche Auth-Annahme; durch den oben gebundenen offiziellen Auth-Beleg fachlich geschlossen, darf aber als Gegenregel nicht entfernt werden.

## LIVE-BLOCKER

Der Nutzer kann sich aktuell nicht wieder in sein ADCELL-Konto einloggen; das versehentlich überschriebene Passwort ist nicht verfügbar und der Passwort-Zurücksetzen-Mailweg funktioniert aktuell nicht.

Folge:
- kein echter ADCELL-Live-API-Request möglich;
- kein Live-PASS behaupten;
- lokaler/kanonischer Source-Fix und harte Tests dürfen jetzt auf dem belegten Auth-Vertrag aufgebaut werden;
- Live-Abnahme bleibt bis zur Wiederherstellung des Zugangs gesperrt.

## NEXT ACTION

**GENAU EIN ARBEITSSTRANG:**
Aus der kanonischen Basis `6.72.8` den kleinsten ADCELL-Provider-Routing-/API-v2-Fix bauen und danach den gebundenen Positiv-/Negativ-/Gesamtworkflow ausführen.

## VERWORFENER SCRATCH-STAND

Ein lokaler, nicht kanonischer Scratch-Prototyp mit Versionslinie `6.72.18` wurde geprüft, aber ausdrücklich NICHT übernommen:
- falsche Basis: aus der nicht abgenommenen 6.72.17-Testlinie statt aus kanonischem 6.72.8;
- Authentifizierungsannahmen widersprachen sich zwischen Prototyp-Test und Implementierung;
- daher kein Kandidat, kein Plugin-PASS, keine Release-Quelle.

Aus dem Scratch dürfen nur Konzepte erneut aus der kanonischen 6.72.8-Basis entwickelt werden; keine Dateiübernahme ohne Neuprüfung.

## TESTVERTRAG VOR JEGLICHER PLUGINABNAHME

Pflicht auf kanonischer Basis:
- PHP-Syntax aller betroffenen Dateien;
- POSITIV: Token wird ausschließlich über den belegten `user/getToken`-Weg erzeugt und als Parameter `token` weitergereicht;
- NEGATIV: kein Basic-/Bearer-Fallback und kein Request an einen unbelegten API-v2-Host;
- POSITIV: ADCELL-Route bleibt ADCELL; accepted+active+allowlisted Programm wird verarbeitet;
- NEGATIV: ADCELL zeigt/benutzt keine Awin-Partnerlogik;
- NEGATIV: altes/fachfremdes accepted Programm ohne Allowlist wird blockiert;
- NEGATIV: pending/inactive/nicht accepted wird blockiert;
- NEGATIV: leere Allowlist blockiert vollständig;
- NEGATIV: falsche API-/Feed-Hosts, malformed response, uneindeutige Feedlage blockieren;
- Regression: Awin/OTTO, Provider-Pause/Veto, Creative-/Output-Sicherheitsregeln unverändert;
- Full bound workflow;
- Fresh-Unpack;
- Source/ZIP byte identity;
- erst danach Test-ZIP.

Live-PASS zusätzlich erst nach wiederhergestelltem ADCELL-Zugang und echtem WordPress/MariaDB-End-to-End-Lauf.

## NICHT ANFASSEN

- Digistore24-Blocker nicht nebenbei reparieren;
- OTTO/Awin-FeedScope-Aufgabe nicht parallel fortsetzen;
- keine neue Providerarchitektur oder separates ADCELL-Plugin;
- keine Pluginversionskette vor vollständigem kanonischem Test;
- keine manuelle CSV-Import/Export-Lösung als Ersatz für die geforderte Automatik;
- keine vom offiziellen v2-Beleg abweichende API-Authentifizierung.
