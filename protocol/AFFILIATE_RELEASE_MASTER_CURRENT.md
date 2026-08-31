# AFFILIATE-ZENTRALE — CURRENT MASTER / HANDOFF

Stand: 2026-08-31
Branch: `affiliate-release-current`
Workstream: `AFFILIATE_ZENTRALE`
Governance: `PFERDE_ATELIER_AFFILIATE_RELEASE_GOVERNANCE_V4`
Candidate: `6.64.0` / `WORKING` / `release_allowed=false`

## Autoritative Quelle

Nur `release/affiliate-zentrale/current/affiliate-portal-router/` plus `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt` ist aktuelle Release-Quelle. Historische ZIPs, alte Chatstände und Archive sind keine Navigations- oder Rekonstruktionsquelle. Bereits hash-identisch bestandene eBay-Gates werden nicht erneut ausgeführt.

## Grundsätzlicher Arbeitsablauf für ChatGPT / GitHub / Codex — VERBINDLICH

Dieser Abschnitt ist für alle folgenden Arbeiten im Workstream verbindlich und soll in neuen Chats zuerst beachtet werden.

1. **GitHub ist Arbeits- und Übergabequelle.** Technische Aufträge, Zielverträge, Evidence und Master werden im Repository dokumentiert. Lokale Chat-Anhänge sind keine dauerhafte Workflow-Autorität.
2. **Codex arbeitet repository-nativ.** Codex bekommt im Normalfall **keine hochzuladenden Dateien, keine ZIPs und keine riesigen Quelltext-Prompts**. Es arbeitet aus dem verbundenen GitHub-Repository.
3. **Vor jedem Codex-Auftrag wird zuerst ein klarer Auftrag im Repo angelegt**, vorzugsweise unter `protocol/AFFILIATE_RELEASE_*.md`. Dieser Auftrag enthält Scope, Zielzustand, erlaubte Dateien/Pfade, Positiv-/Negativtests, Fail-closed-Regeln und erwartete Endausgabe.
4. **Der Nutzer bekommt für Codex nur einen kurzen Startprompt**, der Repository, Branch und exakten Auftrags-Pfad nennt. Beispielprinzip: `Lies zuerst CURRENT_RELEASE.json und führe danach vollständig <TASK_REF> aus.`
5. **Keine Datei-Upload-Anforderung an Codex erfinden.** Wenn Source bereits im Repo existiert oder dort reproduzierbar aus der aktuellen kanonischen Source implementiert werden kann, muss Codex direkt im Repo arbeiten.
6. **Keine Riesen-Copy/Paste-Prompts mit vollständigen Dateien**, solange der Repo-native Weg möglich ist. Quelltext im Chat ist nur zulässig, wenn GitHub technisch wirklich nicht genutzt werden kann und dies vorher nachgewiesen wurde.
7. **Vor jeder Arbeit zuerst Governance lesen:** `control/release-governance/CURRENT_RELEASE.json`. Danach ausschließlich den dort autorisierten Workstream, Branch, Scope und nächsten Schritt verwenden.
8. **Keine Navigation aus alter Chat-Historie.** Alte Chats dienen höchstens als Kontext; autoritativ sind aktueller Master, Governance, aktuelle Source und gebundene Evidence im Repo.
9. **Keine Wiederholung bestandener hash-identischer Gates.** Bereits bestandene eBay-/Release-Gates werden wiederverwendet und nicht vorsorglich neu ausgeführt.
10. **Keine Nebenarchitektur, kein Side-Branch, keine Pluginorgie, kein Microfix ohne gebundenen Grund.** Änderungen werden soweit sinnvoll gebündelt und direkt gegen den Gesamtworkflow geprüft.
11. **Vor jeder Behauptung `PASS`, `fertig`, `integriert` oder `auf GitHub` wird der tatsächliche Repository-Stand erneut gelesen.** Dokumentation allein gilt nicht als Source-Binding.
12. **Source-Binding muss real im kanonischen Baum erfolgt sein.** Master/Evidence dürfen einen lokalen Kandidaten beschreiben, aber solange die Source-Dateien nicht im kanonischen GitHub-Baum liegen, darf kein Source-/Live-PASS behauptet werden.
13. **Manifest und Governance werden erst nach tatsächlicher Source-Änderung neu gebunden**, nie vorzeitig und nie auf nur lokal vorhandene Kandidaten.
14. **Wenn Codex einen Auftrag ablehnt**, zuerst die echte Ursache prüfen: Repo-Verbindung, Branch, Task-Scope, Promptgröße/Format oder Rechte. Nicht sofort neue ZIP-/Upload-/Copy-Paste-Routen erfinden.
15. **Wenn ein GitHub-Connector die Änderung selbst sauber und vollständig ausführen kann**, darf die Änderung direkt über GitHub erfolgen; danach sind Source, Manifest, Governance und Master konsistent zu aktualisieren und erneut zu prüfen.
16. **Der Nutzer soll nur dann eingreifen müssen, wenn eine echte externe Nutzerhandlung erforderlich ist** (z. B. Login/Freigabe/Live-Zugang, den die Werkzeuge nicht besitzen). Keine vermeidbaren Datei-Transfers oder manuellen Zwischenschritte.
17. **Jede Übergabe dokumentiert:** Was geändert wurde, was nicht geändert wurde, welche Tests PASS/FAIL sind, welche Hashes/Commits gelten, was live noch offen ist und exakt welcher nächste gebundene Schritt folgt.

