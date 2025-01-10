from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from ninja import NinjaAPI
from ninja.security import HttpBearer
from typing import Dict
from .schema import *
from rest_framework.authtoken.models import Token
from ninja import Router


# Security class for Bearer Authentication
class BearerAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            user_token = Token.objects.get(key=token)
            request.user = user_token.user
            return user_token.user
        except Token.DoesNotExist:
            return None

# API instance
router = Router()

@router.post("/signup", response={200: MessageResponse, 400: MessageResponse})
def signup(request, payload: SignUpSchema):
    if User.objects.filter(username=payload.username).exists():
        return 400, {"message": "Username already exists"}
    
    user = User.objects.create_user(
        username=payload.username,
        password=payload.password,
        email=payload.email
    )
    user.save()
    return {"message": "User created successfully"}

# Login API
@router.post("/login", response={200: LoginResponse, 401: MessageResponse})
def login_user(request, payload: LoginSchema):
    user = authenticate(username=payload.username, password=payload.password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        login(request, user)
        return {"token": token.key}
    return 401, {"message": "Invalid username or password"}

# Logout API
@router.post("/logout", auth=BearerAuth(), response={200: MessageResponse})
def logout_user(request):
    token = Token.objects.get(user=request.user)
    token.delete()
    logout(request)
    return {"message": "Successfully logged out"}


