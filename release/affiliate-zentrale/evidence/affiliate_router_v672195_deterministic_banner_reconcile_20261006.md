# Affiliate Router 6.72.195 — Deterministischer Banner-Reconcile + explizite Tarifcheck-Gruppen

Datum: 06.10.2026

## Reale Ausgangslage

Nach Installation von 6.72.194 meldete der Nutzer erneut:
- Schabracken-Banner weiterhin falsch;
- zwei Tarifcheck-Bannergruppen wurden manuell importiert: Versicherungen und Kreditvergleich;
- diese Tarifcheck-Banner erscheinen nicht in den erwarteten Kategorien.

Damit ist 6.72.194 fuer den Schabracken-Livefall widerlegt. AFF-ERR-050 bleibt offen.

## Ursachenkette

### 1. 6.72.194 konnte nur korrekt verknuepfte Alt-Automatik sicher entfernen

Der 6.72.194-Rebuild deaktiviert alte automatische Kampagnen ueber Creative-Identitaets-Metakeys. Ein alter output_object_v4-Banner ohne den erwarteten aktuellen oder Legacy-Metakey kann dadurch ausserhalb des Deaktivierungswegs bleiben.

Folge:
- neue Zielkarte kann korrekt Schabracken enthalten;
- eine alte aktive automatische Fütterungs-Kampagne kann trotzdem parallel fortbestehen;
- die Live-Ausgabe bleibt falsch, obwohl der synthetische Rebuild-Test PASS war.

Der 6.72.194-Test bewies den modellierten Altzustand, nicht die Invariante "kein beliebiger alter automatischer Bannerzustand kann ueberleben".

### 2. Tarifcheck-Gruppen wurden fachlich nicht gespeichert

Der bisherige HTML-Sammelimport speichert Partner und Bannercode, aber keine explizite Fachgruppe "Versicherungen" oder "Kreditvergleich/Kosten".
Die Familie wurde ausschliesslich aus einer sicher ermittelten destination_url abgeleitet.

Wenn ein Tarifcheck-HTML-Code nur einen Trackinglink liefert und keine fachlich lesbare reale Ziel-URL aufgeloest wird:
- destination source bleibt tracking_fallback/tracking_checked;
- die semantische Zielauswertung ist leer;
- keine topic_targets werden gespeichert;
- Runtime darf laut HARD KISS ohne gespeicherte Zielkarte keinen Banner anzeigen.

Damit kann ein technisch korrekt importierter Tarifcheck-Banner bewusst unsichtbar bleiben.

## 6.72.195 Konzept

### Eine automatische Zielwahrheit

Creative-Library topic_targets bleibt die einzige fachliche Autoritaet fuer automatische Banner.

Output-Objects und Kampagnen sind nur abgeleitete Ausgabeprojektionen und duerfen keinen alten automatischen Zustand konservieren.

### Deterministischer Reconcile

Beim neuen 6.72.195-Reconcile:

1. Zuerst werden global alle aktiven automatisch erzeugten Bannerkampagnen mit source=output_object_v4 und quality_manual_status=auto_verified deaktiviert.
2. Dieser Reset sucht absichtlich NICHT ueber Creative-Identitaets-Metakeys.
3. Manuelle/FIXED Kampagnen ausserhalb dieser Auto-Bannerprojektion bleiben unberuehrt.
4. Produktkampagnen bleiben unberuehrt.
5. Danach werden bei allen aktiven Creative-Library-Bannern die abgeleiteten topic_targets frisch aufgebaut.
6. Nur Banner mit sicherer gespeicherter Zielkarte und technisch gueltigem Asset werden wieder materialisiert.
7. Ohne Zielkarte bleibt der automatische Banner aus.
8. Der erste begrenzte Reconcile-Schritt laeuft direkt bei admin_init; WP-Cron ist nur Fortsetzung fuer grosse Bestaende.

Damit lautet die Invariante:
Nach Reconcile kann eine alte automatische Bannerkampagne nicht deshalb aktiv bleiben, weil ihre historische Identitaetsverknuepfung fehlt oder falsch ist.

### Tarifcheck explizite Fachgruppe

Beim manuellen Tarifcheck-Import kann jetzt ausdruecklich gewaehlt werden:
- Versicherungen
- Kreditvergleich / Kosten
- Automatisch nur aus sicherer Ziel-URL

Die explizite Auswahl wird als Fachzuordnung im Creative gespeichert.
Bei Tarifcheck ist diese bewusste Fachgruppe autoritativ und muss nicht aus dem Trackinglink geraten werden.

Bestehende Tarifcheck-Banner koennen im Bannerbereich angehakt und gesammelt auf
- Tarifcheck -> Versicherungen
- Tarifcheck -> Kreditvergleich / Kosten
gesetzt werden.

Ohne explizite Gruppe bleibt die alte sichere URL-Erkennung fail-closed.

## Lokale Positiv-/Negativ-Simulation

12/12 PASS.

Positiv:
- explizite Tarifcheck-Gruppe Kredit trotz reinem Trackinglink -> kosten;
- explizite Tarifcheck-Gruppe Versicherung trotz reinem Trackinglink -> versicherung;
- sichere echte Kredit-Zielinformation ohne explizite Gruppe -> kosten;
- globaler Reconcile entfernt stale automatischen Banner auch ohne Identity-Metakey;
- aktuelle Schabracken-Projektion ist danach der einzige aktive automatische Banner im simulierten Schabrackenfall;
- manuelle Banner bleiben erhalten;
- Produktkampagnen bleiben erhalten.

Negativ:
- Trackinglink ohne sichere Zielinformation und ohne explizite Fachgruppe -> BLOCKED;
- gemischtes Kredit+Versicherung-Ziel ohne explizite Fachgruppe -> BLOCKED.

## Historische Einordnung

Das Readme dokumentiert zahlreiche aufeinanderfolgende Eingriffe im gleichen Banner-/Zielbereich, unter anderem 6.72.174, 6.72.175, 6.72.177, 6.72.178, 6.72.179, 6.72.181, 6.72.182, 6.72.183, 6.72.184, 6.72.185, 6.72.186, 6.72.189, 6.72.190, 6.72.191, 6.72.192 und 6.72.194.

Der neue Ansatz behandelt deshalb nicht erneut einen einzelnen Schabracken-Sonderfall, sondern entfernt die strukturelle Moeglichkeit einer ueberlebenden stale Auto-Bannerprojektion.

## Source-Bindung

Version: 6.72.195

Source-Manifest SHA-256:
`7e9cf15d9ff9b066343f78d7e20524b1d2b01d6f31d4d96e59eb6b4183612da5`

Source-Dateien: 28

## Noch offen

Nicht als Release-PASS behandeln, bevor mindestens:
- PHP-Lint des exakten Source-Trees PASS;
- reale WordPress/MariaDB-Positiv-/Negativtests PASS;
- Fresh-Unpack/Byteidentitaet des finalen ZIP PASS;
- reale Live-Abnahme Schabracken PASS;
- reale Live-Abnahme beider explizit zugeordneten Tarifcheck-Gruppen PASS.

Bis dahin release_allowed=false.
