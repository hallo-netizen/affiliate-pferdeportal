# NOTFALL-TRESOR – INHALTSVERTRAG GITHUB

STAND: 2026-09-07
STATUS: VERBINDLICH

## A. GIT

Pflicht:
- vollständiges Git-Bundle aller gesicherten Refs;
- Branches;
- Tags;
- Pull-Request-Refs;
- Commit-Historie;
- Ref-Liste;
- SHA-256.

## B. GITHUB-METADATEN

Pflicht, soweit GitHub exportierbar:
- Repository;
- Branches/Tags;
- Issues + Kommentare + Events;
- Pull Requests + Reviews + Review-Kommentare;
- Releases + Release-Artefakte;
- Labels/Milestones;
- Rulesets;
- Workflows;
- Deployments;
- Environments;
- Collaborators;
- relevante Actions-/Webhook-/Variablen-/Secret-Namen-Einstellungen;
- Wiki, falls initialisiert.

## C. MANIFEST

Pflicht:
- Erstellzeit;
- Repository;
- main-SHA;
- Anzahl Branches/Tags/PR-Refs;
- Metadatenzählung;
- Restore-Ergebnis;
- bekannte Providergrenzen.

## Providergrenze

Secret-Werte sind über GitHub nicht exportierbar.
Nicht lesbare Admin-Endpunkte müssen im Backup ausdrücklich als `UNAVAILABLE` protokolliert werden.

## NEGATIVREGEL

Nicht Bestandteil dieses Vertrags:
- WordPress;
- Website-Dateien/Datenbank;
- ChatGPT-Library/Campus-Archiv als eigener Datenblock;
- Hosting.
