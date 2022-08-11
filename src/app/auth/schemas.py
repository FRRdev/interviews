from uuid import UUID
from pydantic import BaseModel


class Token(BaseModel):
    """ Token out scheme
    """
    access_token: str
    token_type: str


class Msg(BaseModel):
    """ Messages scheme
    """
    msg: str


class VerificationOut(BaseModel):
    """ Scheme for checking email during registration
    """
    link: UUID


class TokenPayload(BaseModel):
    """ Scheme for user id in token
    """
    user_id: int = None
