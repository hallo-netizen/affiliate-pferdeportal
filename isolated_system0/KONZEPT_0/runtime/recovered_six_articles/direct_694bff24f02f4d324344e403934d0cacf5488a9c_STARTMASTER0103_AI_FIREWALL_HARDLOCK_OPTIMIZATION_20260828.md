# STARTMASTER0103 – AI-Tool-Firewall, Package-Hardlock, Optimierung

Stand: 28.08.2026

## Bindender Ausgangsstand
Der reale 6er-Artikeltest ist technisch erfolgreich abgeschlossen: PSERC Workflow Supervisor PASS, PSERC→PPM Bridge EXECUTED, PPM `NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH`, 6 Entwürfe (17123–17128), kein Publish.

PSTE 0.56.25 und PSERC 0.28.14 bleiben byte-identisch. PPM 6.7.9, Textmaschine, LanguageTool, Fach-/Qualitätsregeln, Design, Dubletten-/Kannibalisierungsschutz und Publish-Logik werden nicht verändert.

## Fix 1 – wiederholten Paketfehler technisch sperren
Neu und bindend: `PRODUCTION_PACKAGE_PREFLIGHT_GUARD_STARTMASTER0103.py` zusätzlich zum unveränderten STARTMASTER0039-Boundary-Guard.

Fail-closed bei:
- WordPress-Kategoriename ungleich letztem Segment des gebundenen `hierarchy_path`;
- aus dem Slug synthetisiertem `wordpress_category.name`;
- fehlendem Kategorie-Snapshot-Hash;
- `fact_pack.title_scope != runtime_order.subject_scope`;
- fremdem `plan_slot` im PPM-Plan;
- fehlender Supervisor-Release-Bindung;
- Paket-/Komponenten-Hashdrift.

Der historische fehlerhafte 6er-Paketstand wird damit lokal sicher BLOCKED; das korrigierte und live erfolgreiche Paket PASS.

## Fix 2 – externe AI-Tool-Firewall
Neue äußere Zwangsschicht `AI_TOOL_FIREWALL_CONTROLLER_V1`.

Der Controller:
1. liest nur `PFERDE_ATELIER_START_HERE.json` und den hashgebundenen `CURRENT_STATE.json`;
2. verlangt identischen `NEXT_ALLOWED_STEP` in ROOT/State;
3. verwendet Default DENY für unbekannte Schritte;
4. gibt dem Modell ausschließlich die step-spezifisch erlaubten Tools;
5. nutzt zusätzlich OpenAI `tool_choice.allowed_tools`;
6. akzeptiert Resultate nur für exakt denselben Schritt und ein festes Schema;
7. setzt `state_write_authority=CONTROLLER_ONLY`;
8. verwirft jede zusätzliche/falsche Aktion ohne State-Fortschreibung.

Ab STARTMASTER0103 ist freier Chat keine Produktions-Ausführungsautorität. Produktionsarbeit ist nur über den Controller freigegeben. Neue Chats starten dadurch aus GitHub/MASTER-State, nicht aus Erinnerung oder Modellnavigation.

## Optimierung / Verschlankung ohne Qualitätsverlust
Sicher aktiviert bzw. bestätigt:
- NO-STOP für interne PASS/Hash-Checkpoints;
- hashgebundener PASS-Reuse unveränderter Infrastruktur;
- LanguageTool-Abhängigkeitsidentität einmal prüfen, finalen Text weiterhin pro Artikel prüfen;
- Fail-fast Package-Preflight vor Signatur/Live-Versuch;
- Tool-Firewall verhindert Extra-/Wiederholungsprüfungen und falsche Navigation.

Nicht aktiviert: Medium, unbewiesene Parallelisierung oder irgendein Weglassen/Lockern von Recherche, Fachprüfung, Textqualität, LanguageTool, PPM, Dubletten-/Kannibalisierungs-, Design- oder Publish-Gates.

## Lokaler harter Positiv-/Negativtest
PASS:
- korrigiertes Produktionspaket positiv;
- historischer Scope-Fehler negativ BLOCKED;
- wiederholter Kategorie-Identitätsfehler negativ BLOCKED;
- STARTMASTER0039-Boundary-Verstoß negativ BLOCKED;
- fehlende Release-Bindung negativ BLOCKED;
- Firewall-Authority positiv;
- falscher State-Hash negativ BLOCKED;
- falscher Step negativ BLOCKED;
- nicht erlaubtes Tool negativ BLOCKED;
- Modell-State-Write negativ BLOCKED;
- falsches Result-Step negativ BLOCKED;
- 0102→0103 Protected-Byte-Audit: alle Altdateien außer exakt ROOT/Pointer/CURRENT_STATE byte-identisch;
- PSTE/PSERC Installer-Hashes unverändert;
- ZIP-Re-Extract vollständig byte-identisch.

MASTER-ZIP SHA-256: `8a0093e09efbea84db63859fed4ae02e8ba40b6cf131f9c769c9f12bd9212b30`.

## Aktueller NEXT_ALLOWED_STEP
`USER_CONTENT_REVIEW_6_DRAFTS_17123_17128_NO_PUBLISH`.
