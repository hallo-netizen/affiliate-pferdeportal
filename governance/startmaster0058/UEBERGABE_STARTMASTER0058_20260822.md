# AUSFÜHRLICHE ÜBERGABE – STARTMASTER0058

Stand: 2026-08-22

## A. SOFORTIGER AUSGANGSZUSTAND

1. Der letzte Produktionslauf umfasste exakt fünf Beratung-Beiträge: Boxengitter, Gebisse, Hafer, Striegel, Winterdecken.
2. Supervisor PASS, PPM 6.7.9 PASS, fünf WordPress-Drafts erzeugt, Readback PASS, Publish im Produktionslauf gesperrt.
3. Der Nutzer hat die fünf Beiträge anschließend manuell veröffentlicht.
4. Der danach neu aufgebaute SEO-Redaktionsplan zeigt **Metadaten-Handoff bereit: 0** und **keinen aktuellen READY-Metadatenblock**. Damit sind die fünf Positionen aus dem nächsten Produktionshandoff verschwunden.
5. Die fünf veröffentlichten Beiträge sind ab diesem Nullpunkt Bestandsschutz und dürfen weder erneut produziert noch still verändert werden.

## B. INSTALLIERTER TECHNISCHER STAND

- PSTE 0.56.4
- PSERC 0.28.3
- PPM 6.7.9
- Link Policy Gate 1.0.1

PSERC 0.28.3 ist installiert. Kein Rollback ist Teil dieses Übergabestands. Der Supervisor-Keyring enthält Legacy-Trust und Active-Trust; private Schlüssel liegen nicht in der MASTER.

## C. WAS HEUTE FALSCH GELAUFEN IST UND NIE WIEDER PASSIEREN DARF

- Der vorhandene V2-Signer/Signierpfad wurde nicht früh genug als bestehende Architektur behandelt; dadurch entstand unnötiges Risiko eines neuen Plugin-Updates.
- Nach Installation wurde die aktuelle UI zunächst anhand eines unvollständigen/alten Sichtzustands falsch interpretiert.
- Es wurden fälschlich drei Einzeldateien als erforderlicher Upload genannt, obwohl der installierte Produktionsstart bereits eine einzige hashgebundene Produktionspaket-Datei verlangte.
- Ein alter Screenshot-Zustand wurde kurzzeitig als aktueller Redaktionsplan-Zustand ausgelegt.
- Zu viele historische/statische Prüfungen wurden wiederholt, obwohl ihre Hashes unverändert waren. Das erhöhte Laufzeit und Fehlerrisiko, ohne zusätzliche Sicherheit zu schaffen.

Daraus folgt: **Keine Installations-, UI-, Upload- oder Workflow-Anweisung aus Chatgedächtnis. Vor jeder Nutzeraktion muss der aktuelle Source-/Contract-/Live-Beleg den konkreten Schritt beweisen.**

## D. NEUER SCHNELLER PRODUKTIONSWORKFLOW

### D1 – Einmaliger Run-Bootstrap

Pro Produktionslauf genau einmal: MASTER/SHA laden, Plugin-/Contract-Versionen und Hashes lesen, aktuellen Live-Inventar-/Plan-Snapshot erzeugen, aktuellen Titel-/Dubletten-/Kannibalisierungskorpus aufbauen, CURRENT-POINTER schreiben.

### D2 – Titelphase upstream

Alle neuen Titel eines Batches werden gegen denselben eingefrorenen Bestand geprüft. Keine erneute Vollinventarabfrage je Titel.

Harte Bedingungen: natürliches Deutsch; Intent/Keywordbedeutung unverändert; keine Suchmaschinen-Rohphrase; kein Keyword-Stakkato; keine Generatorformulierung; keine stereotype Phrasenfamilie im Batch oder gegen den Bestand; insbesondere keine Serien aus „richtig auswählen“, „passend auswählen“, „gezielt auswählen“, „nach wichtigen Kriterien auswählen“ oder semantisch gleichförmigen Varianten; kein PASS, wenn keine natürliche eindeutige Variante gefunden wird.

