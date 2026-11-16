# W36 – Zielvertrag, Kategoriebaum, bestehender DataForSEO-Workflow und WordPress-Gesamtbau gemeinsam geprüft

**Stand 16.11.2026 · tatsächliche GitHub Actions: PASS · WordPress live NICHT verändert.**

## Ein Gesamtvorgang, keine neue Pluginversion
- Verbindlichen `ZIELVERTRAG.md` gegen W27/W28/W35 verglichen: konkrete Produktart als letzte WP-Seitenebene; darunter produktbezogene Inhaltskategorien mit ungefähr 3–5 plausiblen Einzelartikeln; 7 Kauf-Hauptbereiche + Industrie-Fachzugang; Magazin/Glossar und HivePress sind eigene Säulen.
- Alle **218** W6-Altowner und der unveränderte W5-SEO-Fingerprint gegen **219** W35-Ziele geprüft. Ergebnis **114 Seiten (113 alt + Pool/Teich-Hub-Entwurf)**, **105 WP-Inhaltskategorien**, **17 Eigentümer-geprüfte URL-Weiterleitungen**. **79** W4-Produktowner bleiben erhalten, davon **71** Hauptmenü- und **8** Industrie-Fachowner.
- Alle **81** W28-Neuproduktkandidaten mit **90** individuellen Artikelrubriken (je mindestens 3 unterscheidbare Artikelideen) gegen W27 und die bestehenden 218 SEO-Begriffe geprüft. Alle 81 behalten ihre Sperren `seo_owner_freigabe=false` und `wp_seitenfreigabe=false`.
- Das byteidentische Original-WT001 **0.1.4** aus dem GitHub-Archiv mit Original-DataForSEO- und PaidResearch-Klassen tatsächlich entpackt und im selben GitHub-Actions-Lauf untersucht. Seine **Original-Normalisierung** direkt auf die 81 echten W28-Keywordvorschläge angewandt: **81/81 formal zulässig, 81/81 verschieden, 0 exakt gleiche Begriffe innerhalb der alten 218**. Positive und negative Fälle gegen den echten PHP-Code PASS. Zwei bekannte inhaltliche W29-Unterart-/Intent-Grenzfälle bleiben **inhaltlich zu prüfen**, trotz 0 wörtlicher Keywordgleichheit.
- Der bestehende `Wassertechnik_PaidResearch::planned()`-Ablauf ist nachweislich fest an **218** W4-Keywords gebunden. W30/W31 lesen die **81** nur schreibfrei als Vorschau; es ist **keine** echte PaidResearch-Verarbeitung für 81. Eine bloße Übergabe ist noch keine gemessene Suchabsicht oder SEO-Freigabe. Der Fehler liegt nicht im Kategorie-Fachbaum.
- In den **bestehenden** W33-Gesamtbuild eine zusätzliche W36-Vertrags-/Quellen-/Provider-Normalisierungsprüfung eingehängt. Der W35-WP-Importer mit exakt **einer** Freigabe/Inventur/Write/Readback-Strecke und **10/10** positiven/negativen WordPress-Mockfällen bleibt unverändert.

## Reale Prüfergebnisse
- GitHub Actions `43883695024` erfolgreich. Prüfcodes `W36_GESAMTABGLEICH_OFFLINE.py` und der ergänzte bestehende `W33_FULL_PLUGIN_MOCK_QA.php`. Original-SEO-Plan/Fingerprint unverändert, 0 bezahlte DataForSEO-Anfragen, 0 echte WordPress-Schreibaktionen.
- Noch **kein** aktueller authentifizierter WordPress-Admin-Readback; öffentliche REST-Antwort war bei W34 HTML. 0.1.7-Original aus vorherigem Chat ist nicht als vollständiges GitHub-Original verfügbar. Deshalb kein Beweis, dass die W35-Rekonstruktion die auf WordPress vorhandene 0.1.7 vollständig ersetzt.
- **Keine installierbare neue Pluginversion**, keine Veröffentlichung der 81 Kandidaten, kein stilles Bezahlen.

## EIN verbleibender integrierter Umsetzungsblock
Im bestehenden WT001-Plugin die 81 als **einen gesondert freizugebenden SEO-Datenauftrag** der bereits vorhandenen PaidResearch-Mechanik zuführen, ohne alte 218er Ergebnisse/Locks erneut zu starten und ohne zweite fachliche Keywordentscheidung. Kostenpflichtige Anfragen nur nach ausdrücklicher gesonderter Freigabe. Danach den tatsächlich installierten WP-Plugin-/Adminbestand innerhalb der einzigen vorhandenen WP-Import-Strecke abgleichen und die vorhandenen Funktionen vor einer Installationsfreigabe nachweisen. Ohne echten Livezugang kann dieser letzte Paritätsnachweis nicht als erbracht gelten. **Kein Nutzer-Upload erforderlich, kein Plugin installieren.**

**Bürostand:** W36 Quelle/Vertrags-/SEO-/Import-Konsistenz erfolgreich geprüft und dokumentiert; endgültige Live-/Installationsfreigabe noch nicht erteilt. PR #814.
