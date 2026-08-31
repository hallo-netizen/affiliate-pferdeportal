# AFFILIATE-ZENTRALE — AUSFÜHRLICHE ÜBERGABE FÜR NEUEN CHAT

Stand: 2026-08-31
Repository: `hallo-netizen/affiliate-pferdeportal`
Aktiver Workstream: `AFFILIATE_ZENTRALE`
Aktiver Branch: `affiliate-release-current`
Candidate: `6.64.0`
Status: `WORKING`
Release erlaubt: `false`

## 0. VERBINDLICHER EINLASS FÜR JEDEN NEUEN CHAT

Vor jeder technischen Aktion ausschließlich in dieser Reihenfolge lesen:

1. `control/release-governance/CURRENT_RELEASE.json`
2. `protocol/AFFILIATE_RELEASE_MASTER_CURRENT.md`
3. diese Übergabe `protocol/AFFILIATE_RELEASE_HANDOFF_NEW_CHAT_20260831.md`
4. danach nur den im Master/Governance aktuell gebundenen Affiliate-Schritt.

HARDLOCK:

- Aktiver Workstream bleibt `AFFILIATE_ZENTRALE`, bis der Nutzer ausdrücklich einen Workstream-Wechsel anordnet.
- Einzelne fremde Tokens, Fehlercodes, Screenshots oder Dateinamen sind KEIN Themenwechsel.
- Insbesondere `107007_*`, `STARTMASTER0107`, H7/H8 oder Textproduktions-Tokens dürfen diesen Affiliate-Chat nicht automatisch in einen anderen Workflow ziehen.
- Vor jedem GitHub-/Codex-Schritt Zielpfad gegen `AFFILIATE_ZENTRALE` prüfen.
- Keine alte Chat-Historie als Workflow-Navigation verwenden.
- Keine bestandenen hash-identischen eBay-Gates wiederholen.
- Keine neue Architektur, kein Side-Branch, keine Pluginorgie, kein Microfix ohne gebundenen Grund.
- Keine Behauptung `PASS`, `fertig`, `integriert`, `auf GitHub` ohne erneutes Lesen des realen Repository-Standes.

Kurzform: **WORKSTREAM VOR TOKEN. MASTER VOR CHAT-HISTORIE. SOURCE VOR DOKUMENTATION. KEIN RERUN BESTANDENER GATES.**

---

# 1. ZIELVERTRAG GESAMTSYSTEM

## 1.1 Grundziel

Die Affiliate-Zentrale soll ein möglichst weit automatisiertes, dauerhaft betreibbares Affiliate-System für das Pferde-Atelier bilden. Es soll Produkte und Banner getrennt behandeln, Quellen sauber priorisieren, automatisch zuordnen, nur geprüfte Werbemittel ausspielen und bei Fehlern fail-closed bleiben.

## 1.2 Harte Trennung PRODUKTE vs. BANNER

### Produkt-/Deal-Quellen

Diese Quellen dienen der Bewerbung konkreter Produkte, Produktvergleichen und später den `Mega-Kracher-Angeboten`:

- eBay
- idealo
- OTTO
- Kaufland
- Kelkoo
- Amazon ganz am Ende

Diese Quellen sind **keine generischen Banner-Netzwerke** im Zielbild.

### Banner-/Partnerquellen

Diese Quellen dienen primär dazu, vorhandene Bannerplätze automatisch und passend zu befüllen:

- Awin
- ADCELL
- ADCocktail
- Digistore24
- weitere geeignete Partner-/Affiliate-Netzwerke oder Direktpartner

Digistore24 bleibt im aktuellen Zielvertrag ausdrücklich **banner-only**.

## 1.3 Wirtschaftliche Priorisierung

Nicht stumpf die höchste Prozentprovision wählen. Ziel ist realer wirtschaftlicher Ertrag bei gleichzeitig gutem Nutzerangebot.

Grundprinzip:

- Produktrelevanz / Themenpassung ist Pflicht.
- Für Produktangebote zählen Preis/Angebotsqualität, Verfügbarkeit, Datenqualität, Trackbarkeit und reale Wirtschaftlichkeit.
- Wenn Angebote für den Nutzer praktisch gleichwertig sind, darf der wirtschaftlich stärkere Partner priorisiert werden.
- Reale Partner-Performance soll langfristig stärker gewichtet werden als reine Nominalprovision.
- Bei `Mega-Kracher-Angeboten` darf keine hohe Provision ein objektiv schlechteres Nutzerangebot erzwingen.

