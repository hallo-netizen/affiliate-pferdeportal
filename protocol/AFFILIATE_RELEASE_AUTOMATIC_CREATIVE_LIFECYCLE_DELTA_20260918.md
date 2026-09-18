# AFFILIATE-ZENTRALE — Kanonischer Delta-Precheck 2026-09-18

Status: `PRECHECK COMPLETE / ROOTFIX REQUIRED`
Kanonische Ausgangssource: `release/affiliate-zentrale/current/affiliate-portal-router/` (6.72.19)

## Bereits vorhanden — nicht neu bauen

- providerneutrale zentrale Provider-Registry und Adapter-Hooks;
- automatische Awin-/ADCELL-Importpfade mit Upsert in die gemeinsame Creative-Library;
- reale Bildprüfung mit echten Pixelmaßen und Bild-Hash;
- bestehende manuelle Portalentscheidungen: Veto, Review, Approved/Fixed und Rückkehr zu Automatic;
- Reconcile-Grundmechanik `active -> quarantine_missing -> inactive_missing` bei vollständig bestätigten Providerläufen;
- zentrale Slot-/Formatentscheidung auf realen Maßen/Ratio statt Provider-Formatlabeln;
- Providerreport-Adapter/Cache als vorhandene Basis für Originaldaten.

## Exakt fehlender kanonischer Delta

1. **Vollautomatische Partneraufnahme im Normalbetrieb**
   - Scheduling darf nicht von einer manuellen Einzelfreigabe jedes neuen gültigen Partnerprogramms abhängen.
   - Providerseitig gültige/zugelassene Programme müssen über den vorhandenen Provider-/Adaptervertrag in den zentralen Sync gelangen.
   - Manuelle Sperren/Vetos bleiben vorrangig und müssen fail-closed wirken.

2. **Creative-Deduplizierung KISS/fail-safe**
   - heutige `identity_hash`-Identität (`provider|partner|external_id`) ist kein Varianten-Dedupe;
   - benötigt wird eine providerneutrale Variantenidentität aus eindeutig belegbaren Creative-Inhalten + Ziel/Kampagnenbindung + Formatfamilie;
   - gleiche Variante innerhalb derselben Formatfamilie: nur größte verifizierte Originalversion produktiv;
   - kleinere eindeutige Duplikate nur schlanke Alias-/Auditbindung;
   - anderer Text/CTA/Rabatt/Angebot oder Unsicherheit => getrennt lassen.

3. **Zentrale Zeitsteuerung**
   - kanonisch aktuell nur `daily`/`twicedaily`;
   - Ziel: normaler Bestands-/Partner-/Creative-Sync alle 2 Wochen;
   - separater tiefer Integritätslauf alle 3 Wochen;
   - `Jetzt prüfen` und späterer externer Cron triggern dieselbe zentrale Fachlogik.

4. **Lifecycle / belegte Verfügbarkeit**
   - Providerstatus sowie belegte Start-/Enddaten müssen in die aktive Eignung einfließen;
   - verschwundene, deaktivierte oder belegbar abgelaufene Creatives aus aktiver Eignungsmenge entfernen;
   - ohne belastbare Laufzeitdaten ausschließlich erneute Providerbestätigung, keine OCR-/Bildtext-Ableitung.

5. **Betroffene Ziele/Slots nach Bestandswechsel neu bewerten**
   - bestehende Import-/Bildprüfpfade planen neue/aktualisierte Creatives bereits an;
   - nach Deaktivierung/Entfall muss der betroffene Ziel-/Slotbestand aktiv neu bewertet werden, damit der nächstbeste gültige Treffer nachrückt bzw. ein besserer neuer Treffer übernehmen kann;
   - manuelle Fixierungen/Vetos dürfen dabei nicht überschrieben werden.

6. **Backend-Statistik ausschließlich aus Original-Providerdaten**
   - `class-ppar-partner-analytics.php` verwendet derzeit eigene lokale Klickzähler zusätzlich zu Providerreports;
   - Backend-Statistik muss ausschließlich verifizierte Originaldaten des jeweiligen Partners/Providers aus dessen Report-/API-Weg verwenden;
   - keine eigene Klick-, Bestell-, Umsatz- oder Provisionserhebung darf dort angezeigt, addiert, ergänzt oder als Ersatzwert benutzt werden;
   - fehlende Providerdaten = `nicht verfügbar`, nicht `0`;
   - Währungen getrennt/korrekt darstellen; keine falsche EUR-Gesamtsumme und keine Bestpartner-Aussage bei unvollständiger/inkompatibler Datenbasis.

## Rootfix-Grenze

Kein Build, kein Installer und keine Versionswahl innerhalb dieses Prechecks. Der nächste zulässige Schritt ist genau ein kanonischer Rootfix-Kandidat auf Basis der 6.72.19-Source. Lokale 6.72.60–6.72.65 bleiben ausschließlich Oracle.
