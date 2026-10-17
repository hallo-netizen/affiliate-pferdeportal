# HD-001 – KATEGORIE-WORKFLOW – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **1.14.12 REAL BLOCKED / 1.14.13 VERWORFEN WEGEN ADMIN-VOLLREADBACK / 1.14.14 HARD SIM PASS / ECHTER WORDPRESS-DRY-RUN OFFEN**

## Reale Ausgangslage

1.14.12 realer Final-Dry-Run:
- BLOCKED;
- 2642 Zielobjekte;
- CREATE 279 / ADOPT 4 / UPDATE 2357 / ARCHIVE 0;
- Kollisionen Libellenbeobachtung und Nachtvogel-Beobachtung;
- kein Apply/Sync.

## Warum 1.14.13 verworfen ist

Die Kollision-/Profilkorrektur war enthalten, aber die Adminseite hatte einen schweren Lastfehler:

Schon beim normalen Öffnen von `Finaler Zielbaum` rief `render()` den kompletten Frontend-/Struktur-Readback auf.

1:1-Simulation mit realer V7.1-Größe:
- get_post: 762;
- get_post_meta: 1524;
- get_term: 2995;
- get_term_meta: 11980;
- get_posts: 1;
- zusätzlich tausende URL-Auflösungen.

Damit ist die gemeldete extreme Backend-Langsamkeit reproduziert.

Außerdem blieb ein gespeicherter alter Dry-Run sichtbar, obwohl er aus 1.14.12 stammte.

## Einziger Kandidat

`HD001_V1.14.14_HOBBY_DEPOT_V7_1_BACKEND_LOAD_FIX_HARDPASS.zip`

SHA-256:
`fdcca9282b0edcb5e0bb557b9f1fc5ec6cfc3c127afb40b6dc531340f653642a`

V7.1-Profil SHA-256:
`23c707b38f1892703f959c5374b736c7b85fa4db56023a22e987debdc215911f`

## Änderungen 1.14.14

Nur enger Reparaturscope:
- normaler Admin-Render führt keinen Voll-Readback mehr aus;
- bei COMPLETE wird der bereits vom Sync gespeicherte Readback benutzt;
- alter gespeicherter Dry-Run einer anderen Pluginversion wird als veraltet markiert und nicht als aktueller Ergebnisblock gerendert;
- 1.14.13-V7.1-Profilbindung und Legacy-Reuse bleiben unverändert;
- keine Kategorie-, Navigation-, Fach- oder Architekturänderung.

## Harte Positiv-/Negativprüfung

Admin-Pfad alt:
- reproduziert 762 + 1524 + 2995 + 11980 Objekt-/Metalesungen.

Admin-Pfad 1.14.14:
- get_post 0;
- get_post_meta 0;
- get_term 0;
- get_term_meta 0;
- get_posts 0;
- alter 2642er Ergebnisblock nicht als aktuell sichtbar.

V7.1-Dry-Run gegen 2357er Altbestand plus die zwei real beobachteten alten Target-Seiten:
- PASS;
- 3487 Zielobjekte;
- CREATE 1126;
- ADOPT 3;
- UPDATE 2358;
- ARCHIVE 1;
- Errors 0.

Konkrete Reuse-Prüfung:
- Libellenbeobachtung → UPDATE der vorhandenen alten Target-Seite;
- Nachtvogel-Beobachtung → UPDATE der vorhandenen alten Target-Seite.

Negativ:
- fremd gebundener Slug → BLOCKED;
- doppelte Legacy-Target-Bindung → BLOCKED.

Technik:
- PHP 33/33 PASS;
- ZIP-Roundtrip 44/44 PASS;
- 0 Provider Calls;
- Dry-Run 0 WordPress-Strukturwrites;
- Dry-Run startet keinen Apply.

## Isoliertes Artefakt

`CURRENT.zip` bleibt noch nicht synchronisiert.

Grund:
1.14.14 ist lokal hart geprüft, aber der echte WordPress-Dry-Run ist noch offen.

## EXAKT EINE NEXT ACTION

**1.14.14 installieren → Adminseite neu öffnen → nur Finalen Delta-Dry-Run ausführen → keinen Apply/Sync.**
