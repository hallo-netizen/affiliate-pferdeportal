# Pferdeatelier – KISS: die nachgelagerte Ersatz-SEO-Prüfung entfällt

**13.11.2026 | Nur QA, nicht installieren.**

## 1. Wo war das Problem?
Der bereits abgelegte PSERC-Stand übersprang die fachliche Doppelprüfung **nur dann**, wenn die fertige PSTE-Freigabe im Fall lag. **Fehlte** sie, führte der Redaktionsplan eine **eigene zweite Suche nach Doppelungen** aus. Das widerspricht dem bestehenden C-Vertrag und der ausdrücklichen Regel: **SEO einmal zentral, später nur Technik**, keine Zusatzarchitektur.

## 2. Was wurde geändert – und warum?
**Genau drei bereits bestehende PSERC-PHP-Dateien** und **die vorhandene 61-Dateien-Integritätsliste**. Kein neuer Worker, kein neues Plugin, keine Tabelle, kein Schreibpfad.

* `class-pserc-seo-reader.php`: Ohne **finalen** PSTE-Nachweis gibt es nicht mehr `ELIGIBLE`, sondern die bereits vorhandene `HELD`-Spur mit einem eindeutigen Grund.
* `class-pserc-compiler.php`: Kein eigener SEO-Ersatzvergleich mehr. Fehlender Nachweis wird im bestehenden Review-Ergebnis zurückgestellt. Fertig freigegebene Themen behalten ihre Weitergabe.
* `class-pserc-plan-compile-job.php`: Dasselbe beim fortsetzbaren Planlauf. Auch **alte unterbrochene** doppelte Prüfungen (`EXISTING` und `PREPARED` ohne Freigabe) werden nicht weiter als SEO-Entscheider ausgeführt. Bereits freigegebene `PREPARED`-Fälle laufen weiter.
* `contracts/compiler-package-binding-v1.json`: **nur** geänderte Originaldateien nachgetragen. Kein neues Manifest.

**Wichtig:** Bei fehlender Vorentscheidung entstehen zunächst weniger fertige Artikel. Das ist kein Verlust freigegebener Themen: der Datensatz bleibt in `HELD`. Der frühere Ersatz-SEO-Entscheid war gerade das abgemachte Fehlverhalten. Erst die noch ausstehende **verbindliche Entscheidung vor MINI** kann ihn korrekt freigeben.

## 3. Originalbeweise und Ergebnisse
- Ausgangs-Archiv SHA-256 `834c4ed73e22f36ec3a0298af17766f8652cda2b9ff3a9c62b91a48a045bea4e`.
- Original PSTE 0.57.144.45 SHA-256 `d3057946defc035af7abe5522c4845625c98ebd3f2cf621e1b3c5ce019f230a4`; Original PSERC 0.28.69 SHA-256 `576e58b51db3f348210dc3d47a894d6551558acc0c6900505be5e11257d2e41b` – **nicht geändert**.
- **27/27** echte `PSERC_SEO_Reader`/Portal-Übergabetests; **15/15** echte `PSERC_Plan_Compile_Job::tickCandidate` einschließlich zwei alter unterbrochener Zustände; **11/11** echte `PSERC_Compiler::compile` einschließlich fünf K0-Felder und Beitragsart.
- **11/11** PSTE-Doppelthemen-Gegenproben; **159/159** echte bisherige 87 SEO-Quellentscheide (`61 FREI, 20 BELEGT, 6 KLÄRUNG`) mit dem aktuellen unberührten MINI-Code; **18/18** alte Gesamtsimulation mit WordPress/PPM/K0-Mocks; **126/126** PHP-Syntaxprüfungen.
- Vorher/Nachher: Der vorherige Code **enthält und ruft** `PSERC_Semantic_Duplicate_Gate::againstExisting` und `againstPreparedCandidates` bei Fällen ohne Freigabe; der neue Code stellt sie ohne diese Anrufe zurück. Im direkten PHP-Compiler-Gegentest war die alte Dublettenklasse **absichtlich nicht definiert** und der Test lief dennoch inklusive positivem freigegebenem Artikel und fünf Feldern erfolgreich.
- Der vorliegende Code-Diff beweist jede einzelne Änderung. Das Paket wurde vor der Ablage vollständig mit ZIP-CRC geprüft.

## 4. Noch offen – nicht als erledigt ausgeben
**Verbindliche reale Platzreservierung VOR MINI**, MINI nur als Titelworker, danach vollständiger WordPress-/K0-Echtlauf. Ohne PPM-Quellvertrag und echte WordPress-Schreibprobe darf aus dem **QA-Paket kein Installationspaket** gemacht werden. Kein nachgelagerter inhaltlicher Ersatzentscheider wird eingeführt.