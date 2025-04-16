from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr, StringConstraints


class UserSchema(BaseModel):
    username: str
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    # phone: Annotated[str, StringConstraints(min_length=6)] | None = None
    # is_varified: bool = False
    # is_active: bool = True
    # is_superuser: bool = False

    model_config = ConfigDict(from_attributes=True)


class UserHashedSchema(BaseModel):
    id: int
    password_hash: str


class UserRequestAddSchema(UserSchema):
    password: Annotated[SecretStr, StringConstraints(min_length=8)]
    password_confirm: Annotated[SecretStr, StringConstraints(min_length=8)]


class UserRequestUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: Annotated[str, StringConstraints(min_length=6)] | None = None
    is_varified: bool | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    password: Annotated[SecretStr, StringConstraints(min_length=8)] | None = None
    password_confirm: Annotated[SecretStr, StringConstraints(min_length=8)] | None = (
        None
    )


class UserHashedPwdAddSchema(UserSchema):
    password_hash: str


class UserShowSchema(UserSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserLoginSchema(BaseModel):
    grant_type: str | None = None
    username: str
    password: str
