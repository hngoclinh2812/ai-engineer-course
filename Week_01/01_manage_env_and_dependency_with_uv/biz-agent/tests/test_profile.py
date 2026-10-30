import pytest
from pydantic import ValidationError

from biz_agent.profile import BusinessProfile

__all__ = ["BusinessProfile"]

def test_valid_profile():
    p = BusinessProfile(name="Quán cà phê Mây", capital=50_000_000)
    assert p.capital == 50_000_000


def test_capital_must_be_positive():
    with pytest.raises(ValidationError):
        BusinessProfile(name="Quán lỗ", capital=0)