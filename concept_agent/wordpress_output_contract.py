"""Hard WordPress output gate for the real PSERC 0.28.23 System-4 direct import contract."""
from __future__ import annotations
from typing import Any
from wordpress_redaktionsplan_upload import validate
def validate_wordpress_package(pkg:dict[str,Any],verify_signature:bool=True)->list[str]:return validate(pkg)
def assert_wordpress_ready(pkg:dict[str,Any])->None:
    errors=validate(pkg)
    if errors:raise RuntimeError("WORDPRESS_PACKAGE_BLOCKED:"+",".join(errors))
