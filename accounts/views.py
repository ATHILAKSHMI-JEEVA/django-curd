from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes
from .models import Account
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAdminUser
def home(request):
    return JsonResponse({
        "message": "Welcome to Custom Admin API"
    })

@api_view(["POST"])
def account_create(request):
    account =Account.objects.create(
        name=request.data.get("name"),
        email=request.data.get("email")
    )
    return Response({
        "message":"account created",
        "id":account.id
    })

@api_view(["GET"])
def account_get(request):
    accounts=Account.objects.all()
    data=[]
    for account in accounts:
        data.append({
            "id":account.id,
            "name":account.name,
            "email":account.email
        })

    return Response(data)

@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_dashboard(request):
    return Response({
        "message":"welcome Admin",
        "username":request.user.username
    })

@api_view(["POST"])
@permission_classes([IsAdminUser])
def user_create(request):
    username=request.data.get("username")
    email=request.data.get("email")
    password=request.data.get("password")

    if not username or not email or not password:
        return Response({
            "error":"username,email,password required"
        },status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({
            "error":"username already exists"
        },status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({
            "error":"email already exits"
        },status=status.HTTP_400_BAD_REQUEST)

    user=User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    return Response({
        "message":"user created",
        "id":user.id,
        "username":user.username,
        "email":user.email
    },status=status.HTTP_201_CREATED)