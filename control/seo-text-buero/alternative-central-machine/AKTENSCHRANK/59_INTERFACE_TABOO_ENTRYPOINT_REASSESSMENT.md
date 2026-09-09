# ACM – SCHNITTPUNKT-TABU / EINSTIEGSPUNKT-NEUBEWERTUNG

Stand: 2026-09-09
Route: Alternative Central Machine (ACM)
Branch: `alternative/seo-text-central-machine-20260908`
Status: VERBINDLICHER BEFUND – KEINE PRODUKTIONSFREIGABE

## Anlass

Vor Fortsetzung wurde die harte Regel erneut bestätigt:

**Bestehende Schnittpunkte sind absolut tabu.**

Insbesondere werden in dieser Alternativroute nicht verändert:
- bestehender Chat/Codex-Entry
- bestehendes FACHWORKFLOW_HANDOFF_REQUEST-Format
- Textmaschine
- PPM/PSERC/PSTE-Fachregeln
- WordPress-Normal-Draft-Import
- WordPress-Signatur-Eingang
- Endstempel-/Publish-Sicherheit
- produktive CURRENT_STATE-/Hobbyraum-Wahrheit

Schnittpunkte dürfen nur read-only geprüft oder exakt über ihren bestehenden Vertrag benutzt werden.

## Harte Prüfung des bisherigen NEXT ACTION ACM-WP-01

Bisheriger offener Punkt:
`ACM-WP-01 – echte One-JSON-WordPress-Runtime-Anbindung fehlt`.

Frisch geprüft:

1. `protocol/WORDPRESS_SIGNATURE_ENTRY_LOCK_V1.json`
   - erlaubt nur Empfang/Prüfung der final signierten JSON und PASS/FAIL
   - verbietet ausdrücklich `IMPORT_LOGIC_CHANGE`
   - verbietet `WORKFLOW_ARCHITECTURE_CHANGE`
   - verbietet neuen Guard/nested lock/alternative route

2. `ENDSTEMPEL_WORDPRESS_VERIFY.php`
   - ist Verification-only bis vor den ersten Write
   - besitzt keinen echten WordPress-Admin-/Runtime-Caller

3. Letzter realer Wiring-Audit
   - `runtime_callers=[]`
   - `single_final_signed_json_wp_upload_wired=false`
   - vorhandener PPM-Normal-Draft-Adminpfad existiert separat

4. `production_package_release_gate.py`
   - kann ein vollständiges `PSERC_APPROVED_PRODUCTION_PACKAGE_V1` bereits als eine Datei prüfen und byte-identisch freigeben
   - endet aber vor WordPress
   - erzeugt keine bestehende WordPress-Runtime-Anbindung

5. Vertragsformate
   - vorhandener WordPress-Endstempel-Verifier prüft den Endstempel-/Artikelmanifest-Vertrag
   - vorhandener Normal-Draft-Import arbeitet mit Fact-Pack-Bundle + Produktionsplan
   - eine direkte unveränderte One-JSON-Import-Schnittstelle zwischen beiden ist nicht vorhanden

## Urteil WP-01

**ACM-WP-01 bleibt ein realer Produktionsadoptionsblocker.**

Er darf unter der Schnittpunkt-Tabu-Regel in der Alternativroute **nicht durch Umbau, Wrapper, neuen Handler, neuen Importer oder neues Übergabeformat geschlossen werden**.

Damit gilt:
- nicht reparieren
- nicht umgehen
- nicht als PASS markieren
- Produktionsadoption bleibt BLOCKED
- kein WordPress-Write

## Letzter zulässiger unveränderter Einstieg

Frisch bestätigt auf main `93ba987c56f7b08ffba009210e3012c036fec18d`:

`offizieller Runtime-Start -> CURRENT_BOUND_ACTION_READY -> bestehende FACHWORKFLOW_HANDOFF_REQUEST.json`

Aktuelles gebundenes Item:
- canonical_article_id: `article:a8282e69ecd43b615de17eb1`
- plan_slot: `9c229b0e6a784a482575e3deb16d105e3b5355becbbbb8ecfc8e1f600b529c56`
- Titel: `Das Wichtigste über Hindernisstangen für Pferde`
- Target Keyword: `Hindernisstangen für Pferde`
- Kategorie: `hindernisstangen-beratung`
- Beitragsart: `Beratung`
- Workerrolle: `CURRENT_CODEX_IS_BOUND_FACHWORKFLOW_WORKER`

Vorhandener Handoff:
- genau 16 Pflichtfelder
- Feldsatz nicht frei wählbar
- keine neue Handoff-Datei erforderlich
- kein neuer Entry erforderlich
- publish_allowed=false

## Nächster zulässiger Alternativ-Test

Nicht an WP-01 weiterbauen.

Stattdessen den **bestehenden realen Einstieg** für genau dieses gebundene Item bis zum ersten echten Block prüfen:

`offizieller Entry -> gebundener Fachworkflow/Codex -> reale Fachprodukte/Fact-Pack -> bestehende FACHWORKFLOW_HANDOFF_REQUEST.json -> unveränderte vorhandene ACM-Laborkette`

Grenzen:
- kein Schnittpunkt wird geändert
- kein neues Handoff
- kein neuer Controller
- keine neue PPM-API
- kein WordPress-Runtime-Handler
- kein WordPress-Write
- kein Auto-Publish
- bei erstem nicht bereits vorhandenen technischen Übergang: STOP

Diese Prüfung ist **keine Umgehung von WP-01**.
WP-01 bleibt Produktionsadoptionsblocker.
Sie dient ausschließlich dazu, den upstream realen ACM-Prototyp bis zu seinem tatsächlichen Endpunkt zu prüfen.

## KISS

PASS.

Es wird nichts an Schnittstellen gebaut.
Der vorhandene Einstieg wird wiederverwendet.
Der vorhandene Blocker wird nicht mit neuer Architektur überdeckt.