## 1.4 Gesamt-Abdeckung statt eBay-Alleinabdeckung

eBay muss **nicht** jede Produktfamilie alleine abdecken. Ziel ist gemeinsame Portalabdeckung über alle Produktquellen. Eine Produktfamilie kann durch eBay, idealo, OTTO, Kaufland, Kelkoo oder später Amazon versorgt werden. Besser sind mehrere seriöse Quellen pro Familie, sofern echte Vergleichbarkeit besteht.

## 1.5 Mega-Kracher-Konzept — Zielbild

Der bereits vorhandene V6.64.0-Deal-Radar/Partner-Analytics-Ansatz soll innerhalb der bestehenden Architektur ausgebaut werden, nicht als neues Subsystem.

Ein `Mega-Kracher` soll kein beliebiges rabattiertes Produkt sein, sondern ein belastbar starkes Angebot. Provider-neutral zu normalisieren sind mindestens:

- eindeutige Produktidentität, idealerweise EAN/GTIN oder andere stabile Produkt-ID,
- Titel,
- Bild,
- aktueller Preis,
- Versandkosten / Gesamtpreis soweit verfügbar,
- Verfügbarkeit,
- Affiliate-trackbare Ziel-URL,
- Datenfrische,
- belastbare Vergleichs-/Referenzbasis.

Keine `UVP-Ersparnis` behaupten, wenn die Referenz keine echte UVP ist.

Ausspielung später bevorzugt als ein Hauptangebot plus maximal sinnvolle Alternativen; keine unübersichtliche Wand aus fünf gleichwertigen Karten.

---

# 2. PARTNER-/PROVIDER-STATUS

## 2.1 eBay

Status des zuletzt real geprüften Gesamtlaufs:

- gleicher Run nach Same-UUID-Recovery bis `completed` gelaufen,
- WordPress zeigte `Fertig (mit übersprungenen Fehlern)`,
- sicherer Frontend-Checkpoint wurde übernommen,
- 771 Pakete sichtbar,
- der Lauf darf nicht einfach neu gestartet werden,
- `completed_with_skips` bedeutet: candidate-lokale Einzelprobleme wurden protokolliert/übersprungen; globale Sicherheits-/Checkpoint-Fehler bleiben fail-closed.

Wichtig: Abschluss des Runs ist **nicht** gleichbedeutend mit 100% BUSINESS-Abdeckung. Sichtbar waren 92/311 BUSINESS-Familien, 219 fehlend. Mit zusätzlichen Produktquellen ist das kein Zielbruch; Ziel ist Gesamt-Abdeckung.

**Regel für neuen Chat:** eBay nicht vorsorglich erneut laufen lassen und keine bereits bestandenen hash-identischen eBay-Gates wiederholen.

## 2.2 idealo

- bestehende Produkt-/Vergleichsquelle,
- im Affiliate-System bereits Teil des Produktquellen-Zielbilds,
- keine Änderung im aktuellen Digistore-Block.

## 2.3 OTTO

- soll als Produktquelle direkt vorbereitet sein,
- fachlich im Backend als `OTTO` führen, auch wenn technischer Affiliate-Zugang über ein Netzwerk erfolgt,
- noch keine erfundene Live-Datenquelle/Feedfreigabe behaupten.

## 2.4 Kaufland

Korrektur eines früheren Fehlers:

- Kaufland **nicht** über ADCocktail fest verdrahten.
- Der aktuelle Zielweg ist `Lead Alliance / Kaufland Private Network`.
- Lead Alliance wurde vom Nutzer als bestätigt gemeldet.
- Diese Bestätigung ist noch nicht automatisch gleichbedeutend mit verifiziertem Publisher-Produktfeed/API-Zugang für Kaufland.
- Kaufland ist Produktquelle, nicht Bannerquelle.

## 2.5 Kelkoo

- noch nicht freigegeben,
- technisch vorbereiten, aber ohne erfundene Credentials/Feedverträge,
- Produkt-/Preisvergleichsquelle im Zielbild.

## 2.6 Amazon

- ganz am Ende integrieren,
- technisch vorbereiten erlaubt,
- keine erfundene API-/PA-API-Freigabe,
- Produktquelle, nicht Teil des aktuellen Digistore-Blocks.

## 2.7 ADCocktail

