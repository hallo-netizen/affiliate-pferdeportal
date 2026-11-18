# Hobbydepot Texterstellung – zusätzliche Funktionsprüfung 0.4.23

**18.11.2026 · Verbindlicher Auftrag: bestehendes Plugin nur von Pferdeatelier-Inhalten bereinigen, keine Architekturänderung.**

## Konkrete Nachweise
- Geprüfte Originalbereinigung **unverändert**: `/hobbydepot/TEXTERSTELLUNG/ARBEITSKOPIEN/Texterstellung_Hobbydepot_0.4.23_BEREINIGT_TEST.zip`, SHA256 `c50caa2ed263fb1f42f4cd485ecb2d23bbece6df072d9cf8f55774161aa6e715`. Keine neue Pluginversion, keine Änderung am Programm.
- **32/33 lokale Prüffälle bestanden, 1 reproduzierbarer Fehler**, davon 3 WordPress-Startvarianten, 25 Funktions-/Oberflächentests (24 PASS, Diagnose FAIL), 5 unabhängige Original-Rückimporttests (5 PASS). Dies sind **PHP-WordPress-Mocks, KEINE realen WordPress-/K0-/DataForSEO-Endtests**.
- ZIP geprüft: 87 Einträge, 78/78 PHP-Lint, 8/8 gültige JSON.
- Sechs Backendbereiche nachgewiesen: Übersicht, Recherche, Redaktionsplan, K0-Export, Rückimport, Diagnose. **5/6 Seiten laden im Mock**, Diagnose bei bestätigt simulierter Testwebsite fällt mit `K0_ARTICLE_TYPE_AUTHORITY_UNAVAILABLE` aus.
- Unveränderter MINI-Regal-Weg übernimmt Approval und hält unvollständige K0-Metadaten zurück, verhindert Wiederholungsduplikate, abweichende Titel und fehlende WordPress-Kategorien.
- Unveränderter PSERC-Rückimport legt nach vollständigem Testformat einen Artikel mit Kategorie und Metadaten als **Entwurf** in einer WordPress-Simulation an. Der TXE-zu-PSERC-Durchlauf mit **testweise bereits exportiert markiertem** Auftrag bindet Post-ID/Slot zurück in das vorhandene Auftragsregal. Dies beweist NICHT die vorgelagerte MINI-/K0-Erzeugung oder echten WP-Betrieb.
- Keine Providerkosten, keine echten Post-Writes; keine Änderungen an Pferdeatelier, K0 oder HD004.

## Nachgewiesener Funktionsblocker
- `texterstellung/contracts/k0-article-type-capabilities-v1.json` enthält seit der **ursprünglichen Hobby-Arbeitskopie** `authority: K0_PORTAL_ADAPTER_PENDING`. `TXE_K0_Article_Types::all()` verlangt unverändert `K0_RULE_VALUES_JSON`, damit ist K0-Export für fertige Fälle nicht freigegeben.
- `TXE_Diagnose::snapshot()` ruft `TXE_K0_Article_Types::snapshot()` ungeschützt auf. Deshalb ist die Diagnose selbst defekt. **Nicht als voll funktionsfähig oder installierbar für Produktion deklarieren.**
- Vorherige bloße Menü-Sichtprüfung wäre unzureichend gewesen. Nun sind die Funktionsgrenzen mit echten PHP-Aufrufen bewiesen.

## Konkrete Grenzen des Auftrags
Die Bereinigung ist erledigt, die technischen Zusatztests sind protokolliert; **der Code wurde nicht verändert**. Ein voll funktionierender K0-Export und das Beheben der Diagnose-Sperre erfordern eine belegte K0-Typautorität bzw. Funktionskorrektur. Dies überschreitet die ausdrücklich auf reine Fachbereinigung begrenzte Weisung und wurde **nicht** heimlich vorgenommen. Weitere Re-Architektur, zusätzliche Plugins, neue HD004-Adapter und spätere Fachentscheidungen bleiben verboten.

## Arbeitsstand
- ZIP bleibt exakt dieselbe geprüfte 0.4.23-Bereinigung (keine neue Version).
- Prüfberichte im Hobbydepot-Büro:
  - `/hobbydepot/TEXTERSTELLUNG/PRUEFBERICHTE/HOBBYDEPOT_0423_ERWEITERTE_FUNKTIONSPRUEFUNG.md`
  - `/hobbydepot/TEXTERSTELLUNG/PRUEFBERICHTE/HOBBYDEPOT_0423_ERWEITERTE_FUNKTIONSPRUEFUNG.json`
- **Kein produktiver Lauf und keine Liveinstallation.** Für eine echte WordPress-Endabnahme brauchen die bestehende K0-Freigabe und der Diagnosetest zuerst einen definierten zulässigen Stand. Keine neue Arbeit in WordPress oder GitHub nach dieser Dokumentation angenommen.

## Zusätzlicher Beleg: tatsächlich gültige K0-Quelle (18.11.2026)

- K0-Sole-Current `konzept0-portal-neutral-20261002:K0_CURRENT_STATE.json` tatsächlich gelesen: `READY_FOR_FRESH_K0_START`. K0-Regelquellen vorhanden, keine Behauptung mehr, die K0-Regeln fehlten insgesamt.
- `RULE_VALUES.json`: Beratung, FAQ, Pflege, Vergleich; `ARTIKELTYPEN/Anleitung.json`: `status=READY`. Originalregelpaket nicht geändert.
- `K0_PORTAL_REGISTRY.json` hat für Profil `portal_id=hobby` ausschließlich `category_exact=["discgolf-beratung"]`, `category_prefixes=[]`. `engine/k0_portal_resolver.py` überprüft genau diese Listen und verweist für übrige Kategorien auf die Kategorieliste des **Pferdeatelier**. Keine belegte Hobbydepot-weite Kategoriezuordnung.
- Also: Ein blindes Freigeben von `K0_PORTAL_ADAPTER_PENDING` würde zwar die lokale Sperre umgehen, aber eine **portalweit sichere K0-Zuordnung nicht nachweisen**. Nicht vornehmen. Das ist kein Auftrag für Neuentwicklung, nur ein belegter Blocker der vorhandenen Herkunftsdaten.
- Konkrete Grenzen bleiben: reine Fachbereinigung erledigt, Plugin unverändert; K0-Portalzuordnung, vorhandene Diagnose und echter WP-/MINI-Endlauf nicht freigegeben.
