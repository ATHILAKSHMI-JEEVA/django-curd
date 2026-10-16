from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User



@api_view(["GET"])
def user_get(request):
    users=User.objects.all()
    data=[
        {
            "id":user.id,
            "name":user.name,
            "email":user.email,
            "age":user.age

        }
        for user in users
    ]
    return Response(data)


@api_view(["POST"])
def user_post(request):
    name=request.data.get("name")
    email=request.data.get("email")
    age=request.data.get("age")
    users = User.objects.create(
        name= name,
        email= email,
        age= age

    )
    return Response({
        "message":"User craeted sucessfully",
        "id":users.id,
        "name":users.name,
        "email":users.email,
        "age":users.age
    },status=status.HTTP_201_CREATED
)

@api_view(["DELETE"])
def user_delete(request,id):
    try:
        users = User.objects.get(id=id)
        users.delete()
        return Response({"message":"user deleted sucessfully"}, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({"message":"user not found"},status=status.HTTP_404_NOT_FOUND)
    
@api_view(["PUT"])
def user_update(request,id):
    try:
        users = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"message":"user not found"}, status = status.HTTP_204_NOT_FOUND)
    
    users.name = request.data.get("name",users.name)
    users.email = request.data.get("email",users.email)
    users.age = request.data.get("age",users.age)

    users.save()

    return Response({
    "message":"user updated successfully",
    "name":users.name,
    "email":users.email,
    "age":users.age 
}, status=status.HTTP_200_OK)
