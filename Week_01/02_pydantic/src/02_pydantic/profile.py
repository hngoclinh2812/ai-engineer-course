from pydantic import BaseModel, field_validator

ALLOWED_INDUSTRY = ["Công nghệ", "Tài chính", "Y tế", "Giáo dục"]

class BusinessProfile(BaseModel):
    ten: str
    nganh: str
    loai_hinh: str
    von: float
    dia_diem: str

    @field_validator("von")
    def von_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Vốn phải là số dương")
        return v

    @field_validator("nganh")
    def nganh_must_be_allowed(cls, v):
        if v not in ALLOWED_INDUSTRY:
            raise ValueError(f"Ngành không được phép. Vui lòng chọn từ: {ALLOWED_INDUSTRY}")
        return v
