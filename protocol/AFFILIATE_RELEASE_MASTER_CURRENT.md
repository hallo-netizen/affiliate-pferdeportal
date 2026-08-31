# AFFILIATE-ZENTRALE — CURRENT MASTER / HANDOFF

Stand: 2026-08-31
Branch: `affiliate-release-current`
Workstream: `AFFILIATE_ZENTRALE`
Governance: `PFERDE_ATELIER_AFFILIATE_RELEASE_GOVERNANCE_V4`
Candidate: `6.64.0` / `WORKING` / `release_allowed=false`

## Autoritative Quelle

Nur `release/affiliate-zentrale/current/affiliate-portal-router/` plus `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt` ist aktuelle Release-Quelle. Historische ZIPs, alte Chatstände und Archive sind keine Navigations- oder Rekonstruktionsquelle. Bereits hash-identisch bestandene eBay-Gates werden nicht erneut ausgeführt.

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

## Testnachweis dieses Blocks

Evidence: `release/affiliate-zentrale/evidence/digistore24_automatic_partner_banner_gate_v6640_static.txt`

Lokal PASS: PHP-Lint beider geänderter Traits; exakter GET-Request; fremde Affiliate-ID blockiert; >50 Produkt-IDs blockiert; approved positiv; pending negativ; stale negativ; atomare Aktivierung positiv; DB-Commit-Rollback negativ; Two-Phase-Supersede positiv; früher generisch aktivierter unapproved Kandidat wird zurückgerollt.

## Noch offen vor Release

Der Digistore-Block besitzt noch keinen echten Live-Nachweis mit dem realen Digistore24-Konto und der realen WordPress/MariaDB-Installation. Deshalb bleibt `release_allowed=false` und der gebundene Gesamtgate `explicit_scope_product_deals_partner_analytics` PENDING. Keine finale Release-ZIP vor dem finalen Gate.

## Aktuell autorisierter nächster Schritt

Den so gebundenen Source-Stand live gegen das reale Digistore24-Konto prüfen: read-only Verbindung, Marketplace-Daten, `getAffiliateCommission`, mindestens ein realer approved/active Partner bzw. korrektes Fail-closed bei keinem approved Partner, reale Werbemittel-URL/Banner, Bildprüfung, automatische Ziel-/Slot-Zuordnung und veröffentlichter/rollbackfähiger Endzustand. Danach nur den bereits gebundenen Release-Gate weiterführen.