- Nutzerkonto wurde angelegt,
- als Banner-/Partnernetzwerk im Zielbild,
- **nicht** als Kaufland-Zugang behandeln,
- reale Provider-Schnittstelle erst auf Basis echter Account-/API-Möglichkeiten integrieren.

## 2.8 Digistore24

WICHTIG: Digistore24 war **bereits verbunden und eingebunden**. Es darf in einem neuen Chat **nicht** wieder bei API-Key-Einrichtung oder Erstverbindung begonnen werden.

Aktuelles Ziel:

- vorhandene read-only Verbindung weiterverwenden,
- Marketplace automatisch auswerten,
- relevante Partner/Produkte erkennen,
- echte Partnerschaft per `getAffiliateCommission` prüfen,
- reale Vendor-Banner importieren,
- Bilder/Tracking prüfen,
- automatisch thematisch und technisch passendem Portalziel/Slot zuordnen,
- nur nach vollständiger Revalidierung automatisch veröffentlichen,
- Last-Known-Good nicht durch einen ungeprüften Draft verdrängen.

---

# 3. DIGISTORE24 — TECHNISCHER ZIELVERTRAG

## 3.1 API

Read-only bleibt verbindlich.

Bestehende Methoden:

- `getUserInfo`
- `listMarketplaceEntries`
- `getMarketplaceEntry`

Zusätzlich gebunden:

- `getAffiliateCommission`

Für `getAffiliateCommission`:

- nur aktuell getestete eigene `affiliate_id`,
- 1 bis 50 kanonische numerische `product_ids`,
- fremde Affiliate-ID vor Netzwerkzugriff blockieren,
- 0 IDs, fehlerhafte IDs oder >50 IDs vor Netzwerkzugriff blockieren,
- Nachweis an getesteten API-Key-Fingerprint binden.

Genutzte dokumentierte Felder:

- `product_id`
- `product_is_active`
- `approval_status`
- `commission_rate` soweit vorhanden

Keine erfundenen Felder.

## 3.2 Automatische Partnerschaftsfreigabe

Automatische Veröffentlichung nur bei frischem Nachweis:

- `approval_status=approved`
- `product_is_active=true`
- gleicher getesteter Credential-Fingerprint
- gleiche eigene Affiliate-ID

Fail-closed bei:

- `pending`
- `rejected`
- `new`
- fehlender Commission-Zeile
- inaktivem Produkt
- stale proof
- Credential-Wechsel
- Affiliate-ID-Mismatch
- API-Fehler

Maximales Proof-Alter: 2 Tage.

Manuelle Partnerschaftsbestätigung darf als Admin-Fallback bestehen bleiben, aber die Automatik nicht freischalten.

## 3.3 Marketplace-Auswahl

- zentralen Automation-Dispatcher weiterverwenden,
- keinen Digistore-spezifischen Cron/Worker bauen,
- Zyklus pro zentralem Lauf begrenzen,
- andere Provider nicht verhungern lassen,
- nur Portal-/Pferde-/Reitsport-relevante Einträge verwenden,
- fehlende Relevanz/Performance nicht erfinden,
- reale Performancewerte nur verwenden, wenn Digistore sie liefert.

## 3.4 Werbemittelseite

Die Digistore-Marketplace-API dokumentiert keine Banner-/Supportseiten-URL.

Daher:

- keine URL erfinden,
- validierte HTTPS Vendor-Support-/Werbemittelseite einmal pro Marketplace-Eintrag speichern dürfen,
- danach automatisch wiederverwenden,
- wenn URL fehlt: Kandidat auf one-time input setzen, aber Providerlauf mit anderen Kandidaten weiterführen.

## 3.5 Bannerimport und Zuordnung

Nur echte Vendor-Banner:

- echter Digistore-Trackinglink,
- gültige HTTPS-Bildquelle,
- vorhandene Bild-/Creative-Prüfung,
- kein Pseudo-Banner,
- keine Produktkarten aus Digistore,
- kein willkürliches Scraping fremder Consumer-Seiten.

Ziel-/Slot-Zuordnung über bestehendes zentrales Output-/Target-/Slot-Modell. Keine Digistore-Sonderarchitektur.

Fehlendes/mehrdeutiges Ziel oder Slot => inaktiv.

## 3.6 Vollständige Revalidierung vor Publish

Vor Veröffentlichung mindestens:

