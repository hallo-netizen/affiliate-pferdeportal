# PRODUKTVERGLEICH – AUTORITATIVE FEHLERQUELLE

STAND: 2026-09-07
ROLLE: einzige detaillierte Fehlerquelle für den aktuellen PRODUKTVERGLEICH-V1-Arbeitsweg.

## PV-ERR-001 – falsche WordPress-Kategoriehierarchie

STATUS: CLOSED

Befund:
Der frühe Prototyp erwartete für `Vergleich Regendecken` eine echte Taxonomie-Unterkategorie. Die reale Pferde-Atelier-Kategorie ist technisch flach.

Realer gebundener Term:
- Term-ID: 11
- Name: `Vergleich Regendecken`
- Slug: `pferdedecken-regendecken-vergleich`
- Parent: 0

Fix:
Ab 0.2.1 werden ID/Name/Slug/Parent exakt geprüft. Bestehende Live-Kategorie wird nicht automatisch neu angelegt.

Beleg:
Run `34141063395` PASS; falscher Parent im Negativtest korrekt BLOCKED.

## PV-ERR-002 – Erst-Draft sprang an Materialisierungsstufe vorbei

STATUS: CLOSED

Befund:
Beim ersten frischen `PV-REG-001`-Drafttest wurde direkt die Link-Finalisierung aufgerufen. Dadurch entstand:
`UPC_LINK_FINALIZER_SOURCE_NOT_UNIQUE`.

Ursache:
Die bestehende WordPress-DRAFT-Materialisierung war vor der Link-Finalisierung nicht aufgerufen worden.

Fix:
Fest gebundene Reihenfolge:
`Import -> WordPress-DRAFT -> Link-Finalisierung -> Grafik-Finalisierung -> Endhash`.

Beleg:
Der nachfolgende Erst-Draft-Test lief vollständig PASS; zweiter Lauf ohne Dublette PASS.

## PV-ERR-003 – 0.2.3 Hauptmenü-Test war falscher Positivtest

STATUS: FIX-KANDIDAT 0.2.4 TECHNISCH PASS / NUTZER-LIVE-VERIFY OFFEN

Realer Nutzerbefund:
Nach dem 0.2.3-Schritt war auf der echten Pferde-Atelier-WordPress-Seite kein Hauptmenüpunkt `Produktvergleich` sichtbar.

Prüfungsfehler:
Der 0.2.3-Test rief `register_menu()` künstlich direkt auf. Er bewies nur, dass die Funktion einen Menüeintrag erzeugen kann, nicht dass WordPress sie im echten Admin-Lifecycle ausführt.

Fix-Kandidat 0.2.4:
- Admin-Hooks werden ohne Bootstrap-`is_admin()`-Abhängigkeit registriert;
- Top-Level-Menü wird im echten `admin_menu`-Hook mit Priorität `99999` gesetzt.

Technischer Beleg:
Run `34154550626` PASS mit:
- sauberer 0.2.4-ZIP;
- WordPress-Installation/Aktivierung;
- echtem WordPress-HTTP-Server;
- echtem Admin-Login;
- gerenderter `/wp-admin/`-Sidebar;
- sichtbarem Top-Level-Menü `Produktvergleich`;
- erfolgreichem Abruf der echten Menüseite;
- weiterhin bestandenem `PV-REG-001`-Drafttest.

OFFEN:
0.2.4 ist auf der echten Nutzerseite noch nicht manuell bestätigt.
Bis dahin kein LIVE-PASS behaupten.

## Regel

Neue Produktvergleichsfehler werden hier ergänzt.
Das zentrale `FEHLERREGISTER.md` bleibt reiner Wegweiser und enthält keine zweite Detailbeschreibung.
