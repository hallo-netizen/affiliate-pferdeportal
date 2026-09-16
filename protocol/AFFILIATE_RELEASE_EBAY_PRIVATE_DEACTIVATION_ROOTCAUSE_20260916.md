# Affiliate-Zentrale – eBay PRIVATE Deaktivierung / Public-Checkpoint Root-Cause Audit

Stand: 2026-09-16
Status: ROOT_CAUSE_CODE_PATH_PROVEN / LIVE_CHECKPOINT_CONTENT_READBACK_PENDING
Kanonische Release-Quelle: `affiliate-release-current`
Kanonischer Pluginstand vor diesem Audit: Affiliate-Zentrale 6.72.19

## Anlass

Live ist nach einem zwischenzeitlichen Deaktivieren/Wiedereinschalten von eBay ein widersprüchlicher Zustand sichtbar:

- HivePress/Taxonomie zeigt weiterhin einen PRIVATE-Bestand deutlich über 250.
- Der reale Post-Check meldet `öffentlich eBay 0`.
- Der aktuelle kanonische eBay-Gesamtlauf ist terminal mit `business_gapfill_public_invariant_failed` beendet; BUSINESS-Abdeckung 81/311, fehlend 230.

Der Nutzer hat ausdrücklich bestätigt, dass PRIVATE-Anzeigen vor dem Deaktivieren sichtbar funktionierten.

## Historische Prüfung – was ist wirklich neu?

Der relevante PRIVATE-Public-Gate-Pfad ist keine neue 6.72.x-Erfindung. Bereits der kanonisch gebundene V6.63.8-Stand (`103d2efa5d2769d3fb52e36c62c50cb338e6afe5`) enthält:

1. `ebay_private_public_post_allowed_base()` → `ebay_private_control_gate()`.
2. `ebay_private_control_gate()` → `control_provider_gate('ebay', ...)`.
3. `control_provider_gate()` sperrt bei zentral deaktiviertem Providerzugang (`enabled=false`).
4. `ebay_public_checkpoint_bootstrap()` prüft die bereits veröffentlichten PRIVATE-Listings über genau `ebay_private_public_post_allowed_base()`.

Damit ist belegt: Die Kopplung zwischen temporärem Provider-Ein/Aus-Zustand und der Inhaltsprüfung des Bootstrap-Public-Checkpoints existiert mindestens seit V6.63.8. Der aktuelle Vorfall ist daher nicht als nachgewiesene neue 6.72.x-Regression zu behandeln.

## Reproduzierbarer Defektpfad im kanonischen Code

Ist noch kein als sicher geltender Public-Checkpoint vorhanden, läuft der Bootstrap so:

1. veröffentlichte eBay-PRIVATE-`hp_listing` werden gelesen;
2. jedes Listing wird über `ebay_private_public_post_allowed_base()` geprüft;
3. bei deaktiviertem eBay-Zugang schlägt darin `control_provider_gate()` für jedes eBay-Listing fehl;
4. dadurch bleibt `private_listing_ids` leer;
5. der Bootstrap speichert trotzdem einen formal sicheren Checkpoint mit `private_listing_ids=[]` und `verification.private_visible=0`;
6. bei späteren Aufrufen wird ein bereits als sicher geltender Checkpoint unverändert wiederverwendet.

Zusätzlich lässt `ebay_run_start($manual=true, ...)` einen manuellen Start auch dann zu, wenn `enabled=false`; damit existiert ein konkreter Eintrittspfad in den Bootstrap während deaktiviertem Providerzugang.

## Warum >300 gezählt werden können, aber 0 sichtbar sind

HivePress/WordPress-Zählung und die spätere eBay-Public-Ausgabe sind getrennt. Vorhandene veröffentlichte `hp_listing` können weiterhin in Taxonomie-/Nachfahren-Zählungen auftauchen. Der spätere `the_posts`-/Public-Checkpoint-Gate kann dieselben eBay-Listings anschließend vollständig aus der tatsächlichen Frontend-Ausgabe entfernen.

Die harte PRIVATE-Auswahlobergrenze von 250 betrifft den ausgewählten/öffentlichen eBay-Bestand; sie beseitigt nicht automatisch jeden historischen Taxonomie-Zähler, solange der abschließende Bereinigungsweg nicht erfolgreich durchgelaufen ist.

## Warum der aktuelle fehlgeschlagene Run den Zustand nicht selbst repariert

Im kanonischen Orchestrator wird der neue Public-Checkpoint erst nach erfolgreichem BUSINESS- und PRIVATE-Public-Gate atomar committed. Erst danach folgen `checkpoint_cleanup_business` und `checkpoint_cleanup_private`.

Der aktuelle Live-Run scheitert bereits im BUSINESS-Safe-Gap/Public-Invariant-Pfad mit `business_gapfill_public_invariant_failed`. Dadurch wird der neue Checkpoint nicht committed und die nachgelagerte PRIVATE-Checkpoint-Bereinigung nicht erreicht.

Das erklärt, warum ein alter/ungeeigneter sicherer Frontend-Stand fortbestehen und gleichzeitig der historische PRIVATE-Postbestand über 250 liegen kann.

## Beweisgrenze

Der Defektpfad ist aus aktueller kanonischer Source und historischer V6.63.8-Source hart bewiesen.

Noch NICHT hart live bewiesen ist, dass der auf der produktiven WordPress-Instanz gespeicherte Checkpoint tatsächlich genau der leere Bootstrap-Checkpoint ist. Dafür fehlt in den verbundenen Quellen ein direkter read-only Readback des aktuellen WordPress-Options-/DB-Werts (`checkpoint_id`, `source`, `created_at`, `private_listing_ids`).

Daher gilt ausdrücklich:

- Keine weitere Pluginversion auf Verdacht.
- Das lokal erzeugte 6.72.27-Testpaket ist NICHT kanonisch und NICHT freigegeben.
- Zuerst read-only Live-Checkpointzustand belegen.
- Erst wenn der Livezustand zum Defektpfad passt, kleinsten Rootfix direkt aus der kanonischen 6.72.19-Source ableiten.
- Danach vollständige erforderliche Positiv-/Negativ-/Regression-/Fresh-Unpack-Prüfung und erst anschließend erneute Live-Abnahme.

## ADCELL-Nebenbefund dieses Chats

Der reale ADCELL-Preflight wurde ausgeführt. Auf dem ursprünglichen Weg kam zunächst HTTP 401 `invalid login data`; Credential-Recovery war damit real erforderlich. Nach Aktualisierung des ADCELL-API-Kennworts wurde auf einem lokalen nichtkanonischen Diagnose-Nachfolger Token/Programmliste erfolgreich gelesen: 11 accepted+aktive Programme, davon 8 explizit freigegeben. Guardianhorse 7143 lief real bis `completed/partial` mit 17 importierten Werbemitteln; Banner/Deeplink verarbeitet, kein eindeutiges CSV-Werbemittel.

Dies ist kein kanonischer 6.72.19-Live-PASS: Der Post-Recovery-Replay auf exakt kanonischer 6.72.19-Source und der vollständige kanonische E2E fehlen.

## Nicht autoritative lokale Testlinie

Im Chat entstanden lokale 6.72.20–6.72.27-Pakete. Sie wurden nicht in `affiliate-release-current` committed und sind nicht durch die kanonische Source-/Manifest-/Release-Bindung gelaufen. Sie sind ausschließlich Diagnose-/Livehistorie und dürfen weder als kanonischer Stand noch als Pluginbüro-`CURRENT.zip` behandelt werden.
