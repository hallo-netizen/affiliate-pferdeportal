# Korrektur: Ausgangsplugins liegen im Campus und wurden tatsächlich gelesen

12.11.2026. **Die frühere pauschale Aussage, die festgelegten Ausgangsplugins seien nicht auslesbar, war falsch.**

## Physischer Ort und nachgerechneter Beweis
Das Projekt-Library-Büro `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/` ist tatsächlich lesbar und enthält:

- `ORIGINAL_PSTE_0.57.144.45_NICHT_INSTALLIEREN.zip`, **652952 Bytes**, SHA-256 `d3057946defc035af7abe5522c4845625c98ebd3f2cf621e1b3c5ce019f230a4`, **121 ZIP-Einträge**.
- `ORIGINAL_PSERC_0.28.69_NICHT_INSTALLIEREN.zip`, **267060 Bytes**, SHA-256 `576e58b51db3f348210dc3d47a894d6551558acc0c6900505be5e11257d2e41b`, **63 ZIP-Einträge**.
- `AKTUELLER_ARBEITSSTAND_TESTIDENTISCH_NICHT_INSTALLIEREN.zip`, **1831122 Bytes**, SHA-256 `8fc55bca1fc7e4fe019203b2c56d169a734f0c3c941b08606fa9bed6b9183e33`, **196 ZIP-Einträge**, enthält zwei originale und zwei Arbeitsverzeichnisse sowie QA-Nachweise.

**Echte ZIP-Dateien aus dem Projekt-Library-Büro materialisiert und die Prüfsummen mit dem Container neu berechnet; PHP-Quellen im Original-ZIP direkt geöffnet:**
- PSTE: `Portal SEO Topic Engine/includes/class-pste-mini-workflow.php`, `exportResults()` Zeile 298, `selectNewRows()` Zeile 332, `createBatch()` Zeile 359.
- PSERC: `portal-seo-editorial-plan-compiler/includes/class-pserc-plan-compile-job.php`, `tickCandidate()` Zeile 137, `tickSlot()` Zeile 217.

Die selbst erstellten fachlichen QA-Archive sind **keine** Installationspakete und dürfen nicht als neuer Originalstand ausgegeben werden. Die zwei originalen Plugins haben den vorher verbindlich festgelegten Ausgangsstand. **Keine ZIP geändert.**

## Unbedingt nicht verwechseln: separater PPM-Code
PPM (Produktionsmaschine 6.7.9) ist ein **anderes** Plugin. Die genannten Original-PSTE-/PSERC-ZIPs enthalten Schnittstellen zu PPM, aber nicht dessen Implementierung. Im gescannten persönlichen Library-Büro `/pferdeatelier/PLUGINS/` inkl. `QA` und `ARBEITSRAUM_PSTE_KISS` ist derzeit kein eigenständiges PPM-ZIP namentlich aufgelistet. Es gibt eine dokumentierte historische PPM-ZIP auf GitHub-Zweig `temp/dev-export-existing-ppm679-20260926`; der aktuelle GitHub-Binärleser gibt dafür keine ZIP-Bytes zurück. **Das darf nicht pauschal als fehlender Zugriff auf unsere bereits vorliegenden Ausgangs-Plugins formuliert werden.** Eine Behauptung, die tatsächliche aktuelle WordPress-PPM-Version sei geprüft, ist ohne deren echte Quellen ebenfalls nicht zulässig.

## Konsequenz
Die Arbeit an PSTE/PSERC muss **jetzt auf genau diesen ausgelesenen Originalen** fortgesetzt werden, nicht mit erneuten Anfragen an den Nutzer oder dem pauschalen Satz „keine Plugins zugänglich“. Für Eingriffe in die PPM-eigene Schreiblogik sind zusätzliche Tatsachen zum PPM-Original erforderlich; **kein neuer Speicher, keine neue Fachentscheidung, keine Zusatz-Worker.** Der vereinbarte Sollablauf bleibt bestehen: eine abschließende fachliche Entscheidung → verbindliche Reservierung vor MINI → MINI nur Titel → PSERC organisieren → K0 schreiben → WordPress-Import.

**Keine Codeänderung in diesem Quellenfund.**
