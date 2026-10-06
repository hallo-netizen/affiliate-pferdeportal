# Affiliate Router 6.72.194 — Live-Schabracken-Zielkarten-Neuaufbau + Tarifcheck-Preset

Datum: 06.10.2026

## Reale Ausgangslage

Nach Installation von 6.72.193 meldete der Nutzer:
- Schabracken-Ausspielung weiterhin fachlich falsch;
- Tarifcheck im Werbemittelimport unter „Aufgenommener Partner“ nicht auswählbar.

Damit bleibt AFF-ERR-050 live OFFEN. 6.72.193 ist für diesen Strang widerlegt.

## Bewiesene Source-Lücken

1. `creative_library_snapshots_for_select()` erzeugte keinen Tarifcheck-Eintrag. Der UI-Hinweis „Provider Direktpartner, Partnername Tarifcheck“ war nur ein manueller Workaround.
2. Der 6.72.190-Zielkarten-Nachlauf `run_v672190_banner_target_map_resync()` baut bestehende lokale Zielkarten nicht direkt neu, sondern startet nur die ADCELL-Programmsynchronisierung und setzt danach seinen Versionszustand.
3. Der vorhandene Kampagnen-Finder las nur den Legacy-Metakey `ppar_library_identity_hash`; aktuelle Output-Object-Kampagnen speichern `_ppar_creative_identity_hash`. Ein aktueller alter Auto-Banner konnte deshalb über diesen Bereinigungsweg unentdeckt bleiben.

## KISS-Fix 6.72.194

### Tarifcheck-Auswahl
Im bestehenden Dropdown „Aufgenommener Partner“ gibt es jetzt den festen Preset:
- Provider: `direct` / Anzeige „Direktpartner“
- Partner-ID: `tarifcheck`
- Partnername: `Tarifcheck`

Kein neuer Provideradapter.

### Einmaliger lokaler Zielkarten-Neuaufbau
Admin-/Background-only:
- arbeitet ausschließlich auf aktiven Bannerzeilen der vorhandenen Creative-Library;
- kein Provider-HTTP;
- kein Frontend-Scan;
- keine Produktzeilen;
- keine neue Tabelle oder Spalte.

Pro Banner:
1. nur automatisch materialisierte `output_object_v4`-Kampagnen fail-closed deaktivieren;
2. nur abgeleitete automatische Felder `topic_score`, `topic_targets`, `classified_at` leeren;
3. feste Zielkarte direkt aus der bereits gespeicherten `destination_url` neu aufbauen;
4. ohne sichere Zielkarte bleibt der automatische Banner inaktiv;
5. nur bei sicherer Zielkarte und technisch verifiziertem Asset über den bestehenden Planer neu materialisieren.

Manuelle/FIXED-Kampagnen bleiben unberührt.

## Source WordPress/MariaDB

Run `37480297999`: SUCCESS.

Bewiesen:
- Tarifcheck-Preset real vorhanden;
- Ausgangszustand mit aktiver falscher Fütterungs-Kampagne reproduziert;
- gespeicherte URL auf Schabracken geändert, alte Fütterungs-Zielkarte bewusst stehen gelassen;
- Neuaufbau entfernt Fütterung;
- Neuaufbau speichert Schabracken;
- aktive automatische Kampagne danach nur Schabracken;
- unbekannte Ziel-URL: keine Zielkarte und alte Auto-Kampagne bleibt deaktiviert;
- manuelle Kampagne bleibt aktiv;
- Scheduler nur `admin_init`;
- PHP-Lint 22/22;
- keine neue Tabelle.

## Exaktes Final-ZIP

Run `37480911019`: SUCCESS.

Bewiesen:
- Source-Delta gegen exakt getestete 6.72.193-Basis beschränkt auf:
  - `trait-ppar-automation-suite.php`
  - `trait-ppar-creative-library.php`
  - Hauptdatei / Versionsverdrahtung
  - Readme
- Fresh-Unpack 28/28 Byteidentität;
- PHP-Lint 22/22;
- exaktes ZIP frisch in WordPress 7.1.2 + MariaDB 10.11 installiert;
- stale-edge Schabracken-Fall PASS;
- Tarifcheck-Preset PASS;
- 6.72.193 Tarifrechner-KISS-Regression PASS;
- 6.72.192 Tarifcheck-HTML-Bannervertrag erneut PASS;
- keine neue Tabelle.

Finaler Installer:
`release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.194.zip`

SHA-256:
`36efb30086ece987cf9a55e3ab24cb85073343b67b5f6b1b761055a0fab08d04`

Größe:
`807040 Byte`

Source-Manifest SHA-256:
`7cf4c7bb1704faf87a3fefa95cf36ef7bf6bf66ddeb58b7149ecbded76edcabb`

Binding-Commit:
`0f503ce5b03d37dfdf994c46373501becbc972b5`

## Noch offen

Nur der reale Live-Beweis:
- 6.72.194 installieren;
- WordPress-Backend einmal aufrufen, damit der admin-only Einmal-Nachlauf geplant wird;
- Nachlauf abschließen lassen;
- Schabracken öffentlich erneut read-only prüfen.

AFF-ERR-050 darf erst danach live geschlossen werden.
