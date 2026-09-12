# AFFILIATE – WAS/WARUM – ADCELL

STAND: 2026-09-12
ROLLE: DAUERHAFTER ENTSCHEIDUNGSBELEG; KEINE CURRENT-/LIVE-WAHRHEIT

## WAS – FACHLICHES ZIEL

ADCELL wird in der bestehenden Affiliate-Zentrale vollautomatisch über den belegten API-v2-Weg betrieben:

`accepted + active Programme -> explizite programId-Allowlist -> CSV/Banner/Deeplink -> bestehende zentrale Creative-/Relevanz-/Asset-/Output-/Pause-/Veto-Logik`

Verbindlich:
- kein Awin-Fallthrough für ADCELL;
- keine manuell konfigurierte CSV-URL als Normalbetrieb;
- nur explizit freigegebene `programId` und zugleich aktuell `accepted` + aktiv;
- alle Gegenfälle fail-closed;
- keine zweite Providerarchitektur und kein separates ADCELL-Plugin.

OTTO/Awin bleibt pausiert/unaufgelöst; Digistore24 zurückgestellt.

## WARUM

Der Affiliate-Betrieb soll ohne wiederkehrenden Handimport arbeiten. Die offizielle ADCELL-API-v2-Dokumentation belegt Programme sowie CSV-, Banner- und Deeplink-Wege. Gleichzeitig dürfen ältere/fachfremde akzeptierte Partnerschaften nicht allein wegen `accepted` ins Pferdeportal gelangen; deshalb ist die explizite `programId`-Allowlist Pflicht.

## VERBINDLICHE INTEGRATIONSLINIE

Die frühere Richtung `6.72.8 -> 6.72.9` ist historisch überholt.

Vor der finalen Versionswahl wurde das PLUGINS-/Pluginbüro frisch geprüft. Dort lag bereits die vollständig geprüfte Affiliate-Zentrale-Linie bis **6.72.17**. Deshalb wurde der getestete ADCELL-v2-Fix konfliktfrei auf **6.72.17** integriert und als **6.72.19** kanonisch gebunden.

WARUM:
Eine ältere Kandidatenlinie hätte neuere, bereits geprüfte Pluginänderungen überschrieben oder zurückgesetzt. Seit AF-064 gilt deshalb dauerhaft: **Vor jeder neuen Affiliate-Kandidatenversion zuerst den jüngsten vollständig geprüften Pluginbüro-Stand bestimmen; Fachänderungen auf diesen Stand integrieren und beide Seiten regressieren.**

## ARTEFAKTREGEL

Ein installierbares Plugin darf ausschließlich **aus der aktuell kanonischen Source** gebaut werden und muss unmittelbar vor Übergabe vollständig gegen deren Manifest geprüft werden.

AF-067 zeigte den Grund: Ein lokal vor der finalen Bindung gebautes 6.72.19-ZIP wich in einer Datei von der kanonischen Source ab und wurde deshalb gesperrt.

Der anschließende Neubau direkt aus `affiliate-release-current` bestand:
- Run `34692865477`, Job `103551115066`;
- Source/Manifest 26/26;
- PHP 21/21;
- Fresh-Unpack 26/26;
- Version 6.72.19;
- Test-ZIP SHA-256 `72f437e5235aaec53631db052e2184b588366c7f8aa7eb72ae1c9e043cdf157f`.

Dauerregel: **Kein altes/pre-bind ZIP durch Dateinamen oder Version als aktuell behandeln. Kanonische Source -> Neubau -> Byte-Identität -> erst dann Übergabe.**

## LIVE-PREFLIGHT-REGEL

Der fehlende ADCELL-Weblogin bzw. eine nicht eintreffende Passwort-Reset-Mail ist **nicht automatisch Beweis**, dass die API nicht nutzbar ist.

Die kanonische 6.72.19 besitzt den read-only Test **`Token + Programme prüfen`**, der die bereits in WordPress gespeicherten API-Zugangsdaten verwendet.

Seit AF-066 gilt deshalb:
1. zuerst diesen read-only API-Preflight im echten WordPress ausführen;
2. bei PASS vorhandenen `accepted` + aktiven `programId` explizit allowlisten und E2E fortsetzen;
3. nur wenn gespeicherte API-Credentials fehlen/ungültig sind, wird Credential-Recovery zum echten Blocker.

WARUM:
Weblogin und API-Credentials sind unterschiedliche technische Nachweise. Ein nicht funktionierender Weblogin darf einen möglicherweise bereits funktionsfähigen API-Weg nicht unnötig blockieren.

## TEST-/ABNAHMEREGEL

Technisch/kanonisch belegt PASS für 6.72.19:
- ADCELL Static + Runtime Positiv/Negativ;
- Allowlist/Gegenfälle;
- kein Awin-Fallthrough;
- Awin/OTTO 18/18;
- Banner Positiv/Negativ;
- PHP 21/21;
- Release-Guard Governance/Source/Tree/Start;
- Fresh-Unpack + Source/ZIP-Identity 26/26;
- kanonischer Artefaktneubau 26/26.

Kein LIVE-PASS ohne:
- echten read-only ADCELL-API-Preflight im realen WordPress;
- danach realen ADCELL-/WordPress-/MariaDB-E2E.

## AKTUELLE AUTORITÄTEN

Dynamischer Stand und NEXT ACTION werden **nicht** hier gepflegt:
- Campus: `CURRENT_STATE.md` + `HOBBYRAUM.md`;
- technische Fehler: `AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md` auf `affiliate-release-current`;
- technischer Scope: `protocol/AFFILIATE_RELEASE_ADCELL_AUTOMATION_SCOPE_20260911.md`;
- Ziel: `ZV-AFFILIATE-ADCELL-001`;
- Plugin-Kontrollvorgang: `PU-20260912-001`.

Kein Codex. Kein Side-Branch als Release-Autorität. Keine zweite aktuelle Wahrheit.
