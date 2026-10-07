# AFF-ERR-057 – Vergleichsrechner im Live-Beitrag

Datum: 07.10.2026

## Ziel

Nachweis ausschließlich für den Rechnerweg:

`zentraler Rechner -> stabile ID -> [affiliate_rechner id="..."] -> Shortcode -> the_content -> finales Artikel-HTML`

Keine Banner-, Schabracken-, Ranking- oder Kategorieanalyse.

## 1. Current-Source WordPress/MariaDB

Fokussierter Lauf: GitHub Actions Run `37677771944`, Job `112985584613`.

Exakter Current-Source 6.72.203 in frischem WordPress 7.1.2 / MariaDB 10.11.

Ergebnis:

- PASS stage_1_shortcode_registered
- PASS stage_2_id_active_html_present
- PASS stage_3_shortcode_callback_returns_html
- PASS stage_4_final_article_html_contains_calculator
- AFF_ERR_057_FOCUSED_WORDPRESS_MARIADB_PASS

Damit liegt im Current-Source 6.72.203 kein reproduzierbarer Fehler im Shortcode- oder the_content-Renderweg vor.

## 2. Live-Beiträge

Finaler kombinierter Read-only-Lauf: GitHub Actions Run `37679085019`, Job `112990119299`.

Öffentliche WordPress-REST-Suche findet exakt 16 veröffentlichte Finanzierungsbeiträge.

Alle 16 enthalten im gespeicherten post_content den Shortcode-Token `affiliate_rechner`.

Exakte Phrase:

- `[affiliate_rechner id="kredit"]` -> 16 Treffer
- falsche Kontroll-ID `[affiliate_rechner id="aff057-falsch"]` -> 0 Treffer

Das fertige gerenderte Live-HTML dieser 16 Beiträge enthält keinen ausgegebenen Rechner.

## 3. Live-Version und Versionsvergleich

Öffentlich ausgelieferte Affiliate-Plugin-Assets auf einem betroffenen Finanzierungsartikel:

- Live-Version: `6.72.202`

Vergleich 6.72.202 gegen Current 6.72.203:

- `includes/trait-ppar-tariff-tools.php`: byteidentisch, Blob-SHA `4d9ed03f21c69a95b0d7f280dda43adbfe81b5cf`
- `register_shortcodes()`: identisch
- `filter_the_content()`: identisch
- Tarifrechner-Hooks vorhanden in beiden Versionen:
  - `tariff_tools_register_hooks()`
  - `init -> register_shortcodes`
  - `the_content -> filter_the_content`

Damit ist der Rechner-Renderweg zwischen der live laufenden 6.72.202 und Current 6.72.203 unverändert.

## 4. Erster bewiesener Live-FAIL

Die Live-Beiträge enthalten die korrekte ID `kredit`, der identische Renderer liefert live aber keine Rechnerausgabe.

Der Renderer gibt genau dann leer zurück, wenn der zentrale Rechnerdatensatz die Gültigkeitsbedingung nicht erfüllt:

- ID `kredit` fehlt, oder
- `kredit` ist inaktiv, oder
- gespeicherter HTML-/Widget-Code für `kredit` ist leer.

Damit ist **Stufe 2 – zentraler Live-Rechnerdatensatz gültig** die erste bewiesene Fehlerstufe.

Welcher der drei Unterfälle konkret vorliegt, ist ohne authentifizierten Readback der Live-Option `ppar_tariff_tools_v1` nicht unterscheidbar.

## 5. Konsequenz

Kein Source-Fix.

Kein Banner-Fix.

Kein neues ZIP.

NEXT ACTION:

`Live ppar_tariff_tools_v1['kredit'] lesen -> genau fehlende Eigenschaft korrigieren -> denselben Live-Artikel erneut rendern`.

Nur vertrauenswürdigen, bereits vorgesehenen Widget-/HTML-Code verwenden. Kein erfundener Ersatzcode und kein Fallback.
