# eBay QA24 – belegter Frühabbruch im bestehenden GitHub-Taktgeber, kein WordPress-Plugin-Fix

**11.11.2026. Installierter aktueller Stand laut Nutzer: 6.72.329.** Diese Version blieb unverändert. Kein neues ZIP gebaut.

## Echter, bisher übersehener gemeinsamer Fehler

GitHub Actions Job **130555151217** (Run **43030248519**) protokolliert um **2026-11-11 14:02:40 UTC**: `heartbeat 25 status=idle`, unmittelbar danach `terminal heartbeat status=idle; no successor runner required`. Der bestehende GitHub-Runner hat damit aufgehört, Folgeaufrufe zu schicken. Der unveränderte Plugin-PHP-Code `handle_ebay_external_tick` liefert bei einem unabhängigen Verfügbarkeits-Arbeitspaket **`status=idle; reason=availability_tick; run_status=running`**, obwohl der Produktlauf weiterläuft. Der Nutzerexport meldet **`availability_saved` am 1794405753 (14:02:33 UTC)** bei `status=running` und `phase=refresh_remote`; die spätere manuelle Pause folgte erst um `1794405827`. Der Runner hat somit **einen noch aktiven Lauf vorzeitig für beendet gehalten**. Das ist hier der erstmals **an echten WordPress- und GitHub-Daten gemeinsam nachgewiesene Steuerungsfehler**.

Andere bereits erledigte Fachänderungen QA9–QA23 sind nicht Gegenstand eines neuen Fixes.

## Lokale A–Z-Steuerungstests, ehrlich abgegrenzt

Unveränderte 6.72.329-ZIP SHA256 `97df9edc9b883194ff9666ad285b3f090db6e1889090fd25f1e22440a701b2db`. Originaler PHP-Koordinator für alle **13 Phasen**, signierten Folgeaufruf, Sperre gegen Doppelarbeit, Speicherstand, vollständige Endphase, Ausgabe-Checkpoint und Protokoll benutzt. WordPress-Funktionen/Provider/Phasendetails und 365 Produkt-IDs sind **synthetisch simuliert**: **26/26** Kontrollen PASS; separat **15 externe Takte** bei verloren gegangenen internen Aufrufen bis Ende ohne Verlust der simulierten Freigaben. Der echte PHP-Heartbeat-Response `idle/availability_tick/running` wurde erzeugt und gegen die GitHub-Entscheidung mit **13/13** Positiv- und Negativfällen geprüft. Kein MariaDB-/eBay-API-/Live-Frontend-Gesamtnachweis.

Persistente Testdateien im persönlichen Pluginbüro `/pferdeatelier/PLUGINS/QA/` als `EBAY_QA24_*` inklusive Original-PHP-Test und Gegenproben.

## Eine vorhandene Steuerung korrigiert – derzeit durch Hardlock blockiert

**GitHub-PR #756:** https://github.com/hallo-netizen/affiliate-pferdeportal/pull/756. GitHub-Commit `2d49eb7dcccf51c95efbb8f89249e5b6df728a35`. **Einzige Änderung an der bereits bestehenden Datei** `.github/workflows/pferde-atelier-ebay-heartbeat.yml`: Bei `status=idle + reason=availability_tick + run_status=running|paused` darf der vorhandene Taktgeber nicht aussteigen, sondern interpretiert intern `active_idle`. Bei echtem Leerlauf, manueller Pause, Fehler, Abschluss und Deaktivierung stoppt er weiterhin. Bestehende 15-Minuten-Planung, limitierte 30 Arbeitspakete, 60-Sekunden-Pausen, Konfliktschutz, Timeout und Folgejob bleiben unangetastet. **Keine WP-Plugin-Datei verändert.**

PR-CI: **Pferde Atelier eBay heartbeat / contract – 16/16 PASS**; **Pferde Atelier Deterministic Entrance Gate – PASS**. Der separate, bestehende **Pferde Atelier Immutable Base Hardlock – FAIL**, weil er **sämtliche Änderungen unter `.github/workflows/` verbietet**. Direkter Schreibversuch nach `main` 409 wegen PR-Pflicht; der zulässige PR-Weg scheitert an dieser zusätzlichen übergeordneten Sperre. **PR offen, nicht produktiv**. Keine Umgehung des Sicherheits-Hardlocks. Nur ein expliziter Admin-Entscheid über diese eine Schutz-Ausnahme ermöglicht Merge. Danach braucht der echte, fortgesetzte Lauf eine Live-Abnahme einschließlich sichtbarer Produkte; vorher kein Gesamt-PASS.

## Verbindliche Schlussfolgerung

Der konkrete Grund für den verfrühten Abbruch des GitHub-Taktgebers ist **bewiesen**. Die KISS-Korrektur ist **lokal geprüft und auf GitHub als genau eine Änderung vorgelegt**. Eine funktionierende Produktivsteuerung kann ohne Freigabe der bereits existierenden Sicherheitsrichtlinie **nicht wahrheitsgemäß bestätigt werden**. Es wird weder ein neues Plugin benötigt noch ein weiterer Einzelfix vorgeschlagen.
