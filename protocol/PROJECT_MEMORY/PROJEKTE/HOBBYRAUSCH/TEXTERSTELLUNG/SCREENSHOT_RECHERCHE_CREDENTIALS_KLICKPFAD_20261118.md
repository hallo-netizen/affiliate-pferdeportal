# 18.11.2026 – Screenshot Recherche: Zugangsdaten im Diagnose-Reiter, Recherche gestoppt

Quellen: Screenshot des Betreibers auf `hobby-depot.de/wp-admin/admin.php?page=texterstellung-recherche` um 18:19 Uhr und Originalcode der aktuellen `Texterstellung_Hobbydepot_0.4.24.2_TESTOBERFLAECHE_BEREINIGT.zip`.

- Screenshot zeigt aktive Ansicht **Texterstellung → Recherche**, mit Status `RECHERCHE GESTOPPT`, Grund `PLUGIN_ACTIVATED_MANUAL_START_REQUIRED`, Button `Status einmal aktualisieren`. Dies ist laut bestehender `TXE_Workshop::activate()` der sichere Stopp beim Aktivieren/Ersetzen, **kein Nachweis eines laufenden Rechercheauftrags**.
- Screenshot zeigt zudem `Die originale PSTE-Migration ist noch nicht abgeschlossen`. Bestehende Daten unverändert.
- **Originalcode überprüft:** Zugangsdaten-Formular steht ausschließlich unter **Texterstellung → Diagnose** (`if($view==='diagnose')`), mit den Feldern `DataForSEO Login`, `Passwort` und Button `Zugangsdaten der Originalengine speichern`. `TXE_Workshop::handle()` nimmt `txe_credentials_save` entgegen und verwendet bestehende `PSTE_Credentials::saveFromAdmin()`. Das Speichern selbst startet keinen kostenpflichtigen Recherchelauf.
- Bereits gelieferte Diagnose `texterstellung-diagnose-20261118-165236.json`: DataForSEO-Credentials nicht vorhanden; K0 `BLOCKED/K0_ARTICLE_TYPE_AUTHORITY_UNAVAILABLE`; 0 Aufträge und 0 Recherchen. Nach dem Speichern ist dies als historischer Status zu interpretieren, nicht automatisch als aktualisiert.
- **Nächster konkreter Nutzer-Klick:** Texterstellung → Diagnose → DataForSEO Login + API-Passwort → Zugangsdaten der Originalengine speichern. Kein Recherche-Start, keine K0-Produktion; anschließend vorhandene PSTE-Migration und Kostenkontrolle separat prüfen.
- **Kein neues Plugin, kein Code-/Architekturumbau und kein erneuter Diagnosebericht angefordert.** Version 0.4.24.2 bleibt im zentralen Pluginbüro unverändert.
