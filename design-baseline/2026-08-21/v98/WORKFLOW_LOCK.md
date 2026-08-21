# Workflow Lock V98

1. Verbindliche Referenz für Journal-Unterkategorie-Beitragskarten ist die bestätigte Journal-Hauptseitenkarte.
2. Der dokumentierte Abstandstoken beträgt 20 px.
3. V98 darf ausschließlich registrierte Journal-Unterkategoriearchive verändern.
4. Fremde WordPress-Kategorien müssen fail-closed unverändert bleiben.
5. Tabellenfix und Journal-Hauptseite sind Regression-Locks und müssen byteidentisch bleiben.
6. Keine Freigabe allein aufgrund von PHP-Lint oder statischen CSS-Prüfungen. Pflicht sind Positiv-/Negativ-Scope-Harness, Browser-Geometrie-Fixture, Fresh-Unpack-Parität und Master-Manifestprüfung.
7. Reale Live-Sichtprüfung bleibt letzter Gate vor endgültigem PASS.
8. `main` bleibt unverändert; V98 liegt auf `fix/journal-category-spacing-v98-20260821`.