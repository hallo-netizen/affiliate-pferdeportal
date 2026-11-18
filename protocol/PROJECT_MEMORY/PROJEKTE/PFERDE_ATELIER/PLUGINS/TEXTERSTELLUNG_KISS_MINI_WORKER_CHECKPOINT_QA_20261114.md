# Pferdeatelier Texterstellung KISS – bestehende MINI-Arbeitsschritte einzeln sichern (14.11.2026)

**STATUS: QA ONLY, NICHT INSTALLIEREN, KEINE PRODUKTIONSFREIGABE.** Der verbindliche [Gesamtzielvertrag](TEXTERSTELLUNG_KISS_ENDGUELTIGER_WORKFLOW_20261114.md) bleibt maßgeblich. Weiterarbeit auf exakt dem gesicherten 113-PASS-Stand; keine neue WordPress-/K0-Architektur.

## Was am vorhandenen Code tatsächlich geändert wurde

**Nur die bestehende `texterstellung.php` geändert.** Im **bereits vorhandenen** WordPress-MINI-Importer `TXE_Workshop::seoImport()` können die drei bestehenden MINI-Arbeitsschritte Kategorie, Redaktionsentscheidung und Titel jeweils ihren Abschluss **pro Themenzeile** im bisherigen einen WordPress-Auftragsregal sichern. Keine neue WordPress-Aktion, kein neues Plugin/kein Worker/kein Plan/keine Tabelle. Die ursprüngliche Schreibsperre, der vorhandene bestehende Auftrag und der unveränderte WordPress-Datenbestand bleiben die einzigen Zuständigkeiten.

Der originale `seoExport()` übergibt jedem **neuen** Auftrag den aktuell von PSTE gelesenen Bestand und vollständigen Kategorie-/Seitenbaum, plus verbindliche Schrittfolge und den Nachweis, dass Zwischenspeicherung erforderlich ist. Beim erneuten Download des **gleichen** aktiven Auftrags bleibt sein Bestand eingefroren; die gespeicherten Arbeitsschritte und offene Fehler werden als Lesedaten mitgegeben. Ein Folgeschritt wird **nur nach dem gespeicherten vorherigen Schritt** angenommen. Die Fachentscheidungen des vorigen Workers dürfen nicht verändert werden. Fehlende / manipulierte Ergebnisse werden pro Themenzeile offengehalten, andere laufen weiter; ein tatsächlich unveränderter erneut zugestellter Schritt wird nur als bereits erledigt erkannt.

Original-61-FREI und Titel werden **nicht** erneut entschieden. Es fehlt dort nur die Kategorie-/Fach-Magazin-Redaktionsbüro-Zuordnung. Die beiden weiteren Schritte werden für diese Altfälle übersprungen, ebenso die Titelarbeit bei BELEGT/KLÄRUNG. Bei allen anderen Themen hat nur der jeweilige eine Worker seinen inhaltlichen Verantwortungsbereich. Der fertige MINI-Rückimport ist bei neuen Aufträgen ohne die passenden unveränderten einzelnen Zwischenspeicherungen technisch gesperrt. Die vorhandenen PPM-Originalplätze, K0-Fünffelderverträge, Entwurfs-Importfunktionen und originalen PSTE-/PSERC-Klassen sind unverändert.

## Wirklich ausgeführte lokale QA mit Originaldaten

**247/247 lokale PHP-Gegenproben PASS; 117/117 PHP-Syntaxprüfungen PASS; 164/164 ursprüngliche PSTE-/PSERC-Dateien gegenüber dem vorherigen QA-Stand byteidentisch.**

Historisch reale Eingaben: 87 alte MINI-Themenentscheidungen (61 FREI / 20 BELEGT / 6 KLÄRUNG), 1.179 archivierte WP-/Planartikel, 1.124 originale Kategorien samt Seitenpfaden. Tests: Abbruch nach **11 Kategorie-Zwischenspeicherungen**, Wiederaufnahme restlicher 76; Abbruch nach **7 Redaktions-Zwischenspeicherungen**, Wiederaufnahme restlicher 80; Abbruch nach **9 WordPress-Endimporten** mit gesicherten Ergebnissen; Titel-Einzelfehler repariert ohne Wiederholung anderer Themen. Historische 61 FREI in vier Chargen 20/20/20/1 ohne SEO- oder Titel-Neuentscheidung. Bei **neuer** Charge geänderten 1.180er Testbestand frisch geladen; laufende Charge blieb bei ihrem ursprünglichen 1.179er Bestandsbeleg.

**Prüfgrenzen:** Originale WordPress-Daten wurden als Archivinputs verwendet, aber die **WordPress-Datenbank, aktuelle PPM-Signatur und externe MINI-KI-GitHub-Ausführung waren in diesen Tests nachgebildet bzw. nicht verbunden.** Die PDF-/WordPress-/K0-Live-Abnahme und das tatsächlich automatische Zurückmelden der externen Worker liegen nicht vor. Der gespeicherte WP-Job hat bei einer historischen 20er-Charge im lokalen Test ungefähr **1,0 MB**; tatsächliche Schreibzeiten im WP-Testserver wurden noch nicht gemessen.

## Verifizierte Dateien – im schon bestehenden privaten Plugin-Büro

Unter `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/`:

- `MINI_KISS_WORKER_CHECKPOINTS_EXAKT_20261114.patch` – SHA256 `d293d8698681206faecf326509b55088509806b0a3dfc4beba2f0cad6fd0395d`.
- `MINI_KISS_WORKER_CHECKPOINTS_QUELLE_QA_20261114.php` – SHA256 `19afdf3f25790a92280c59b1d952b24ae2d8227044cdd61cfb6a61189c8b075e`.
- `MINI_KISS_WORKER_CHECKPOINTS_QA_ERGEBNIS_20261114.json`, `MINI_KISS_WORKER_CHECKPOINTS_QA_STAND_20261114.md`, zwei PHP-Originaldaten-Testskripte und der Test-Runner.

Die neue Quelle und der exakte Patch wurden **nach** dem privaten Ablagevorgang erneut geladen und bytegenau mit dem geprüften Stand verglichen; Original-Patch ist auf vorherigem Quellstand exakt anwendbar.

## Verbindlicher noch offener Blocker

Die externe KI-/GitHub-MINI-Ausführung muss ihre Zwischenergebnisse real an **die bereits vorhandene eine WordPress-Importaktion** schicken und beim Abbruch den gespeicherten Zwischenschritt abrufen. **Das kann die WordPress-Seite nun sicher annehmen, aber ein realer externer Aufruf/selbsttätiger Wiederanlauf wurde noch nicht getestet.** Die tatsächliche isolierte WordPress-Testinstallation inklusive signierter PPM 6.7.9-Platzvergabe, K0-Schreibworker und fertig gespeichertem Entwurf war ebenfalls nicht erreichbar. Also **keine Garantie eines echten vollständigen MINI-/K0-Gesamtlaufs, kein Installer, kein Merge als Produktionsfreigabe.** `release_allowed=false`.

**Einziger nächster Test:** Mit dem bereits bestehenden GitHub-MINI-Start den echten MINI-Worker nach jeder Station abbrechen/wiederaufnehmen, gespeicherte Original-WP-Stände rücklesen und danach K0→WP-Entwurf mit Unterbrechung im isolierten Testportal abnehmen. Ohne neuen Worker oder zweite inhaltliche Prüfung.
