# ZIELVERTRAG — SYSTEM 4 / MASCHINEN-PUNKT-0 + CODEX-WRITER

Status: **VERBINDLICHER AKTUELLER ZIELVERTRAG DES ISOLIERTEN SYSTEM-4-PROTOTYPS**

Er ersetzt für System 4 die frühere Annahme „Codex recherchiert selbst“. STARTMASTER0107, Textmaschine, PPM 6.7.9, LanguageTool 6.8, Design, WordPress-Plugin und Theme bleiben unverändert/read-only.

## Zielkette

`gebundene Metadaten -> Maschine erzeugt Punkt-0 -> Maschine beschafft/verifiziert reale Quellen -> Root bindet Punkt-0 -> Supervisor besitzt den Lauf -> hashgebundener Worker-Dispatch -> Facts -> Context -> Codex schreibt -> echte LT/PPM-Prüfer -> Same-Article-Repair -> Batch -> V2-Handoff -> bytegleiche Rekonstruktion`

## Verantwortungen

Die Maschine ist Eigentümer von Start, Quellenbeschaffung, Quellenintegrität, Snapshot, Root-/Manifest-/Head-Bindung, Supervisor-State, Worker-Dispatch, Prüfern, Batch und Handoff.

Codex ist **nicht** Orchestrator und **nicht** Besitzer der Web-Runtime. Codex darf keine freie Websuche zur Laufzeit verwenden. Der Worker erhält ausschließlich den vom Supervisor gebundenen Research-Pool. `controller research` muss jede ungebundene URL/Evidence fail-closed blockieren.

Codex wird im realen Lauf nur dort zugeschaltet, wo Sprach-/Denkleistung nötig ist: aus den gebundenen Quellen Fakten/Context unterstützen, den Artikel schreiben und denselben Artikel gezielt reparieren. Kein Restart bei Hardblocker.

## Punkt-0

Ein gültiger Punkt-0-Snapshot muss mindestens enthalten/binden:
- exakt den Produktionssnapshot;
- `publish_allowed=false`;
- aktuellen Root-Manifest-Hash;
- aktuellen Head;
- reale Research-Quellen mit HTTP-Erfolg, URL, Titel, Retrieval-Zeit, Evidence und SHA-256;
- Integritätshash des gesamten Punkt-0.

HTTP 401/403, leere Quelle, falscher Source-Hash, Head-/Manifest-Mismatch oder Snapshot-Tamper müssen **vor Worker-Dispatch** blockieren.

## Root / Supervisor / Worker

Root prüft und bindet Punkt-0. Der Supervisor erzeugt ein Root-Receipt und besitzt danach den gültigen Lauf. Erst daraus darf exakt ein hashgebundener Worker-Dispatch entstehen. Ohne gültiges Receipt/Dispatch darf weder Controller-Ingress noch Codex-Worker starten.

## Prüf- und Handoffregeln

Unverändert gelten:
- echtes LanguageTool 6.8;
- echter PPM 6.7.9;
- bestehende Textmaschinen-/SEO-/PSERC-/PSTE-/Link-/Metadaten-/Designregeln;
- Same-Article-Repair;
- Batch-Gate in gebundener Input-Reihenfolge;
- `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`;
- Inline-Pack/Unpack mit SHA-/Schema-/Bytegleichheit;
- kein Merge, kein Publish ohne separate Freigabe.

## Testpflicht

Jede Änderung muss lokal positiv und negativ gegen den Gesamtworkflow geprüft werden. Bekannte historische Fehler bleiben verpflichtende Regressionen. Ein Codex-Produktionslauf ist erst zulässig, wenn exakt der aktuelle Remote-Head diese Tests bestanden hat und der Hardlock auf genau diesem Head SUCCESS ist.
