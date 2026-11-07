# HD009 – einzige aktuelle Hobby Depot Affiliate-Zentrale

**07.11.2026 · 0.1.16-dev · technisch geprüft, WordPress-Liveprüfung offen.**

- Einzige Installationsdatei: `CURRENT.zip`
- Größe: **712.675 Bytes**
- SHA-256: `7f65fae7a3aac98bfb5f9bc7f7673fc726f64f0b3cbf5eb8b5a51c3e4ad40640`
- Git-Blob: `2256f6a3c7b8762b0d68ecb1fa36f1a9370894d3`
- Pluginordner: `affiliate-portal-router/`; Hauptdatei: `hobby-depot-affiliate-router.php`
- Prüfung: vollständige ZIP-CRC PASS, **24/24 PHP-Syntax PASS**, vorhandener Kategorie-/Elternpfad-, Format- und Glossarcode unverändert.
- Prüfnachweis: `../../PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/HD009_0116_SLOT_FIX_PASS.txt`
- Reproduzierbarer KISS-Build: `../../PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/build_0116_restore_native.py`

## Einziger gezielter Fix gegenüber 0.1.15-dev

**Fehler live durch Screenshot auf** `https://hobby-depot.de/gestalten/malen-zeichnen/` **belegt:** Die Version 0.1.15 gab bei fehlender normaler Affiliate-Kampagne die freigegebene **Mietwerbung aus HD003** in einen schmalen **Affiliate-Querbannerplatz** aus. Die Mietwerbegrafik 2170×725 hat ein Verhältnis von etwa 2,99:1; der bereits vorhandene fachliche Kategorie-Bannervertrag verlangt **5:1 bis 12:1**. Die zusätzliche Abkürzung umging den normalen Format- und Themenfilter. Das Bild wurde im Frontend abgeschnitten. Außerdem war „Hier könnte Ihre Werbung stehen“ an diesem Affiliate-Produktplatz fachlich falsch.

**Korrektur 0.1.16:** Den erst in 0.1.15 hinzugefügten Mietwerbungs-Fallback vollständig **aus HD009 entfernt**, inklusive überflüssiger Bildkopie. Der ursprüngliche Pferdeatelier-/Hobby-Rahmen aus `render_affiliate_slot_for_context`, `overview_wide_banner_campaign_eligible`, `category_large_banner_rule`, bestehender Kampagnenauswahl, HD004-Zuordnung sowie Glossar-Zielslots bleibt unverändert. **Kein neuer Banneralgorithmus, kein zusätzlicher Import und keine neue Architektur.**

**HD003 bleibt unangetastet:** Dort liegt die freigegebene Originalgrafik mit Logo, „Hier könnte Ihre Werbung stehen“ und den Buttons „Werbebedingungen“/„Preise“. Diese Grafik ist ausschließlich für **freie, direkt vermietbare Werbeflächen**, niemals als Ersatz für Amazon-/idealo-Produkte oder die standardmäßigen flachen Partnerbanner gedacht.

## Harte Testgrenze und konkrete Testseiten

- **Genau eine Querbanner-Testseite:** `https://hobby-depot.de/gestalten/malen-zeichnen/` (im Screenshot vorhanden).
- **Quadratische/hohe Einzelbanner:** vorhandene Slots `glossary_single_desktop_banner` und `glossary_single_mobile_banner` auf veröffentlichten **Glossar-Einzelbeiträgen (`uge_term`)**. Kein fertig geprüftes Motiv freigegeben; damit kann derzeit **kein sichtbares Quadratbanner** erwartet werden. Für das Hobbyregister liegt hier kein belegter separater Quadrat-Integrationspunkt vor; nicht behaupten.
- **Echte Partnerbanner** erscheinen nur nach erfolgreicher relevanter Partnerkampagne im vorhandenen automatischen Kreativbestand. Die heute noch fehlenden Amazon-/idealo-Daten werden durch 0.1.16 nicht erfunden oder aktiviert.
- **Frontend-Regression nach Installation weiterhin offen.** Ein technisch bestandener ZIP-/Syntax-Test beweist kein WordPress-Liveverhalten.
