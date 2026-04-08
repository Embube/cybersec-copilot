from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    username: str
    password: str
    email: EmailStr | None = None
    full_name: str | None = None
    role: str = "viewer"


class UserResponse(BaseModel):
    id: int
    username: str
    email: str | None = None
    full_name: str | None = None
    role: str
    is_active: bool

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
