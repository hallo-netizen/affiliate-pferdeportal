# GITHUB RELEASE HARDLOCK – STARTMASTER0054

Verbindliche Governance-Ergänzung nach der Übergabelücke F-44.

- MASTER bleibt oberste fachliche/technische Autorität.
- GitHub ist zwingende lückenlose zweite Wiederherstellungs- und Versionssicherung.
- Nie direkt auf `main`; pro Arbeitsblock eigener Branch; kein Merge ohne ausdrückliche Freigabe.
- Jede tatsächlich geänderte Source- und Vertrags-/Dokumentationsdatei muss gesichert werden.
- Audittexte/Hashes allein reichen nicht, wenn der reale geänderte Source-Stand dadurch nicht vollständig wiederherstellbar ist.
- Tests positiv/negativ, Rule-1-Deltascope, Installer-SHA, MASTER-SHA, Manifestzahl, Branch/Base/Head und Commitliste müssen dokumentiert werden.
- Vor `FERTIG` muss ein frischer GitHub-Checkout/Download den gesicherten Source-Stand reproduzieren; Installer und MASTER müssen dauerhaft über GitHub-Artefaktmechanismen abrufbar und zusätzlich dem Nutzer tatsächlich übergeben sein.
- Ein nur lokaler Build oder die Aussage `wurde gebaut` zählt nicht als Übergabe.
- Nicht abrufbar/nicht gehasht/nicht übergeben = BLOCKED.
- Keine Force-Pushes oder Historienumschreibung.
- Dieser Hardlock ändert keine Runtime-/Produktions-/Text-/Designlogik.
