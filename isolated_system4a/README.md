# SYSTEM 4A — ISOLIERTER KAPSEL-/AUTORITÄTS-PROTOTYP

STATUS: **TEST ONLY / PRODUKTION BLOCKED / KEIN MERGE / KEIN PUBLISH**

Diese Datei ist die eine aktuelle 4A-Statuswahrheit.

## Zweck

4A ist **keine neue Textmaschine**.

Einzige Existenzfrage:

> Kann exakt die fachliche, Design-, Qualitäts- und WordPress-Kette von System 4 laufen, während Workflow-State, Route, Kontrollbindung und PASS-Verwendung technisch außerhalb der Worker-/Codex-Autorität bleiben?

Wenn nein oder nur mit neuer Signer-/Token-/Room-/Receipt-/Package-Kaskade: 4A stoppen.

## Aktuelle Vergleichsbasis

System 4 PR #238: `edfe6049768db68f85bf3babedce3199538217ef`.

Der Vergleich System 4 -> 4A enthält ausschließlich `isolated_system4a/**`. System-4-Dateien werden durch 4A nicht verändert.

Der im Nachbarweg vorbereitete/applizierte Word-Floor-Follow-up ist noch nicht auf PR #238 angekommen und wird deshalb noch nicht als aktuelle System-4-Basis behandelt.

Nicht als 4A-Vorteil gewertet:
- Artikelzahl / 1..N;
- Beitragsart;
- Fach-/Textregeln;
- Design;
- LT / PPM;
- WordPress-/V2-Handoff.

4A muss diese Punkte mindestens gleich zu System 4 beweisen.

## Verbleibender struktureller Unterschied

4A entfernt ausschließlich Steuerautorität aus dem Worker:

- äußerer Supervisor = einzige Workflow-Autorität;
- externer Fachinput enthält nur Fach-/Metadaten, keine Route/PASS/Kontrollbindung;
- `system4_root_manifest_sha256` wird vom Supervisor selbst aus den gebundenen System-4-Bytes erzeugt;
- Worker besitzt keinen Workflow-State, Authority-Key, PASS oder Publish-Recht;
- Prüfer sind read-only;
- FAIL bleibt derselbe Artikel / dieselbe Kapsel;
- Supervisor-State ist dauerhaft und HMAC-gebunden;
- Ausgang bleibt `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` -> Parent-Chat-Readback.

## Workergrenzen

Zwei technisch getrennte Wege existieren:

1. **Cross-UID-Prozessworker** außerhalb des Repositorys.
2. **Repo-loser Managed-Agent-Worker** mit genau einer persistenten Session je Artikel.

Für Managed Agents gilt zusätzlich:
- generische/self-certified Transports dürfen im Testmodus verwendet werden, aber **nicht** als Produktionsgrenze;
- Produktionsweg akzeptiert nur den strikt gebundenen Managed-Agent-Transport;
- offizielle Basis-URL ist gebunden;
- Session muss serverseitig `environment.type = none` zeigen;
- keine Vaults;
- keine Required Actions;
- Multi-Agent deaktiviert;
- exakt Websuche als Werkzeug;
- dieselbe Sessionkonfiguration wird vor weiteren Turns erneut geprüft.

## Frischer lokaler Vollkettennachweis

**Kein Codex-Lauf.**

Aktuell frisch lokal ausgeführt, mit `PYTHONWARNINGS=error`:

### Kompletter Kapsel-/Eintritt-/Ausgangsweg

**34/34 PASS**.

Positiv enthalten:
- 1 Artikel -> kompletter Weg -> Parent-Chat-Datei;
- 3 Artikel;
- 25 Artikel;
- 1000 Artikel;
- gemischte/neue Beitragsarten;
- Same-Article-Repair;
- repo-loser persistenter Managed Worker;
- roher externer Fachinput ohne Kontrollmanifest;
- Supervisor bindet Kontrollidentität selbst;
- V2-WordPress-Handoff;
- Parent-Chat-Rekonstruktion byteidentisch.

