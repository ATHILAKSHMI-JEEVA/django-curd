
# from rest_framework.decorators import api_view 
# from rest_framework.response import Response
# from rest_framework import status

# from .models import User
# from .serializers import UserSerializer


# @api_view(["GET", "POST"])
# def user_list(request):

#     if request.method == "GET":
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

#     if request.method == "POST":
#         serializer = UserSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

from rest_framework.decorators import api_view
from rest_framework.response import Response        
from rest_framework import status

from myadmin.models import Admin
from myadmin.serializers import Adminserializer

@api_view(["GET", "POST"])
def admin_list(request):

    if request.method == "GET":
        admins = Admin.objects.all()
        serializer = Adminserializer(admins, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = Adminserializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    
# @api_view(["PUT", "DELETE"])
# def user_detail(request, id):

#     try:
#         user = User.objects.get(id=id)
#     except User.DoesNotExist:
#         return Response(
#             {"error": "User not found"},
#             status=status.HTTP_404_NOT_FOUND
#         )

#     if request.method == "PUT":
#         serializer = UserSerializer(user, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     if request.method == "DELETE":
#         user.delete()
#         return Response(
#             {"message": "User deleted successfully"},
#             status=status.HTTP_204_NO_CONTENT
#         )

@api_view(["PUT", "DELETE"])
def admin_detail(request, id):

    try:
        admin = Admin.objects.get(id=id)
    except Admin.DoesNotExist:
        return Response(
            {"error": "Admin not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "PUT":
        serializer = Adminserializer(admin, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    if request.method == "DELETE":
        admin.delete()
        return Response(
            {"message": "Admin deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )