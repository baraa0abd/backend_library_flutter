from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from ninja import Router
from rest_framework.authtoken.models import Token
from ninja.security import HttpBearer
from typing import Dict
from .schema import *

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

# Signup API
@router.post("/signup", response={200: MessageResponse, 400: MessageResponse})
def signup(request, payload: SignUpSchema):
    # Check if the username already exists
    if User.objects.filter(username=payload.username).exists():
        return 400, {"message": "Username already exists"}
    
    # Validate the password
    try:
        validate_password(payload.password)
    except ValidationError as e:
        return 400, {"message": " ".join(e.messages)}
    
    # Create the user
    try:
        user = User.objects.create_user(
            username=payload.username,
            password=payload.password,
            email=payload.email
        )
        user.save()
        return {"message": "User created successfully"}
    except IntegrityError:
        return 400, {"message": "Error creating user"}

# Login API
@router.post("/login", response={200: LoginResponse, 401: MessageResponse})
def login_user(request, payload: LoginSchema):
    user = authenticate(username=payload.username, password=payload.password)
    if user is not None:
        if not user.is_active:
            return 401, {"message": "User account is inactive"}
        token, _ = Token.objects.get_or_create(user=user)
        login(request, user)
        return {"token": token.key}
    return 401, {"message": "Invalid username or password"}


# Logout API
@router.post("/logout", auth=BearerAuth(), response={200: MessageResponse})
def logout_user(request):
    # Delete the user's token
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
    except Token.DoesNotExist:
        return 400, {"message": "Token not found"}
    
    # Log out the user
    logout(request)
    return {"message": "Successfully logged out"}
