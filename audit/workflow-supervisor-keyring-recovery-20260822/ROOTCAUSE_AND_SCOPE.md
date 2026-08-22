# Workflow-Supervisor Keyring Recovery – 2026-08-22

Branch: `rootfix/workflow-supervisor-keyring-recovery-20260822`

Root Cause: PSERC 0.28.2 band genau einen Workflow-Supervisor-Ed25519-Public-Key. Der zugehörige private Workflow-Key war nicht wie der PPM-Build-Key dauerhaft als externes verschlüsseltes Backup mit separater Passphrase übergeben.

Reparatur: additive Trust-Keyring-Rotation in PSERC 0.28.3. Der bisherige Public Key `workflow-ed25519-153d2518dba7b025` bleibt `LEGACY_TRUSTED`; neuer aktiver Public Key ist `workflow-ed25519-b15660ee915a5826`. Der neue Private Key bleibt ausschließlich extern verschlüsselt und wird nicht in Plugin, MASTER oder GitHub abgelegt.

Rule-1-Scope: keine Änderung an Redaktionsplan, READY, Titeln, Keywords, Kategorien, Artikeltypen, Plan-Slots, Recherche, Fact-Packs, Artikeltext, HTML, Textmaschine, PPM, Design oder WordPress-Schreibpfaden. Kein Publish.

`main` bleibt unverändert.