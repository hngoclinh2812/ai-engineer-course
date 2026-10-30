from pydantic import BaseModel, Field

class BusinessProfile(BaseModel):
    name: str
    capital: int = Field(gt=0)