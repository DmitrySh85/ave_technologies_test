from pydantic import BaseModel, field_validator


class PhoneAddress(BaseModel):
    phone: str
    address: str

    @field_validator("phone")
    def validate_phone(cls, v):
        if not v.startswith("+"):
            raise ValueError("Phone number must start with '+'")

        if not v[1:].isdigit():
            raise ValueError("Phone number must contain only digits after '+'")

        if len(v) != 12:
            raise ValueError("Phone number must be exactly 12 characters long")

        return v


class UpdatePhoneAddress(BaseModel):
    address: str