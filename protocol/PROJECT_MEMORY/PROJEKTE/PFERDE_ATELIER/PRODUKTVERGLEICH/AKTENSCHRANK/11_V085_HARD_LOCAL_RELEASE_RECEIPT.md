# PRODUKTVERGLEICH 0.8.5 – HARD LOCAL RELEASE RECEIPT

Stand: 2026-09-11
Status: FINAL-FRESH-ZIP HARD PASS / WORDPRESS-LIVE-VORCHECK OFFEN

Artefakt:
`universal-product-comparison-0.8.5-prototype.zip`

SHA-256:
`0174051e6584902142f5be5787642426b30aab6c7ba15ef0b07ccbdb4a5844fd`

## Ziel

Vorhandenes Product Knowledge besser nutzen, ohne Markt-Vollständigkeit zu behaupten:
- weitere echte Mehrhersteller-Gruppen fachlich profilieren;
- vollständiges Cross-Family-Paaruniversum öffnen;
- gleiche Herstellerfamilien-Wahrheit in Readiness und Planner erzwingen.

## Aktivierte vorhandene Gruppen

- Winterdecken: 20 Paare;
- Übergangsdecken: 14;
- Stalldecken: 28;
- Unterdecken: 63;
- Steigbügel: 5.

Summe:
**130 zusätzliche aktuelle echte Cross-Family-Paare**.

Keine Top-N-/Pair-Cap.
Research-Vollständigkeit bleibt `UNPROVEN`.

## Herstellerfamilien-Fix

`Aesculap/Kerbl` und `Kerbl` werden identisch als `kerbl-family` behandelt.

Schermaschinen mit aktuellem Bestand:
- 4 Produkte;
- 1 echte Herstellerfamilie;
- 0 echte Cross-Family-Paare;
- `INSUFFICIENT_MANUFACTURERS`.

Positiver Gegenfall:
Ein echter zweiter Hersteller `Lister` erzeugt im Test exakt 4 Kerbl-Family-vs-Lister-Paare.

## Harte Prüfung

Working tree:
- 35/35 Regression PASS;
- 50/50 PHP-Lint PASS.

Prefinal Fresh-ZIP:
- Source equality 70/70 PASS;
- Regression 35/35 PASS;
- PHP-Lint 50/50 PASS.

Final Fresh-ZIP:
- Source equality 71/71 PASS;
- Regression 35/35 PASS;
- PHP-Lint 50/50 PASS;
- Report-Hashbindung 70/70 PASS.

## Negativtests

Drei Herstellerfamilien-Rückfallmutationen korrekt ROT:
1. Readiness wieder auf rohe Herstellerlabels zurückstellen;
2. Research-Zählung wieder rohe Herstellerzahl verwenden lassen;
3. Kerbl-Familienalias entfernen.

Bestehende 0.8–0.8.4 Mutation Guards weiter PASS.

## Bestehende Schutzgrenzen

Weiter PASS:
- 175/175 Portalregistry;
- keine stille Gruppe;
- kein Top-N-/Pair-Cap;
- Same-Family vor SEO ausgeschlossen;
- Research-Kandidaten ≠ Research COMPLETE;
- Dossier V2 / Decision-Policy;
- persistente SEO-Evidenz/Kostenschutz;
- Audit fail-closed;
- kein Writer-/Draft-/Publishweg;
- kein Auto-Publish.

## Abhängigkeiten

Universal Product Knowledge 0.5.0:
`80218ec721631353d62a7e3058e76d9c4a4829802c4d5c6bd6f1f2014b6879e3`

PSTE 0.56.25:
`8122e3fa2273fe4d8e53476f557ed0ddd99a197e8b1c40302f35db245ebb0f95`

Portal v279:
`b86a160e6b8cf720077830422ca6b574203ce171fdc65d357fe9c6bed039c2e0`

SEO-Discovery weiter byte-identisch zum realen PSTE-Gegenbeweis:
`bba970b7135671cb1d09f5f33fe29598b2a44b8328153597cd3347bb4acdbdf4`

SEO-Kostenbindung weiter unverändert:
`863a724d9f349770d9f62c7c65ee7c74565d4247f9bf15504984ae4ece2c9003`

## Live-Grenze

Noch kein WordPress-LIVE-PASS für 0.8.5.

Nächster Schritt:
installieren -> Seite nur öffnen -> keine Providerarbeit starten -> Coverage-/Readiness-Screenshot prüfen.
