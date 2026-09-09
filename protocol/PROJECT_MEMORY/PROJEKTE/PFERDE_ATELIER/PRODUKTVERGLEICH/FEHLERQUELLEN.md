# PRODUKTVERGLEICH – FEHLERQUELLEN

STAND: 2026-09-09
ROLLE: AUTORITATIVE FEHLERQUELLE DIESES BÜROS

## PV-LIVE-001 – FALSCHER GESAMT-PASS BEI 0 GÜLTIGEN VERGLEICHEN

STATUS: AKTIV / KORREKTUR IM HOBBYRAUM

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