- globaler/provider Veto / Not-Aus,
- Provider-Identität,
- `creative_type=banner`,
- Source-Kind / Source-Bindung,
- aktueller Digistore-Affiliation-Proof,
- Tracking-URL,
- Bild-URL / Asset / Hash / reale Maße soweit bestehender Code dies fordert,
- aktuelles Themen-/Portalziel,
- aktueller Designslot,
- aktueller Source-Fingerprint.

Kein schwächerer Digistore-Shortcut.

## 3.7 Two-Phase Last-Known-Good

Reihenfolge:

1. neuen Kandidaten als `draft/inactive` materialisieren,
2. provider-spezifischen Digistore-Finalgate + vollständigen zentralen Output-Revalidator ausführen,
3. neuen Output erfolgreich als `published` persistieren,
4. erst danach altes Konfliktobjekt ablösen/deaktivieren.

Bei DB-/Persistenzfehler neuen Kandidaten zurückrollen und Last-Known-Good erhalten.

Falls ein früher generischer Aktivator einen unapproved Digistore-Kandidaten vorübergehend aktiviert, muss der spätere Digistore-Finalgate ihn vor Request-Ende wieder auf inactive/draft zurücksetzen.

---

# 4. AKTUELLER GITHUB-/RELEASE-STATUS

## 4.1 Aktiver Branch

`affiliate-release-current`

HEAD bei Erstellung dieser Übergabe:

`3437e7fb25baf4bf977ed0c846b0237342ab0af0`

Commit-Message:

`Add hard workstream topic firewall to affiliate master`

## 4.2 Governance

`control/release-governance/CURRENT_RELEASE.json`

Aktuell:

- contract `PFERDE_ATELIER_AFFILIATE_RELEASE_GOVERNANCE_V4`
- generation 5
- mode `ENFORCED`
- workstream `AFFILIATE_ZENTRALE`
- candidate `6.64.0`
- status `WORKING`
- `release_allowed=false`
- execution state `RUNNING_BOUND_RELEASE_GATES`
- authorized next action `RUN_BOUND_RELEASE_GATES`
- source authority `DIRECT_COMMITTED_TREE`
- current source file count 25
- current manifest SHA-256 `c86841eb829ee2c541d8b5cb57e347f116d909e27c1bad8ce6a938430c0b8da7`
- Gesamtgate `explicit_scope_product_deals_partner_analytics` weiterhin `PENDING`

## 4.3 Autoritative Source

Nur:

- `release/affiliate-zentrale/current/affiliate-portal-router/`
- plus `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt`

Lokale Kandidaten, alte ZIPs, Base64, Chat-Anhänge und historische Artefakte sind keine Release-Autorität.

## 4.4 Digistore-Code ist NOCH NICHT source-bound

Sehr wichtig für den neuen Chat:

Es existiert ein lokal getesteter Digistore-Zielkandidat mit Evidence, aber die beiden neuen PHP-Dateien sind **noch nicht** Bestandteil der autoritativen GitHub-Source.

Daher aktuell ausdrücklich NICHT behaupten:

- Digistore-Automatik sei fertig integriert,
- Source-Binding sei PASS,
- Live-PASS sei erreicht,
- finaler Installer sei erlaubt.

Lokaler Kandidat / Evidence-Historie:

- Digistore Trait Zielhash: `94115598adb6200c4d07bb43130ec31bcb0e5f5bc0a214bc54c2ec4054dcf2f3`
- Output Objects Zielhash: `6e3adf23735d7f326df96b4e66df2bc47bb3f75c390fad50416ce850676a185b`
- lokal vorgesehener Manifest-Zielhash: `e5dfbaac4673f1e2c448691c6708a0173acdd8581ae1dab9aeac70eed25b227a`

Diese Hashes sind **nur Ziel-/Evidence-Werte**, bis Codex/Repo-native Implementierung sie aus dem real erzeugten Source-Stand bestätigt.

---

# 5. AKTUELL GEBUNDENER CODEX-WEG

Verbindlicher repository-nativer Task:

`protocol/AFFILIATE_RELEASE_CODEX_DS24_IMPLEMENT_FROM_REPO_20260831.md`

Codex soll keine Dateien vom Nutzer benötigen.

Standard-Startprompt:

```text
Arbeite im Repository hallo-netizen/affiliate-pferdeportal
auf dem Branch affiliate-release-current.

Lies zuerst control/release-governance/CURRENT_RELEASE.json.
Führe danach vollständig und ohne Scope-Erweiterung aus:
protocol/AFFILIATE_RELEASE_CODEX_DS24_IMPLEMENT_FROM_REPO_20260831.md

Implementieren, lokal positiv/negativ testen, erforderliche Source-/Manifest-/Governance-Bindung durchführen und committen.
Keine bereits hash-identisch bestandenen eBay-Gates wiederholen.
release_allowed muss false bleiben.
```