Negativ enthalten:
- Publish am Eingang;
- zusätzliches Steuerfeld im Artikel;
- zusätzliches Top-Level-Steuerfeld;
- extern eingespeistes Manifest;
- Worker-PASS/Phase-Injektion;
- Research-Fail;
- Facts-Fail;
- Context-Fail;
- Draft/Design-Fail;
- Checker-Hash-Mismatch;
- unzulässige Repair-Kontinuität;
- Batch-Fail;
- JSON-Ausgangsmanipulation;
- Parent-Chat-Inline-Manipulation;
- nicht isolierter Managed Transport;
- self-certified Fake-Transport als Produktionsgrenze;
- falsche Managed-Session-Umgebung;
- Vault-Zugriff;
- Multi-Agent;
- zusätzliche Tools;
- nicht offizielle Managed-Agent-Basis-URL.

### Zusätzliche lokale Regressionen

Separat frisch ausgeführt:
- Managed Worker: **5/5 PASS**;
- strikter Produktions-Ingress: **8/8 PASS**;
- persistenter Supervisor-State: **3/3 PASS**;
- Managed-/Cross-UID-Host + Ingress: **8/8 PASS**.

Summe dieses Zusatzsatzes: **24/24 PASS**.

### OS-Autoritätsgrenze

Lokaler Cross-UID-Test:
- erlaubter Fachkanal: PASS;
- Authority-Key lesen: BLOCK;
- Supervisor-State lesen: BLOCK;
- Authority-Key schreiben: BLOCK;
- Supervisor-State schreiben: BLOCK;
- Fake-`state.json` im Authority-Bereich erzeugen: BLOCK;
- Supervisorprozess durch Worker terminieren: BLOCK;
- Authority-Bytes nach Angriffen unverändert: PASS.

## Beweisgrenze

Die 34/34- und 24/24-Ergebnisse sind **Architektur-/Autoritäts-/Transport-Evidenz**.

Sie sind **kein Produktions-PASS für Inhalt/Design/Qualität**, weil der komplette positive lokale Lauf mit den echten hashgebundenen LT-/PPM-Abhängigkeiten noch fehlt.

Inhalt, Design und Qualität werden in 4A nicht neu definiert oder verändert. Der Produktionsadapter verweist weiterhin read-only auf die bestehenden System-4-Prüfer.

## Echter lokaler Produktionsblocker

System 4 verlangt exakt:

`LanguageTool 6.8 / Bestand 43`

Hashgebundener JAR-SHA256:

`2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8`

Dieser exakte JAR ist im aktuellen lokalen Modell-Hobbyraum nicht vorhanden.

Daher aktuell korrekt:

`FULL_CHAIN_LOCAL_PRODUCTION_REAL_LT_PPM_OVER_4A_HOST = BLOCKED:LANGUAGETOOL_6_8_HASH_BOUND_JAR_MISSING`

Kein Ersatz-JAR, kein Mock-PASS, keine synthetische LT-/PPM-Evidence.

## Codex-Regel

**Kein Codex-Lauf ohne ausdrückliche vorherige Freigabe des Users.**

Ein unmittelbar vor dieser User-Regel bereits geposteter Verifikationsauftrag wurde ausdrücklich als `CANCELLED BY USER` markiert und wird nicht als 4A-Beweis verwendet.

Aktuell:

`REAL_CODEX_4A_RUN = NOT AUTHORIZED`

## NEXT ACTION / HOBBYRAUM

1. Ausschließlich lokal weiterarbeiten.
2. Exakt den gebundenen LanguageTool-6.8-JAR und die gebundene PPM-6.7.9-Abhängigkeit lokal materialisieren und Hash prüfen.
3. Danach dieselbe **komplette** Kette lokal mit echten Prüfern positiv und negativ ausführen:

`Fachinput -> Supervisor-Ingress -> Worker -> Research -> Facts -> Context -> Draft -> echter LT/PPM-FULLCHECK -> Same-Article-Repair -> erneuter echter FULLCHECK -> Batch -> V2 -> Parent-Chat byteidentisch`

4. Erst wenn dieser lokale Realtest vollständig PASS ist, darf ein weiterer Schritt diskutiert werden.
5. Kein Codex-Auftrag ohne vorherige ausdrückliche User-Freigabe.

## Abbruchregel

Wenn System 4 State/Route/PASS ebenfalls technisch aus der Worker-Autorität entfernt, verliert 4A seinen einzigen strukturellen Vorteil und wird als eigenes Konzept beendet.

Wenn 4A dafür wieder zusätzliche Übergabe-/Signer-/Token-/Receipt-Komplexität benötigt, ebenfalls stoppen.
