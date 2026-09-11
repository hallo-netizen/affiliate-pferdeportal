# AFFILIATE – CURRENT STATE

STAND: 2026-09-11
STATUS: ADCELL API-V2-AUTOMATISIERUNG AKTUELL / SOURCE-FIX OFFEN / LIVE-AUTH BLOCKED

## AUTORITÄT

Diese Datei ist die einzige aktuelle Campus-Standzusammenfassung des Büros AFFILIATE.

- aktuelle Arbeit / NEXT ACTION → `HOBBYRAUM.md`
- Fehler → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → Originalquelle
- Zielvertrag → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`
- Warum/Änderungen → `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- technische Release-Autorität → Branch `affiliate-release-current` → `control/release-governance/CURRENT_RELEASE.json`
- kanonische Source → `release/affiliate-zentrale/current/affiliate-portal-router/`

## AKTUELLER AUFTRAG

Explizite Nutzerentscheidung 11.09.2026:

**ADCELL vollautomatisch über API v2 integrieren. Kein manueller Import/Export als Normalbetrieb. Vor Pluginabnahme harte lokale Positiv-/Negativ-/Gesamtworkflow-Prüfung.**

Digistore24 bleibt nicht erledigt, BLOCKED und zurückgestellt. Detailwahrheit ausschließlich `DIGISTORE24_STATUS.md`.

OTTO/Awin ist nicht erledigt; die bisherige FeedScope-Aufgabe ist durch den aktuellen ADCELL-Auftrag pausiert, nicht als PASS/abgelöst erklärt.

## ADCELL – HART BELEGT

WordPress-Liveoberfläche:
- ADCELL-Zugangsdaten sind gespeichert;
- die ADCELL-Fachseite besitzt Produktdaten, Synchronisierung und einen Button `ADCELL-Automatisierung öffnen`;
- im bisherigen Betriebsprofil existiert noch `ADCELL-CSV-Export-URL (optional)`.

Vom Nutzer in ADCELL API v2 geöffnet/belegt:
- `Affiliate -> Program -> export`;
- `Affiliate -> Promotion -> getPromotionTypeCsv`;
- `Affiliate -> Promotion -> getPromotionTypeBanner`;
- `Affiliate -> Promotion -> getPromotionTypeDeeplink`.

Zielweg:
`accepted + active Programme -> explizite programId-Allowlist -> CSV/Banner/Deeplink automatisch -> bestehende zentrale Relevanz-/Creative-/Output-/Veto-Logik`.

Alte/fachfremde akzeptierte ADCELL-Partnerschaften dürfen ohne explizite `programId`-Freigabe nicht eingelesen werden.

## AKTUELL ENTDECKTE FEHLER

Keine zweite Fehlerliste hier. Detailautorität:
Branch `affiliate-release-current` → `AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md`.

Dort sind für den aktuellen ADCELL-Weg neu gebunden:
- AF-058 Provider-Routing/Fallthrough zu Awin;
- AF-059 manueller CSV-URL-Weg statt API-v2-Normalbetrieb;
- AF-060 unbestätigte/geratene API-Authentifizierung im verworfenen Scratch.

## TECHNISCHER SICHERER STAND

Kanonischer technischer Basisstand vor ADCELL-Sourceänderung:
- Branch `affiliate-release-current`;
- Kandidat `6.72.8`;
- Source-Manifest SHA-256 `816f49dc5178e32ead1ea7fd53f0962acb3f457b08a0139f6b9ff1f9239a0a8d`;
- 26 Source-Dateien;
- Release NICHT freigegeben.

Bei Abschlussprüfung lag `affiliate-release-current` auf Head `cb563f914690cea473db6e02177544f61bd0f2d8` vor den reinen Protokoll-/Task-Nachträgen dieses Abschlussblocks.

Ein Side-Branch `hobbyroom/adcell-api-v2-automation-20260911` wurde frisch geprüft und war byte-/commitseitig identisch zum damaligen Release-Head: 0 ahead / 0 behind. Er enthält daher keinen ADCELL-Fix und ist keine zweite technische Standwahrheit.

## VERWORFENER LOKALER SCRATCH

Ein lokaler Scratch `6.72.18` ist ausdrücklich KEIN Kandidat:
- er basierte auf der nicht abgenommenen 6.72.17-Testlinie statt kanonisch auf 6.72.8;
- sein Test nahm Query-`token` an, während die Scratch-Implementierung Basic Auth verwendete;
- der tatsächliche ADCELL-API-v2-Authentifizierungsvertrag war dafür nicht autoritativ belegt.

Der Scratch wird nicht übernommen und nicht als PASS/Release/Plugin ausgegeben.

## TESTSTAND DIESES ADCELL-CHATS

Tatsächlich lokal am verworfenen Scratch ausgeführt:
- PHP-Lint: 22 PHP-Dateien, 0 Syntaxfehler;
- isolierter ADCELL-Adapter-Prototyptest: 18/18 PASS;
- bestehender Pferde-Atelier-Klassifikator: positives Regendecken-Beispiel klassifiziert; Tarot/Kartenlegen blockiert; Spielzeugpferd blockiert.

Diese Ergebnisse sind **kein Plugin-PASS**, weil Basis und Authentifizierungsannahme nicht kanonisch waren.

Noch NICHT ausgeführt:
- kanonischer ADCELL-Source-Fix aus 6.72.8;
- kanonischer Positiv-/Negativ-Runtime-Test;
- vollständige Awin/OTTO-/Pause-/Veto-Regression nach ADCELL-Fix;
- Fresh-Unpack + Source/ZIP-Byte-Identity eines ADCELL-Kandidaten;
- echter ADCELL-API-Live-Request;
- WordPress/MariaDB-ADCELL-End-to-End;
- reale Ausgabe von ADCELL-Produkten/Bannern/Deeplinks.

## LIVE-BLOCKER

Der Nutzer kann sich aktuell nicht in sein ADCELL-Konto/API-Dokumentation einloggen. Das versehentlich überschriebene Passwort ist nicht verfügbar; der Passwort-Zurücksetzen-Mailweg funktioniert aktuell nicht.

Dadurch ist die Live-Authentifizierung BLOCKED. Der technische Authentifizierungsvertrag darf nicht geraten werden.

## NEXT ACTION

Exakt aus `HOBBYRAUM.md` arbeiten:
1. exakten ADCELL-API-v2-Authentifizierungsvertrag autoritativ belegen;
2. erst danach aus kanonischem 6.72.8 den kleinsten Provider-Routing-/API-v2-Fix bauen;
3. harte Positiv-/Negativ-/Gesamtworkflow-/Fresh-Unpack-/Identity-Prüfung;
4. erst danach Test-Plugin; Live-PASS erst nach wiederhergestelltem ADCELL-Zugang.
