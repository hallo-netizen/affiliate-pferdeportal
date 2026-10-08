# Affiliate Zentrale 6.72.208 – KISS Cleanup / DB / Performance

Datum: 2026-10-08

## Auftrag
Nur Altlasten und Vereinfachungen. Kein Umbau des funktionierenden Prozesses.

## Automatik / Rückversicherung – unverändert bestätigt
- Provider-Automation standardmäßig aktiv.
- Standard-Importzyklus: alle 2 Wochen via WP-Cron.
- Worker verarbeitet offene Jobs in kleinen Paketen.
- Neu/importiert/aktualisiert -> bestehende Assetprüfung -> Zielzuordnung -> bestehende Ausgabeplanung.
- Partner-Reconcile: 1. vollständiges Fehlen = quarantine_missing; 2. vollständiges Fehlen = inactive_missing.
- Nach bestätigtem Fehlen werden nur automatische Bannerkampagnen deaktiviert; manuelle FIXED-Kampagnen bleiben geschützt.
- Separater Health-Check bleibt aktiv; Standard alle 3 Wochen, failure_threshold=3.

## KISS-Bereinigung 6.72.208
- Alte Fachmenüs werden nicht mehr per CSS versteckt.
- Sie werden sauber per WordPress remove_submenu_page() aus der sichtbaren Navigation entfernt.
- Direkte Spezialseiten und interne Links bleiben registriert/erreichbar.
- Technische Route-/Aktivierungsdetails werden aus der normalen KISS-Quellenansicht entfernt; interne Daten bleiben unverändert.
- Import, Automation, Reconcile, Health, Ranking, Banner-/Produkt-Ausgabe, Rechner und Provider wurden nicht geändert.

## Bewusst NICHT gelöscht
- Die gebundene historische Recovery-Datei bleibt bestehen, weil sie noch von einem eng begrenzten Produkt-Incident-Fallback referenziert wird. Löschen wäre möglicher Funktionsverlust.
- Der bestehende Vollpool-Nachlauf wurde nicht umgebaut. Er ist ein möglicher Performance-Hotspot, aber seine Ablösung wäre Prozessänderung und damit außerhalb des Auftrags.

## DB-/Performance-Check
Fresh WordPress + MariaDB, Run 37770855906:
- Cleanup source diff only: PASS
- geschützte Runtime-Traits unverändert: PASS
- Automation/Reconcile/Health-Invarianten unverändert: PASS
- PHP-Syntax: PASS
- sichtbare Altmenüs entfernt: PASS
- KISS-Hauptmenüs erhalten: PASS
- versteckte Spezialseite weiterhin registriert: PASS
- alter CSS-Hide-Mechanismus entfernt: PASS
- alter terminaler Automation-Job wird gelöscht: PASS
- offener/aktiver Automation-Job bleibt erhalten: PASS
- alte Recovery-Optionen AFF039/AFF043/AFF044 werden entfernt: PASS
- insgesamt: 37 PASS / 0 FAIL
- ZIP/Source-Identität: 28/28 PASS

## Installer
- AFFILIATE_ZENTRALE_6.72.208.zip
- SHA256: a3023fb4c0afd4a8210321fb59f9784eeab166e09665490d2dc10795620300d8
- Bytes: 821581
- Workflow artifact ID: 11547371311

Status: KISS_CLEANUP_PASS / READY