### Standard-Codex-Startprompt

Wenn ein im Repo gebundener Auftrag existiert, ist der Nutzerprompt grundsätzlich kurz zu halten:

```text
Arbeite im Repository hallo-netizen/affiliate-pferdeportal
auf dem gebundenen Branch.

Lies zuerst control/release-governance/CURRENT_RELEASE.json.
Führe danach vollständig und ohne Scope-Erweiterung aus:
<EXAKTER_TASK_REF_IM_REPOSITORY>

Implementieren, lokal positiv/negativ testen, erforderliche Source-/Manifest-/Governance-Bindung durchführen und committen.
Keine bereits hash-identisch bestandenen Gates wiederholen.
```

Abweichungen von diesem Ablauf müssen technisch begründet und im Master dokumentiert werden. Bequemlichkeit oder Chatwechsel sind kein Grund für eine neue Übergaberoute.

## Aktueller Funktionsstand

- eBay: bestehender freigegebener/gebundener Stand bleibt unverändert; keine Wiederholung der bestandenen historischen Gates.
- idealo: bestehende Produkt-/Vergleichsquelle bleibt unverändert.
- Produkt-/Deal-Radar und Partner-Analytics: Bestandteil des V6.64.0-Kandidaten; gesamter Release-Gate weiterhin PENDING.
- Lead Alliance: vom Nutzer am 31.08.2026 als bestätigt gemeldet. Für Kaufland ist der technische Zielweg `Lead Alliance / Kaufland Private Network` gebunden; keine ADCocktail-Ersatzroute. Diese Bestätigung wird nicht als erfundene Kaufland-Programm-/Feedfreigabe ausgelegt: konkrete Publisher-/Produktdaten werden erst aktiviert, wenn der reale Zugang dies bestätigt.
- Kelkoo: noch nicht freigegeben; vorbereitet, nicht live verdrahtet.
- Amazon: vorbereitet; kein erfundener Datenzugang.
- Digistore24: bestehender read-only Provider wird im aktuellen Block weiter automatisiert; weiterhin Banner-only.

## Digistore24 — gebundener Automatisierungsstand

