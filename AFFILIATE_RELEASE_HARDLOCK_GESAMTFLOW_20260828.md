# Affiliate-Zentrale – verbindlicher Release-Hardlock Gesamtworkflow

Ab 28.08.2026 gilt für jede neue Plugin-Version und jeden Fix:

1. Keine Freigabe allein wegen lokaler Einzeltests.
2. Vor jeder Freigabe muss der Fix gegen den gesamten bestehenden Workflow geprüft werden.
3. Pflicht ist ein NEGATIV-Test des bisherigen Fehlers: alter Stand muss reproduzierbar FAIL zeigen.
4. Pflicht ist ein POSITIV-Test des Fixes: neuer Stand muss denselben Fall PASS zeigen.
5. Zusätzlich müssen alle vom Fix berührbaren Workflow-Phasen/Transporte regressionsgeprüft werden, nicht nur die unmittelbar sichtbare Fehlerstelle.
6. Unveränderte Bereiche werden byteweise gegen die freigegebene Basis geprüft. Keine stillen Änderungen an Providerlogik, Ranking, Feed, Portalstruktur, Design, idealo oder anderen Plugins.
7. Aktive persistente Runs, Checkpoints und Cursors dürfen durch ein Upgrade nicht unbeabsichtigt zurückgesetzt werden; dieser Upgradepfad ist ausdrücklich zu prüfen.
8. Installer und MASTER müssen Fresh-Unpack/PHP-Lint/Integrität bestehen und der Installer in der MASTER muss byteidentisch zum geprüften Installer sein.
9. Erst wenn NEGATIV + POSITIV + Gesamtworkflow-Regressionsgate PASS sind, darf ein Installer als freigegeben bezeichnet oder zur Installation empfohlen werden.
10. Bei einem offenen oder nicht belegten Gate lautet der Status ausdrücklich: NICHT FREIGEGEBEN.

Diese Regel ist bindend und hat Vorrang vor schneller Versionsausgabe.
