# HD009 0.1.34 – geprüfter, lesender Idealo-Feedvergleich

**Status:** Installierbarer Vergleichskandidat; CURRENT 0.1.33 unverändert.

**Fakten:** Hobby Depot PID 568912, zwei freigeschaltete Feeds: 2747 Fashion/Sport/Outdoor und 2901 Standard. Aus Feed 2747 wurden zuletzt 2.530 Produkte auf 52 Hobbyziele mit 429 Produktkarten zugeordnet. Die wirkliche 2901-Abdeckung war bisher **nicht getestet**.

**Umsetzung:** Ein neuer Vergleichsknopf auf der vorhandenen idealo-Fachseite von HD009. Er nutzt den vorhandenen API-Key nur auf dem Server, bestätigt Feed 2901 für PID 568912 erneut über die offizielle iPN-findFeeds-API und liest den 2901-CSV.GZ-Feed einmalig im Hintergrund ohne Produktimport. Die passenden Produktzeilen werden mit dem *unveränderten* Originalmatcher und denselben Bild- und GTIN-Regeln geprüft. Die 2747-Versorgung wird nur per SELECT aus bestehenden Produkteinträgen gelesen. Ausgabe: Überlappung, zusätzliche 2901-Hobbys, bei Wechsel verlorene 2747-Hobbys, Gesamtsumme und Hobbytitel.

**Datenschutz und Schutz:** Kein geänderter Idealo-Feed, keine geänderten Anzeigen, keine neuen Kampagnen, kein veröffentlichter Produktwechsel, keine Änderung an Amazon/DataForSEO, eBay, Design oder WordPress-Kern. Nur ein Vergleichsbericht in einer isolierten WordPress-Option. Button benötigt Administratorrecht und Nonce, Hintergrundarbeiter hat ein einmaliges Zeit-Token. Keine automatischen oder wiederholten Feedvergleiche.

**Hard-QA:** Unveränderte 41 Original-ZIP-Dateieinträge, Syntax aller 24 PHP-Dateien, 13 vorhandene Originalmethoden exakt unverändert, verbotene Schreibzugriffe im Vergleich statisch ausgeschlossen, 25 echte PHP-Funktionstests mit synthetischen CSV.GZ-Feeds (Zuordnung, falsche Treffer, EAN/GTIN, Bilder, Feedverfügbarkeit, fremde Werbefläche, Doppelstart und Abgleich 2901 gegen vorhandene 2747-Konzeptliste). Keine Behauptung über noch nicht gelesene echte 2901-Daten.

**Live-Abnahme:** Nach bewusster Installation auf Hobby Depot den Vergleichsknopf einmal betätigen. Nach Abschluss echte Zahlen für beide Feeds vergleichen. Vorher **keine Änderung der Feed-ID und keine Umstellung des Imports**.

Belege: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43395306016
Release: https://github.com/hallo-netizen/affiliate-pferdeportal/releases/tag/hobby-hd009-0.1.34-safe-feedcompare-20261113
SHA256: 131298bc6dfa2344ae3a3c898372344d9cda56c12f98835c1482834a0ab34c3e
