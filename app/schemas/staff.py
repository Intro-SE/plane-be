from __future__ import annotations

from typing import TYPE_CHECKING,List, Optional,Union
from uuid import UUID


from pydantic import BaseModel, Field, EmailStr, ConfigDict,field_validator,validator
from datetime import date

from app.models.staff import StaffProfile

config = ConfigDict(from_attributes=True)

class StaffBase(BaseModel):
    model_config = config
    first_name: str = Field(min_length=1, description="First name of staff")
    last_name: str = Field(min_length=1, description="Last name of staff")
    dob: date

class StaffAccount(StaffBase):
    model_config = config
    uuid: UUID
    email: EmailStr
    password: str
    
class InternalStaffCreate(BaseModel):
    model_config = config
    username: str
    password: str
    first_name: str
    last_name: str
    
    

class StaffResponse(BaseModel):
    id: UUID
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    role: Optional[str]
    is_active: Optional[bool]
    is_internal_staff: Optional[bool]


class InternalStaffResponse(BaseModel):
    id: UUID
    username: str
    first_name: str
    last_name: str
    email: Optional[str]
    role: Optional[str]


class StaffLoginResponse(StaffResponse):
    model_config = config
    access_token: str


class AllStaffsResponse(BaseModel):
    model_config = config
    uuid: UUID
    email: EmailStr
    first_name: str
    last_name: str


class StaffVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class StaffBasicInfo(BaseModel):
    model_config = config
    first_name: str = Field(min_length=1, description="First name fo the Staff")
    last_name: str = Field(min_length=1, description="Last name of the Staff")
    staff_id: UUID
    email: str
    age: Optional[int] = 20


class StaffProfileSchema(BaseModel):
    model_config = config
    staff_id: UUID
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    country: Optional[str] = None
    occupation: Optional[str] = None
    city: Optional[str] = None
    location: Optional[str] = None
    year_of_birth: Optional[int] = None
    avatar_url: Optional[str] = None
    locale: Optional[str] = None
    age: Optional[int] = None
    is_locked: Optional[bool] = None


class StaffProfileFetch(BaseModel):
    staff_id: UUID
    email: EmailStr
    avatar_url: Optional[str] = None
    locale: Optional[str] = None


class StaffProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    year_of_birth: Optional[int] = None
    city: Optional[str] = None
    country: Optional[str] = None

