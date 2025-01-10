from ninja import Schema

class SignUpSchema(Schema):
    username: str
    password: str
    email: str

class LoginSchema(Schema):
    username: str
    password: str

class MessageResponse(Schema):
    message: str

class LoginResponse(Schema):
    token: str
