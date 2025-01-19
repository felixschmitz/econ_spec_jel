from __future__ import annotations

import econ_spec_jel


def test_import():
    assert hasattr(econ_spec_jel, "__version__")
