from pydantic import BaseModel, EmailStr

class SignUpSchema(BaseModel):
    username: str
    password: str
    email: EmailStr

class LoginSchema(BaseModel):
    username: str
    password: str

class MessageResponse(BaseModel):
    message: str

class LoginResponse(BaseModel):
    token: str