1. Der API-Zugang bleibt read-only. Neben `getUserInfo`, `listMarketplaceEntries` und `getMarketplaceEntry` ist `getAffiliateCommission` erlaubt.
2. `getAffiliateCommission` darf nur die mit dem aktuell getesteten API-Key gebundene eigene Affiliate-ID und 1–50 kanonische numerische Produkt-IDs abfragen.
3. Automatische Veröffentlichung erfordert einen frischen API-Nachweis `approval_status=approved` plus aktives Produkt. Pending, rejected, fehlende Zeile, Credential-Wechsel oder veralteter Nachweis bleiben fail-closed.
4. Manuelle Partnerschaftsbestätigung bleibt nur Fallback für manuellen Import; sie kann die automatische Veröffentlichung nicht freischalten.
5. Die Vendor-Support-/Werbemittelseite wird pro interessantem Marketplace-Eintrag einmal als validierte HTTPS-URL gespeichert. Danach darf der zentrale Automationslauf sie erneut verwenden.
6. Importiert werden ausschließlich reale Banner mit provisionssicherem Digistore24-Trackinglink und gültiger HTTPS-Bildquelle. Keine Produkt-/Listing-Ausgabe für Digistore24.
7. Ziel und Slot werden nicht in Digistore24 neu erfunden, sondern durch das bestehende zentrale Output-Modell klassifiziert.
8. Vor automatischer Aktivierung wird das komplette Output-Objekt erneut geprüft. Ein neues Digistore24-Banner bleibt zunächst inaktiv/draft und darf Last-Known-Good nicht verdrängen.
9. Erst nach erfolgreicher Revalidierung und persistierter `published`-Markierung wird ein Konfliktobjekt abgelöst. Bei Persistenzfehler wird die Kampagne zurückgerollt.
10. Ein früherer generischer Banner-Aktivator kann den Digistore-Sicherheitsvertrag nicht umgehen: die spätere provider-spezifische Schlussprüfung rollt nicht freigegebene Kandidaten vor Request-Ende wieder auf inactive/draft zurück.

## Testnachweis des lokalen Kandidaten

Evidence: `release/affiliate-zentrale/evidence/digistore24_automatic_partner_banner_gate_v6640_static.txt`

Lokal PASS: PHP-Lint beider Kandidaten-Traits; exakter GET-Request; fremde Affiliate-ID blockiert; >50 Produkt-IDs blockiert; approved positiv; pending negativ; stale negativ; atomare Aktivierung positiv; DB-Commit-Rollback negativ; Two-Phase-Supersede positiv; früher generisch aktivierter unapproved Kandidat wird zurückgerollt.

Wichtig: Dieser Nachweis beschreibt den lokal getesteten Zielvertrag. Die beiden geänderten PHP-Dateien sind noch **nicht** Bestandteil der autoritativen GitHub-Source. Deshalb darf aus den Kandidaten-Hashes noch kein Release- oder Live-PASS abgeleitet werden.

## Korrigierter Codex-/GitHub-Übergabeweg

Der frühere Attachment-/Riesenprompt-Weg ist verworfen und im Repository ausdrücklich als `DEPRECATED` markiert.

Verbindlicher repository-nativer Auftrag:

`protocol/AFFILIATE_RELEASE_CODEX_DS24_IMPLEMENT_FROM_REPO_20260831.md`

Codex benötigt dafür keine lokale Datei, kein ZIP und keinen eingefügten Quelltext. Es arbeitet aus dem verbundenen Repository, liest Governance, Master, Evidence und die aktuellen Source-Dateien und implementiert den gebundenen Digistore-Zielvertrag direkt im aktuellen Baum.

## Noch offen vor Release

- Repository-native Implementierung der Digistore24-Automatisierung in der kanonischen Source.
- Neu berechnetes 25-Dateien-Source-Manifest und passende Governance-Bindung.
- Danach echter Live-Nachweis mit dem realen Digistore24-Konto und der realen WordPress/MariaDB-Installation.

Bis dahin bleibt `release_allowed=false` und der gebundene Gesamtgate `explicit_scope_product_deals_partner_analytics` PENDING. Keine finale Release-ZIP vor dem finalen Gate.

## Aktuell autorisierter nächster Schritt

Repository-nativen Auftrag `protocol/AFFILIATE_RELEASE_CODEX_DS24_IMPLEMENT_FROM_REPO_20260831.md` gegen die aktuelle kanonische Source ausführen. Nach Source-/Manifest-/Governance-PASS unmittelbar den realen Digistore24-Livegate durchführen: read-only Verbindung, Marketplace-Daten, `getAffiliateCommission`, mindestens ein realer approved/active Partner bzw. korrektes Fail-closed bei keinem approved Partner, reale Werbemittel-URL/Banner, Bildprüfung, automatische Ziel-/Slot-Zuordnung und veröffentlichter/rollbackfähiger Endzustand. Danach nur den bereits gebundenen Release-Gate weiterführen.