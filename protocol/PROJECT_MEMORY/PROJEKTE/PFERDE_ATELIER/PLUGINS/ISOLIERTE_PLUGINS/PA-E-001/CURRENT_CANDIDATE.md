# PA-E-001 – aktueller Optimierungskandidat

Plugin: Affiliate Portal Template Kit (Pferde-kompatibel)
Plugin-ID: PA-E-001
Fachbüro: DESIGN

## Ausgangsbasis
Server-Originaldatei: pferde-template-kit.php
Version: 1.50.559
SHA256: 2e6571e27f72a751899c88a47c1ffce682bb03971ba5b88899a42f2009f0d509

## Kandidat
Datei: pferde-template-kit-1.50.560.php
Version: 1.50.560
SHA256: 9617bbd4cc45d4d0e73b7e365a5a1cdd38c179579e42130ef756cdf07974b8db

Zweck:
- Performance-Ursache direkt im Template-Kit beseitigen.
- Kein neues Plugin.
- Menüarbeit für Desktop/Mobil im Template-Kit wiederverwenden.
- alter Performance-Helper danach nicht mehr erforderlich.

Lokaler Hardtest:
- PHP-Syntax PASS
- Desktop/Mobil identisch PASS
- Menüänderung invalidiert PASS
- Admin/REST/AJAX/Cron/WP-CLI ohne Cache PASS
- Übergang mit altem Helper ohne Doppelpfad PASS

Installationsbindung:
Nur exakt der Kandidat mit obigem SHA256 darf als 1.50.560 verwendet werden.
Fallback bleibt exakt Server-Original 1.50.559 mit obigem SHA256.
