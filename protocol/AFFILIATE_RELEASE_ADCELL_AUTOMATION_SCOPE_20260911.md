# AFFILIATE RELEASE – ADCELL API-V2 AUTOMATISIERUNG – SCOPE 2026-09-11

STAND: 2026-09-11
STATUS: AKTIV / LIVE-AUTH BLOCKED / KANONISCHER SOURCE-FIX NOCH NICHT AUSGEFÜHRT

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
- Branch-Head bei Abschlussprüfung: `cb563f914690cea473db6e02177544f61bd0f2d8`
- Source-Manifest SHA-256: `816f49dc5178e32ead1ea7fd53f0962acb3f457b08a0139f6b9ff1f9239a0a8d`

Release-scoped Änderungen dürfen gemäß Release-Governance nicht über einen parallelen Side-Branch zur zweiten Standwahrheit werden.

## LIVE / DOKUMENTATION HART BELEGT

Aus den vom Nutzer geöffneten ADCELL-API-v2-Seiten sind folgende read-only/Promotion-Wege belegt:

Programme:
- `Affiliate -> Program -> export`
- angenommene Programme können über `affiliateStatus=accepted` gefiltert werden;
- Ergebnis enthält u. a. `programId`, `programName`, `isActive`, `affiliateStatus`.

Werbemittel:
- `Affiliate -> Promotion -> getPromotionTypeCsv`
- `Affiliate -> Promotion -> getPromotionTypeBanner`
- `Affiliate -> Promotion -> getPromotionTypeDeeplink`

Belegt ist außerdem:
- CSV-Werbemittel liefern eine `csvUrl`;
- Banner liefern programmspezifische IDs/Status, Ziel-/Trackingdaten, Maße und `bannerUrl`;
- Deeplinks sind programmspezifisch.

Nicht belegt ist derzeit der exakte technische Authentifizierungsvertrag für API-v2-Requests außerhalb der eingeloggten Dokumentationsoberfläche. Kein Query-Token-, Basic-Auth- oder anderer Auth-Weg darf geraten werden.

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

Dort nachgetragen:
- ADCELL-Automatisierungsbutton fällt in den vorhandenen Awin-orientierten Automationspfad;
- ADCELL-Automation ist im kanonischen Stand noch an eine manuell konfigurierte CSV-Export-URL gebunden statt an den bestätigten API-v2-Weg.

## LIVE-BLOCKER

Der Nutzer kann sich aktuell nicht in sein ADCELL-Konto/API-Dokumentation einloggen; das versehentlich überschriebene Passwort ist nicht verfügbar und der Passwort-Zurücksetzen-Mailweg funktioniert aktuell nicht.

Folge:
- kein echter ADCELL-Live-API-Request möglich;
- kein Live-PASS behaupten;
- lokale Entwicklung darf den Authentifizierungsvertrag nicht erfinden.

NEXT ACTION vor Source-Fix:
**exakten ADCELL-API-v2-Authentifizierungsvertrag aus autoritativer ADCELL-Dokumentation belegen.**

## VERWORFENER SCRATCH-STAND

Ein lokaler, nicht kanonischer Scratch-Prototyp mit Versionslinie `6.72.18` wurde geprüft, aber ausdrücklich NICHT übernommen:
- falsche Basis: aus der nicht abgenommenen 6.72.17-Testlinie statt aus kanonischem 6.72.8;
- Authentifizierungsannahmen widersprachen sich zwischen Prototyp-Test und Implementierung;
- daher kein Kandidat, kein Plugin-PASS, keine Release-Quelle.

Aus dem Scratch dürfen nur Konzepte erneut aus der kanonischen 6.72.8-Basis entwickelt werden; keine Dateiübernahme ohne Neuprüfung.

## TESTVERTRAG VOR JEGLICHER PLUGINABNAHME

Pflicht auf kanonischer Basis:
- PHP-Syntax aller betroffenen Dateien;
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
- keine API-Authentifizierung raten.