### D3 – Statische Belege wiederverwenden

Nur bei exakter Hashidentität und vollständigem vorhandenen PASS-Beleg. Kein erneuter Volltest aus Gewohnheit.

### D4 – Dynamische Gates frisch

Live-Inventar/READY, Dubletten/Kannibalisierung, Supervisor, Signatur/Package, Request Identity/Replay, PPM, WordPress-Readback und Publish-Lock bleiben frisch und fail-closed.

### D5 – Forschung/Fact-Packs/LanguageTool

Unabhängige Positionen dürfen parallel vorbereitet werden; Provenienz bleibt strikt getrennt. LanguageTool wird nur für den finalen sichtbaren Text ausgeführt und nur bei Contentänderung erneut. Quellen dürfen nur dann wiederverwendet werden, wenn Vertrag/Freshness/Hash dies ausdrücklich erlauben.

### D6 – Ein Produktionspaket

Der installierte kontrollierte Produktionsstart arbeitet mit einer freigegebenen, hashgebundenen Produktionspaket-Datei. Keine Rückkehr zu drei Einzeluploads, solange der aktuelle Contract nicht ausdrücklich etwas anderes verlangt.

## E. WELCHE PRÜFUNGEN ENTFALLEN ALS WIEDERHOLUNG

Die Prüfung selbst wird nicht abgeschafft; ihre unnötige erneute Ausführung wird abgeschafft: vollständige MASTER-Manifestprüfung nur bei Masterbau/Transfer oder Hashänderung; Source↔Installer-Parität nur bei Source-/Installeränderung; PHP-Syntax/Package-Integrität nur bei Code-/Installeränderung; historische Vollregression nur bei betroffener Code-/Contractänderung; statische Contract-/Schema-Prüfungen einmal pro Hash; LanguageTool nicht erneut bei identischem finalem sichtbaren Text-Hash; Recherche-/Fact-Pack-Belege nur erneut, wenn Hash/Freshness dies verlangt; Live-Inventar einmal pro unveränderter Inventory Revision.

## F. WAS IMMER FRISCH BLEIBT

Aktueller WordPress-Bestand nach Draft/Publish; READY-/Plan-Snapshot und Inventory Revision; Batch-Identität und Plan-Slot-Bindung; Titel-Dubletten-/Kannibalisierungsprüfung gegen aktuellen Bestand; Package Hash/Tamper/Signature; Supervisor-Freigabe; Request Identity, Replay, Double Submit, Lease/Resume; PPM-Write; Draft-/Publish-Status und Readback; keine unerlaubte Änderung bestehender Beiträge.

## G. NÄCHSTER CHAT – EXAKTER START

Ein neuer Chat liest zuerst: `00_READ_FIRST_STARTMASTER0058.md`, `CURRENT_POINTER_STARTMASTER0058_20260822.json`, diese Übergabe, Prüfungsabbauvertrag, Titelqualitäts-Hardlock, Fehlerkatalog, Arbeitsprotokoll. Erst danach – falls eine technische Änderung nötig ist – konkret relevanten Source und konkrete GitHub-Historie. Keine allgemeine Rekonstruktion des Projekts.

## H. OFFENER TECHNISCHER PUNKT

Die allgemeine Titelregel gegen stereotype Phrasen existierte bereits in der MASTER, war im beobachteten Beratungsbatch aber nicht ausreichend wirksam. STARTMASTER0058 macht sie für **alle künftig neu erzeugten Titel aller Beitragsarten** zum allgemeinen upstream Hardlock.

Dieser Governanceblock ändert keinen Plugin-Code. Vor dem nächsten neuen Titelbatch muss die vorhandene upstream Titelprüfung nachweislich diesen Batch-/Bestands-Phrasencheck technisch durchsetzen. Eine Sourceänderung dazu ist ein separater, eng begrenzter Reparaturblock mit Positiv-/Negativtests und Gesamtworkflow-Regression. Die Textmaschine selbst bleibt unverändert.
