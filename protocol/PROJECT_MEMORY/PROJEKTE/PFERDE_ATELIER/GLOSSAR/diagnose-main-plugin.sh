#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.10-rc1.sh"
nl -ba /tmp/uge0210rc1/universal-glossary-engine/universal-glossary-engine.php
