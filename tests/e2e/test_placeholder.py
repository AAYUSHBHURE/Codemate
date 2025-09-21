from __future__ import annotations

import pytest

@pytest.mark.skip(reason='E2E tests require live services.')
def test_e2e_placeholder() -> None:
    pass
