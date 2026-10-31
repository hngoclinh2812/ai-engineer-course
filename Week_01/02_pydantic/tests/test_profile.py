import importlib

import pytest
from pydantic import ValidationError


BusinessProfile = importlib.import_module("02_pydantic.profile").BusinessProfile

VALID_PROFILE = {
    "ten": "Quán cà phê Mây",
    "nganh": "Công nghệ",
    "loai_hinh": "Công ty trách nhiệm hữu hạn",
    "von": 50_000_000,
    "dia_diem": "Hà Nội",
}


def test_valid_profile_is_created_with_expected_values():
    profile = BusinessProfile(**VALID_PROFILE)

    assert profile.ten == "Quán cà phê Mây"
    assert profile.nganh == "Công nghệ"
    assert profile.loai_hinh == "Công ty trách nhiệm hữu hạn"
    assert profile.von == 50_000_000
    assert profile.dia_diem == "Hà Nội"


@pytest.mark.parametrize("industry", ["Công nghệ", "Tài chính", "Y tế", "Giáo dục"])
def test_each_allowed_industry_is_accepted(industry):
    profile = BusinessProfile(**{**VALID_PROFILE, "nganh": industry})

    assert profile.nganh == industry


@pytest.mark.parametrize("capital", [0, -1, -0.01])
def test_zero_or_negative_capital_is_rejected(capital):
    with pytest.raises(ValidationError) as exc_info:
        BusinessProfile(**{**VALID_PROFILE, "von": capital})

    assert exc_info.value.errors()[0]["loc"] == ("von",)


@pytest.mark.parametrize("industry", ["", "Công nghệ thông tin", "Nông nghiệp"])
def test_industry_outside_allowlist_is_rejected(industry):
    with pytest.raises(ValidationError) as exc_info:
        BusinessProfile(**{**VALID_PROFILE, "nganh": industry})

    assert exc_info.value.errors()[0]["loc"] == ("nganh",)


@pytest.mark.parametrize("field", ["ten", "nganh", "loai_hinh", "von", "dia_diem"])
def test_each_profile_field_is_required(field):
    profile_data = {key: value for key, value in VALID_PROFILE.items() if key != field}

    with pytest.raises(ValidationError) as exc_info:
        BusinessProfile(**profile_data)

    assert any(error["loc"] == (field,) and error["type"] == "missing" for error in exc_info.value.errors())


def test_positive_fractional_capital_is_accepted():
    profile = BusinessProfile(**{**VALID_PROFILE, "von": 0.01})

    assert profile.von == 0.01


def test_numeric_string_capital_is_converted_before_validation():
    profile = BusinessProfile(**{**VALID_PROFILE, "von": "1250.5"})

    assert profile.von == 1250.5
