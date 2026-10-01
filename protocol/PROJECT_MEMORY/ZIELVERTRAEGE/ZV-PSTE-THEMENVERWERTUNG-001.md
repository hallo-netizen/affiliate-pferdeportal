# ZV-PSTE-THEMENVERWERTUNG-001 – Gespeicherten Themenbestand vor Neurecherche verwerten

STATUS: AKTIV
FASSUNG: 2026-10-01
GELTUNGSBEREICH: PFERDE_ATELIER / TEXT / PSTE / REDAKTIONSPLAN

## Ziel

Den bereits gespeicherten PSTE-Themenbestand, seine Fundstellen und die Sandbox so weit wie möglich **mit bereits vorhandener Evidenz** in belastbare Artikelkandidaten überführen, bevor neue Keyword-/Provider-Recherche gestartet wird.

## KISS-Grenze

Keine neue Architektur, kein neues Plugin und keine zweite Themen-Datenbank.

Verwendet werden ausschließlich die bereits vorhandenen PSTE-Felder, Status, Reason-Codes, Portal-Kontextdaten und der bestehende Normal-Reentry-/Planungsweg.

## Harte Nicht-Missverständnis-Regeln

1. **Gespeichert ≠ produktionsreif.**
2. Kein pauschales „alles freigeben“.
3. Kein Umgehen von Dubletten-, Kannibalisierungs-, Kategorie-, Artikeltyp-, Titel-, Plan-Slot-, PSTE-, PSERC- oder Publish-Regeln.
4. Kein neuer externer Rechercheaufruf, solange vorhandene verwertbare Kandidaten noch nicht systematisch ausgewertet sind.
5. `PENDING_EXTERNAL_RELEVANCE` bleibt geparkt, solange reale externe Relevanzevidenz fehlt.
6. `STRUCTURE_GAP` bedeutet: Portalrelevanz ist bestätigt, aber passende aktuelle Familie/Kategorie fehlt. Das ist **kein Produktions-PASS**; vorhandene Evidenz bleibt erhalten und wird erst über Strukturentscheidung + normalen Reentry weitergeführt.
7. `RESEARCH_KEYWORD`, `RESEARCH_CLUSTER`, `HEAD_TERM`, `KEYWORD_VARIANT`, `NON_EDITORIAL` und `ALREADY_COVERED` sind keine direkten Produktionsthemen.
8. `BLOCKED_FOR_CATEGORY` ist ein Sammelstatus; Entscheidung immer anhand der Reason-Codes. Bereits abgedeckte/duplizierte Intentionen dürfen nicht reaktiviert werden.
9. Rot bedeutet fachliche Prüfung, nicht automatisch „gutes Thema“. Gelb bedeutet vorläufige Einordnung. Grün beantwortet nur den manuellen Prüfbedarf; technische Planungseignung bleibt separat.
10. Solange der aktuelle Portalabgleich nicht `COMPLETE` ist, keine manuelle Freigabe und keine endgültige Verwertbarkeitsbewertung.

## Verwertbarkeits-Lanes nach COMPLETE

A. **DIREKT PLANBAR**
- Rolle `ARTICLE_TOPIC`;
- Kontext `CURRENT` oder `NOT_REQUIRED`;
- `planning_suitability=YES` oder zulässiges `PROVISIONAL`;
- vorhandene Zielkategorie + Artikeltyp;
- keine nachgewiesene Abdeckung/Dublette;
- normaler Titel-/Kannibalisierungs-/Plan-Slot-Weg bleibt verpflichtend.

B. **OHNE NEUE EXTERNE RECHERCHE REPARIERBAR**
- gespeicherte Evidenz reicht;
- Problem liegt nur in Titel-/Kategorie-/Familien-/internem Reentry-Schritt;
- bestehende PSTE-Normalpfade erneut anwenden, nicht manuell bypass-en.

C. **STRUKTUR-/MENSCHENENTSCHEIDUNG**
- `STRUCTURE_GAP`, `MATCHER_REVIEW`, echte rote Fachfälle;
- vorhandene Evidenz erhalten;
- nur konkrete Struktur-/Zuordnungsentscheidung, danach normaler Reentry.

D. **GEPRÜFT PARKEN / NICHT PRODUZIEREN**
- `PENDING_EXTERNAL_RELEVANCE` ohne Evidenz;
- `ALREADY_COVERED`, echte Dublette/Kannibalisierung;
- `NON_EDITORIAL`, `STALE_RESEARCH_TERM`, bloße `KEYWORD_VARIANT`;
- kein künstlicher Artikel nur zur Verwertung eines gespeicherten Suchbegriffs.

## PASS-Bedingung

PASS erst, wenn nach `COMPLETE`:
- der vorhandene Themenbestand read-only in A/B/C/D klassifiziert wurde;
- direkte und reparierbare Kandidaten dedupliziert sind;
- für jeden an Produktion übergebbaren Kandidaten Titel, Zielkeyword, Kategorie, Artikeltyp und Plan-Slot eindeutig gebunden sind;
- kein neuer externer Recherchelauf nötig war, solange A/B-Kandidaten vorhanden sind;
- kein Gate oder Qualitätsstandard abgesenkt wurde;
- kein Artikel automatisch veröffentlicht wurde.

