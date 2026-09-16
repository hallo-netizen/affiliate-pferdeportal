# ZIELVERTRAG — SYSTEM 4 / POINT-0 V2 + CODEX-WRITER

Status: **verbindliche aktuelle System-4-Architektur**.

## Zielkette

`Chat-Rohauftrag → Maschine bindet Metadaten/Slot/Kategorie/Links/Textschienen → Maschine beschafft/verifiziert je Artikel reale Quellen → Point-0 V2 → Root → Supervisor → hashgebundener Worker-Dispatch → Codex: fachliche Recherche aus genau diesem Pool → Facts → Context-Ergänzung ohne Schienenänderung → Codex-Text → echtes LT 6.8 → echter PPM 6.7.9 → Same-Article-Repair → Batch → V2-Handoff → 107008 Final Review/Output Release → gebundener Chat-Delivery-Transport → bestehendes PSERC-Import-Envelope + Recovery-Manifest → signierter GitHub-ENDSTEMPEL → reale WordPress-Importformat-Prüfung → bytegleiche finale Importdatei im Parent-Chat`

## Alleinige Maschinenautorität vor Codex

Vor Worker-Start müssen für **jeden Artikel** bereits unveränderlich gebunden sein:
- Titel, Target Keyword, Artikeltyp und `plan_slot`;
- WordPress-Kategorie;
- verbindliche interne Links einschließlich Rolle, Ziel, Anchor und Abschnitt;
- `quality_binding` / Textmaschinen-Schienen;
- eigener artikelbezogener Research-Pool;
- Root-Manifest und Git-Head;
- `publish_allowed=false`.

Point-0-Vertrag: `SYSTEM4_POINT0_SNAPSHOT_V2`.

Jeder Artikel besitzt einen eigenen Quellenpool. Ein globaler Sammelpool für den ganzen Batch ist unzulässig. HTTP 401/403, leere Evidenz, falscher Hash, Pool-/Index-/Slot-Mismatch, Head-/Manifest-Mismatch oder Prewrite-Tamper blockieren **vor** Codex.

## Codex-Rolle

Codex ist fachlicher Worker, nicht Orchestrator. Er darf:
- den gebundenen artikelbezogenen Quellenpool fachlich auswerten;
- daraus Facts bilden;
- nur faktabhängige Context-Angaben ergänzen;
- innerhalb des maschinengebundenen Schreibvertrags formulieren;
- ausschließlich denselben Artikel nach einem konkreten Repair-Befund reparieren.

Codex darf **nicht** Route, Slot, Kategorie, Links, Quality-Binding, Prüfer, PASS, Publish-Status oder Research-Pool ändern und keine freie Websuche starten.

## Prüfer und Ausgang

Unverändert und allein entscheidend:
- echtes LanguageTool 6.8, SHA-gebunden;
- echter PPM 6.7.9, SHA-gebunden;
- bestehender Authoring-/Content-/Design-Guard;
- kompletter Batch-Gate in Input-Reihenfolge;
- `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`;
- Canonicalize → Inline-Pack → Inline-Unpack → Bytegleichheit;
- real gebundener bestehender PSERC-/ENDSTEMPEL-Importweg;
- reale WordPress-Importformat-Prüfung unmittelbar vor der Parent-Chat-Dateiausgabe;
- Byte-/SHA-Identität der ausgegebenen Datei mit der unmittelbar zuvor geprüften Finaldatei.

Der rohe `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` ist **kein** direkter WordPress-Importvertrag. Er darf weder `WORDPRESS_DIRECT_IMPORT` noch `direct_wordpress_upload_ready=true` begründen. Die bestehende signierte PSERC-/ENDSTEMPEL-Grenze bleibt zwingend.

Kein Worker und kein Chat darf PASS behaupten; PASS entsteht nur aus den echten Prüfern/Gates. Kein Merge und kein Publish ohne separate Freigabe.

## 1..N

Der Produktionssnapshot ist die einzige Batch-Wahrheit. Jeder endliche Batch `1..N` durchläuft denselben Root/Supervisor/Controller/Batch/Handoff- und nachgelagerten Stempel-/Importweg. Artikelindex, `plan_slot`, Quellenpool und Prewrite-Bindung müssen exakt zusammengehören. Kein Artikel darf fehlen, ersetzt, dupliziert oder umsortiert werden.

Historische Dateinamen mit `7` dürfen aus Kompatibilitätsgründen bestehen bleiben, solange sie **keine Mengenautorität** besitzen. Mengenautorität entsteht ausschließlich aus dem gebundenen Release-/Source-Manifest und muss `article_count >= 1` exakt erfüllen.

## Verbindliche Testpflicht

Die Abschlussstrecke muss den Liveweg verwenden, nicht eine vereinfachte Parallelstrecke. Nur Codex darf im Test durch einen deterministischen Testworker ersetzt werden; Root, Supervisor, Dispatch, Controller, echte LT-/PPM-Prüfer, Repair, Batch, Handoff, bestehender PSERC-/ENDSTEMPEL-Weg und WordPress-Importformatprüfung bleiben identisch.

Pflichtregressionen umfassen mindestens: Chat-/Manifest-Bindung, Head/Checkout, 401/403, Point-0-Tamper, Index/Slot/Pool-Verwechslung, Dispatch-Tamper, freie Webfreigabe, Prewrite-/Link-/Kategorie-Tamper, ungebundene Research/Facts, unbekannter PPM-Vertrag, Wortminimum, Design-/Link-/Fact-ID-Verstöße, zu großer Repair, Batch-Reihenfolge/-Vollständigkeit, Handoff-/Inline-Tamper, Mengen-Mismatch, Null-Batch, Import-Envelope-/Manifest-Hashfehler, Signatur-/Identitätsfehler und abweichende Parent-Chat-Dateibytes.

## Harte Abschlussgrenze

Ein grüner lokaler oder Remote-Lauf bleibt Testkandidat. Ein **Gesamt-PASS** ist erst zulässig, wenn dieselbe finale, real formatgeprüfte WordPress-Importdatei tatsächlich im Parent-Chat als Datei ausgegeben wurde und deren Bytes/SHA-256 mit der unmittelbar zuvor geprüften Finaldatei identisch sind. Bis dahin bleiben `publish_allowed=false` und die Produktionsfreigabe offen/blockiert.
