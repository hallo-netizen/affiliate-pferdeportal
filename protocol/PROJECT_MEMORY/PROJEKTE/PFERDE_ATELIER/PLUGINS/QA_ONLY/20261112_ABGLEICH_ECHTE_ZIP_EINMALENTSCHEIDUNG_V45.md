# Pferdeatelier – Prüfung der TATSÄCHLICHEN Paketdateien, 12.11.2026

## Bereits erledigt und unverändert
- Der aktive K0-Zweig `konzept0-portal-neutral-20261002` steht bei Commit `83419e7827cbc0ff02bcaef7cefd0bd0900ac93a`. GitHub-Selbsttest https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43201428924 **PASS**. Die 10.-November-Bereinigung und die 81 verbleibenden Artikelregeln wurden nicht erneut verändert.
- Alte Testpakete PSTE .44 und PSERC .69 sind noch nicht als WordPress-Live-Betrieb bestätigt.

## NEUE zentrale Feststellung: getestete Quelle und ausgelieferte ZIP waren nicht identisch
Die echte gelieferte `PSTE-0.57.144.44-KISS-EINMALFREIGABE-QA.zip` wurde byteweise mit dem lokal getesteten Pluginverzeichnis verglichen. **ZWEI Quelldateien unterschieden sich**: `class-pste-repository.php` und `class-pste-compiler-read-capability.php`. Besonders wichtig: Die tatsächlich ausgelieferte ZIP .44 enthielt weiterhin den Befehl, bei Kontext-Neuprüfung mehrere bestehende Freigaben zu entwerten, und einen globalen Sperrfall im späteren Themen-Leser. Die lokale Testkopie enthielt beide Korrekturen bereits. **Die vorherige Aussage, .44 sei insgesamt getestet und beseitige diese Fälle, war daher nicht belegt. .44 nicht installieren.**

## Weiteren nachgelagerten Eigentümerkonflikt am ORIGINALPHP reproduziert
`PSTE_Repository::reanalyzeRetainedBacklogBatch` wird von der vorhandenen Produktionswellen-Verarbeitung aufgerufen und führte selbst für einen bereits freigegebenen, unveränderten Themen-Datensatz die zuvor getroffene SEO-/Titelentscheidung erneut aus. Beweis: echter PHP-Aufruf, WordPress-Datenbank simuliert, die vorhandene SEO-Funktion auf einen kontrollierten Test-Abbruch gesetzt. Der Aufruf erfolgte. Das ist eine andere Stelle als die bereits korrigierte Kontextaktualisierung.

Korrektur in der **bereits vorhandenen** Repository-Methode: Bei vollständig unterschriebenem ursprünglichen SEO-Beleg, unveränderter Quelle, unverändertem Strukturstand und bestehender Freigabe **die alte Entscheidung erhalten**. Bei verändertem oder ungültigem Beleg bleibt der bisherige ursprüngliche Bearbeitungsweg notwendig; insbesondere bleibt der **aktuelle Abgleich gegen inzwischen importierte WordPress-Artikel** aktiv. Keine neue Datenbanktabelle, kein zusätzlicher Entscheidungsdienst, keine Abschaltung der Artikelqualitätsprüfung.

## Zusammengeführter QA-Kandidat .45
`PSTE-0.57.144.45-EINMALFREIGABE-GESAMT-QA.zip`, SHA-256 `d3057946defc035af7abe5522c4845625c98ebd3f2cf621e1b3c5ce019f230a4`.
Gegenüber der **tatsächlich ausgelieferten** PSTE .44 wurden genau **3 vorhandene Dateien** geändert: Repository-Methode, Themen-Lesefunktion und Plugin-Versionskopf. ZIP: **121 Dateien**, alle vollständig extrahiert. Es wurde eine **frische Testkopie ausschließlich aus dieser ZIP** aufgebaut.

`PSERC-0.28.69-KISS-EINMALFREIGABE-QA.zip`, SHA-256 `576e58b51db3f348210dc3d47a894d6551558acc0c6900505be5e11257d2e41b`. Alle **63** extrahierten Dateien bytegleich zur geprüften PSERC-Quelle; Original-Integritätsprüfung **61/61 PASS**.

### Auf extrahierten, bytegenau abgeglichenen ZIP-Inhalten ausgeführt
- Echte Quellfunktion, verbliebene doppelte Entscheidung: vorher nachgewiesen; nach Korrektur **5/5** Tests: signierter alter SEO-Bescheid bleibt unverändert, aktuelle Bestandsprüfung läuft weiter; Strukturänderung, falscher Signaturnachweis, geänderte Quelle und nie freigegebenes Thema werden NICHT als bestehende Freigabe wiederverwendet.
- Bestehende normale PSTE-/PSERC-Tests: neun PHP-Testprogramme **PASS** auf neu ausgepackten Dateien, darunter **64/64** kombinierte PSTE/PSERC-Simulationsfälle, originale drei gespeicherte Aufträge und 5.016-Themen-/8-Freigaben-Tests.
- Syntax: Themenengine **83/83** PHP-Dateien PASS, Redaktionsplan **43/43** PASS.
- Kein externer Anbieter aufgerufen; keine wirkliche WordPress-DB und keine echten neuen Artikel 2 oder 3 erzeugt. K0-Code wurde nicht verändert.

## Noch zu prüfen, bevor eine Installation als freigegeben gelten darf
- Status und ursprüngliche Freigaben **in der realen Testseite**. Falls bei den alten 5.016 Themen bereits alle Quellfreigaben entwertet sind, repariert bloßes Nicht-Löschen diese verlorenen Belege noch nicht. Eine mögliche Wiederherstellung darf nur auf wirklich belegten ursprünglichen Freigaben erfolgen, nicht durch blindes Freischalten.
- Die echten Metadaten/Manifeste, echte K0-Texterstellung aller drei Artikel, LanguageTool 6.8 und WordPress-Importdateien.
- Tests und Dateivergleich sind eine Offline-QA; **kein** bestätigter Live-E2E-Nachweis. Keine produktive Freigabe und keine weiteren Plugininstallationen nur wegen einzelner Teiltests.

Ablage: persönliche Library `/pferdeatelier/PLUGINS/QA/`, frühere Versionen bleiben als Archiv erhalten. Zurzeit gilt **.45 QA statt .44 QA** als konsolidierter, bytegenau getesteter Kandidat.