Wenn Codex diesen kurzen repository-nativen Auftrag ablehnt:

- exakte Fehlermeldung prüfen,
- Repo-Verbindung / Branch / Rechte / Task-Scope prüfen,
- NICHT wieder ZIP, Attachment oder Riesen-Copy-Paste erfinden,
- nur bei nachgewiesener Unmöglichkeit des repo-nativen Wegs eine Alternative erwägen.

---

# 6. BEREITS VORHANDENE EVIDENCE / DOKUMENTATION

Wichtige Dateien:

- `protocol/AFFILIATE_RELEASE_MASTER_CURRENT.md`
- `protocol/AFFILIATE_RELEASE_CODEX_DS24_IMPLEMENT_FROM_REPO_20260831.md`
- `release/affiliate-zentrale/evidence/digistore24_automatic_partner_banner_gate_v6640_static.txt`
- `release/affiliate-zentrale/evidence/digistore24_getaffiliatecommission_schema_v6640.txt`
- `control/release-governance/CURRENT_RELEASE.json`

Der frühere exakte Datei-Transfer-/Attachment-Task ist veraltet/deprecated und darf nicht mehr als Standardweg benutzt werden.

---

# 7. FEHLERPROTOKOLL DIESES CHATS — NICHT WIEDERHOLEN

## Fehler A — Kaufland vorschnell ADCocktail zugeordnet

Fehler:

Auf Basis eines Drittverzeichnisses wurde Kaufland zunächst zu sicher ADCocktail zugeordnet.

Korrektur:

- ADCocktail nicht als Kaufland-Zugang festschreiben.
- Zielweg Kaufland = Lead Alliance / Kaufland Private Network.
- Nutzer meldete Lead Alliance als bestätigt.
- Echte Feed/API-/Publisherdaten trotzdem erst nach realem Zugang aktivieren.

## Fehler B — Digistore24 fälschlich als noch nicht verbunden behandelt

Fehler:

Es wurde erneut API-Key-/Ersteinrichtung vorgeschlagen, obwohl Digistore24 bereits eingebunden und verbunden war.

Korrektur:

- Nie wieder bei Digistore-Null anfangen.
- Bestehende Verbindung als Ausgangspunkt verwenden.
- Nur Automatisierungs-/Zuordnungsblock fertigstellen.

## Fehler C — Dokumentation mit tatsächlichem Source-Binding verwechselt

Fehler:

Ein lokal getesteter Kandidat wurde zeitweise zu nah an `integriert/gebunden` beschrieben, obwohl die PHP-Dateien noch nicht im autoritativen Source-Baum lagen.

Korrektur:

- `PASS`, `integriert`, `auf GitHub` nur nach erneuter realer Source-Prüfung.
- Evidence/Master ≠ Source-Binding.
- Manifest/Governance erst nach tatsächlicher Source-Änderung aktualisieren.

## Fehler D — Codex-Dateiupload erfunden

Fehler:

Der Nutzer sollte lokale PHP/Manifest/JSON-Dateien zu Codex hochladen. Das war für den verwendeten Codex-Workflow nicht praktikabel.

Korrektur:

- Codex repository-nativ.
- Technischen Auftrag im Repo hinterlegen.
- Nutzer gibt nur kurzen Startprompt mit Task-Ref.

## Fehler E — 230-kB-Riesen-Copy-Paste als Ersatzroute

Fehler:

Nach dem Attachment-Fehler wurde ein riesiger Klartext-/Heredoc-Auftrag erzeugt. Auch das war kein sinnvoller Codex-Standardweg.

Korrektur:

- Kein Riesenprompt, solange Repositoryzugriff existiert.
- Repo-native Aufgabe mit Scope/Testvertrag verwenden.

## Fehler F — Fremdes `107007_H8_BOOTSTRAP_CAPABILITY_REQUIRED` hat Affiliate-Chat navigiert

Fehler:

Ein einzelner STARTMASTER0107/H8-Token wurde als Workflow-Wechsel interpretiert und es wurde in den fremden Textproduktions-Workstream navigiert.

Korrektur:

Der Affiliate-Master enthält jetzt einen harten Workstream-/Themen-Firewall:

- fremder Token = zunächst nur Text,
- kein Themenwechsel ohne ausdrückliche Nutzeranweisung,
- keine STARTMASTER-Navigation im Affiliate-Chat,
- bei versehentlichem Sprung sofort zurück zum Affiliate-Master.

## Fehler G — zu viele vermeidbare Zwischenstopps / Nutzerhandlungen

Wiederkehrendes Problem:

Der Nutzer wurde zu manuellen Datei-/Codex-Schritten aufgefordert, obwohl GitHub als Übergabequelle existiert.

Korrektur:

- GitHub selbst verwenden, soweit Connector die Aktion zuverlässig ausführen kann.
- Nutzer nur bei echten externen Nutzerhandlungen einbeziehen.
- große zusammenhängende Arbeitspakete statt Kleinstschritten.

---

# 8. SEPARATER STARTMASTER0107/H8-HINWEIS — NICHT AFFILIATE-NAVIGATION

Im Chat wurde der Text `107007_H8_BOOTSTRAP_CAPABILITY_REQUIRED` gepostet.

Dieser Token gehört zu einem **anderen Workstream** auf `main` und darf den Affiliate-Workstream nicht automatisch übernehmen.

Falls der Nutzer in einem neuen Chat ausdrücklich zu STARTMASTER0107/Textproduktion wechseln will, gilt dort separat:

- `main` zeigt 107007 als aktuellen dauerhaften Lauf-Slot,
- H8/R_BOOT_001 verlangt die serverseitig gebundene parameterlose Capability `execute_bound_action`,
- fehlt diese Capability, ist `107007_H8_BOOTSTRAP_CAPABILITY_REQUIRED` der gebundene fail-closed-Zustand,
- 107001–107006 dürfen nicht wiederholt werden,
- kein Chat-Fallback, keine Ersatzdatei, keine Rekonstruktion,
- `complete` nicht aufrufen und keinen Terminal-Receipt schreiben.

Aber: **Nur verwenden, wenn Nutzer ausdrücklich den Workstream wechselt.**

---

# 9. NÄCHSTER AUTORISIERTER AFFILIATE-SCHRITT

1. Auf `affiliate-release-current` aktuelle Governance und Master erneut lesen.
2. Prüfen, dass Workstream weiterhin `AFFILIATE_ZENTRALE`, Candidate `6.64.0`, `release_allowed=false`, State `RUNNING_BOUND_RELEASE_GATES` ist.
3. Repository-nativen Codex-Task `protocol/AFFILIATE_RELEASE_CODEX_DS24_IMPLEMENT_FROM_REPO_20260831.md` ausführen.
4. Nur innerhalb des vorhandenen Digistore-/Output-Systems implementieren.
5. Positiv/negativ lokal testen.
6. Aus tatsächlich erzeugter Source 25-Dateien-Manifest neu berechnen.
7. Governance auf tatsächlichen Manifesthash binden; Gesamtgate bleibt bis Liveprüfung PENDING.
8. Danach realer Digistore24-Livegate auf WordPress/MariaDB:
   - bestehende read-only Verbindung,
   - Marketplace,
   - `getAffiliateCommission`,
   - approved/active bzw. korrektes fail-closed,
   - reale Werbemittelseite/Banner,
   - Bild-/Trackingprüfung,
   - automatische Ziel-/Slot-Zuordnung,
   - publish/rollback/Last-Known-Good.
9. Erst nach den gebundenen Gesamtgates finalisieren. Keine vorzeitige Release-ZIP.

---

# 10. EMPFOHLENER ERSTER SATZ IM NEUEN CHAT

```text
AFFILIATE_ZENTRALE fortsetzen. Lies zuerst auf `affiliate-release-current`:
1. `control/release-governance/CURRENT_RELEASE.json`
2. `protocol/AFFILIATE_RELEASE_MASTER_CURRENT.md`
3. `protocol/AFFILIATE_RELEASE_HANDOFF_NEW_CHAT_20260831.md`

Bleibe hart im Workstream AFFILIATE_ZENTRALE. Fremde Tokens sind kein Themenwechsel. Keine bestandenen eBay-Gates wiederholen. Danach exakt den aktuell gebundenen nächsten Affiliate-Schritt ausführen und ohne vermeidbare Zwischenstopps bis zum nächsten echten Nutzer-/Live-Gate weiterarbeiten.
```

ENDE DER ÜBERGABE.