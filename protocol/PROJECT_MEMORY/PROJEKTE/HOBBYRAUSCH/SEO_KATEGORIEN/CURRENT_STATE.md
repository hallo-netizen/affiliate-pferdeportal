# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-05
STATUS: LIVE: BUCHBINDEN SICHTBAR / UNTERKATEGORIEN NICHT SICHTBAR / V1.9.7 FRONTEND-ENDSTATE LOKAL HARD PASS / LIVE-UPDATE OFFEN

## Harte Abnahmeregel

**Keine Abnahme ohne dokumentierte lokale Positiv- UND Negativsimulation bis zum sichtbaren Frontend-Endzustand und anschließenden realen WordPress-/Frontend-Readback.**

Ein technischer WordPress-Objekt-Readback allein ist ausdrücklich **kein PASS**.

## Zielvertrag

`ZIELVERTRAG_HD001_AUTOMATISCHE_SEO_HIERARCHIE_20261003.md`

Ziel:
Konzept → DataForSEO → Hauptportal + Magazin + HivePress → WordPress → Publish → sichtbare Frontend-Struktur/Navigation → Readback.

## Tatsächlich beobachteter Livezustand

Am 2026-10-05 real im Frontend beobachtet:
- Seite `Buchbinden` ist sichtbar;
- die vorgesehenen direkten Content-Kinder `Einstieg`, `Ausrüstung`, `Material`, `Techniken & Praxis` sind auf der Buchbinden-Seite **nicht sichtbar**;
- damit ist der bisherige Endzustand **NICHT PASS**.

## Exakte Ursache

Der bestehende Writer erzeugt:
- `Buchbinden` als WordPress-Seite;
- die vier Kinder als WordPress-Taxonomie-Terme.

Da ein Taxonomie-Term nicht nativ Kind einer WordPress-Seite sein kann, wird die fachliche Beziehung nur über `_apkw_parent_concept_id` gespeichert.

Der bisherige Readback prüfte diese technische Bindung, aber es gab:
- keinen persistenten Frontend-Navigationsblock in der Elternseite;
- keinen Menü-Write;
- keinen Frontend-Endzustandscheck auf tatsächlich sichtbare/verlinkte Kinder.

Dadurch konnte Write + technischer Readback PASS sein, obwohl die Buchbinden-Seite im Frontend leer blieb.

## V1.9.7 – Frontend-Endstate-Kandidat

KISS-Fix auf derselben Pluginlinie:
- kein Zusatzplugin;
- kein Theme-Umbau;
- kein Laufzeit-`the_content`-Filter;
- keine neue DataForSEO-Recherche;
- kein Neuaufbau des bestehenden Baums.

Der Writer erzeugt für Seiten mit direkten Content-Kindern einen persistenten verwalteten Navigationsblock im echten `post_content` der Elternseite:
`<!-- APKW:CHILDREN:BEGIN --> ... <!-- APKW:CHILDREN:END -->`

Eigenschaften:
- nur direkte Content-Kinder;
- echte WordPress-Links via `get_permalink` / `get_term_link`;
- Marketplace/HivePress und Magazin bleiben getrennt;
- vorhandener redaktioneller Seiteninhalt außerhalb des verwalteten Blocks bleibt erhalten;
- spätere Sparse-Erweiterungen aktualisieren nur diesen Block;
- kein kompletter Neuaufbau;
- Block-Tampering/kaputte Marker fail-closed;
- Frontend-Mismatch nach Write → automatischer Rollback einschließlich ursprünglichem Seiteninhalt.

## Harte lokale E2E-Evidenz

Vor-Fix realistisch reproduziert:
- Deployment/Write PASS;
- technischer Readback PASS;
- Seite `publish`;
- Seiteninhalt leer;
- Frontend-Endzustand FAIL.

Nach Fix:
- exakte reale Buchbinden-Topologie verwendet;
- sichtbar/verlinkt erwartet und geprüft: `Einstieg`, `Ausrüstung`, `Material`, `Techniken & Praxis`;
- `Buchbinden Set` und `Buchbinden Online` dürfen nicht in den Content-Block leaken;
- spätere fünfte Content-Kategorie wird ergänzt, bestehende vier bleiben;
- zweiter identischer Lauf erzeugt keine unnötigen Writes;
- manuelle Inhalte außerhalb des verwalteten Blocks bleiben erhalten;
- Manipulation / fehlender Frontend-Endzustand / kaputte Marker → BLOCKED bzw. Rollback.

Gesamtsuite:
- 275/275 PASS;
- Fresh-Source 275/275 PASS;
- Source↔Installer Runtime 23/23 byteidentisch;
- Source PHP 17/17 PASS;
- Installer PHP 17/17 PASS.

V1.9.7 Installer SHA-256:
`89790e0b12b4c72c96c8c5a9387dabc160c21707d6147e65898303eef70a0f40`

V1.9.7 Source SHA-256:
`7d324512d2d0e89faac82be50b54bd580facb4e2eef782eba32ab0ce8378af1a`

## Beleggrenze

V1.9.7 ist **noch nicht live installiert**.
Es gibt daher noch keinen realen Frontend-PASS.

Die lokale E2E-Simulation nutzt den echten Plugin-Code und die echte Buchbinden-Paket-/Knotentopologie mit WordPress-API-kompatibler Testumgebung. Sie ist kein vollständiger Clone des IONOS-/Theme-Hostings. Der Live-Screenshot bestätigt jedoch exakt den lokal reproduzierten Fehlerzustand.

## NEXT ACTION

V1.9.7 über den aktuellen Kategorie-Workflow installieren.

Danach genau einmal den bestehenden Publish-/Republish-Weg ausführen.

Erwarteter realer Endzustand:
`Buchbinden` bleibt sichtbar und zeigt exakt die vier verlinkten Content-Kinder:
- Einstieg
- Ausrüstung
- Material
- Techniken & Praxis

Keine neue DataForSEO-Recherche.
Keine neuen Kategorien.
Kein weiterer Pluginumbau vor diesem realen Frontend-Readback.
