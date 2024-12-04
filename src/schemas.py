from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class ContactsModel(BaseModel):
    first_name: str = Field(...,max_length=50, min_length=2, description="First name")
    last_name: str = Field(..., max_length=50, min_length=2, description="Last name")
    email: EmailStr = Field(..., max_length=50, description="Email")
    phone: str =Field(...,max_length=15, min_length=10, description="Phone")
    dob: Optional[date] = Field(None, description='Date of birth (YYYY-MM-DD)')

class UpdateContactModel(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50, min_length=2, description="First name")
    last_name: Optional[str] = Field(None, max_length=50, min_length=2, description="Last name")
    email: Optional[EmailStr] = Field(None, max_length=50, description="Email")
    phone: Optional[str] = Field(None,max_length=15, min_length=10, description="Phone")
    dob: Optional[date] = Field(None, description='Date of birth (YYYY-MM-DD)')

class ContactsResponse(ContactsModel):
    id: int

    model_config = ConfigDict(from_attributes=True)
