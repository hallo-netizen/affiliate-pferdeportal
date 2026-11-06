# 06.11.2026: PSTE 0.57.144.12 Original-ZIP dauerhaft im Campus-Pluginbüro gesichert

**ECHTE ABGELAGERTE DATEI, NICHT NUR BERICHT**

Pfad: `protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PLUGINS/INSTALLATIONS_PAKETE/PFERDEATELIER_PSTE_0.57.144.12_MINI_ZUM_REDAKTIONSPLAN_NUR_TEST.zip`
Größe: 627824 Bytes.
Original SHA256: `fac094d994276608453ed4a731b49212528fe71184823f3885127e4ee6f16bd9`.
Original Git-Blob und zurückgelesener GitHub-Blob: `e5d709bbb45b3c4c79fd75056db076a2c1ce7cb2`.

Datei unverändert vom Betreiber hochgeladen. **NICHT erneut beim Benutzer erfragen. Vor Behauptungen über fehlende Zugriffsrechte die Datei im Campus lesen.** K0/PSERC/LIVE nicht verändert.

87 JA-Titel unverändert im MINI zur Planung übergeben; 9 VIELLEICHT geparkt; 4 NEIN raus. 87 Reentry: 7 PASS / 78 HELD / 2 BLOCKED. 50 Kategorieentscheidungen offen: im bestehenden Redaktionsbüro sammeln; bei Bedarf manuell neue Kategorie prüfen. 7 Relevanzbelege, 6 bereits gelieferte Sprachtitel und 3 Titelbelege erneut verlangt: Ursache liegt im unvollständig gebundenen Übergang vom externen MINI zu alter Planung, keine erneute Sprach-/Relevanz-Fachprüfung zulassen. 12 Planungsgründe (Dubletten/Artikelart/Intent) im einzigen vorhandenen Planungsowner unterscheiden; keine echten Dubletten freigeben. 1 Produktauswahl / 1 Familie offen. Nichts beim Nutzer neu anfordern, keine Titel neu produzieren.

**Originalcode in 0.57.144.12**: `PSTE_Mini_Workflow::forwardToPlan` schreibt Titel über `PSTE_Repository::saveManualTitleOverride` und startet `PSTE_Admin::scheduleTitleDeskReentry`; externes JA wird nicht fachlich gebunden zum Reentry übergeben. Status alter Belege und Kategoriezuordnung nur anhand des einmaligen Bestandsowners behandeln. Ziel KISS: einmalige Redaktion, nicht doppelte Fachentscheidung. Keine Live-Freigabe und kein Pluginfix dokumentiert.

Zur präzisen Einzelzahl- und Ereignisquelle vgl. `EVIDENCE/PSTE_MINI_REIMPORT_URSACHENBEFUND_20261106.json` und `EVIDENCE/pste-gesamtdiagnose-2026-11-06.json`. Ein weiterer Nachweis liegt in PR #643, hier wird der aktuelle **Campus-Branch** selbst um die echte ZIP ergänzt.
