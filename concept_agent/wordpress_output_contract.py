"""Hard WordPress output gate for the proven Redaktionsplan upload contract."""
from __future__ import annotations
from typing import Any
from wordpress_redaktionsplan_upload import validate

def validate_wordpress_package(pkg:dict[str,Any],verify_signature:bool=True)->list[str]:
    # Signature is deliberately irrelevant for this direct Redaktionsplan contract.
    # The installed System4 importer rejected ENDSTEMPEL wrappers and accepts the
    # 107008 Redaktionsplan upload shape instead.
    return validate(pkg)

def assert_wordpress_ready(pkg:dict[str,Any])->None:
    errors=validate(pkg)
    if errors:
        raise RuntimeError("WORDPRESS_PACKAGE_BLOCKED:"+",".join(errors))
