from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

from .models import App

@api_view(["POST"])
def app_login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(request, username=username, password=password)

    if user is  None:
        return Response(
            {
                "message":"invalid credentials"
            },status=status.HTTP_401_UNAUTHORIZED

        )
    request.session["user_id"] = user.id

    return Response(
        {
            "message":"login successful"
        },status=status.HTTP_200_OK
    )



@api_view(["POST"])
def app_logout(request):
    if "user_id" in request.session:
        del request.session["user_id"]

    return Response({
        "message": "Logout successful"  
    })