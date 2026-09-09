# PRODUKTVERGLEICH – FEHLERQUELLEN

STAND: 2026-09-09
ROLLE: AUTORITATIVE FEHLERQUELLE DIESES BÜROS

## PV-LIVE-001 – FALSCHER GESAMT-PASS BEI 0 GÜLTIGEN VERGLEICHEN

STATUS: FIX-KANDIDAT 0.7.1 LOCAL + FRESH-ZIP PASS / WORDPRESS-RETEST OFFEN

Realer WordPress-Befund 2026-09-09 mit Universal Product Comparison 0.7.0-prototype:
- Regendecken: 8 Kandidaten;
- nach SEO-Lauf: 0 SEO-PASS, 0 SEO-offen, 8 blockiert;
- 0 gebundene Dossiers;
- 16 Provider-Aufrufe;
- reale Kosten $0.1920;
- UI meldete trotzdem grün `PASS`.

Rootcause:
Der Workflow setzte nach vollständig abgearbeiteten SEO-Signalen standardmäßig `PASS`, solange weder WAITING, RESEARCH_REQUIRED noch Dossier-Drift vorlag. Der Fall `alle Kandidaten terminal blockiert + kein gültiges Dossier` war im Statusgate nicht abgebildet.

Zweiter UI-Befund:
Nach dem Lauf zeigte die Seite `Maximale Providerkosten dieses Laufs: $0.0000`. Tatsächlich war dies bereits die Schätzung für einen **neuen** Lauf auf dem post-run Zustand (0 offene SEO-Paare), während der gerade abgeschlossene Lauf $0.1920 gekostet hatte. Die Berechnung war nicht zwingend falsch, aber die Beschriftung war zustandsfalsch und irreführend.

Verbindlicher Fix:
- `0 gültige/gebundene Dossiers + 0 SEO-PASS + alles terminal blockiert` => `NO_ELIGIBLE_COMPARISONS`, niemals PASS;
- eigener Reason-Code;
- NO_ELIGIBLE wird als Warnung, nicht Erfolg ausgegeben;
- Run-Notice zeigt finalen SEO-PASS-/Blockiert-Stand;
- Kostenfeld wird eindeutig als maximale Kosten eines **jetzt neu gestarteten** Laufs beschriftet;
- exakter Live-Fall 8→16 Calls→8 BLOCKED→0 Dossiers wird als ausführbare Regression aufgenommen;
- keine neue Architektur.

PASS-GRENZE:
Erst lokale Positiv-/Negativ-Gesamtsuite + Fresh-ZIP-Gesamtsuite PASS. Danach genau ein neuer WordPress-Retest.


### Fix-Kandidat 0.7.1 – Prüfbeleg 2026-09-09

- exakter Realfall 8 → 16 Provider-Aufrufe → $0.1920 → 8 BLOCKED → 0 Dossiers ergibt `NO_ELIGIBLE_COMPARISONS`;
- Admin rendert diesen Zustand als Warnung, nicht Success;
- echter PASS bleibt Success;
- autoritative PSTE-Kostenschätzung für 8 offene Kandidaten = max. $0.2496;
- post-run Kostenanzeige ist eindeutig als Schätzung eines jetzt neu gestarteten Laufs beschriftet;
- komplette Suite aus frisch gepackter ZIP PASS;
- Mutationstest beweist, dass der alte False-PASS und die alte falsche Notice von den Regressionen verworfen werden.

Release-Kandidat SHA-256:
`5d5bcdc191d64524145486064f6830b6843032402dbae4095bb734939b8fe0fd`.

Fehler bleibt bis realem WordPress-Retest **offen**.


## PV-LIVE-002 – BIDIREKTIONALE SEO-LOGIK UNVOLLSTÄNDIG

STATUS: AKTIV / 0.8.0-KORREKTUR IM HOBBYRAUM

Befund nach dem 0.7.1-Liveretest:
Der Statusfehler PV-LIVE-001 ist korrigiert. Die 8 Regendecken-Kandidaten bleiben jedoch sämtlich SEO-blockiert.

Rootcause aus Code-/Gesamtworkflowprüfung:
- Produktnachfrage wurde im SEO-Discovery-Bestand zwar erkannt, aber ohne direkte A-gegen-B-Evidenz nicht als vollständiges Vergleichssignal bis zur Dossierfreigabe geführt;
- der Live-PSTE-Weg recherchierte primär das konkrete Paar, nicht zwingend beide konkreten Produkte einzeln;
- damit konnte echte Nachfrage nach Produkt A **und** Produkt B unberücksichtigt bleiben, obwohl genau daraus ein sinnvoller Vergleich entstehen soll.

Verbindliche Regel:
Ein Produktvergleich darf SEO-seitig freigegeben werden, wenn entweder
1. direkte belastbare Paar-Nachfrage A gegen B / vs / oder vorhanden ist, **oder**
2. beide konkreten Produkte belastbare externe Nachfrage haben,
und danach derselbe Planning-/Kannibalisierungs-Gate PASS ist.

Nur ein Produkt mit Nachfrage reicht nicht.
Generische Produktgruppen-Nachfrage reicht nicht.
Same-Brand und fachlich nicht vergleichbare Produkte bleiben ausgeschlossen.

## PV-LIVE-003 – SEO-SIGNALE OHNE ALTERUNG / CURRENT-READINESS-REBINDUNG

STATUS: AKTIV / 0.8.0-KORREKTUR IM HOBBYRAUM

Rootcause:
0.7.x speicherte normalisierte Provider-Signale ohne verbindliche Ablaufzeit. Ein negativer Altbefund konnte dadurch dauerhaft terminal bleiben. Positive Signale waren zudem nicht zwingend an den aktuellen WordPress-Inventar-/Strukturzustand gebunden.

Verbindlicher Fix:
- regelmäßig veränderliche SEO-Evidenz hat eine Ablaufzeit;
- alte 0.7.x-Providerverträge werden unter dem neuen Vertrag als stale behandelt und erneut geprüft;
- aktuelle positive Signale werden read-only gegen aktuellen PSTE-Planning-/Kannibalisierungszustand revalidiert;
- Inventar-/Strukturhash wird in die Dossierbindung aufgenommen;
- kein stilles Weiterverwenden veralteter SEO-Freigaben.
