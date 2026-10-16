from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Admin


@api_view(["GET"])
def admin_get(request):
    admins = Admin.objects.all()
    data=[
        {
            "id":admin.id,
            "name":admin.name,  
            "email":admin.email,
            "age":admin.age,
            "address":admin.address
        }
        for admin in admins
    ]
    return Response(data)

@api_view(["POST"])
def admin_post(request):
    admins = Admin.objects.create(
        name=request.data.get("name"),
        email=request.data.get("email"),
        age=request.data.get("age"),
        address=request.data.get("address")
    )
    return Response({
        "message":"Admin created successfully",
        "id":admins.id,
        "name":admins.name,
        "email":admins.email,
        "age":admins.age,
        "address":admins.address
    },status=status.HTTP_201_CREATED)

@api_view(["DELETE"])
def admin_delete(request,id):
    try:
        admins = Admin.objects.get(id=id)

        admins.delete()
        return Response({"message":"Admin deleted successfully"}, status=status.HTTP_200_OK)
    except Admin.DoesNotExist:
        return Response({"message":"Admin not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(["PUT"])
def admin_update(request,id):
    try:
        admins = Admin.objects.get(id=id)
    except Admin.DoesNotExist:
        return Response({"message":"Admin not found"}, status=status.HTTP_404_NOT_FOUND)
    
    admins.name = request.data.get("name", admins.name)
    admins.email = request.data.get("email", admins.email)
    admins.age = request.data.get("age", admins.age)
    admins.address = request.data.get("address", admins.address)
    admins.save()

    return Response({
        "message":"Admin updated successfully",
        "id":admins.id,
        "name":admins.name,
        "email":admins.email,
        "age":admins.age,
        "address":admins.address
    }, status=status.HTTP_200_OK)